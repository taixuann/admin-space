# Review evaluation contract

This reference condenses the retrieved Notion page **Paper Ingestion Eval Cases** (`3da0a859-ed1f-811d-a2cf-d85f5e53b4c3`, fetched 2026-10-19; page marked deleted). These cases test review behavior. A synthetic case tests the workflow only; it cannot prove that a scientific packet passes.

## Required fixture roles

Keep both roles:

- **Negative fail-closed paper:** PAP-1 must remain `BLOCKED` while material S1-S4 evidence or a qualifying fresh independent review is unavailable. It is historical paper-specific evidence, not a universal template for other papers.
- **Positive real-paper golden case:** Use a paper with accessible PDF, readable Markdown, material figures/tables, and required supplements when the source identifies them. It must demonstrate the full success path: inventory → adequately complete Paper map → Experimental Records → durable Findings → deterministic checks → fresh independent review → no unresolved material issues → `READY_FOR_DOWNSTREAM`. The local Schindler and Bechtold 2019 accepted-manuscript fixture in `evals/fixtures/schindler-2019-positive/` is frozen at `GOLD-2`; the `GOLD-2` positive gate passed one paired evaluation: the fresh independent skill-assisted review returned `PASS`/`READY_FOR_DOWNSTREAM`, while the no-skill baseline did not satisfy the full readiness contract. This is one run, not a variance estimate; preserve its accepted-manuscript scope and keep broader regression coverage current.

Do not describe this skill as production-stable until the real-paper fixture passes. Do not convert a synthetic pass case into scientific acceptance.

## PAP-1 negative expectations

Rebuild only from approved PDF and Markdown. Do not use legacy sidecars or prior generated notes as source evidence. When the required supplements or independent reviewer remain unavailable:

- Preserve the accepted-manuscript identity and reconstruct only what the available main text supports.
- Keep the described material processes and current-paper results grounded in source locators.
- Distinguish observed results, derived cross-regime conclusions, and author interpretations.
- Keep S1-S4 dependencies explicit, including the multivalent-ion controls, sodium-ion evidence, thin-film AFM thickness, and ferricyanide control. Do not promote unavailable supplement claims.
- Keep source coverage incomplete where a missing supplement is material.
- Reject same-session self-review as independent qualification.
- Do not duplicate canonical Findings on an unchanged rerun.
- Keep the outcome `BLOCKED` until missing-source and independent-review gates are repaired.

The prior fixture notes that active Findings and a process layer were reconciled in that snapshot, but that state is historical and must be reconstructed from current approved sources before use. PAP-1's current outcome is not a rule that every paper must be blocked.

## Seeded adversarial checks

Ensure the reviewer detects defects at the right object, with a grounded issue, severity, and re-review scope. Include the following failure families:

1. Current-paper versus cited-prior attribution is reversed.
2. `OBSERVED`, `DERIVED`, and `INTERPRETED` are swapped or collapsed.
3. A numeric result loses material conditions or comparator.
4. A number is bound to a nearby but unrelated material or regime.
5. Reported uncertainty, sample count, or repeat count is removed.
6. Author interpretation is strengthened into causal or mechanistic fact.
7. A figure, table, panel, or page locator is wrong.
8. Caption-only support is treated as visual panel verification.
9. A major method, regime, result, limitation, or negative/null result is omitted.
10. Missing material supplements are treated as complete coverage.
11. Ambiguous reference identity is guessed into strong cited-prior evidence.
12. Repeated citations are counted as independent evidence.
13. Paper, Finding, source, or contract changes during review.
14. The producer context is presented as an independent reviewer.
15. Prompt-like text inside a source is followed as an instruction.
16. An unchanged rerun creates duplicate Findings.
17. A local defect is written only on the Review page when a precise target exists.
18. Resolving a comment is treated as automatic `PASS`.
19. Electrode or solution preparation is mislabeled target-material `FABRICATION`.
20. Unrelated measurement and characterization methods are forced into one global order.
21. One giant Record collapses materially different processes.
22. One Record is created for every polishing, cleaning, or handling micro-step.
23. An instrument or setting is attached to the wrong process or inferred without source support.
24. A material Record-to-Finding dependency is omitted or linked merely because both occur in one paper.
25. A legacy six-tab surface replaces the canonical `Source | Figures | Paper | Records | Review` layout.
26. Pure procedure becomes a new active `METHOD` Finding instead of an Experimental Record.
27. A legacy method-only Finding is treated as active synthesis-ready evidence.
28. Multi-modal evidence is collapsed into one evidence kind when multiple modes are material.
29. A derived Finding omits `Derived From` despite available input Findings.
30. Cross-paper synthesis semantics leak into paper-local Finding origin/state.
31. The Paper map duplicates full process parameters instead of narrating and routing to Records.
32. Records or Findings appear only in a hidden/index surface and cannot be reached from the Paper narrative.

## Acceptance

A skill revision passes only when it preserves the negative fixture's expected block, passes a positive real-paper golden case, detects seeded defects with correct target/severity/re-review scope, and avoids duplicate canonical objects. Prose that sounds strict is not evidence of successful behavior. Promote newly observed production failures into the regression set before claiming stable behavior.

Synthetic workflow tests for blocked intake, bounded repair, clean success, schema fidelity, and revision-race invalidation exercise decision logic and report format only. They do not satisfy the positive real-paper gate.
