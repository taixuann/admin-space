# Agent contract: Update Plugins MCP Skills

Read `README.md` first. It owns the schedule, outcomes, and recovery.

## Ownership

- Source repository: `/Users/tai/.agents`. Layout: Space-owned (Admin `automation/<job-name>`).
- Branch convention: `automation/update_plugins-mcp-skills`.
- Source folder: `/Users/tai/.agents/automation/update_plugins-mcp-skills`. It owns `launchd.plist`, the runbook, and any runner.
- Report root: `/Users/tai/.agents/automation/update_plugins-mcp-skills/logs`. Space-contained layout; keep it git-ignored.

## Boundaries

- Edit the source plist here. `~/Library/LaunchAgents/com.tai.update-plugins-mcp-skills.plist` is a build output.
- Activate, restart, enable, disable, or remove the job only with explicit authorization for this label.
- Commit, push, merge, or publish only with explicit authorization.
- Change the schedule, environment, or command in the source plist and the README together.

## Checks before reporting work complete

1. `plutil -lint launchd.plist` returns OK.
2. `verify_automation.py "/Users/tai/.agents/automation/update_plugins-mcp-skills" --static --report-root "/Users/tai/.agents/automation/update_plugins-mcp-skills/logs"` exits 0.
3. A live check, only when authorized, shows a fresh terminal outcome in `/Users/tai/.agents/automation/update_plugins-mcp-skills/logs/latest-result.json`.

State which checks ran, which were skipped, and why.
