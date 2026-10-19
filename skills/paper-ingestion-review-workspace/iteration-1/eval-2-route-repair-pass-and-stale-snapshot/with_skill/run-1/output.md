# Synthetic paper-ingestion review results

These are three independent synthetic packets. No Notion records were read or written. The fixture supplies the packet facts; no paper files or real source evidence are involved.

## Case A — source-sufficient local repair

**Route:** `FULL`  
**Scope:** Full initial review; Finding FND-07 requires a bounded local correction and neighborhood re-review.  
**Frozen revision / source access:** Paper, Record, Finding, and contract revisions are recorded and stable. Approved PDF and Markdown are accessible; stable file IDs and hashes match the manifest. Blind inventory and visual inventory are complete.  
**Reviewer qualification:** `QUALIFYING_INDEPENDENT` — fresh, separate context.  
**Object under review:** FND-07 is currently `NEEDS_REVIEW` and remains out of `PASS` pending repair and re-review.

| Dimension | State | Basis |
|---|---|---|
| Source & Identity | `PASS` | Approved source identities and revisions match the manifest. |
| Paper Coverage | `PASS` | Blind inventory and paper-map coverage are complete. |
| Record Coverage | `PASS` | No Record coverage defect is reported. |
| Figure/Table Coverage | `PASS` | Figures and tables are inventoried. |
| Finding Fidelity | `FAIL` | FND-07 omits source-reported uncertainty. |
| Traceability & Lineage | `PASS` | Source locator is clear; no lineage defect is reported. |

**Issue:**

```text
[ISSUE R-001]
Severity: MAJOR
Class: quantity
Target: FND-07
Source locator: The clear source locator for the reported value (exact page/panel locator is not supplied in the synthetic fixture)
Observed: FND-07 omits the reported uncertainty.
Expected: Preserve the source-reported uncertainty with the Finding's value.
Repair required: Producer adds the reported uncertainty to FND-07 from the approved source.
Re-review scope: NEIGHBORHOOD
Status: OPEN
```

**Verdict:** `REPAIR` — evidence is sufficient and the defect is locally repairable.  
**Object lifecycle state:** FND-07 `REPAIR`; do not set it to `PASS` before neighborhood re-review. Other material objects may be finalized `PASS` only if they were individually adjudicated and the final manifest still matches; the fixture does not enumerate them or state their current lifecycle states.  
**Readiness:** `NOT_READY` (repair required). Gate: correct FND-07, re-review the Finding and its neighborhood, and repeat the final revision/source identity check. Do not hand off `READY_FOR_DOWNSTREAM` while this major issue is open.

## Case B — clean, qualifying, complete packet

**Route:** `FULL`  
**Scope:** Full packet review and downstream-readiness qualification.  
**Frozen revision / source access:** Paper/map revisions, all material Record and active Finding revisions, source identities, and contract version are in the manifest. Approved PDF, Markdown, and required supplements are accessible and identified by stable IDs and hashes. The final reread matches the manifest; no source gaps are reported.  
**Reviewer qualification:** `QUALIFYING_INDEPENDENT` — fresh context, with producer conclusions withheld until after the blind source inventory.

| Dimension | State | Basis |
|---|---|---|
| Source & Identity | `PASS` | Required sources are accessible, identified, and match the final manifest. |
| Paper Coverage | `PASS` | Inventory covers methods, conditions, regimes, positive and negative results, limitations, supplements, and bibliography; map coverage is adequate. |
| Record Coverage | `PASS` | Material Records are represented and reachable from the Paper narrative. |
| Figure/Table Coverage | `PASS` | Figures, tables, and captions are inventoried and adequately covered. |
| Finding Fidelity | `PASS` | Material Findings have correct locators, conditions, quantities, comparators, and evidence modes. |
| Traceability & Lineage | `PASS` | Required links and lineage are correct; no open blocker or major issue remains. |

**Issues:** None open.  
**Verdict:** `PASS`.  
**Object lifecycle states:** Every material Record and active Finding is eligible for `PASS` after the successful final check; set each to `PASS`.  
**Readiness:** `READY_FOR_DOWNSTREAM` — all stated readiness gates pass, including approved-source access, qualifying full review, dimensions, material object states, coverage, and final revision match.

## Case C — source revision and Finding inventory change at final check

**Route:** `FULL`  
**Scope:** Full review must be repeated on a newly frozen packet. The prior blind inventory and adjudication concern the old snapshot.  
**Frozen revision / source access:** The pending review used the prior PDF revision and Finding inventory. Immediately before verdict, the provider reports a new PDF revision and the active Finding inventory gains one Finding. The prior manifest no longer matches. New source bytes and the added Finding have not been reviewed.  
**Reviewer qualification:** `QUALIFYING_INDEPENDENT` for the previous review context; independence does not repair this snapshot race.  
**Object lifecycle state:** No object or review may be set to `PASS` on this pending decision. Keep affected material objects at `NEEDS_REVIEW`; withhold all pending `PASS` states until the new packet is frozen and reviewed.

| Dimension | State | Basis |
|---|---|---|
| Source & Identity | `NOT_ASSESSED` | The source identity changed after admission; the new PDF revision is not reviewed. |
| Paper Coverage | `NOT_ASSESSED` | Current coverage cannot be established against the changed source snapshot. |
| Record Coverage | `NOT_ASSESSED` | The changed snapshot invalidates the pending coverage adjudication. |
| Figure/Table Coverage | `NOT_ASSESSED` | Visual coverage against the new PDF revision is unverified. |
| Finding Fidelity | `NOT_ASSESSED` | The added active Finding was not in the reviewed inventory. |
| Traceability & Lineage | `NOT_ASSESSED` | The new Finding's links and lineage have not been reviewed. |

**Issue:**

```text
[ISSUE R-001]
Severity: BLOCKER
Class: stale_revision
Target: Review packet
Source locator: Final race check immediately before verdict; provider reports a new PDF revision and the active Finding inventory adds one Finding.
Observed: The source identity and Finding universe no longer match the frozen manifest used for review.
Expected: Freeze the new source and complete current object inventory before adjudicating.
Repair required: Re-freeze the packet, record the new PDF identity/revision and complete Finding inventory, then run a fresh full review.
Re-review scope: FULL
Status: OPEN
```

**Verdict:** `BLOCKED` — the snapshot race invalidates the pending decision.  
**Readiness:** `BLOCKED`; no downstream handoff. Gates: establish the new source identity and complete inventory, perform a fresh full review, and rerun the final race check. The previous review's passes cannot carry forward.
