# Executor Archify bundle

Hidden build support for [the Executor profile](../../docs/profiles/executor/README.md).

| Path | Responsibility |
| --- | --- |
| `workflow/lifecycle-candidate.json` | Maintained task-run state machine source |
| `workflow/executor-workflow.html` | Canonical rendered HTML (public symlink: `docs/profiles/executor/executor-workflow.html`) |
| `workflow/review-4/` | Receipts for the current bytes (`review-1/` = earlier sandbox design, `review-2/` = previous, `review-3/` = previous) |

Rebuild from `~/.agents` with a fresh `--out-dir`:

```sh
node skills/archify/bin/archify.mjs finalize lifecycle .archify/executor/workflow/lifecycle-candidate.json .archify/executor/workflow/executor-workflow.html --quality showcase --out-dir .archify/executor/workflow/review-4 --json
```

The diagram documents the proposed per-task flow. Automated gates passed with no route crossings; perceptual visual review is not yet done.
