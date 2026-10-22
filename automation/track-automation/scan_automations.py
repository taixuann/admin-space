#!/usr/bin/env python3
"""
Track Automation Scanner
Scans macOS LaunchAgents, Crontab, and local workspace automation registries.
Produces a unified, structured automations.json registry for the visual dashboard.
Zero-dependency: uses Python 3 standard library only.
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import plistlib
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent
OUTPUT_JSON_PATH = Path(__file__).resolve().parent / "automations.json"


def run_command(args: List[str], timeout: int = 10) -> tuple[int, str, str]:
    try:
        res = subprocess.run(args, capture_output=True, text=True, timeout=timeout, check=False)
        return res.returncode, res.stdout.strip(), res.stderr.strip()
    except Exception as exc:
        return -1, "", str(exc)


def format_bytes(size_bytes: int) -> str:
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.1f} MB"
    return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"


def inspect_file(path_str: Optional[str], tail_lines: int = 5) -> Optional[Dict[str, Any]]:
    if not path_str:
        return None
    p = Path(os.path.expanduser(path_str))
    if not p.exists():
        return {
            "path": str(p),
            "exists": False,
            "size": 0,
            "size_formatted": "0 B",
            "modified": None,
            "snippet": "",
        }

    try:
        stat = p.stat()
        size = stat.st_size
        mtime = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")

        snippet = ""
        try:
            with open(p, "r", encoding="utf-8", errors="replace") as f:
                lines = f.readlines()
                snippet = "".join(lines[-tail_lines:]).strip()
        except Exception:
            pass

        return {
            "path": str(p),
            "exists": True,
            "size": size,
            "size_formatted": format_bytes(size),
            "modified": mtime,
            "snippet": snippet,
        }
    except Exception:
        return {
            "path": str(p),
            "exists": False,
            "size": 0,
            "size_formatted": "0 B",
            "modified": None,
            "snippet": "",
        }


def get_live_launchctl_map() -> Dict[str, Dict[str, Any]]:
    """Returns a map of label -> {pid: int|None, status: int, state: str} from launchctl list."""
    mapping = {}
    code, stdout, _ = run_command(["launchctl", "list"])
    if code != 0 or not stdout:
        return mapping

    lines = stdout.splitlines()
    for line in lines[1:]:  # skip header PID Status Label
        parts = line.split("\t")
        if len(parts) >= 3:
            pid_raw, status_raw, label = parts[0].strip(), parts[1].strip(), parts[2].strip()
            pid = int(pid_raw) if pid_raw != "-" and pid_raw.isdigit() else None
            try:
                exit_code = int(status_raw)
            except ValueError:
                exit_code = 0

            mapping[label] = {
                "pid": pid,
                "exit_code": exit_code,
                "loaded": True,
            }
    return mapping


def humanize_cron(expr: str) -> str:
    """Turn 5-part cron expression into human-readable string."""
    parts = expr.strip().split()
    if len(parts) < 5:
        return expr
    m, h, dom, mon, dow = parts[:5]

    days = {"0": "Sun", "1": "Mon", "2": "Tue", "3": "Wed", "4": "Thu", "5": "Fri", "6": "Sat", "7": "Sun"}
    
    if m == "*" and h == "*" and dom == "*" and mon == "*" and dow == "*":
        return "Every minute"
    if m.startswith("*/") and h == "*" and dom == "*" and mon == "*" and dow == "*":
        return f"Every {m[2:]} minutes"
    if m == "0" and h == "*" and dom == "*" and mon == "*" and dow == "*":
        return "Every hour"
    if m == "0" and h != "*" and dom == "*" and mon == "*" and dow == "*":
        return f"Daily at {h.zfill(2)}:00"
    if m != "*" and h != "*" and dom == "*" and mon == "*" and dow == "*":
        return f"Daily at {h.zfill(2)}:{m.zfill(2)}"
    if dow in days and dom == "*" and mon == "*":
        return f"Every {days[dow]} at {h.zfill(2)}:{m.zfill(2)}"

    return expr


def humanize_schedule(plist_data: Dict[str, Any]) -> tuple[str, str]:
    """Returns (human_summary, schedule_type)."""
    cal = plist_data.get("StartCalendarInterval")
    interval = plist_data.get("StartInterval")
    run_at_load = plist_data.get("RunAtLoad", False)
    keep_alive = plist_data.get("KeepAlive", False)
    watch_paths = plist_data.get("WatchPaths")

    if cal is not None:
        if isinstance(cal, dict):
            hour = cal.get("Hour")
            minute = cal.get("Minute", 0)
            weekday = cal.get("Weekday")
            if hour is not None:
                time_str = f"{str(hour).zfill(2)}:{str(minute).zfill(2)}"
                if weekday is not None:
                    day_names = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
                    day_str = day_names[weekday] if 0 <= weekday < 7 else f"Day {weekday}"
                    return f"Every {day_str} at {time_str}", "calendar"
                return f"Daily at {time_str}", "calendar"
            elif minute is not None:
                return f"Every hour at :{str(minute).zfill(2)}", "calendar"
        elif isinstance(cal, list):
            return f"Multiple times daily ({len(cal)} slots)", "calendar"

    if interval is not None:
        try:
            sec = int(interval)
            if sec < 60:
                return f"Every {sec}s", "interval"
            elif sec < 3600:
                return f"Every {sec // 60}m", "interval"
            elif sec < 86400:
                return f"Every {sec // 3600}h", "interval"
            return f"Every {sec // 86400}d", "interval"
        except (ValueError, TypeError):
            return f"Interval: {interval}s", "interval"

    if keep_alive:
        return "Always Running (Daemon)", "daemon"

    if watch_paths:
        return f"Trigger on file change ({len(watch_paths)} paths)", "watcher"

    if run_at_load:
        return "Runs once at Login / Boot", "login"

    return "Manual / On-demand", "manual"


def classify_category(label: str, prog: str) -> str:
    combined = f"{label} {prog}".lower()
    if any(k in combined for k in ("hermes", "ollama", "codex", "opencode", "llama", "model", "paperflow")):
        return "ai"
    if any(k in combined for k in ("bridge", "sync", "rclone", "oakreader", "zotero", "notion-export", "git")):
        return "sync"
    if any(k in combined for k in ("rhythm", "tasknotes", "taskwarrior", "gcal", "notion-pulse", "briefing", "daily")):
        return "lifeos"
    if any(k in combined for k in ("updater", "keystone", "steamclean", "mysql", "maintenance")):
        return "system"
    return "custom"


def get_job_description(label: str, prog: str, schedule_str: str) -> str:
    l_lower = label.lower()
    if "bridge.sync" in l_lower:
        return "Bridge Daily Unattended Sync: Pulls Wiki updates (--ff-only), auto-commits & pushes tracked repos, and mirrors 4 local workspaces to Google Drive."
    if "model-control" in l_lower:
        return "Model Control & Feature Registry Sync: Probes OpenCode free router models, enforces HyperResearch lock, auto-routes pqa-kb ($0.00), and auto-indexes PDF drops in ~/knowledge-base."
    if "learn.notion-export" in l_lower:
        return "Notion to Local Markdown Export: Exports Notion Raw Knowledge and database pages to local ~/learn workspace."
    if "zotero-oakreader" in l_lower:
        return "Zotero OakReader Sync: Synchronizes scientific papers, annotations, and reading metadata."
    if "notion-pulse" in l_lower:
        return "Notion Pulse: Syncs periodic health and life logs with Notion."
    if "hermes" in l_lower:
        return "Hermes Gateway: Local AI gateway proxy service."
    if "ollama" in l_lower:
        return "Ollama Local LLM Runner: Manages background local language model engine."
    if "codex-router" in l_lower:
        return "Codex Router: High-performance routing daemon for Codex agent sessions."
    if "engineering-maintenance" in l_lower:
        return "Engineering System Maintenance: Regular workspace cleanup, git maintenance, and environment verification."
    if "daily-briefing" in l_lower:
        return "Daily Briefing Generator: Compiles daily tasks, events, and focus items."
    if "paperflow" in l_lower:
        return "Paperflow GUI: Academic paper writing and workflow pipeline interface."
    if "tasknotes" in l_lower or "taskwarrior" in l_lower:
        return "Task Synchronization: Syncs tasks and time-tracking between Tasknotes, Taskwarrior, and Google Calendar."
    if "daily-news" in l_lower or "scientific-news" in l_lower:
        return "News Scraping Job: Gathers daily scientific and technical news feeds."
    return f"Automated background task running {Path(prog).name if prog else 'script'}."


def scan_launch_agents() -> List[Dict[str, Any]]:
    agents_dir = Path.home() / "Library/LaunchAgents"
    live_map = get_live_launchctl_map()
    items = []

    if not agents_dir.exists():
        return items

    for plist_path in sorted(agents_dir.glob("*.plist")):
        try:
            with open(plist_path, "rb") as fp:
                data = plistlib.load(fp)
        except Exception as exc:
            # Record malformed plist with error notice
            items.append({
                "id": plist_path.stem,
                "label": plist_path.stem,
                "category": "system",
                "type": "LaunchAgent",
                "status": "Malformed",
                "status_code": "malformed",
                "schedule": "Unknown",
                "schedule_type": "unknown",
                "program": "",
                "arguments": [],
                "working_dir": None,
                "plist_path": str(plist_path),
                "stdout_log": None,
                "stderr_log": None,
                "last_exit_code": None,
                "pid": None,
                "is_active": False,
                "description": f"Malformed or invalid plist file: {exc}",
                "error": str(exc),
            })
            continue

        label = data.get("Label", plist_path.stem)
        prog_args = data.get("ProgramArguments", [])
        prog = data.get("Program") or (prog_args[0] if prog_args else "")
        working_dir = data.get("WorkingDirectory")
        stdout_path = data.get("StandardOutPath")
        stderr_path = data.get("StandardErrorPath")

        schedule_str, sched_type = humanize_schedule(data)
        category = classify_category(label, prog)
        description = get_job_description(label, prog, schedule_str)

        live_info = live_map.get(label, {})
        is_loaded = live_info.get("loaded", False)
        pid = live_info.get("pid")
        exit_code = live_info.get("exit_code")

        if pid:
            status = "Running"
            status_code = "running"
        elif is_loaded:
            if exit_code == 0:
                status = "Loaded (Idle)"
                status_code = "idle"
            elif exit_code == -9:
                status = "Stopped (SIGKILL)"
                status_code = "stopped"
            else:
                status = f"Failed (Exit {exit_code})"
                status_code = "error"
        else:
            status = "Unloaded"
            status_code = "unloaded"

        items.append({
            "id": label,
            "label": label,
            "name": label.replace("com.tai.", "").replace("com.", "").replace(".", " ").title(),
            "category": category,
            "type": "LaunchAgent",
            "status": status,
            "status_code": status_code,
            "schedule": schedule_str,
            "schedule_type": sched_type,
            "program": prog,
            "arguments": prog_args,
            "working_dir": working_dir,
            "plist_path": str(plist_path),
            "stdout_log": inspect_file(stdout_path),
            "stderr_log": inspect_file(stderr_path),
            "last_exit_code": exit_code,
            "pid": pid,
            "is_active": (status_code in ("running", "idle")),
            "description": description,
            "keep_alive": bool(data.get("KeepAlive")),
            "run_at_load": bool(data.get("RunAtLoad")),
        })

    return items


def scan_crontab() -> List[Dict[str, Any]]:
    items = []
    code, stdout, _ = run_command(["crontab", "-l"])
    if code != 0 or not stdout:
        return items

    lines = stdout.splitlines()
    for idx, line in enumerate(lines):
        raw = line.strip()
        if not raw or raw.startswith("#"):
            continue

        parts = raw.split(maxsplit=5)
        if len(parts) >= 6:
            cron_expr = " ".join(parts[:5])
            command = parts[5]
            human_sched = humanize_cron(cron_expr)
            job_id = f"cron-job-{idx + 1}"
            category = classify_category(job_id, command)

            items.append({
                "id": job_id,
                "label": f"Cron Job #{idx + 1}",
                "name": f"Cron: {Path(command.split()[0]).name if command.split() else 'Task'}",
                "category": category,
                "type": "Crontab",
                "status": "Active (Cron)",
                "status_code": "idle",
                "schedule": human_sched,
                "schedule_type": "cron",
                "program": command,
                "arguments": command.split(),
                "working_dir": str(Path.home()),
                "plist_path": None,
                "stdout_log": None,
                "stderr_log": None,
                "last_exit_code": 0,
                "pid": None,
                "is_active": True,
                "description": f"Scheduled cron execution: {command}",
                "keep_alive": False,
                "run_at_load": False,
            })
    return items


def scan_bridge_profile_details() -> Optional[Dict[str, Any]]:
    """Gathers rich metadata from local Bridge configuration files."""
    gh_track = WORKSPACE_ROOT / "assets/bridge/config/github-track.yaml"
    dr_track = WORKSPACE_ROOT / "assets/bridge/config/drive-track.yaml"
    stdout_log = WORKSPACE_ROOT / "assets/bridge/logs/launchd.stdout.log"
    stderr_log = WORKSPACE_ROOT / "assets/bridge/logs/launchd.stderr.log"

    if not gh_track.exists():
        return None

    try:
        import yaml
        with open(gh_track, "r", encoding="utf-8") as f:
            gh_data = yaml.safe_load(f) or {}
        with open(dr_track, "r", encoding="utf-8") as f:
            dr_data = yaml.safe_load(f) or {}

        workspaces = gh_data.get("workspaces", [])
        profiles = dr_data.get("profiles", [])

        last_run = None
        if stdout_log.exists():
            with open(stdout_log, "r", encoding="utf-8", errors="replace") as f:
                for line in f:
                    m = re.search(r"\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\] Starting Bridge Daily", line)
                    if m:
                        last_run = m.group(1)

        return {
            "tracked_github_repos": [w.get("id") for w in workspaces if w.get("tracked")],
            "pull_enabled_repos": [w.get("id") for w in workspaces if w.get("pull_enabled")],
            "untracked_repos": [w.get("id") for w in workspaces if not w.get("tracked") and not w.get("pull_enabled")],
            "drive_profiles": [p.get("id") for p in profiles if p.get("enabled", True)],
            "last_scheduled_run": last_run,
        }
    except Exception:
        return None


def scan_model_control_details() -> Optional[Dict[str, Any]]:
    spec_path = WORKSPACE_ROOT / "assets/model-control/model-control-spec.json"
    if not spec_path.exists():
        return None
    try:
        with open(spec_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        features = data.get("local_features", {})

        pqa = features.get("pqa-kb", {})
        hyper = features.get("hyperresearch", {})
        codex = features.get("codex_workbench", {})
        hermes = features.get("hermes_agent", {})

        return {
            "version": data.get("version"),
            "updated_at": data.get("updated_at"),
            "hyperresearch": {
                "name": hyper.get("name", "HyperResearch"),
                "policy": hyper.get("model_policy", "LOCKED"),
                "assigned_model": hyper.get("assigned_model"),
                "provider": hyper.get("provider"),
            },
            "pqa_kb": {
                "name": pqa.get("name", "PaperQA KB"),
                "policy": pqa.get("model_policy", "DYNAMIC_FREE_REASONING"),
                "assigned_model": pqa.get("assigned_model"),
                "target_cost": pqa.get("target_cost", "$0.00"),
                "status": pqa.get("last_health_check", {}).get("status", "HEALTHY"),
                "candidates_count": len(pqa.get("candidate_ranking", [])),
            },
            "features_count": len(features),
        }
    except Exception:
        return None


def run_full_scan() -> Dict[str, Any]:
    launch_agents = scan_launch_agents()
    cron_jobs = scan_crontab()
    bridge_extra = scan_bridge_profile_details()
    model_control_extra = scan_model_control_details()

    all_automations = launch_agents + cron_jobs

    # Enrich Bridge & Model Control entries if found
    for a in all_automations:
        if a["id"] == "com.tai.bridge.sync" and bridge_extra:
            a["bridge_details"] = bridge_extra
        if "model-control" in a["id"] and model_control_extra:
            a["model_control_details"] = model_control_extra

    # Compute high-level statistics
    total = len(all_automations)
    running = sum(1 for a in all_automations if a["status_code"] == "running")
    idle = sum(1 for a in all_automations if a["status_code"] == "idle")
    errors = sum(1 for a in all_automations if a["status_code"] in ("error", "malformed"))
    scheduled = sum(1 for a in all_automations if a["schedule_type"] in ("calendar", "interval", "cron"))

    categories = {
        "sync": sum(1 for a in all_automations if a["category"] == "sync"),
        "lifeos": sum(1 for a in all_automations if a["category"] == "lifeos"),
        "ai": sum(1 for a in all_automations if a["category"] == "ai"),
        "system": sum(1 for a in all_automations if a["category"] == "system"),
        "custom": sum(1 for a in all_automations if a["category"] == "custom"),
    }

    result = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "stats": {
            "total": total,
            "running": running,
            "idle": idle,
            "active": running + idle,
            "errors": errors,
            "scheduled": scheduled,
        },
        "category_counts": categories,
        "automations": all_automations,
    }

    return result


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


def print_cli_table(data: Dict[str, Any], stdout=sys.stdout) -> None:
    stats = data.get("stats", {})
    autos = data.get("automations", [])

    stdout.write(f"\n{Colors.BOLD}=== macOS Automation Status Overview ==={Colors.RESET}\n")
    stdout.write(
        f"Total: {stats.get('total', 0)} | "
        f"Active: {Colors.GREEN}{stats.get('active', 0)}{Colors.RESET} "
        f"(Running: {stats.get('running', 0)}, Idle: {stats.get('idle', 0)}) | "
        f"Scheduled: {stats.get('scheduled', 0)} | "
        f"Errors: {Colors.RED}{stats.get('errors', 0)}{Colors.RESET}\n\n"
    )

    stdout.write(f"{Colors.BOLD}{Colors.BLUE}Automations & Background Daemons ({len(autos)} registered):{Colors.RESET}\n")
    stdout.write(f"{'ID':<32} {'CATEGORY':<10} {'STATUS':<16} {'SCHEDULE':<22} {'EXIT':<10} {'DESCRIPTION / WORKFLOW'}\n")
    stdout.write("-" * 118 + "\n")

    for a in autos:
        aid = a.get("id", "")
        if len(aid) > 30:
            aid = aid[:29] + "…"
        cat = a.get("category", "")
        st_code = a.get("status_code", "")

        if st_code == "running":
            status_str = f"{Colors.GREEN}Running (PID){Colors.RESET}"
        elif st_code == "idle":
            status_str = f"{Colors.BLUE}Loaded (Idle){Colors.RESET}"
        elif st_code in ("error", "malformed"):
            status_str = f"{Colors.RED}Failed/Error{Colors.RESET}"
        else:
            status_str = f"{Colors.DIM}{a.get('status', 'Unloaded')}{Colors.RESET}"

        sched = a.get("schedule", "-")
        if len(sched) > 20:
            sched = sched[:19] + "…"

        exit_code = a.get("last_exit_code")
        if a.get("pid"):
            exit_str = f"PID:{a.get('pid')}"
        elif exit_code == 0:
            exit_str = f"{Colors.GREEN}0 (OK){Colors.RESET}"
        elif exit_code is not None:
            exit_str = f"{Colors.RED}{exit_code}{Colors.RESET}"
        else:
            exit_str = "-"

        desc = a.get("description", "")
        if len(desc) > 38:
            desc = desc[:37] + "…"

        stdout.write(f"{aid:<32} {cat:<10} {status_str:<25} {sched:<22} {exit_str:<19} {desc}\n")

    stdout.write("\n")


def main():
    parser = argparse.ArgumentParser(description="Scan macOS automations and generate track-automation registry.")
    parser.add_argument("command", nargs="?", default="status", choices=["status", "scan", "list"], help="CLI command (default: status table)")
    parser.add_argument("--json", action="store_true", help="Print scanned JSON data to stdout")
    parser.add_argument("--open", action="store_true", help="Open visual dashboard in default browser after scan")
    parser.add_argument("--output", "-o", help="Custom output JSON path", default=str(OUTPUT_JSON_PATH))
    args = parser.parse_args()

    data = run_full_scan()

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    # Also emit automations_data.js for zero-friction file:// offline browser opening
    js_path = out_path.parent / "automations_data.js"
    with open(js_path, "w", encoding="utf-8") as f:
        f.write(f"window.EMBEDDED_DATA = {json.dumps(data, indent=2, ensure_ascii=False)};\n")

    if args.json:
        print(json.dumps(data, indent=2, ensure_ascii=False))
    elif args.command in ("status", "list"):
        print_cli_table(data)
    else:
        print(f"Scanned {data['stats']['total']} automations ({data['stats']['active']} active, {data['stats']['errors']} errors).")
        print(f"Saved registry to: {out_path}")

    if args.open:
        index_html = Path(__file__).resolve().parent / "index.html"
        if index_html.exists():
            subprocess.run(["open", str(index_html)])


if __name__ == "__main__":
    main()
