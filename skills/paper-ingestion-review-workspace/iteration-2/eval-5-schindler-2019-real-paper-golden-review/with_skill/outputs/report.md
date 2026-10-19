# Independent review — Schindler & Bechtold (2019)

## Route and frozen scope

- **Route:** FULL — first review of the full packet, including source coverage, material Records, active Findings, figures/tables, and reference lineage.
- **Scope:** `PAPER-SCHINDLER-2019`, `EXP-01`–`EXP-03`, `FND-01`–`FND-06`, and the paper-local Reference Map. IDs are evaluation-fixture-local.
- **Frozen revision:** `GOLD-1`; handoff date in the manifest: 2026-10-19 (no exact time supplied). Paper/map, Records, Findings, and Reference Map each identify `GOLD-1`.
- **Approved source:** accepted manuscript, DOI `10.1016/j.jelechem.2019.01.069`; PDF and Markdown were accessible and matched the manifest SHA-256 values: PDF `5fcccdb2215a53b84fde0a208cd81fd1b13fe26e90276c5e2aa087d380ab431a`; Markdown `8b8821ba978e91ac04a62da196fcd8c5ce7850361d8fe46dbb326b9dafa240e3`.
- **Reviewer qualification:** `QUALIFYING_INDEPENDENT`. This isolated evaluation context had no producer conversation/history and completed the source inventory before opening the map, Records, Findings, or Reference Map.
- **Contract basis:** bundled `review-contract.md` and `quality-contracts.md`; the live Notion review page was fetchable, and its active ledger schema exposes the six grouped dimensions used below. The linked Paper Map, Evidence, Experimental Record, Paper Finding, Reference Map, and Review Issue pages return as deleted, so their bundled contract summaries controlled. No Notion write was made; this is an offline evaluation report.

## Blind source inventory

The article studies the initial anodic oxidation of dopamine on gold near physiological pH. It combines cyclic voltammetry at pH 5.8 and 7.0 with a calculated pH-dependent species distribution. The authors propose a fast reversible one-electron step followed by deprotonation to a semiquinone, with pH-dependent follow-up reactions. The radical is not directly isolated or identified.

The source reports dopamine hydrochloride solutions (0.5, 2, 5 mM); phosphate buffer preparation and an ambiguously specified PBS/NaCl relation; a separate pH 5 acetate buffer; three-electrode CV (2 mm Au working electrode, Pt counter, Ag/AgCl 3 M KCl reference), EG&G 264 A potentiostat and Rikadenki X–Y recorder; Ar deoxygenation for 8 min; room temperature; scan rates 5–100 mV/s; duplicate runs and means; electrode cleaning; and reference-potential checks. The species distribution uses published pKa values and CurTiPot; the cited pKa conditions differ from the CV conditions. The paper reports anodic/cathodic peak data, a scan-rate relation, qualitative air-oxidation appearance over time and pH, and an author-proposed mechanism. Limits include difficult isolation of individual products and unresolved reaction pathways. The accepted manuscript cites 29 references; no supplement is identified or required by it.

All figures are **MATERIAL**: Figure 1 (dopamine/DQ context), Figure 2 (species structures/distribution), Figures 3 and 5 (CV and scan-rate results), Figure 4 (time/pH-dependent oxidation appearance), and Figures 6 and 7 (reaction-pathway proposals). **Table 1 is MATERIAL** quantitative CV evidence. I visually inspected the panels, axes, conditions, and table cells in their PDF pages (figures on PDF pp. 3, 7, 10, 12, 13, 15; table on PDF p. 9). Captions were not treated as visual verification.

## Six active dimension states

| Dimension | State | Basis |
|---|---|---|
| Source & Identity | PASS | Approved PDF/Markdown accessible; both source hashes match the manifest and identify the accepted-manuscript version. |
| Paper Coverage | PASS | The map preserves the question, methods, regimes, key results, interpretation limits, buffer ambiguity, and all figure/table routes. |
| Record Coverage | FAIL | The Figure 4 air-oxidation demonstration has no distinct process Record; EXP-03 also omits source-reported calculation inputs and misstates software-version availability. |
| Figure/Table Coverage | PASS | All seven material figures and Table 1 are inventoried and visually inspected; result/context routes are present. |
| Finding Fidelity | FAIL | FND-06 combines an observed current comparison with an interpreted explanation while assigning both evidence modes to one Finding. |
| Traceability & Lineage | FAIL | Reference identities and all 29 bibliography entries are mapped, but several raw citation transcriptions contain PDF folio extraction artifacts. |

## Anchored issues

### R-001 — MAJOR — EXP-03 calculation inputs

