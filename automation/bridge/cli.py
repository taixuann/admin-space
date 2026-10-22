#!/usr/bin/env python3
"""Bridge CLI: Unified terminal automation hub for GitHub multi-repo sweeps
and Google Drive 1:1 cloud backup.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import List, Optional

# Add bridge root to sys.path so backend modules can be imported
BRIDGE_ROOT = Path(__file__).resolve().parent
if str(BRIDGE_ROOT) not in sys.path:
    sys.path.insert(0, str(BRIDGE_ROOT))
if str(BRIDGE_ROOT.parent.parent) not in sys.path:
    sys.path.insert(0, str(BRIDGE_ROOT.parent.parent))

from backend.config_manager import (
    load_github_config,
    save_github_config,
    load_drive_config,
    save_drive_config,
    get_tracked_workspaces,
    get_enabled_drive_profiles,
    update_workspace,
    update_drive_profile,
)
from backend.git_engine import (
    sync_tracked_repo,
    sync_all_tracked_repos,
    safe_pull_repo,
    pull_all_repos,
)
from backend.drive_engine import (
    sync_drive_profile,
    check_drive_diff,
    get_public_share_link,
)
from backend.scanner import inspect_git_workspace


class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    GREEN = "\033[32m"
    AMBER = "\033[33m"
    BLUE = "\033[34m"
    PURPLE = "\033[35m"
    CYAN = "\033[36m"
    RED = "\033[31m"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="bridge",
        description="Bridge CLI — Unified GitHub multi-repo automation and Google Drive 1:1 sync manager.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # 1. status
    p_status = subparsers.add_parser("status", help="Inspect live status of GitHub workspaces and Drive profiles")
    p_status.add_argument("--json", action="store_true", help="Output status report as structured JSON")

    # 2. sync
    p_sync = subparsers.add_parser("sync", help="Synchronize GitHub repositories or Google Drive cloud targets")
    sync_subs = p_sync.add_subparsers(dest="sync_target", help="Target subsystem to synchronize")

    # 2a. sync github
    p_sync_gh = sync_subs.add_parser("github", help="Stage uncommitted changes, commit (automation format), and push tracked repos")
    p_sync_gh.add_argument("--repo", "-r", help="Specific repository ID to sync (defaults to all tracked)")
    p_sync_gh.add_argument("--pull", action="store_true", help="Safe pull from remote using fast-forward only (--ff-only)")
    p_sync_gh.add_argument("--dry-run", "-n", action="store_true", help="Preview what would be committed/pushed without making changes")
    p_sync_gh.add_argument("--date", help="Custom date for automation commit message (YYYY-MM-DD)")
    p_sync_gh.add_argument("--json", action="store_true", help="Output sync results as JSON")

    # 2b. sync drive
    p_sync_drive = sync_subs.add_parser("drive", help="Execute 1:1 mirror sync to Google Drive via rclone")
    p_sync_drive.add_argument("--profile", "-p", help="Specific Drive profile ID to sync (defaults to all enabled)")
    p_sync_drive.add_argument("--dry-run", "-n", action="store_true", help="Run rclone sync with --dry-run")
    p_sync_drive.add_argument("--force", "-f", action="store_true", help="Override Git gatekeeper check if local working tree is dirty")
    p_sync_drive.add_argument("--no-auto-commit", dest="auto_commit", action="store_false", default=True, help="Do not commit dirty local repo before syncing")
    p_sync_drive.add_argument("--date", help="Custom date for automation commit message (YYYY-MM-DD)")
    p_sync_drive.add_argument("--diff", "-d", action="store_true", help="Only check diff against Google Drive without syncing")
    p_sync_drive.add_argument("--json", action="store_true", help="Output sync results as JSON")

    # 3. track
    p_track = subparsers.add_parser("track", help="Enable or disable tracking for a GitHub repo or Drive profile")
    track_subs = p_track.add_subparsers(dest="track_subsystem", help="Subsystem: github or drive")

    p_track_gh = track_subs.add_parser("github", help="Manage GitHub workspace tracking")
    p_track_gh.add_argument("id", help="Repository workspace ID")
    p_track_gh_group = p_track_gh.add_mutually_exclusive_group(required=True)
    p_track_gh_group.add_argument("--enable", action="store_true", help="Mark repository as tracked")
    p_track_gh_group.add_argument("--disable", action="store_true", help="Mark repository as untracked")

    p_track_drive = track_subs.add_parser("drive", help="Manage Google Drive profile auto-sync")
    p_track_drive.add_argument("id", help="Drive profile ID")
    p_track_drive_group = p_track_drive.add_mutually_exclusive_group(required=True)
    p_track_drive_group.add_argument("--enable", action="store_true", help="Enable drive auto-sync")
    p_track_drive_group.add_argument("--disable", action="store_true", help="Disable drive auto-sync")

    # 4. share
    p_share = subparsers.add_parser("share", help="Get public read-only Google Drive link")
    share_subs = p_share.add_subparsers(dest="share_subsystem", help="Subsystem: drive")
    p_share_drive = share_subs.add_parser("drive", help="Retrieve public read-only shareable link for a profile")
    p_share_drive.add_argument("id", help="Drive profile ID")

    # 5. pull
    p_pull = subparsers.add_parser("pull", help="Safe fast-forward pull from GitHub (alias for sync github --pull)")
    p_pull.add_argument("pull_subsystem", nargs="?", default="github", help="Subsystem: github")
    p_pull.add_argument("--repo", "-r", help="Specific repository ID to pull (defaults to pull-enabled / tracked repos)")
    p_pull.add_argument("--dry-run", "-n", action="store_true", help="Preview pull without making changes")
    p_pull.add_argument("--json", action="store_true", help="Output pull results as JSON")

    return parser


def cmd_status(args=None, gh_config_path=None, drive_config_path=None, stdout=sys.stdout):
    gh_cfg = load_github_config(gh_config_path)
    drive_cfg = load_drive_config(drive_config_path)

    workspaces = gh_cfg.get("workspaces", [])
    profiles = drive_cfg.get("profiles", [])

    is_json = getattr(args, "json", False) if args else False

    if is_json:
        gh_data = []
        for ws in workspaces:
            target_branch = ws.get("default_branch", "main")
            git_info = inspect_git_workspace(ws.get("path", ""), target_branch=target_branch)
            gh_data.append({**ws, "git": git_info})

        dr_data = []
        for p in profiles:
            source = p.get("source_path", "")
            is_clean, uncommitted = (False, 0)
            if Path(source).exists():
                from backend.drive_engine import check_drive_gatekeeper
                is_clean, uncommitted = check_drive_gatekeeper(source)
            dr_data.append({**p, "git_clean": is_clean, "uncommitted_count": uncommitted})

        stdout.write(json.dumps({"github": gh_data, "drive": dr_data}, indent=2) + "\n")
        return 0

    stdout.write(f"\n{Colors.BOLD}=== Bridge Status Overview ==={Colors.RESET}\n\n")

    # GitHub Repos Table
    stdout.write(f"{Colors.BOLD}{Colors.CYAN}GitHub Workspaces ({len(workspaces)} registered):{Colors.RESET}\n")
    stdout.write(f"{'ID':<18} {'NAME':<22} {'TRACKED':<10} {'BRANCH':<10} {'AHEAD':<8} {'BEHIND':<8} {'DIRTY':<8} {'REMOTE'}\n")
    stdout.write("-" * 98 + "\n")

    for ws in workspaces:
        ws_id = ws.get("id", "")
        ws_name = ws.get("name", ws_id)
        tracked = ws.get("tracked", True)
        track_label = f"{Colors.GREEN}Tracked{Colors.RESET}" if tracked else f"{Colors.DIM}Untracked{Colors.RESET}"
        
        target_branch = ws.get("default_branch", "main")
        git_info = inspect_git_workspace(ws.get("path", ""), target_branch=target_branch)

        ahead_str = str(git_info.get("ahead", 0))
        behind_str = str(git_info.get("behind", 0))
        dirty_cnt = git_info.get("uncommitted_count", 0)
        dirty_str = f"{Colors.AMBER}{dirty_cnt} files{Colors.RESET}" if dirty_cnt > 0 else f"{Colors.GREEN}Clean{Colors.RESET}"

        remote = ws.get("remote_repo", "No remote")
        stdout.write(f"{ws_id:<18} {ws_name:<22} {track_label:<19} {target_branch:<10} {ahead_str:<8} {behind_str:<8} {dirty_str:<17} {remote}\n")

    # Google Drive Profiles Table
    stdout.write(f"\n{Colors.BOLD}{Colors.BLUE}Google Drive 1:1 Cloud Profiles ({len(profiles)} registered):{Colors.RESET}\n")
    stdout.write(f"{'ID':<24} {'NAME':<24} {'ENABLED':<10} {'GIT GATE':<18} {'REMOTE TARGET'}\n")
    stdout.write("-" * 98 + "\n")

    for p in profiles:
        prof_id = p.get("id", "")
        prof_name = p.get("name", prof_id)
        enabled = p.get("enabled", True)
        enabled_label = f"{Colors.GREEN}Enabled{Colors.RESET}" if enabled else f"{Colors.DIM}Disabled{Colors.RESET}"

        # Check gatekeeper
        source = p.get("source_path", "")
        if Path(source).exists():
            from backend.drive_engine import check_drive_gatekeeper
            is_clean, uncommitted = check_drive_gatekeeper(source)
            gate_str = f"{Colors.GREEN}Clean (Ready){Colors.RESET}" if is_clean else f"{Colors.AMBER}Dirty ({uncommitted} uncommitted){Colors.RESET}"
        else:
            gate_str = f"{Colors.RED}Path Missing{Colors.RESET}"

        target = p.get("remote_target", "")
        stdout.write(f"{prof_id:<24} {prof_name:<24} {enabled_label:<19} {gate_str:<27} {target}\n")

    stdout.write("\n")
    return 0


def cmd_sync_github(args, gh_config_path=None, log_dir=None, stdout=sys.stdout):
    log_file = (Path(log_dir) / "github-sync.log") if log_dir else None
    dry_run = getattr(args, "dry_run", False)
    specific_repo = getattr(args, "repo", None)
    date_str = getattr(args, "date", None)
    is_json = getattr(args, "json", False)
    is_pull = getattr(args, "pull", False)

    cfg = load_github_config(gh_config_path)
    workspaces = cfg.get("workspaces", [])

    if is_pull:
        if not is_json:
            mode_label = f"{Colors.AMBER}[Dry Run]{Colors.RESET} " if dry_run else ""
            stdout.write(f"\n{Colors.BOLD}=== {mode_label}Executing Safe Fast-Forward Pull ==={Colors.RESET}\n")

        results = pull_all_repos(
            workspaces=workspaces,
            dry_run=dry_run,
            specific_id=specific_repo,
            log_path=log_file,
        )

        if is_json:
            stdout.write(json.dumps(results, indent=2) + "\n")
            return 0

        if not results:
            stdout.write("No eligible repositories to pull matching filter.\n")
            return 0

        for r in results:
            r_id = r["id"]
            status = r["status"]
            if status == "clean":
                stdout.write(f"  {Colors.GREEN}✓{Colors.RESET} {r_id}: Up to date with origin/{r['target_branch']} (Clean)\n")
            elif status == "ahead":
                stdout.write(f"  {Colors.GREEN}✓{Colors.RESET} {r_id}: Local is ahead by {r['ahead']} commits (No pull needed)\n")
            elif status == "dry_run":
                stdout.write(f"  {Colors.AMBER}⚡{Colors.RESET} {r_id}: Would fast-forward pull {r['behind']} commits\n")
            elif status == "pulled":
                stdout.write(f"  {Colors.GREEN}✓{Colors.RESET} {r_id}: Fast-forward pulled {r['behind']} new commits from origin/{r['target_branch']}\n")
            elif status == "dirty_blocked":
                stdout.write(f"  {Colors.AMBER}⚠{Colors.RESET} {r_id}: Pull blocked — {r.get('error')}\n")
            elif status == "diverged":
                stdout.write(f"  {Colors.RED}✕{Colors.RESET} {r_id}: Pull stopped — {r.get('error')}\n")
            else:
                stdout.write(f"  {Colors.RED}✕{Colors.RESET} {r_id}: Failed ({r.get('error')})\n")

        stdout.write(f"\nAudit log saved to {log_file or 'logs/github-sync.log'}\n\n")
        return 0

    if not is_json:
        mode_label = f"{Colors.AMBER}[Dry Run]{Colors.RESET} " if dry_run else ""
        stdout.write(f"\n{Colors.BOLD}=== {mode_label}Syncing Tracked GitHub Repositories ==={Colors.RESET}\n")

    cfg = load_github_config(gh_config_path)
    workspaces = cfg.get("workspaces", [])

    results = sync_all_tracked_repos(
        workspaces=workspaces,
        dry_run=dry_run,
        date_str=date_str,
        specific_id=specific_repo,
        log_path=log_file,
    )

    if is_json:
        stdout.write(json.dumps(results, indent=2) + "\n")
        return 0

    if not results:
        stdout.write(f"No tracked repositories to sync matching filter.\n")
        return 0

    for r in results:
        r_id = r["id"]
        status = r["status"]
        if status == "clean":
            stdout.write(f"  {Colors.GREEN}✓{Colors.RESET} {r_id}: Up to date (Clean)\n")
        elif status == "dry_run":
            would = []
            if r.get("would_commit"):
                would.append(f"commit {r['uncommitted_count']} files ({r['commit_message']})")
            if r.get("would_push"):
                would.append(f"push to origin/{r['target_branch']}")
            stdout.write(f"  {Colors.AMBER}⚡{Colors.RESET} {r_id}: Would {' and '.join(would)}\n")
        elif status == "synced":
            actions = []
            if r.get("committed"):
                actions.append(f"committed {r['uncommitted_count']} files")
            if r.get("pushed"):
                actions.append(f"pushed to origin/{r['target_branch']}")
            stdout.write(f"  {Colors.GREEN}✓{Colors.RESET} {r_id}: Successfully {' and '.join(actions)}\n")
        else:
            stdout.write(f"  {Colors.RED}✕{Colors.RESET} {r_id}: Failed ({r.get('error')})\n")

    stdout.write(f"\nAudit log saved to {log_file or 'logs/github-sync.log'}\n\n")
    return 0


def cmd_sync_drive(args, drive_config_path=None, log_dir=None, stdout=sys.stdout):
    log_file = (Path(log_dir) / "drive-sync.log") if log_dir else None
    dry_run = getattr(args, "dry_run", False)
    force = getattr(args, "force", False)
    auto_commit = getattr(args, "auto_commit", True)
    date_str = getattr(args, "date", None)
    is_diff = getattr(args, "diff", False)
    is_json = getattr(args, "json", False)
    specific_profile = getattr(args, "profile", None)

    cfg = load_drive_config(drive_config_path)
    profiles = cfg.get("profiles", [])

    targets = [p for p in profiles if p.get("enabled", True) is not False]
    if specific_profile:
        targets = [p for p in targets if p.get("id") == specific_profile]

    if not targets:
        if is_json:
            stdout.write(json.dumps([], indent=2) + "\n")
        else:
            stdout.write("No enabled Drive profiles found.\n")
        return 0

    if is_diff:
        if not is_json:
            stdout.write(f"\n{Colors.BOLD}=== Checking Google Drive Diffs ==={Colors.RESET}\n")
        diff_results = []
        for p in targets:
            if not is_json:
                stdout.write(f"Checking diff for {Colors.CYAN}{p['id']}{Colors.RESET}...\n")
            res = check_drive_diff(p, log_path=log_file)
            diff_results.append(res)
            if not is_json:
                stdout.write(f"{res.get('output', '')}\n")
        if is_json:
            stdout.write(json.dumps(diff_results, indent=2) + "\n")
        return 0

    if not is_json:
        mode_label = f"{Colors.AMBER}[Dry Run]{Colors.RESET} " if dry_run else ""
        stdout.write(f"\n{Colors.BOLD}=== {mode_label}Executing Google Drive 1:1 Mirror Sync ==={Colors.RESET}\n")

    results = []
    for p in targets:
        p_id = p["id"]
        if not is_json:
            stdout.write(f"Processing {Colors.CYAN}{p_id}{Colors.RESET} ({p.get('source_path')} -> {p.get('remote_target')})...\n")
        res = sync_drive_profile(
            p,
            dry_run=dry_run,
            force=force,
            auto_commit=auto_commit,
            date_str=date_str,
            log_path=log_file,
        )
        results.append(res)

        if not is_json:
            if res.get("would_commit"):
                stdout.write(f"  {Colors.AMBER}⚡ [Dry-Run] Would commit {res['uncommitted_count']} files locally ({res['commit_message']}){Colors.RESET}\n")
            elif res.get("committed"):
                stdout.write(f"  {Colors.GREEN}✓ Committed {res['uncommitted_count']} files locally ({res['commit_message']}){Colors.RESET}\n")

            if res["status"] == "blocked_by_git":
                stdout.write(f"  {Colors.AMBER}⚠️ Blocked by Git Gatekeeper:{Colors.RESET} {res['error']}\n")
            elif res["success"]:
                stdout.write(f"  {Colors.GREEN}✓ {'[Dry-Run] ' if dry_run else ''}Sync complete.{Colors.RESET}\n")
            else:
                stdout.write(f"  {Colors.RED}✕ Sync failed:{Colors.RESET} {res.get('error')}\n")

    if is_json:
        stdout.write(json.dumps(results, indent=2) + "\n")
        return 0

    stdout.write(f"\nAudit log saved to {log_file or 'logs/drive-sync.log'}\n\n")
    return 0


def cmd_track(args, gh_config_path=None, drive_config_path=None, stdout=sys.stdout):
    sub = args.track_subsystem
    target_id = args.id

    if sub == "github":
        enable = args.enable
        ok = update_workspace(target_id, {"tracked": enable}, config_path=gh_config_path)
        if ok:
            status_txt = f"{Colors.GREEN}tracked{Colors.RESET}" if enable else f"{Colors.DIM}untracked{Colors.RESET}"
            stdout.write(f"Repository {Colors.BOLD}{target_id}{Colors.RESET} is now {status_txt}.\n")
            return 0
        stdout.write(f"{Colors.RED}Repository '{target_id}' not found in github-track.yaml.{Colors.RESET}\n")
        return 1

    elif sub == "drive":
        enable = args.enable
        ok = update_drive_profile(target_id, {"enabled": enable}, config_path=drive_config_path)
        if ok:
            status_txt = f"{Colors.GREEN}enabled{Colors.RESET}" if enable else f"{Colors.DIM}disabled{Colors.RESET}"
            stdout.write(f"Drive profile {Colors.BOLD}{target_id}{Colors.RESET} is now {status_txt}.\n")
            return 0
        stdout.write(f"{Colors.RED}Drive profile '{target_id}' not found in drive-track.yaml.{Colors.RESET}\n")
        return 1

    return 1


def cmd_share(args, drive_config_path=None, stdout=sys.stdout):
    target_id = args.id
    cfg = load_drive_config(drive_config_path)
    profiles = cfg.get("profiles", [])
    prof = next((p for p in profiles if p.get("id") == target_id), None)

    if not prof:
        stdout.write(f"{Colors.RED}Drive profile '{target_id}' not found.{Colors.RESET}\n")
        return 1

    stdout.write(f"Generating public read-only link for {Colors.BOLD}{prof['id']}{Colors.RESET} ({prof.get('remote_target')})...\n")
    link = get_public_share_link(prof)
    if link:
        stdout.write(f"\n{Colors.GREEN}{Colors.BOLD}Public Read-Only Link:{Colors.RESET}\n{link}\n\n")
        return 0
    else:
        stdout.write(f"{Colors.RED}Could not generate public link via rclone.{Colors.RESET}\n")
        return 1


def main(argv=None, gh_config_path=None, drive_config_path=None, log_dir=None, stdout=sys.stdout) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if not args.command:
        parser.print_help(stdout)
        return 0

    if args.command == "status":
        return cmd_status(args=args, gh_config_path=gh_config_path, drive_config_path=drive_config_path, stdout=stdout)

    elif args.command == "sync":
        if args.sync_target == "github":
            return cmd_sync_github(args, gh_config_path=gh_config_path, log_dir=log_dir, stdout=stdout)
        elif args.sync_target == "drive":
            return cmd_sync_drive(args, drive_config_path=drive_config_path, log_dir=log_dir, stdout=stdout)
        else:
            parser.parse_args(["sync", "--help"])
            return 0

    elif args.command == "track":
        return cmd_track(args, gh_config_path=gh_config_path, drive_config_path=drive_config_path, stdout=stdout)

    elif args.command == "share":
        return cmd_share(args, drive_config_path=drive_config_path, stdout=stdout)

    elif args.command == "pull":
        setattr(args, "pull", True)
        return cmd_sync_github(args, gh_config_path=gh_config_path, log_dir=log_dir, stdout=stdout)

    return 0


if __name__ == "__main__":
    sys.exit(main())
