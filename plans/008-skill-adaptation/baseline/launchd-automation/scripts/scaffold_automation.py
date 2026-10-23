#!/usr/bin/env python3
"""
Scaffolds a standardized macOS launchd automation folder structure with templates.
Usage:
    python3 scaffold_automation.py \
        --target-dir /path/to/my-space/automation/job-name \
        --label com.tai.myspace.jobname \
        --title "My Space Daily Sync" \
        --description "Synchronizes local records with remote storage" \
        --schedule "0 4 * * *" \
        --command "python3 scripts/sync.py"
"""

import argparse
import os
import re
import sys
from datetime import datetime
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = SKILL_DIR / "templates"

def parse_schedule_to_plist_block(schedule_str: str) -> tuple[str, str]:
    """
    Parses a schedule string (e.g. '0 4 * * *', 'interval:3600', 'daily:04:00')
    into a launchd XML block and human-readable text.
    """
    schedule_str = schedule_str.strip()
    
    # Format: interval:SECS or every X seconds/minutes
    interval_match = re.match(r"(?:interval:|every\s+)?(\d+)\s*(s|m|h)?", schedule_str, re.IGNORECASE)
    if "interval:" in schedule_str or (interval_match and interval_match.group(2)):
        val = int(interval_match.group(1))
        unit = (interval_match.group(2) or "s").lower()
        multiplier = {"s": 1, "m": 60, "h": 3600}.get(unit, 1)
        seconds = val * multiplier
        xml = f"""    <key>StartInterval</key>
    <integer>{seconds}</integer>"""
        return xml, f"Every {seconds} seconds ({val}{unit})"

    # Format: daily:HH:MM or cron minute hour * * *
    parts = schedule_str.split()
    if len(parts) == 5:
        minute, hour, dom, month, dow = parts
        xml_lines = [
            "    <key>StartCalendarInterval</key>",
            "    <dict>"
        ]
        readable = []
        if minute != "*":
            xml_lines.append(f"        <key>Minute</key>\n        <integer>{int(minute)}</integer>")
            readable.append(f"minute {minute}")
        if hour != "*":
            xml_lines.append(f"        <key>Hour</key>\n        <integer>{int(hour)}</integer>")
            readable.append(f"hour {hour}:00")
        if dom != "*":
            xml_lines.append(f"        <key>Day</key>\n        <integer>{int(dom)}</integer>")
            readable.append(f"day of month {dom}")
        if month != "*":
            xml_lines.append(f"        <key>Month</key>\n        <integer>{int(month)}</integer>")
            readable.append(f"month {month}")
        if dow != "*":
            xml_lines.append(f"        <key>Weekday</key>\n        <integer>{int(dow)}</integer>")
            readable.append(f"day of week {dow}")
        xml_lines.append("    </dict>")
        return "\n".join(xml_lines), "Scheduled at " + ", ".join(readable)

    # Fallback default: daily at 04:00
    return """    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>4</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>""", "Daily at 04:00 AM (default)"