- **Class:** omission
- **Source locator:** accepted manuscript §3 and Figure 2 (PDF p. 7); reference [24] (PDF p. 19).
- **Observed:** EXP-03 names three pKa inputs but does not preserve their plotted values. It also says the software version is not reported, although reference [24] identifies CurTiPot version 4.2.
- **Expected:** record pKa1 = 9.05, pKa2 = 10.58, pKa3 = 12.07 and CurTiPot v4.2; retain that the exact calculation input file is not specified by the manuscript.
- **Repair required:** correct EXP-03’s reported inputs/version.
- **Re-review scope:** NEIGHBORHOOD (EXP-03 and dependent FND-01/FND-04).
- **Status:** OPEN.

### R-002 — MAJOR — missing Figure 4 process Record

- **Class:** coverage
- **Target:** Paper §4.1 / Figure 4 and Records coverage.
- **Source locator:** accepted manuscript §4.1 and Figure 4 caption/image (PDF p. 10; printed p. 9).
- **Observed:** Figure 4 is routed to FND-05, but the packet has no distinct Record for the air-exposed auto-oxidation demonstration. EXP-01 covers solution/buffer preparation, not the pH/time series and visible oxidation process.
- **Expected:** add a coherent Record for the Figure 4 demonstration using only reported conditions (pH 5.0, 6.1, 6.5, 7.0; 24 h and 96 h; room temperature; air exposure from §4.1), preserve unspecified preparation/concentration/replicate details as unreported or unresolved, and link FND-05. Do not infer missing values.
- **Repair required:** create and link the source-bounded process Record.
- **Re-review scope:** FULL, because the material Record inventory changes.
- **Status:** OPEN.

### R-003 — MAJOR — FND-06 mixes evidence modes

- **Class:** evidence_mode
- **Target:** FND-06.
- **Source locator:** accepted manuscript §4.3 and Table 1 (PDF pp. 9, 14; printed pp. 8, 13).
- **Observed:** FND-06 states `OBSERVED` for the 23-to-3 µA cathodic-current comparison and `INTERPRETED` for the proposed faster-follow-up explanation, but presents both as one Finding.
- **Expected:** use one evidence mode per bounded Finding. Preserve the measured comparison as `OBSERVED`; place the proposed reaction-rate explanation in a separate `INTERPRETED` Finding or remove it from this Finding.
- **Repair required:** split the quantitative observation from the author interpretation and retain the conditions and links.
- **Re-review scope:** NEIGHBORHOOD (FND-06 and direct dependencies).
- **Status:** OPEN.

### R-004 — MINOR — citation transcription artifacts

- **Class:** reference_lineage
- **Target:** Reference Map entries R011, R022, and R029.
- **Source locator:** bibliography (PDF pp. 17–19; printed pp. 16–18).
- **Observed:** the map’s extracted “raw citations” contain page-folio artifacts, including `Anal. 17 Chem.` for [11], `9. 18 A13+` for [22], and a trailing `19` for [29]. The PDF shows these as page-layout artifacts rather than citation text.
- **Expected:** correct the affected transcriptions against the approved PDF and check the remaining bibliography entries for the same extraction artifact while retaining the paper-local numbering.
- **Repair required:** clean and verify the affected raw citation strings.
- **Re-review scope:** LOCAL (Reference Map entries only).
- **Status:** OPEN.

## Verdict, object states, and readiness

- **Verdict:** `REPAIR`. Source evidence is sufficient for the listed producer repairs; no scientific failure is inferred.
- **Object lifecycle states after this adjudication:** `EXP-01 PASS`, `EXP-02 PASS`, `EXP-03 REPAIR`; `FND-01 PASS`, `FND-02 PASS`, `FND-03 PASS`, `FND-04 PASS`, `FND-05 PASS`, `FND-06 REPAIR`. The missing Figure 4 Record has no current object state; if created, it starts at `NEEDS_REVIEW`. These states are reported for the fixture only and were not written to Notion.
- **Readiness:** `NOT_READY` pending R-001 through R-004 and full re-review after the Figure 4 Record is added.

## Final snapshot check and limitations

Immediately before recording this verdict, I re-read the packet revision markers and recomputed hashes for the manifest, PDF, Markdown, Paper map, Records, Findings, Reference Map, and both bundled contracts. They matched the reviewed snapshot; PDF and Markdown hashes still match the manifest. No stale-revision issue was found.

The review covers only the supplied accepted-manuscript version; the final typeset article was not compared, and the paper identifies no required supplement. The cited works were not independently retrieved. The manifest supplies only a handoff date, not an exact time. This report is not an Ingestion Reviews ledger entry.
