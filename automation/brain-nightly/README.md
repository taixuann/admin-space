# Brain nightly

Nightly lint, curate and morning summary for the brain vault

| Field | Value |
| --- | --- |
| Label | `com.tai.brain.nightly` |
| Source owner | Space-owned (Admin `automation/<job-name>`), repository /Users/tai/.agents |
| Branch | `automation/brain-nightly` |
| Source folder | `/Users/tai/.agents/automation/brain-nightly` |
| Report root | `/Users/tai/.agents/automation/brain-nightly-runtime/logs` |
| Installed plist | `~/Library/LaunchAgents/com.tai.brain.nightly.plist` |

## Schedule and time

Scheduled at minute 0, hour 2 local time. The installed plist is the only authority for the trigger; this file describes it.

Wall-clock times use the Mac's local timezone at fire time (+07 when scaffolded). A timezone change moves the next run. `StartCalendarInterval` fires late after sleep; a time that passes while the Mac is asleep runs only if launchd replays it. `StartInterval` counts from the last start and does not count sleep. Record the real start time in the run report rather than assuming the nominal one.

## Runtime

The job calls `/bin/bash` with absolute arguments. `PATH`, `HOME`, and `LANG` come from the plist `EnvironmentVariables`. The job loads no `.env`, no shell profile, and no version-manager init.

A thin wrapper runs at `scripts/run.sh`. It holds the job lock and writes one terminal event per run. It loads no other file.

## Reports and retention

Reports go to `/Users/tai/.agents/automation/brain-nightly-runtime/logs`:

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
1. `launchctl bootout gui/$(id -u)/com.tai.brain.nightly`
2. Copy the saved plist over `~/Library/LaunchAgents/com.tai.brain.nightly.plist`.
3. `launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.tai.brain.nightly.plist`
4. Confirm a fresh terminal outcome in `latest-result.json`.

## Known limit

A runner cannot report its own absence. A run that never starts leaves no local trace. Detect missed runs with a separate observer that reads the age of `latest-result.json`; do not claim the job is healthy from schedule alone.

## Commands

```bash
# Static check. Never starts the job.
python3 ~/.agents/skills/launchd-automation/scripts/verify_automation.py "/Users/tai/.agents/automation/brain-nightly" --static --report-root "/Users/tai/.agents/automation/brain-nightly-runtime/logs"

# Manual run, when authorized.
/bin/bash /Users/tai/admin-space/brain/scripts/night-opencode.sh --report-root "/Users/tai/.agents/automation/brain-nightly-runtime/logs"
```
