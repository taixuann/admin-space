# Independent packet reviews

These are synthetic packet assessments based only on the supplied case facts. Each case is adjudicated separately.

## Case A — source-sufficient local repair

**Route:** `FULL` initial review. The reviewer is fresh and independent, source identity and revisions are stable, and the inventory is complete. The single identified defect is locally repairable.

**Six dimensions:**

1. Source identity and integrity — `PASS`; PDF and Markdown are accessible and their stable IDs and hashes match the manifest.
2. Source coverage — `PASS`; blind inventory and figures/tables are complete.
3. Paper/map coverage — `PASS`; no coverage defect is reported.
4. Record and Finding fidelity — `FAIL`; FND-07 omits reported uncertainty.
5. Traceability and locators — `PASS`; the source locator and reported value are clear.
6. Lineage and revision control — `PASS`; object and contract revisions are recorded and stable.

**Verdict:** `REPAIR`.

**Object state:** Material object remains `NEEDS_REVIEW`. FND-07 is the exact repair target and must remain out of `PASS` until corrected and reviewed. Create one actionable `MAJOR` issue anchored to FND-07. After correction, re-review FND-07 and the explicitly affected local neighborhood; no broader inventory review is indicated by the supplied facts.

**Final revision check:** Paper, Record, Finding, and contract revisions are stable and recorded. No revision race is reported.

**Readiness:** Not ready for downstream use. The open major issue and unpassed Finding block readiness.

## Case B — clean, qualifying, complete packet

**Route:** `FULL` independent review, qualifying as `QUALIFYING_INDEPENDENT`. The reviewer is fresh, has not seen producer conclusions before completing the source inventory, and the complete packet is identified by stable IDs and hashes.

**Six dimensions:**

1. Source identity and integrity — `PASS`; approved sources and required supplements are accessible and identified by stable IDs and hashes.
2. Source coverage — `PASS`; methods, conditions, regimes, positive and negative results, limitations, figures, tables, captions, supplements, and bibliography are accounted for.
3. Paper/map coverage — `PASS`; map coverage is adequate.
4. Record and Finding fidelity — `PASS`; all material Records and Findings are reachable and have correct locators, conditions, quantities, comparators, and evidence modes.
5. Traceability and lineage — `PASS`; lineage is correct and source gaps are explicitly none.
6. Revision control and adjudication — `PASS`; the manifest covers the Paper/map, all material Records and active Findings, and contract version; no blocker or major issue is open.

**Verdict:** `PASS`.

**Object state:** All material objects are eligible for `PASS`. After the final revision and identity check, set each material object to `PASS`.

**Final revision check:** Confirmed. Every revision and source identity matches the manifest.

**Readiness:** `READY_FOR_DOWNSTREAM`.

## Case C — revision changes during adjudication

**Route:** Stop adjudication and block the current review. The source snapshot used for the inventory and review is stale because the provider reports a new PDF revision and the active Finding inventory has changed.

**Six dimensions:**

1. Source identity and integrity — `BLOCKED`; the current PDF revision no longer matches the reviewed snapshot.
2. Source coverage — `BLOCKED`; the newly added active Finding was not included in the reviewed inventory.
3. Paper/map coverage — `BLOCKED`; coverage was assessed against the previous snapshot.
4. Record and Finding fidelity — `BLOCKED`; the changed Finding inventory means completeness and fidelity cannot be concluded for the current packet.
5. Traceability and lineage — `BLOCKED`; current links and lineage require reassessment against the new Finding set.
6. Revision control and adjudication — `BLOCKED`; the final revision check failed due to a stale revision.

**Verdict:** `BLOCKED` — issue class `stale_revision`.

**Object state:** Do not mark any object or the review `PASS`. Preserve the prior review as tied to its old snapshot; it does not qualify the changed packet.

**Final revision check:** Failed. A new PDF revision and one added active Finding were reported immediately before verdict, after review of the previous snapshot.

**Readiness:** Not ready. Freeze the new source and Finding inventory, update the manifest, then conduct a fresh full review before adjudicating again.
