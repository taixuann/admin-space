# Model sync backend

`model_sync.py` owns daily catalog refresh, benchmark matching and scoring, bounded native OpenCode probes, cooldown state, and the default-model update.
`../selection.json` lists provider groups in priority order and defines the benchmark sources and weights. Dynamic groups use provider catalogs; fixed groups list exact model IDs.
`../model-list.json` is generated state. It contains no credentials and is ignored by Git.

```sh
python3 tools/opencode-free-router/backend/model_sync.py --status
python3 tools/opencode-free-router/backend/model_sync.py
python3 -m unittest discover -s tools/opencode-free-router/backend/tests
```

A real refresh reads public Zen/Go catalogs and public LMArena agent, webdev, and text datasets, then checks ranked candidates through native OpenCode, with a sixty-second subprocess limit.
The score is the weighted mean of each matched model's percentile within each leaderboard. The configured agent and webdev sources must both match; model IDs without both coding benchmarks remain unranked.
Ranking data older than the configured seven-day limit blocks a refresh before any default-model change.
No live probe output or raw provider error is copied to the catalog.
A same-day successful cache avoids network discovery and model probes.

The earlier `verify_routes.py` and `verify_zen_cli.py` remain explicit diagnostics. They are not called by daily automation.
Their reports describe the earlier complete probe campaign, not today's default-model update.
