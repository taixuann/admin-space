# Update Plugins MCP Skills

Daily 03:00 maintenance for global plugins (superpowers, caveman), skills across Claude, Codex, Gemini, and OpenCode, and pruning of merged local branches in `~/.agents`

## Phases

1. Superpowers plugin update. 2. Caveman hooks. 3. Global skills update. 4. Skill mirror sync.
5. Merged-branch prune: deletes local branches of `~/.agents` already merged into `master` with `git branch -d`. It never merges, never touches remotes, and never deletes `master`/`main`, the checked-out branch, or any branch checked out in a worktree (those are reported as skipped). Squash-merged branches are also deleted: a branch not listed by `git branch --merged` is removed when merging it into `master` leaves the tree unchanged (`git merge-tree --write-tree`, tree equal to `master^{tree}`). Those use `git branch -D`, since `-d` refuses them; the tree check is the proof. Rebased branches, branches whose files `master` changed later, and branches with conflicts or unmerged work are kept (git < 2.38 keeps every unmerged branch). Recovery for a deleted branch: `git reflog`, then `git branch <name> <sha>`.

| Field | Value |
| --- | --- |
| Label | `com.tai.update-plugins-mcp-skills` |
| Source owner | Harvey-owned (`bots/bot-management/harvey/cron/<job-name>`), repository /Users/tai/.agents |
| Branch | `automation/update_plugins-mcp-skills` |
| Source folder | `/Users/tai/.agents/bots/bot-management/harvey/cron/update_plugins-mcp-skills` |
| Report root | `/Users/tai/.agents/bots/bot-management/harvey/cron/update_plugins-mcp-skills/logs` (Space-contained layout) |
| Installed plist | `~/Library/LaunchAgents/com.tai.update-plugins-mcp-skills.plist` |

## Schedule and time

Scheduled at minute 0, hour 3 local time. The installed plist is the only authority for the trigger; this file describes it.

Wall-clock times use the Mac's local timezone at fire time (+07 when scaffolded). A timezone change moves the next run. `StartCalendarInterval` fires late after sleep; a time that passes while the Mac is asleep runs only if launchd replays it. `StartInterval` counts from the last start and does not count sleep. Record the real start time in the run report rather than assuming the nominal one.

## Runtime

The job calls `/opt/miniconda3/envs/core/bin/python3` with absolute arguments. `PATH`, `HOME`, and `LANG` come from the plist `EnvironmentVariables`. The job loads no `.env`, no shell profile, and no version-manager init.

The plist calls the program directly. It has no wrapper.

## Reports and retention

Reports go to `/Users/tai/.agents/bots/bot-management/harvey/cron/update_plugins-mcp-skills/logs` (Space-contained layout):

| File | Purpose |
| --- | --- |
| `stdout.log` | Process output and one-line run events |
| `stderr.log` | Diagnostics and tracebacks |
| `latest-result.json` | Last terminal outcome, written atomically |
| `runs/` | One record per run, named by `run_id` |

A run record holds `run_id`, label, source revision and dirty state, start and end time, outcome, exit code, and duration. Keep 30 days and at most 100 completed runs. Rotation never removes `latest-result.json`.

## Outcomes

| Outcome | Meaning |
| --- | --- |
| `success` | The job reached its intended effect. |
| `cached` | No change was needed. This is a successful run. |
| `skipped_locked` | Another run held the lock. Record the skip, exit 0, leave the active run's record alone. |
| `failed` | The tool failed. Keep the previous valid state and exit nonzero. |

Delivery failure: a local report stays valid when external delivery fails. Pending deliveries stay in the tool's own queue, are reconciled before retry, and retry within a bounded limit.

## Replay and recovery

Replay a failed run by calling the same entrypoint with the old parameters and a new `run_id`. A replay is a new run; it does not rewrite history.

Recovery keeps the last valid configuration:
1. `launchctl bootout gui/$(id -u)/com.tai.update-plugins-mcp-skills`
2. Copy the saved plist over `~/Library/LaunchAgents/com.tai.update-plugins-mcp-skills.plist`.
3. `launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.tai.update-plugins-mcp-skills.plist`
4. Confirm a fresh terminal outcome in `latest-result.json`.

## Known limit

A runner cannot report its own absence. A run that never starts leaves no local trace. Detect missed runs with a separate observer that reads the age of `latest-result.json`; do not claim the job is healthy from schedule alone.

## Commands

```bash
# Static check. Never starts the job.
python3 ~/.agents/skills/launchd-automation/scripts/verify_automation.py "/Users/tai/.agents/bots/bot-management/harvey/cron/update_plugins-mcp-skills" --static --report-root "/Users/tai/.agents/bots/bot-management/harvey/cron/update_plugins-mcp-skills/logs"

# Manual run, when authorized.
/opt/miniconda3/envs/core/bin/python3 /Users/tai/.agents/bots/bot-management/harvey/cron/update_plugins-mcp-skills/backend/main.py --report-root /Users/tai/.agents/bots/bot-management/harvey/cron/update_plugins-mcp-skills/logs
```
