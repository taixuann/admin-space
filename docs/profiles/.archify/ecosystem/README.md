# Ecosystem Archify bundle

Public view: [ecosystem.html](../../ecosystem.html).

This hidden bundle groups the existing ecosystem candidate and receipts. The visible HTML was not regenerated in this documentation-first step. It predates the Executor review draft and is not yet the complete proposed Secretary/Coordinator/Executor operating model.

- [source/candidate.json](source/candidate.json): existing native Archify source.
- `ecosystem.delivery.json`: original delivery receipt.
- `ecosystem.finalize.json` and `ecosystem.finalize-summary.json`: original finalization evidence.
- `ecosystem.browser-check.json`: original automated browser evidence.

The old root `.archify/architecture-profile-ecosystem-20261025-104355/` path is a compatibility symlink to `source/`. Files were moved with byte comparisons; their contents and recorded paths were preserved. Relocation is not a new runtime or visual verification.

After the Executor definition is approved, update the single ecosystem diagram to show Tai, Secretary, Coordinator, Executor, task sandboxes, review, and owning Spaces. Use Archify's current authoring and delivery contract. Keep future candidates, scripts, and receipts here, not beside the visible HTML. If the renderer emits sidecars next to an output, stage that generation in this bundle and preserve artifact identity when publishing the visible view. Do not claim that archived receipts certify changed HTML.

No runtime profiles, configuration, services, or execution sandboxes are created by this bundle.
