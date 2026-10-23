# Batch 4: model tool and tool-owned refresh automation

Request: 008. Executed 2026-10-23 in
`/Users/tai/development-space/worktrees/admin/opencode-free-router_008`, branch
`admin/opencode-free-router_008`, based on tool `main` at
`21cb19c8251152e90b1b04c0e6a4fde8781581ec`.

## Source changes

| File | Change |
| --- | --- |
| `backend/model_sync.py` | Stage-attributed `StageFailure`, safe messages, result envelope with `stage`, `errorCategory`, `selectedModel`, `previousModel`, `configChanged`, `dateUpdated`; `--result-json` and `--run-id`; exit 75 for lock contention |
| `backend/tests/test_model_sync.py` | Added catalog failure, all-probes-failed, apply failure, state-write failure, and manual/scheduled lock contention cases |
| `automation/model-refresh/runner.py` | One run lifecycle: explicit report root, timeout, classification, bounded diagnostics, redaction, atomic run evidence, retention, incident forwarding, recovery after a failed run |
| `automation/model-refresh/launchd.plist` | Direct absolute interpreter invocation, 00:00 local, `RunAtLoad` false, declared `PATH`/`HOME`, logs under the report root |
| `automation/model-refresh/tests/test_runner.py` | 17 runner cases |
| `automation/model-refresh/README.md` | Schedule, invocation, reports, failure behavior, recovery, rollback |
| `automation/model-refresh/AGENTS.md` | Ownership, boundaries, verification, secret rules |

## Behavior preserved

- Provider priority, free-quota constraints, selection rules, and OpenCode
  config writes stay in `backend/model_sync.py`.
- A failed refresh preserves the previous valid model and the previous
  successful date.
- A fresh selection is re-applied without probing.
- The tool lock still prevents manual and scheduled overlap.
- The OpenCode binary was not updated.
- The installed schedule was not changed.

## Evidence and results

| Check | Command | Result |
| --- | --- | --- |
| Model tests | `python3 -m unittest discover -s backend/tests` | 17/17 pass |
| Runner tests | `python3 -m unittest discover -s automation/model-refresh/tests` | 17/17 pass |
| Plist syntax | `plutil -lint automation/model-refresh/launchd.plist` | OK |
| Dry run | runner with a temporary `--report-root` | Prints plan, invokes no tool, creates no path |
| Secret redaction | runner tests | Token-shaped output replaced with `[redacted]` |
| Retention | runner test | 30 days / 100 runs; pending incident events survive |
| Recovery | runner test + real incident CLI with fake transport | Failure creates one ticket; next success appends recovery evidence, status stays `Captured` |

End-to-end fake-transport run: failure exit 1 then success exit 0 produced one
incident with one occurrence and one recovery row. No live Notion call, no
OpenCode configuration change, no live report root.

## Residual risk

- Report retention and timeouts are proposed values, not measured against
  production volume.
- The runner cannot detect its own absence. Missing-run detection is deferred.
- Activation remains blocked on old-runner continuity and unattended Notion
  authentication.

## Not done

- No commit in the worktree (no authorization).
- No merge to tool `main`.
- No launchd install, bootstrap, bootout, or kickstart.
- No live model refresh.
