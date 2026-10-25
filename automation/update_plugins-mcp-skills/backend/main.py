#!/usr/bin/env python3
"""Main entrypoint for daily global plugins and skills maintenance."""
from __future__ import annotations

import argparse
import datetime
import fcntl
import glob
import json
import os
import sys
import tempfile
import time
import uuid

# Ensure backend package can be imported directly
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from notion_reporter import report_incident
from plugins_updater import update_caveman, update_superpowers
from skills_updater import sync_mirrors, update_global_skills

LABEL = "com.tai.update-plugins-mcp-skills"
RETENTION_DAYS = 30


def write_atomic_json(filepath: str, data: dict) -> None:
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    temp_fd, temp_path = tempfile.mkstemp(
        dir=os.path.dirname(filepath),
        prefix=".tmp_result_",
        suffix=".json",
    )
    with os.fdopen(temp_fd, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    os.replace(temp_path, filepath)


def cleanup_old_records(report_root: str, retention_days: int = RETENTION_DAYS) -> int:
    """Removes run records older than retention_days."""
    now = time.time()
    cutoff = now - (retention_days * 86400)
    removed_count = 0

    runs_dir = os.path.join(report_root, "runs")
    if os.path.isdir(runs_dir):
        for entry in os.scandir(runs_dir):
            if entry.is_file() and entry.stat().st_mtime < cutoff:
                try:
                    os.remove(entry.path)
                    removed_count += 1
                except Exception:
                    pass

    # Also clean any rotated log archives if present (e.g. stdout.log.*)
    for archive in glob.glob(os.path.join(report_root, "*.log.*")):
        try:
            if os.path.getmtime(archive) < cutoff:
                os.remove(archive)
                removed_count += 1
        except Exception:
            pass

    return removed_count


def run_maintenance(
    report_root: str,
    dry_run: bool = False,
) -> int:
    run_id = f"run_{int(time.time())}_{uuid.uuid4().hex[:8]}"
    start_dt = datetime.datetime.now(datetime.timezone.utc)
    start_time_iso = start_dt.isoformat()
    t0 = time.time()

    os.makedirs(report_root, exist_ok=True)
    stdout_log = os.path.join(report_root, "stdout.log")
    stderr_log = os.path.join(report_root, "stderr.log")
    lock_file = os.path.join(report_root, ".lock")

    def log(msg: str) -> None:
        ts = datetime.datetime.now(datetime.timezone.utc).isoformat()
        line = f"[{ts}] {msg}"
        print(line)
        try:
            with open(stdout_log, "a", encoding="utf-8") as f:
                f.write(line + "\n")
        except Exception:
            pass

    def log_err(msg: str) -> None:
        ts = datetime.datetime.now(datetime.timezone.utc).isoformat()
        line = f"[{ts}] ERROR: {msg}"
        print(line, file=sys.stderr)
        try:
            with open(stderr_log, "a", encoding="utf-8") as f:
                f.write(line + "\n")
        except Exception:
            pass

    # Clean old records > 30 days
    cleaned = cleanup_old_records(report_root, RETENTION_DAYS)
    if cleaned > 0:
        log(f"Retention policy: cleaned {cleaned} file(s) older than {RETENTION_DAYS} days.")

    # Acquire file lock to prevent concurrent executions
    lock_fd = None
    try:
        lock_fd = open(lock_file, "w")
        fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except (IOError, BlockingIOError):
        if lock_fd:
            try:
                lock_fd.close()
            except Exception:
                pass
        log("Skipping run: Another instance holds the lock (.lock).")
        result_payload = {
            "run_id": run_id,
            "label": LABEL,
            "start_time": start_time_iso,
            "end_time": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "duration_seconds": round(time.time() - t0, 4),
            "outcome": "skipped_locked",
            "exit_code": 0,
            "details": {"reason": "concurrent run locked"},
        }
        write_atomic_json(os.path.join(report_root, "latest-result.json"), result_payload)
        print('terminal={"outcome": "skipped_locked", "exit_code": 0}')
        return 0

    log(f"=== Starting global plugins and skills maintenance {run_id} (dry_run={dry_run}) ===")

    if dry_run:
        log("DRY RUN: skipping mutations.")
        details = {
            "superpowers": {"dry_run": True},
            "caveman": {"dry_run": True},
            "skills_update": {"dry_run": True},
            "skills_sync": {"dry_run": True},
        }
        outcome = "cached"
        exit_code = 0
    else:
        # Phase 1: Update Superpowers
        log("Phase 1: Updating Superpowers plugin from upstream...")
        sp_res = update_superpowers()
        if sp_res["success"]:
            log(f"Phase 1: Superpowers OK (updated={sp_res['updated']}, HEAD={sp_res['head_sha'][:12] if sp_res['head_sha'] else 'unknown'})")
        else:
            log_err(f"Phase 1: Superpowers update failed: {sp_res['output']}")
            report_incident(
                title="[Auto-Sync] Superpowers plugin update failure",
                error_details=sp_res["output"],
                component="Skills & Integrations",
            )

        # Phase 2: Update Caveman hooks
        log("Phase 2: Updating Caveman command rewrite hooks...")
        caveman_res = update_caveman()
        if caveman_res["success"]:
            log("Phase 2: Caveman hooks installed/verified OK")
        else:
            log_err(f"Phase 2: Caveman hooks failed: {caveman_res['output']}")
            report_incident(
                title="[Auto-Sync] Caveman hooks install failure",
                error_details=caveman_res["output"],
                component="Automations & Runtime",
            )

        # Phase 3: Update Global Skills via npx skills (with lockfile reconciliation & 404 detection)
        log("Phase 3: Reconciling lockfile and updating global skills...")
        skills_res = update_global_skills()
        if skills_res["success"]:
            log(f"Phase 3: Global skills update OK (exit {skills_res['exit_code']}, reconciled={skills_res.get('reconciled_skills')}, removed={skills_res.get('removed_skills')})")
        else:
            log_err(f"Phase 3: Global skills update failed: {skills_res['output']}")

        # Phase 4: Sync Skill Mirrors to ~/.claude/skills and ~/.gemini/config/skills
        log("Phase 4: Syncing skill mirrors...")
        sync_res = sync_mirrors()
        if sync_res["success"]:
            log("Phase 4: Skill mirrors synchronized OK")
        else:
            log_err(f"Phase 4: Skill mirrors sync failed: {sync_res['output']}")
            report_incident(
                title="[Auto-Sync] Skill mirrors sync failure",
                error_details=sync_res["output"],
                component="Skills & Integrations",
            )

        all_ok = sp_res["success"] and caveman_res["success"] and skills_res["success"] and sync_res["success"]
        outcome = "success" if all_ok else "failed"
        exit_code = 0 if all_ok else 1

        details = {
            "superpowers": sp_res,
            "caveman": caveman_res,
            "skills_update": skills_res,
            "skills_sync": sync_res,
        }

    duration = time.time() - t0
    end_dt = datetime.datetime.now(datetime.timezone.utc)
    end_time_iso = end_dt.isoformat()

    result_payload = {
        "run_id": run_id,
        "label": LABEL,
        "start_time": start_time_iso,
        "end_time": end_time_iso,
        "duration_seconds": round(duration, 4),
        "outcome": outcome,
        "exit_code": exit_code,
        "details": details,
    }

    latest_result_path = os.path.join(report_root, "latest-result.json")
    try:
        write_atomic_json(latest_result_path, result_payload)
    except Exception as exc:
        log_err(f"Failed to write latest-result.json: {exc}")

    # Also record individual run record under runs/
    runs_dir = os.path.join(report_root, "runs")
    try:
        os.makedirs(runs_dir, exist_ok=True)
        write_atomic_json(os.path.join(runs_dir, f"{run_id}.json"), result_payload)
    except Exception:
        pass

    log(f"=== Maintenance completed with outcome={outcome} (exit_code={exit_code}, duration={duration:.2f}s) ===")
    print(f'terminal={{"outcome": "{outcome}", "exit_code": {exit_code}}}')

    # Release lock
    if lock_fd:
        try:
            fcntl.flock(lock_fd, fcntl.LOCK_UN)
            lock_fd.close()
        except Exception:
            pass

    return exit_code


def main() -> None:
    parser = argparse.ArgumentParser(description="Daily maintenance service for global plugins and skills.")
    parser.add_argument(
        "--report-root",
        required=True,
        help="Absolute path to runtime report directory (holds logs and latest-result.json)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run without making network calls or updates",
    )

    args = parser.parse_args()
    code = run_maintenance(
        report_root=os.path.abspath(args.report_root),
        dry_run=args.dry_run,
    )
    sys.exit(code)


if __name__ == "__main__":
    main()
