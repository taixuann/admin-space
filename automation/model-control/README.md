# Daily model synchronization

The LaunchAgent `com.tai.model-control-sync` runs `run-sync.sh` at 00:00 local time. Its plist is `~/Library/LaunchAgents/com.tai.model-control-sync.plist`.

`run-sync.sh` calls the installed `opencode-model-router --sync --space all` with `OPENCODE_MODEL_ROUTER_REGISTRY` set to Admin's consumer registry, [`../../config/opencode-model-router/register.yaml`](../../config/opencode-model-router/register.yaml). `logs/` holds the output; `logs/latest-result.json` is the last result. `index.html` links to the tool's dashboard.

The tool is owned by Development Space. Read its [runbook](../../tools/opencode-model-router/README.md).

## Run and inspect

```sh
/bin/bash ~/.agents/automation/model-control/run-sync.sh
opencode-model-router --status
opencode-model-router consumer list
launchctl print gui/$(id -u)/com.tai.model-control-sync
```
