"""Skills updater module for global skills via npx skills, lockfile reconciliation, and mirror sync."""
from __future__ import annotations

import json
import os
import re
import subprocess
from typing import Any, Dict, List, Optional, TypedDict

try:
    from .notion_reporter import report_incident
except ImportError:
    from notion_reporter import report_incident

AGENTS_DIR = os.path.expanduser("~/.agents")
SKILL_LOCK_PATH = os.path.join(AGENTS_DIR, ".skill-lock.json")
SKILLS_DIR = os.path.join(AGENTS_DIR, "skills")


class SkillsUpdateResult(TypedDict):
    success: bool
    exit_code: int
    output: str
    reconciled_skills: List[str]
    skipped_custom_skills: List[str]
    failures: List[Dict[str, str]]


class SyncMirrorsResult(TypedDict):
    success: bool
    exit_code: int
    output: str


def get_environment() -> Dict[str, str]:
    """Prepares execution environment with fnm default node in PATH."""
    fnm_bin = os.path.expanduser("~/.local/share/fnm/aliases/default/bin")
    env = os.environ.copy()
    env["PATH"] = f"{fnm_bin}:{env.get('PATH', '')}"
    return env


def reconcile_skill_lock(
    agents_dir: str = AGENTS_DIR,
    lock_file: str = SKILL_LOCK_PATH,
) -> Dict[str, Any]:
    """Scans ~/.agents/skills/ and reconciles newly discovered external skills into .skill-lock.json.

    Local custom skills (source is None) are preserved and passed without adding.
    """
    env = get_environment()
    reconciled: List[str] = []
    skipped_custom: List[str] = []

    # Read existing lockfile
    lock_data: Dict[str, Any] = {"version": 3, "skills": {}}
    if os.path.isfile(lock_file):
        try:
            with open(lock_file, "r", encoding="utf-8") as f:
                lock_data = json.load(f)
        except Exception:
            pass

    existing_locked_skills = lock_data.get("skills", {})

    # Query skills CLI for current global skills
    try:
        proc = subprocess.run(
            ["npx", "--yes", "skills", "list", "-g", "--json"],
            env=env,
            cwd=agents_dir,
            capture_output=True,
            text=True,
            timeout=45,
            check=False,
        )
        if proc.returncode == 0 and proc.stdout.strip():
            skills_list = json.loads(proc.stdout)
            for item in skills_list:
                name = item.get("name")
                item_path = item.get("path", "")
                source = item.get("source")
                source_url = item.get("sourceUrl")

                # Only consider skills located inside ~/.agents/skills/
                if not name or not item_path.startswith(SKILLS_DIR):
                    continue

                if source is None or source_url is None:
                    # Local custom skill -> pass
                    skipped_custom.append(name)
                else:
                    # External skill
                    if name not in existing_locked_skills:
                        # Register into lockfile
                        existing_locked_skills[name] = {
                            "source": source,
                            "sourceType": item.get("sourceType", "github"),
                            "sourceUrl": source_url,
                            "skillPath": f"skills/{name}/SKILL.md",
                            "skillFolderHash": "",
                            "installedAt": datetime_now_iso(),
                            "updatedAt": datetime_now_iso(),
                        }
                        reconciled.append(name)

            if reconciled:
                lock_data["skills"] = existing_locked_skills
                with open(lock_file, "w", encoding="utf-8") as f:
                    json.dump(lock_data, f, indent=2)
    except Exception:
        pass

    return {
        "reconciled": reconciled,
        "skipped_custom": skipped_custom,
    }


def datetime_now_iso() -> str:
    import datetime
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def detect_and_report_failures(output: str) -> List[Dict[str, str]]:
    """Detects 404s, missing repos, or network errors and reports them to Notion."""
    failures: List[Dict[str, str]] = []

    # Patterns for 404 or repository not found
    patterns = [
        r"(?:Updating|Checking skills from source:)\s*([^\n\r]+)[\s\S]*?(?:404|Repository not found|fatal: repository .* not found)",
        r"(?:Error|Failed).*?skill\s+([a-zA-Z0-9_-]+):?\s*([^\n]+)",
        r"fatal: repository '([^']+)' not found",
    ]

    for pat in patterns:
        matches = re.finditer(pat, output, re.IGNORECASE)
        for m in matches:
            target = m.group(1).strip()
            details = m.group(0).strip()
            failures.append({
                "target": target,
                "error": details,
            })
            # Report to Notion Agents Ticket
            try:
                report_incident(
                    title=f"[Auto-Sync] Skill update failure: {target}",
                    error_details=details,
                    component="Skills & Integrations",
                )
            except Exception:
                pass

    return failures


def update_global_skills(timeout: int = 180) -> SkillsUpdateResult:
    """Reconciles lockfile, runs `npx skills update -g -y`, and tracks failures."""
    env = get_environment()

    # Step A: Reconcile lockfile with skills folder
    reconcile_res = reconcile_skill_lock()

    # Step B: Run skills update
    try:
        proc = subprocess.run(
            ["npx", "--yes", "skills", "update", "-g", "-y"],
            env=env,
            cwd=AGENTS_DIR,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
        combined = (proc.stdout + "\n" + proc.stderr).strip()

        # Step C: Detect 404s or specific skill failures
        failures = detect_and_report_failures(combined)

        return {
            "success": proc.returncode == 0,
            "exit_code": proc.returncode,
            "output": combined,
            "reconciled_skills": reconcile_res.get("reconciled", []),
            "skipped_custom_skills": reconcile_res.get("skipped_custom", []),
            "failures": failures,
        }
    except Exception as exc:
        err_msg = f"Exception updating global skills: {exc}"
        try:
            report_incident(
                title="[Auto-Sync] Global skills process exception",
                error_details=err_msg,
                component="Skills & Integrations",
            )
        except Exception:
            pass

        return {
            "success": False,
            "exit_code": -1,
            "output": err_msg,
            "reconciled_skills": reconcile_res.get("reconciled", []),
            "skipped_custom_skills": reconcile_res.get("skipped_custom", []),
            "failures": [{"target": "global_skills", "error": err_msg}],
        }


def sync_mirrors(sync_bin: str = "/Users/tai/.agents/bin/sync-skills") -> SyncMirrorsResult:
    """Runs sync-skills to mirror ~/.agents/skills into ~/.claude/skills and ~/.gemini/config/skills."""
    if not os.path.isfile(sync_bin):
        return {
            "success": False,
            "exit_code": 1,
            "output": f"Sync script not found: {sync_bin}",
        }

    try:
        proc = subprocess.run(
            ["/bin/bash", sync_bin],
            capture_output=True,
            text=True,
            timeout=45,
            check=False,
        )
        combined = (proc.stdout + "\n" + proc.stderr).strip()
        return {
            "success": proc.returncode == 0,
            "exit_code": proc.returncode,
            "output": combined,
        }
    except Exception as exc:
        return {
            "success": False,
            "exit_code": -1,
            "output": f"Exception syncing skill mirrors: {exc}",
        }
