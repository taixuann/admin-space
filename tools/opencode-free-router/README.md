# OpenCode model selection

This shared Admin tool checks available models, ranks them with current coding-agent benchmark data, saves a dated catalog, selects the best reachable model, and updates OpenCode's default.
OpenCode remains the runtime. There is no HTTP gateway and no Hindsight-specific service here.

## Use

```sh
model-control-sync
model-control-sync --status
model-control-sync --force
```

The existing global `model-control-sync` command points to `backend/model_sync.py`.
Run the backend directly with Python if the global command is unavailable.
`--status` only reads state. Normal execution uses today's successful cache, or refreshes if it is stale.
`--force` explicitly repeats live discovery and probes.

## Daily state

[`selection.json`](selection.json) is the editable ordered provider-group configuration and benchmark-weight file.
`model-list.json` records `dateUpdated`, timezone, ordered provider groups, model scores and sources, the selected model, route checks, and cooldowns.
To add a provider with no built-in catalog, add a fixed group with explicit model IDs and place it in the desired order. Confirm its billing behavior before adding it; only Zen and Go currently have automatic catalog refresh.
`dateUpdated` records the latest successful refresh in `Asia/Ho_Chi_Minh`.
A timestamp from a different day or from the future is stale.
A successful catalog response alone does not mark a model healthy.
Candidates are probed in quality order until one returns the expected synthetic OK response. Unranked models are recorded but never probed as a guessed fallback.

The tool follows the groups in `selection.json`: Zen free, Go free, Google AI Studio free, then Go Muse Spark.
Within each free group, it probes the highest Arena percentile composite first. Arena agent and webdev contribute 0.35 each; text contributes 0.15. Both agent and webdev matches are required for a comparable coding score.
Benchmark data expires after seven days. Missing or stale data blocks selection and preserves the current OpenCode default; it never falls back to alphabetical model IDs.
Free-name filtering matches the existing provider convention. It is not an independent billing audit.
Google is considered before Muse only if Google credentials already exist in native OpenCode's auth store.
The Hindsight-only Google key does not silently become a global OpenCode credential.
Muse Spark is the last permitted subscription fallback. No additional paid fallback is added.
Exhausted quota applies to that route, not all free routes at the same provider.
Provider reset metadata is not available to this CLI probe. Quota errors use a six-hour cooldown, other failures thirty minutes.

## Configuration and failure handling

The tool changes only top-level `model` in `~/.config/opencode/opencode.jsonc`.
It preserves other fields and creates a private backup before changing the configuration.
The current file contains strict JSON. If comments or invalid JSON appear, the tool refuses to rewrite it.
An active tool lock prevents overlapping refreshes.
If every candidate fails, OpenCode keeps its previous default. The successful date stays unchanged.
Use a fresh OpenCode session to load the new default. Existing sessions and explicit model pins remain separate.

## Source and compatibility

The upstream launcher remains at `~/.config/opencode/free-router/opencode-free`, linked here as `opencode-free`.
That launcher still uses upstream `free/auto` routing. Plain `opencode` uses the default selected by this tool.
Upstream: https://github.com/lettland/opencode-free-router

`model-control/` holds the moved legacy dashboard, spec, and conditional PaperQA indexing helper.
Old automation paths link here so existing API consumers keep their previous behavior.
The retired sync implementation is preserved as text under `docs/history/` and is not executed.
The legacy API spec is not synchronized to the selected native-only Zen model.

The existing [automation runner](../../automation/model-control/README.md) owns scheduling and logs.
[Documentation](docs/README.md) contains the interactive diagram and prior probe evidence.
[Backend](backend/README.md) contains implementation and verification commands.