def main():
    parser = argparse.ArgumentParser(description="Scaffold launchd automation structure")
    parser.add_argument("--target-dir", required=True, help="Directory to scaffold the automation into")
    parser.add_argument("--label", required=True, help="Unique reverse-DNS label (e.g. com.tai.bridge.sync)")
    parser.add_argument("--title", default="", help="Human title for service")
    parser.add_argument("--description", default="", help="Summary of purpose")
    parser.add_argument("--schedule", default="0 4 * * *", help="Schedule cron format (e.g. '0 4 * * *') or 'interval:3600'")
    parser.add_argument("--command", default="echo 'Hello from automation'", help="Main command to execute inside runner")
    parser.add_argument("--run-at-load", action="store_true", help="Whether to run immediately upon load")
    parser.add_argument("--deploy", action="store_true", help="Copy plist to ~/Library/LaunchAgents and bootstrap")

    args = parser.parse_args()

    target_dir = Path(args.target_dir).resolve()
    target_dir.mkdir(parents=True, exist_ok=True)
    scripts_dir = target_dir / "scripts"
    logs_dir = target_dir / "logs"
    scripts_dir.mkdir(parents=True, exist_ok=True)
    logs_dir.mkdir(parents=True, exist_ok=True)

    # Ensure .gitignore in logs directory
    gitignore_file = logs_dir / ".gitignore"
    if not gitignore_file.exists():
        gitignore_file.write_text("*\n!.gitignore\n")

    label = args.label.strip()
    title = args.title or label
    description = args.description or f"Automated background service for {label}"
    schedule_xml, schedule_readable = parse_schedule_to_plist_block(args.schedule)
    
    home_dir = str(Path.home())
    runner_path = str(scripts_dir / "run.sh")
    stdout_log = str(logs_dir / "stdout.log")
    stderr_log = str(logs_dir / "stderr.log")
    plist_path = target_dir / f"{label}.plist"
    path_value = f"/opt/homebrew/bin:/opt/homebrew/sbin:/usr/local/bin:/usr/local/sbin:{home_dir}/.local/bin:{home_dir}/.cargo/bin:/usr/bin:/bin:/usr/sbin:/sbin"

    # 1. Render plist
    plist_tpl = (TEMPLATES_DIR / "plist.template.xml").read_text()
    rendered_plist = plist_tpl.replace("{{LABEL}}", label) \
                              .replace("{{RUNNER_PATH}}", runner_path) \
                              .replace("{{WORKING_DIR}}", str(target_dir)) \
                              .replace("{{PATH_VALUE}}", path_value) \
                              .replace("{{HOME_DIR}}", home_dir) \
                              .replace("{{STDOUT_LOG}}", stdout_log) \
                              .replace("{{STDERR_LOG}}", stderr_log) \
                              .replace("{{RUN_AT_LOAD}}", "true" if args.run_at_load else "false") \
                              .replace("{{SCHEDULE_BLOCK}}", schedule_xml)
    plist_path.write_text(rendered_plist)
    print(f" Generated plist: {plist_path}")

    # 2. Render runner.sh
    runner_tpl = (TEMPLATES_DIR / "runner.sh.template").read_text()
    rendered_runner = runner_tpl.replace("{{LOCK_NAME}}", label) \
                                .replace("{{JOB_NAME}}", label) \
                                .replace("{{MAIN_EXECUTION_COMMAND}}", args.command)
    runner_file = scripts_dir / "run.sh"
    runner_file.write_text(rendered_runner)
    runner_file.chmod(0o755)
    print(f" Generated runner script: {runner_file} (chmod +x)")

    # 3. Render README.md
    readme_tpl = (TEMPLATES_DIR / "README.template.md").read_text()
    rendered_readme = readme_tpl.replace("{{SERVICE_TITLE}}", title) \
                                .replace("{{SERVICE_DESCRIPTION}}", description) \
                                .replace("{{LABEL}}", label) \
                                .replace("{{SCHEDULE_HUMAN_READABLE}}", schedule_readable) \
                                .replace("{{WORKING_DIR}}", str(target_dir)) \
                                .replace("{{RUNNER_RELATIVE_PATH}}", "scripts/run.sh") \
                                .replace("{{DIR_NAME}}", target_dir.name) \
                                .replace("{{MAIN_TASK_FILE}}", "run.sh")
    (target_dir / "README.md").write_text(rendered_readme)
    print(f" Generated runbook: {target_dir / 'README.md'}")

    # 4. Render AGENTS.md
    agents_tpl = (TEMPLATES_DIR / "AGENTS.template.md").read_text()
    rendered_agents = agents_tpl.replace("{{SERVICE_TITLE}}", title) \
                                .replace("{{LABEL}}", label) \
                                .replace("{{WORKING_DIR}}", str(target_dir)) \
                                .replace("{{DIR_NAME}}", target_dir.name) \
                                .replace("{{MAIN_TASK_FILE}}", "run.sh")
    (target_dir / "AGENTS.md").write_text(rendered_agents)
    print(f" Generated agent contract: {target_dir / 'AGENTS.md'}")

    # 5. Render metadata.json for track-automation
    metadata_tpl = (TEMPLATES_DIR / "track_metadata.template.json").read_text()
    rendered_meta = metadata_tpl.replace("{{SERVICE_ID}}", label.replace(".", "-")) \
                                .replace("{{LABEL}}", label) \
                                .replace("{{SERVICE_NAME}}", title) \
                                .replace("{{SERVICE_DESCRIPTION}}", description) \
                                .replace("{{SPACE_NAME}}", target_dir.parent.name) \
                                .replace("{{WORKING_DIR}}", str(target_dir)) \
                                .replace("{{RUNNER_PATH}}", runner_path) \
                                .replace("{{SCHEDULE_TYPE}}", "calendar" if "StartCalendarInterval" in schedule_xml else "interval") \
                                .replace("{{CRON_EXPRESSION}}", args.schedule) \
                                .replace("{{SCHEDULE_HUMAN_READABLE}}", schedule_readable) \
                                .replace("{{STDOUT_LOG}}", stdout_log) \
                                .replace("{{STDERR_LOG}}", stderr_log) \
                                .replace("{{CREATED_AT}}", datetime.utcnow().isoformat() + "Z")
    (target_dir / "metadata.json").write_text(rendered_meta)
    print(f" Generated tracking metadata: {target_dir / 'metadata.json'}")

    # 6. Optional deploy to LaunchAgents
    if args.deploy:
        user_launch_agents = Path.home() / "Library" / "LaunchAgents"
        user_launch_agents.mkdir(parents=True, exist_ok=True)
        dest_plist = user_launch_agents / f"{label}.plist"
        
        # Unload if existing
        os.system(f"launchctl bootout gui/$(id -u)/{label} 2>/dev/null || true")
        dest_plist.write_text(rendered_plist)
        os.system(f"launchctl bootstrap gui/$(id -u) '{dest_plist}'")
        print(f" Deployed and bootstrapped to launchd: {dest_plist}")

    print("\n Scaffolding complete! Run verify script to validate.")

if __name__ == "__main__":
    main()
