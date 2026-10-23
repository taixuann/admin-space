# Automation

Automation source follows its owner. Choose the owner from the job's primary
responsibility and its independent lifecycle, not from the helpers it calls.

## Classify the owner

| The job… | Owner | Source location | Branch |
| --- | --- | --- | --- |
| serves one tool | that tool | `<tool>/automation/<job-name>/` | `admin/<tool-name>_<request-id>` |
| coordinates several independently owned tools, or applies Space policy | Admin | `~/.agents/automation/<job-name>/` | `automation/<job-name>` |

A job that calls a shared incident reporter is still tool-owned. A shared
dependency does not move source.

Branch naming rules live in [Admin tool handoff](tools.md).

## Where runtime evidence goes

Both kinds write reports to:

`/Users/tai/.agents/automation/<stable-job-name>/logs/`

`<stable-job-name>` is the runtime name, not always the source folder name. A
Space-owned job uses `<source-folder>-runtime` so the report root sits outside
its source. A tool-owned job may use the job name, because its source lives in
the tool repository. Never point a report root inside the source folder.

That path is ignored by Admin Git (`/automation/*-runtime/` and the per-job
entries). A short README there may point at the owning runbook. It is not a
second runbook, and it does not restate the plist or the schedule.

| Artifact | Location |
| --- | --- |
| Runner, plist source, runbook, `AGENTS.md`, process diagram | The owning source folder |
| Run reports, rotated logs, latest result | The centralized report root |
| Durable pending incident events | The incident tool's private runtime store |
| Installed plist | `~/Library/LaunchAgents/<label>.plist` |

Pass the report root to the scheduled entrypoint as an explicit absolute path.
A worktree test uses a temporary report root, temporary state, and fake
configuration. It never writes to the live report root, the live OpenCode
configuration, the credential store, or the incident queue.

## Rules for every job

- The installed job calls the stable canonical checkout, never a development
  worktree.
- The label comes from the plist contents, not from the filename.
- Use an absolute executable path. A wrapper earns its place only when it does
  work the job cannot do directly.
- Do not load a shell profile, a version manager, or a `.env` file implicitly.
  Declare the environment the job needs.
- One writer per run record. Update the latest result atomically.
- Keep the previous valid state when an update fails.
- A successful dispatch is not a completed run. Check the terminal outcome and
  the intended effect.
- A runner cannot report its own absence. Missing-run detection needs a separate
  observer; state that limit in the runbook.

Lifecycle rules — scaffolding, deployment, verification, exit codes, recovery —
belong to the `launchd-automation` skill. Read it before creating or changing a
job. This page decides ownership and placement; that skill decides execution.

## Current jobs

| Label | Source owner | Schedule | Notes |
| --- | --- | --- | --- |
| `com.tai.model-control-sync` | Admin (`automation/model-control/`) | Daily 00:00 | Active. Its runner calls model sync plus an unrelated indexing helper. A replacement job is implemented but not installed. |
| `com.tai.linear-notion-sync` | Development Space (`automation/linear-notion-tracking/`) | Daily 00:00 | Path repaired after the workshop rename. No tracked source plist. |
| `com.tai.bridge.sync` | Admin (`automation/bridge/`) | Per its installed plist | Unchanged by the 2026-10-23 upgrade. |

An installed schedule is state, not intent. Compare it with the source plist
before claiming what runs.
