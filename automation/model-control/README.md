# Daily model synchronization

The existing LaunchAgent `com.tai.model-control-sync` runs this job at 00:00 in the host local timezone.
Its installed plist remains at `~/Library/LaunchAgents/com.tai.model-control-sync.plist`.
The schedule is unchanged. The tool defines daily freshness in `Asia/Ho_Chi_Minh` independently of host timezone.

## Responsibilities

`run-sync.sh` sets PATH and calls the tool's model sync and existing conditional PaperQA indexing commands.
`logs/` holds stdout and stderr. Logic, catalog, and UI assets live under `../../tools/opencode-free-router/`.

Compatibility links for `model-control-spec.json`, `index.html`, and `app.css` preserve existing callers and URLs.
The legacy spec remains a separate snapshot for API consumers. It is not silently assigned a Zen model that rejects API calls.
New OpenCode callers use the tool's `model-list.json`.

## Run and inspect

```sh
/bin/bash /Users/tai/.agents/automation/model-control/run-sync.sh
/Users/tai/.local/bin/model-control-sync --status
launchctl print gui/$(id -u)/com.tai.model-control-sync
```

The tool refreshes once per successful Vietnam calendar day. Use its `--force` flag for an explicit new health check.
If discovery or all model probes fail, the job exits nonzero and preserves the last successful selection and configuration.
A failed refresh does not advance `dateUpdated`.

Read the [tool runbook](../../tools/opencode-free-router/README.md) for selection and recovery.
