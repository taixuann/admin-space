"""Bridge Google Drive Engine: Handles 1:1 mirror synchronization via rclone,
pre-sync Git gatekeeper checks, exclude rules formatting, and audit logging.
"""
from __future__ import annotations

import os
import subprocess
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

DEFAULT_LOG_FILE = Path(__file__).resolve().parent.parent / "logs" / "drive-sync.log"


def run_cmd(args: List[str], cwd: Optional[str] = None, timeout: Optional[int] = 60) -> tuple[int, str, str]:
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


def append_drive_log(msg: str, log_path: Optional[Path] = None) -> None:
    p = Path(log_path) if log_path else DEFAULT_LOG_FILE
    p.parent.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(p, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {msg}\n")


def build_rclone_exclude_flags(excludes_str: str) -> List[str]:
    raw = [e.strip() for e in (excludes_str or "").split(",") if e.strip()]
    flags = []
    
    # Always ensure .git is strictly excluded from Google Drive (root and nested)
    has_git = False
    for item in raw:
        clean = item.rstrip("/")
        if clean in (".git", ".git/**"):
            has_git = True
            flags.extend(["--exclude", ".git/**", "--exclude", "**/.git/**"])
        elif clean.endswith("/**"):
            base = clean[:-3]
            flags.extend(["--exclude", clean, "--exclude", f"**/{base}/**"])
        elif clean.endswith("*"):
            flags.extend(["--exclude", clean, "--exclude", f"**/{clean}"])
        elif clean in (".DS_Store", "Thumbs.db"):
            flags.extend(["--exclude", clean, "--exclude", f"**/{clean}"])
        else:
            # Match folder at root and any nested level
            flags.extend(["--exclude", f"{clean}/**", "--exclude", f"**/{clean}/**"])

    if not has_git:
        flags.extend(["--exclude", ".git/**", "--exclude", "**/.git/**"])

    return flags


def check_drive_gatekeeper(source_path: str) -> Tuple[bool, int]:
    source = Path(os.path.expanduser(source_path))
    if not source.exists() or not source.is_dir():
        return False, 0

    code, out, _ = run_cmd(["git", "rev-parse", "--is-inside-work-tree"], cwd=str(source))
    if code != 0 or out != "true":
        # Not a git repo, no git commit gatekeeper restriction
        return True, 0

    code, stat_out, _ = run_cmd(["git", "status", "--porcelain"], cwd=str(source))
    if code == 0:
        lines = [l for l in stat_out.split("\n") if l.strip()]
        return (len(lines) == 0), len(lines)

    return True, 0


def check_drive_diff(profile: Dict[str, Any], log_path: Optional[Path] = None) -> Dict[str, Any]:
    prof_id = profile.get("id", "unknown")
    source_path = str(Path(os.path.expanduser(profile.get("source_path", ""))).resolve())
    remote_target = profile.get("remote_target", "")

    if not source_path or not Path(source_path).exists():
        return {"id": prof_id, "success": False, "error": "Source path does not exist", "output": ""}

    exclude_flags = build_rclone_exclude_flags(profile.get("exclude_patterns", ""))
    cmd = ["rclone", "check", source_path, remote_target, "--combined", "-", "--fast-list"] + exclude_flags

    append_drive_log(f"[{prof_id}] Checking diff: {source_path} <=> {remote_target}", log_path)
    code, out, err = run_cmd(cmd, timeout=30)
    
    return {
        "id": prof_id,
        "success": (code == 0),
        "code": code,
        "output": out or err,
    }


def format_automation_commit_msg(date_str: Optional[str] = None) -> str:
    today = date_str or datetime.now().strftime("%Y-%m-%d")
    return f"automation: {today} commit automatically"


def sync_drive_profile(
    profile: Dict[str, Any],
    dry_run: bool = False,
    force: bool = False,
    auto_commit: bool = True,
    date_str: Optional[str] = None,
    log_path: Optional[Path] = None,
) -> Dict[str, Any]:
    prof_id = profile.get("id", "unknown")
    prof_name = profile.get("name", prof_id)
    source_path = str(Path(os.path.expanduser(profile.get("source_path", ""))).resolve())
    remote_target = profile.get("remote_target", "")

    result = {
        "id": prof_id,
        "name": prof_name,
        "source_path": source_path,
        "remote_target": remote_target,
        "status": "unknown",
        "success": False,
        "error": None,
        "uncommitted_count": 0,
        "would_commit": False,
        "committed": False,
        "commit_message": None,
        "output": "",
    }

    if not source_path or not Path(source_path).exists():
        result["status"] = "missing_source"
        result["error"] = f"Local source directory does not exist: {source_path}"
        append_drive_log(f"[{prof_id}] Error: Local directory missing ({source_path})", log_path)
        return result

    # Pre-sync Git Gatekeeper & Local Auto-commit Check
    is_clean, uncommitted_count = check_drive_gatekeeper(source_path)
    result["uncommitted_count"] = uncommitted_count

    if not is_clean:
        if auto_commit:
            commit_msg = format_automation_commit_msg(date_str)
            result["commit_message"] = commit_msg
            if dry_run:
                result["would_commit"] = True
                append_drive_log(
                    f"[{prof_id}] Dry-run: Would stage & commit {uncommitted_count} files locally ({commit_msg})",
                    log_path,
                )
            else:
                c_add, _, err_add = run_cmd(["git", "add", "-A"], cwd=source_path)
                if c_add != 0:
                    result["status"] = "error"
                    result["error"] = f"git add failed: {err_add}"
                    append_drive_log(f"[{prof_id}] Error during git add: {err_add}", log_path)
                    return result

                c_commit, _, err_commit = run_cmd(["git", "commit", "-m", commit_msg], cwd=source_path)
                if c_commit != 0:
                    result["status"] = "error"
                    result["error"] = f"git commit failed: {err_commit}"
                    append_drive_log(f"[{prof_id}] Error during git commit: {err_commit}", log_path)
                    return result

                result["committed"] = True
                append_drive_log(f"[{prof_id}] Committed {uncommitted_count} files locally: {commit_msg}", log_path)
        elif not force:
            result["status"] = "blocked_by_git"
            result["error"] = f"Git commit required ({uncommitted_count} uncommitted changes). Commit local changes or use --force to override."
            append_drive_log(f"[{prof_id}] Blocked by Git Gatekeeper: {uncommitted_count} uncommitted files", log_path)
            return result

    # Build rclone 1:1 mirror sync command with network retry & resilience flags
    exclude_flags = build_rclone_exclude_flags(profile.get("exclude_patterns", ""))
    cmd = [
        "rclone", "sync", source_path, remote_target,
        "--fast-list",
        "--retries", "5",
        "--low-level-retries", "10",
        "--retries-sleep", "5s",
        "--timeout", "60s",
        "--contimeout", "30s",
        "--checkers", "8",
        "--transfers", "4",
    ] + exclude_flags

    if dry_run:
        cmd.append("--dry-run")
        result["status"] = "dry_run"
        append_drive_log(f"[{prof_id}] Dry-run: rclone {' '.join(cmd)}", log_path)
    else:
        append_drive_log(f"[{prof_id}] Starting 1:1 sync: {source_path} -> {remote_target}", log_path)

    custom_timeout = profile.get("timeout")
    if custom_timeout:
        sync_timeout = int(custom_timeout) if not dry_run else 180
    else:
        sync_timeout = 180 if dry_run else 7200  # 3 minutes for dry-run, up to 2 hours for live upload

    # Retry loop for whole rclone operation on transient network failure
    max_sync_attempts = 1 if dry_run else 3
    code, out, err = -1, "", ""
    for attempt in range(1, max_sync_attempts + 1):
        code, out, err = run_cmd(cmd, timeout=sync_timeout)
        if code == 0:
            break
        if attempt < max_sync_attempts:
            append_drive_log(
                f"[{prof_id}] Sync attempt {attempt} failed ({err or out or 'code ' + str(code)}). Retrying in {10 * attempt}s...",
                log_path,
            )
            time.sleep(10 * attempt)

    if code == 0:
        result["success"] = True
        result["status"] = "dry_run" if dry_run else "synced"
        result["output"] = out or "Sync completed cleanly."
        append_drive_log(f"[{prof_id}] {'Dry-run complete' if dry_run else 'Sync completed successfully'}.", log_path)
    else:
        result["status"] = "error"
        result["error"] = err or out or "rclone sync failed"
        append_drive_log(f"[{prof_id}] Error during rclone sync: {result['error']}", log_path)

    return result


def get_public_share_link(profile: Dict[str, Any]) -> Optional[str]:
    remote_target = profile.get("remote_target", "")
    if not remote_target:
        return None

    code, out, _ = run_cmd(["rclone", "link", remote_target], timeout=15)
    if code == 0 and out:
        # Last non-empty line contains the URL
        lines = [l.strip() for l in out.split("\n") if l.strip()]
        return lines[-1] if lines else None
    return None
