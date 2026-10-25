# Forge Archify bundle

Build support for [the Forge profile](../../docs/profiles/forge/README.md). `workflow/lifecycle-candidate.json` is the state-machine source; `workflow/forge-workflow.html` is the rendered page (public symlink `docs/profiles/forge/forge-workflow.html`); `workflow/review-1/` holds the finalize receipts.

Rebuild from `~/.agents` with a fresh `--out-dir`:

```sh
node skills/archify/bin/archify.mjs finalize lifecycle .archify/forge/workflow/lifecycle-candidate.json .archify/forge/workflow/forge-workflow.html --quality showcase --out-dir .archify/forge/workflow/review-2 --json
```

Automated gates passed; two route crossovers are advisory and perceptual review is not done. The diagram describes intent, not a tested run.
