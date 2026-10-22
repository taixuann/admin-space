"""Bridge Git Engine: Handles automated local staging, commit, and remote push for tracked repositories."""
from __future__ import annotations

import os
import subprocess
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

DEFAULT_LOG_FILE = Path(__file__).resolve().parent.parent / "logs" / "github-sync.log"


def run_cmd(args: List[str], cwd: Optional[str] = None, timeout: int = 20) -> tuple[int, str, str]:
    try:
        res = subprocess.run(
            args,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
        return res.returncode, res.stdout.strip(), res.stderr.strip()
    except subprocess.TimeoutExpired:
        return -1, "", "Command timed out"
    except Exception as exc:
        return -1, "", str(exc)


def append_sync_log(msg: str, log_path: Optional[Path] = None) -> None:
    p = Path(log_path) if log_path else DEFAULT_LOG_FILE
    p.parent.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(p, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {msg}\n")


def format_automation_commit_msg(date_str: Optional[str] = None) -> str:
    ds = date_str or datetime.now().strftime("%Y-%m-%d")
    return f"automation: {ds} commit automatically"


def sync_tracked_repo(
    ws: Dict[str, Any],
    dry_run: bool = False,
    date_str: Optional[str] = None,
    log_path: Optional[Path] = None,
) -> Dict[str, Any]:
    ws_id = ws.get("id", "unknown")
    ws_name = ws.get("name", ws_id)
    repo_path = ws.get("path", "")
    target_branch = ws.get("default_branch", "main")

    result = {
        "id": ws_id,
        "name": ws_name,
        "path": repo_path,
        "target_branch": target_branch,
        "status": "unknown",
        "committed": False,
        "would_commit": False,
        "pushed": False,
        "would_push": False,
        "uncommitted_count": 0,
        "ahead": 0,
        "behind": 0,
        "commit_message": None,
        "error": None,
    }

    if not repo_path or not Path(repo_path).exists():
        result["status"] = "missing_path"
        result["error"] = f"Directory not found: {repo_path}"
        append_sync_log(f"[{ws_id}] Error: Directory not found ({repo_path})", log_path)
        return result

    code, is_git, _ = run_cmd(["git", "rev-parse", "--is-inside-work-tree"], cwd=repo_path)
    if code != 0 or is_git != "true":
        result["status"] = "no_git"
        result["error"] = "Not a git repository"
        append_sync_log(f"[{ws_id}] Error: Not a git repository", log_path)
        return result

    # Check uncommitted changes
    code, status_out, _ = run_cmd(["git", "status", "--porcelain"], cwd=repo_path)
    dirty_lines = [l for l in status_out.split("\n") if l.strip()] if code == 0 else []
    result["uncommitted_count"] = len(dirty_lines)

    # Check ahead / behind status focused on origin/{target_branch}
    ref_target = f"origin/{target_branch}"
    code, _, _ = run_cmd(["git", "rev-parse", "--verify", ref_target], cwd=repo_path)
    has_remote_ref = (code == 0)

    if has_remote_ref:
        code, ab_out, _ = run_cmd(
            ["git", "rev-list", "--left-right", "--count", f"{ref_target}...HEAD"],
            cwd=repo_path,
        )
        if code == 0 and ab_out:
            try:
                behind_str, ahead_str = ab_out.split()
                result["behind"] = int(behind_str)
                result["ahead"] = int(ahead_str)
            except Exception:
                pass

    commit_msg = format_automation_commit_msg(date_str)
    result["commit_message"] = commit_msg

    # 1. Handle uncommitted dirty files
    if len(dirty_lines) > 0:
        if dry_run:
            result["would_commit"] = True
            result["status"] = "dry_run"
            append_sync_log(f"[{ws_id}] Dry-run: Would stage & commit {len(dirty_lines)} files ({commit_msg})", log_path)
        else:
            # Stage all changes
            code, _, err = run_cmd(["git", "add", "-A"], cwd=repo_path)
            if code != 0:
                result["status"] = "error"
                result["error"] = f"git add failed: {err}"
                append_sync_log(f"[{ws_id}] Error during git add: {err}", log_path)
                return result

            # Commit
            code, _, err = run_cmd(["git", "commit", "-m", commit_msg], cwd=repo_path)
            if code != 0:
                result["status"] = "error"
                result["error"] = f"git commit failed: {err}"
                append_sync_log(f"[{ws_id}] Error during git commit: {err}", log_path)
                return result

            result["committed"] = True
            result["ahead"] += 1
            append_sync_log(f"[{ws_id}] Committed {len(dirty_lines)} files: {commit_msg}", log_path)

    # 2. Handle remote push if ahead
    if (result["ahead"] > 0 or result["committed"]) and has_remote_ref:
        if dry_run:
            result["would_push"] = True
            result["status"] = "dry_run"
            append_sync_log(f"[{ws_id}] Dry-run: Would push to origin/{target_branch}", log_path)
        else:
            max_push_retries = 3
            push_success = False
            last_err = ""
            for attempt in range(1, max_push_retries + 1):
                code, _, err = run_cmd(["git", "push", "origin", target_branch], cwd=repo_path, timeout=45)
                if code == 0:
                    push_success = True
                    break
                last_err = err
                is_net_err = any(w in err.lower() for w in (
                    "could not resolve", "timed out", "unreachable", "failed to connect",
                    "connection reset", "ssl", "handshake", "network"
                ))
                if is_net_err and attempt < max_push_retries:
                    append_sync_log(
                        f"[{ws_id}] Git push attempt {attempt} failed (transient network: {err}). Retrying in {5 * attempt}s...",
                        log_path,
                    )
                    time.sleep(5 * attempt)
                else:
                    break

            if not push_success:
                result["status"] = "error"
                result["error"] = f"git push failed: {last_err}"
                append_sync_log(f"[{ws_id}] Error during git push: {last_err}", log_path)
                return result

            result["pushed"] = True
            append_sync_log(f"[{ws_id}] Pushed to origin/{target_branch}", log_path)

    if result["status"] == "unknown":
        if result["committed"] or result["pushed"]:
            result["status"] = "synced"
        elif not result.get("would_commit") and not result.get("would_push"):
            result["status"] = "clean"
            if not dry_run:
                append_sync_log(f"[{ws_id}] In sync with origin/{target_branch} (Clean)", log_path)

    return result


def sync_all_tracked_repos(
    workspaces: Optional[List[Dict[str, Any]]] = None,
    dry_run: bool = False,
    date_str: Optional[str] = None,
    specific_id: Optional[str] = None,
    log_path: Optional[Path] = None,
) -> List[Dict[str, Any]]:
    from backend.config_manager import get_tracked_workspaces

    ws_list = workspaces if workspaces is not None else get_tracked_workspaces()
    results = []

    for ws in ws_list:
        # Strictly skip untracked repositories!
        if ws.get("tracked", True) is False:
            continue

        if specific_id and ws.get("id") != specific_id:
            continue

        res = sync_tracked_repo(ws, dry_run=dry_run, date_str=date_str, log_path=log_path)
        results.append(res)

    return results


def safe_pull_repo(
    ws: Dict[str, Any],
    dry_run: bool = False,
    log_path: Optional[Path] = None,
) -> Dict[str, Any]:
    ws_id = ws.get("id", "unknown")
    ws_name = ws.get("name", ws_id)
    repo_path = ws.get("path", "")
    target_branch = ws.get("default_branch", "main")

    result = {
        "id": ws_id,
        "name": ws_name,
        "path": repo_path,
        "target_branch": target_branch,
        "status": "unknown",
        "action": "pull",
        "pulled": False,
        "would_pull": False,
        "behind": 0,
        "ahead": 0,
        "uncommitted_count": 0,
        "error": None,
        "message": None,
    }

    if not repo_path or not Path(repo_path).exists():
        result["status"] = "missing_path"
        result["error"] = f"Directory not found: {repo_path}"
        append_sync_log(f"[{ws_id}] Pull Error: Directory not found ({repo_path})", log_path)
        return result

    code, is_git, _ = run_cmd(["git", "rev-parse", "--is-inside-work-tree"], cwd=repo_path)
    if code != 0 or is_git != "true":
        result["status"] = "no_git"
        result["error"] = "Not a git repository"
        append_sync_log(f"[{ws_id}] Pull Error: Not a git repository", log_path)
        return result

    # 1. Condition: Check working tree status FIRST
    code, status_out, _ = run_cmd(["git", "status", "--porcelain"], cwd=repo_path)
    dirty_lines = [l for l in status_out.split("\n") if l.strip()] if code == 0 else []
    result["uncommitted_count"] = len(dirty_lines)

    if len(dirty_lines) > 0:
        result["status"] = "dirty_blocked"
        result["error"] = f"Working tree has {len(dirty_lines)} uncommitted changes. Stash or commit before pulling."
        append_sync_log(f"[{ws_id}] Pull Blocked: {len(dirty_lines)} uncommitted local changes", log_path)
        return result

    # 2. Fetch remote (with retry on transient network errors)
    ref_target = f"origin/{target_branch}"
    max_fetch_retries = 3
    fetch_success = False
    last_err = ""
    for attempt in range(1, max_fetch_retries + 1):
        code, _, err = run_cmd(["git", "fetch", "--prune", "origin", target_branch], cwd=repo_path, timeout=45)
        if code == 0:
            fetch_success = True
            break
        last_err = err
        is_net_err = any(w in err.lower() for w in (
            "could not resolve", "timed out", "unreachable", "failed to connect",
            "connection reset", "ssl", "handshake", "network"
        ))
        if is_net_err and attempt < max_fetch_retries:
            append_sync_log(
                f"[{ws_id}] Git fetch attempt {attempt} failed (transient network: {err}). Retrying in {5 * attempt}s...",
                log_path,
            )
            time.sleep(5 * attempt)
        else:
            break

    if not fetch_success:
        result["status"] = "fetch_failed"
        result["error"] = f"git fetch failed: {last_err}"
        append_sync_log(f"[{ws_id}] Pull Error during git fetch: {last_err}", log_path)
        return result

    # 3. Check ahead / behind count
    code, _, _ = run_cmd(["git", "rev-parse", "--verify", ref_target], cwd=repo_path)
    if code != 0:
        result["status"] = "no_remote_branch"
        result["error"] = f"Remote branch {ref_target} not found"
        append_sync_log(f"[{ws_id}] Remote branch {ref_target} does not exist", log_path)
        return result

    code, ab_out, _ = run_cmd(
        ["git", "rev-list", "--left-right", "--count", f"{ref_target}...HEAD"],
        cwd=repo_path,
    )
    if code == 0 and ab_out:
        try:
            behind_str, ahead_str = ab_out.split()
            result["behind"] = int(behind_str)
            result["ahead"] = int(ahead_str)
        except Exception:
            pass

    behind = result["behind"]
    ahead = result["ahead"]

    # State A: Clean, no new commits on remote (behind == 0, ahead == 0) -> Skip
    if behind == 0 and ahead == 0:
        result["status"] = "clean"
        result["message"] = f"In sync with {ref_target} (Clean)"
        append_sync_log(f"[{ws_id}] Pull check: In sync with {ref_target} (Clean)", log_path)
        return result

    # State B: Local has commits not pushed (behind == 0, ahead > 0) -> Do not overwrite
    if behind == 0 and ahead > 0:
        result["status"] = "ahead"
        result["message"] = f"Local is ahead of {ref_target} by {ahead} commits. No pull needed."
        append_sync_log(f"[{ws_id}] Pull check: Local is ahead by {ahead} commits", log_path)
        return result

    # State C: Diverged (behind > 0 and ahead > 0) -> Stop and report conflict!
    if behind > 0 and ahead > 0:
        result["status"] = "diverged"
        result["error"] = f"Branch diverged (ahead {ahead}, behind {behind}). Fast-forward not possible; manual conflict resolution required."
        append_sync_log(f"[{ws_id}] Pull Stopped: Diverged branches (ahead {ahead}, behind {behind})", log_path)
        return result

    # State D: Clean, remote has new commits (behind > 0, ahead == 0) -> Safe fast-forward pull
    if behind > 0 and ahead == 0:
        if dry_run:
            result["would_pull"] = True
            result["status"] = "dry_run"
            result["message"] = f"Would fast-forward pull {behind} commits from {ref_target}"
            append_sync_log(f"[{ws_id}] Dry-run: Would fast-forward pull {behind} commits from {ref_target}", log_path)
            return result

        code, out, err = run_cmd(["git", "pull", "--ff-only", "origin", target_branch], cwd=repo_path, timeout=45)
        if code == 0:
            result["status"] = "pulled"
            result["pulled"] = True
            result["message"] = f"Fast-forward pulled {behind} new commits from {ref_target}"
            append_sync_log(f"[{ws_id}] Successfully fast-forward pulled {behind} commits", log_path)
            return result
        else:
            result["status"] = "pull_failed"
            result["error"] = f"git pull --ff-only failed: {err or out}"
            append_sync_log(f"[{ws_id}] Fast-forward pull failed: {err or out}", log_path)
            return result

    return result


def pull_all_repos(
    workspaces: Optional[List[Dict[str, Any]]] = None,
    dry_run: bool = False,
    specific_id: Optional[str] = None,
    log_path: Optional[Path] = None,
) -> List[Dict[str, Any]]:
    from backend.config_manager import load_github_config

    cfg = load_github_config()
    ws_list = workspaces if workspaces is not None else cfg.get("workspaces", [])
    results = []

    for ws in ws_list:
        ws_id = ws.get("id")
        if specific_id and ws_id != specific_id:
            continue
        # If no specific repo is requested: pull repos that have pull_enabled: True or tracked: True
        if not specific_id and not ws.get("pull_enabled", False) and not ws.get("tracked", False):
            continue

        res = safe_pull_repo(ws, dry_run=dry_run, log_path=log_path)
        results.append(res)

    return results
