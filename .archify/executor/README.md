# Executor Archify bundle

Hidden build support for [the Executor profile](../../docs/profiles/executor/README.md).

| Path | Responsibility |
| --- | --- |
| `workflow/lifecycle-candidate.json` | Maintained task-run state machine source |
| `workflow/executor-workflow.html` | Canonical rendered HTML (public symlink: `docs/profiles/executor/executor-workflow.html`) |
| `workflow/review-6/` | Receipts for the current bytes (`review-1/` = earlier sandbox design, `review-2/` … `review-5/` = previous) |

Rebuild from `~/.agents` with a fresh `--out-dir`:

```sh
node skills/archify/bin/archify.mjs finalize lifecycle .archify/executor/workflow/lifecycle-candidate.json .archify/executor/workflow/executor-workflow.html --quality showcase --out-dir .archify/executor/workflow/review-6 --json
```

The diagram documents the per-task flow: a kanban card carrying the plan, the task branch, the OpenCode run, and review before merge. Automated gates passed. One advisory route crossing remains; perceptual visual review is not done.
