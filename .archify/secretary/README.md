# Secretary Archify bundle

Canonical support: `~/.agents/.archify/secretary/`. Profile access: `docs/profiles/secretary/.archify` is a relative symlink here.

## Current workflow

Public view: [Secretary workflow](../../docs/profiles/secretary/secretary-workflow.html). That entry is a relative symlink to `workflow/secretary-workflow.html`, a self-contained native Archify document.

| Path | Responsibility |
| --- | --- |
| `workflow/lifecycle-candidate.json` | Maintained request state machine, artifacts and capability-loading gates |
| `workflow/candidate.json`, `workflow/archive-before-state-machine/` | Previous role/lane diagram source and byte-preserved predecessor artifact/evidence |
| `workflow/secretary-workflow.html` | Canonical rendered HTML |
| `workflow/secretary-workflow.*.json` | Native delivery, validation and automated browser evidence |
| `native/profile-legacy.html` | Byte-preserved retired public profile explorer |
| `scripts/` | Legacy explorer/inventory tools, mapping and regression checks |
| `sources/`, other `native/` files, `inventory/` | Earlier sources, baselines and evidence |

From `~/.agents`, rebuild only the current workflow with:

```sh
node skills/archify/bin/archify.mjs finalize lifecycle .archify/secretary/workflow/lifecycle-candidate.json .archify/secretary/workflow/secretary-workflow.html --quality showcase --out-dir .archify/secretary/workflow/state-review-2 --json
```

For each changed candidate, choose a fresh `--out-dir` revision so prior browser evidence remains bound to its original bytes. The public symlink follows the canonical HTML; no sidecars appear in the visible profile folder. This rebuild needs no watcher or service.

The current workflow shows the intended self/other-profile management process. It does not install Executor or configure models, integrations or memory. The earlier draft at `../workflow-secretary-shared-20261025-144403/` remains historical; it is not the maintained workflow source.

The current diagram is a native Lifecycle state machine inside the same public workflow HTML. It shows required definition and plan artifacts before Executor handoff, actual capability loading/health checks, approval/readiness waits and rework/resume events. Current passing evidence is under `workflow/state-review-2/`. Earlier root-level finalize receipts belong to the previous role/lane diagram. Automatic routing reports two branch crossovers; automated checks passed, but visual polish has not been accepted.

## Legacy support and rollback

The previous `profile.html` was archived byte-for-byte as `native/profile-legacy.html`. Legacy explorer rebuilds now target that hidden path, never the retired public path. Those scripts are not the current workflow generator. Do not regenerate the archive merely to rebuild the current workflow. Previous compatibility links remain intact; recorded historical receipt paths are not rewritten or treated as current verification.

Legacy regression checks:

```sh
python3 -m unittest discover -s .archify/secretary/scripts -p 'test_*.py'
node .archify/secretary/scripts/test_secretary_explorer_browser.cjs
```

If Tai authorizes restoring the old public view, copy the verified archive back to `docs/profiles/secretary/profile.html` and reconcile navigation and writer destinations together. Do not silently restore that filename during a workflow rebuild. Keep SOUL, its active runtime link, credentials and mutable runtime stores unchanged.
