# Automation

Scheduled jobs. A job lives with the owner of its main responsibility.

| The job | Owner | Source |
| --- | --- | --- |
| Serves one tool | Development Space (the tool's repo) | `<tool>/automation/<job-name>/` |
| Coordinates several tools or applies Admin policy | Admin | `~/.agents/automation/<job-name>/` |

Calling a shared helper (such as the incident reporter) does not change the owner.

## Where things go

| Artifact | Location |
| --- | --- |
| Runner, plist source, runbook, `AGENTS.md`, diagram | The owning source folder |
| Run reports, rotated logs, latest result | `~/.agents/automation/<stable-job-name>/logs/` (ignored by Git) |
| Durable incident events | The incident tool's private store |
| Installed plist | `~/Library/LaunchAgents/<label>.plist` |

An Admin job's report folder is `<source-folder>-runtime`, so reports never land inside source.

## Current jobs

| Label | Owner | Schedule | Notes |
| --- | --- | --- | --- |
| `com.tai.model-control-sync` | Admin (`model-control/`) | Daily 00:00 | Active. A replacement job is implemented but not installed. |
| `com.tai.linear-notion-sync` | Development Space (`automation/linear-notion-tracking/`) | Daily 00:00 | No tracked source plist. |
| `com.tai.bridge.sync` | Admin (`bridge/`) | Per installed plist | |

An installed schedule is state, not intent. Compare it with the source plist before saying what runs. Rules for changing jobs are in [AGENTS.md](AGENTS.md).
