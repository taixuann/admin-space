# Shared OpenCode selection contract

The tool checks models and writes a verified default into native OpenCode configuration.
Consumers run OpenCode normally. Hindsight integration is a separate task.

[`selection.json`](selection.json) is the single ordered configuration:

1. OpenCode Zen free models, ranked by the Arena agent/webdev/text composite.
2. OpenCode Go free models, ranked the same way.
3. Google AI Studio Gemini 3.8 Flash free tier, only when native OpenCode already has Google auth.
4. OpenCode Go Muse Spark contributor, the final fixed fallback.

The model list in each catalog-backed group refreshes daily. The groups determine provider priority; benchmark scores determine order inside each free group. Unranked models are visible in `model-list.json` and skipped. If the benchmark feed is missing or older than seven days, refresh fails closed and preserves the current default.
Google precedes Muse by owner choice. A key stored only in Hindsight is not a native OpenCode credential.
Unavailable routes enter cooldown. A successful daily refresh caches its selection in `model-list.json`.
The tool is not an HTTP fallback gateway and does not change model pins inside existing sessions.

The selected runtime is `backend/model_sync.py`; `selection.json` controls group order, model membership, and benchmark weights.
The scheduling entrypoint remains `automation/model-control/run-sync.sh`.
Read README.md for cache, quota, backup, and compatibility details.
