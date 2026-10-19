# Evaluation fixture: route, verdict, and race checks

These cases are synthetic contract tests, not evidence from real papers. Treat each packet as a separate review.

## Case A — source-sufficient local repair

- Reviewer context is fresh and separate from the producer.
- PDF and Markdown are accessible; stable file IDs and hashes match the manifest.
- Paper, Record, Finding, and contract revisions are recorded and stable.
- Blind source inventory and figures/tables are complete.
- All six dimensions pass except Finding Fidelity, which fails because Finding FND-07 omits the reported uncertainty. The source locator and value are clear.
- No other defect exists. FND-07 is the exact repair target; a local correction can fix it without changing the paper inventory or any dependent Finding.
- The material object is still `NEEDS_REVIEW`.

Expected: `FULL` if this is the initial review, `REPAIR`, FND-07 remains out of PASS, one actionable MAJOR issue at FND-07, neighborhood or local re-review explicitly bounded, and no readiness.

## Case B — clean, qualifying, complete packet

- Reviewer context is fresh and has not read producer conclusions before the source inventory.
- Approved PDF, Markdown, and all required supplements are accessible and identified by stable IDs and hashes.
- The manifest lists the Paper/map revisions, every material Record and active Finding revision, source gaps (none), and contract version.
- Blind inventory accounts for the paper's methods, conditions, regimes, positive and negative results, limitations, figures/tables/captions, supplements, and bibliography.
- Paper map coverage is adequate. All material Records and Findings are reachable from the Paper narrative and have correct locators, conditions, quantities, comparators, evidence modes, and lineage.
- All six grouped dimensions pass; all material objects are eligible for PASS; there are no open blocker/major issues.
- Final reread confirms every revision and source identity matches the manifest.

Expected: `FULL`, `QUALIFYING_INDEPENDENT`, all six dimensions `PASS`, `PASS`, each material object `PASS` after final check, and `READY_FOR_DOWNSTREAM`.

## Case C — revision changes during adjudication

The facts match Case B through the final check, except that immediately before verdict the source provider reports a new PDF revision and the Finding inventory changes by one added active Finding. The blind inventory and current paper review used the previous snapshot.

Expected: `BLOCKED`, issue class `stale_revision`, no object or review PASS, new freeze and fresh full review required, no readiness.
