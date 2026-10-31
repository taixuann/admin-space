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
| Run reports, rotated logs, latest result | `~/.agents/automation/<stable-job-name>/logs/` or `<job>-runtime/logs/` (ignored by Git) |
| Durable incident events | The incident tool's private store |
| Installed plist | `~/Library/LaunchAgents/<label>.plist` |

An Admin job's report folder is `<source-folder>-runtime`, so reports never land inside source.

## Current jobs

| Label | Owner | Schedule | Notes |
| --- | --- | --- | --- |
| `com.tai.brain.nightly` | Admin (`brain-nightly/`) | 02:00 local (see source plist) | Brain vault lint, curate, morning summary |

An installed schedule is state, not intent. Compare it with the source plist before saying what runs. Rules for changing jobs are in [AGENTS.md](AGENTS.md).
