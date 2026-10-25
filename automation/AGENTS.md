# Automation instructions

Scope: `automation/`. Read [README.md](README.md) for ownership and placement. Read the `launchd-automation` skill before creating or changing a job; it owns scaffolding, deployment, verification, exit codes, and recovery.

## Rules for every job

- Point the installed job at the stable checkout, never a worktree.
- Read the label from the plist contents, not the filename.
- Use absolute executable paths. Declare the environment the job needs; load no shell profile, version manager, or `.env` implicitly.
- Pass the report root as an explicit absolute path. Test runs use temporary report and state folders and never touch live config, credentials, or the incident queue.
- Use one writer per run record. Update the latest result atomically. Keep the previous valid state when an update fails.
- Check the terminal outcome and intended effect; a successful dispatch is not a completed run.
- State in the runbook that a runner cannot report its own absence; missing-run detection needs a separate observer.

A tool-owned job is Development Space's. For a problem with one, follow [tools/AGENTS.md](../tools/AGENTS.md).
