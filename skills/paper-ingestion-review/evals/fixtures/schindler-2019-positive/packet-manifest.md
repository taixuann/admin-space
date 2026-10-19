# Frozen evaluation packet manifest

This is an offline evaluation fixture, not a Notion review row and not a claim that the paper is accepted for the user's downstream research. The object IDs below are fixture-local IDs. All packet artifacts are frozen at revision `GOLD-2` for this run.

## Identity and scope

- Paper: “Mechanistic insights into the electrochemical oxidation of dopamine by cyclic voltammetry,” Sabrina Schindler and Thomas Bechtold.
- Supplied version: accepted manuscript, accepted 29 January 2019; DOI `10.1016/j.jelechem.2019.01.069`; Journal of Electroanalytical Chemistry.
- PDF: `approved-paper.pdf`, SHA-256 `5fcccdb2215a53b84fde0a208cd81fd1b13fe26e90276c5e2aa087d380ab431a`.
- Model-readable text: `approved-markdown.md`, deterministic `pdftotext -layout` representation of that PDF, SHA-256 `8b8821ba978e91ac04a62da196fcd8c5ce7850361d8fe46dbb326b9dafa240e3`.
- A matching publisher HTML page was found in the source knowledge base. It contains abstract/metadata, is not part of the approved full-text packet, and is not used as paper-content evidence.
- Scope is the accepted-manuscript version only. The final typeset journal version was not compared. No supplementary file is cited or required by the supplied manuscript; no claim is made about unseen publisher attachments.
- Source folder remains read-only. The evaluation copy is byte-identical to its knowledge-base PDF.

## Frozen objects and contracts

- Paper/map: `PAPER-SCHINDLER-2019@GOLD-2`, `paper-map.md`.
- Material Experimental Records: `EXP-01@GOLD-2`, `EXP-02@GOLD-2`, `EXP-03@GOLD-2`, `EXP-04@GOLD-2`, `records.md`.
- Active Findings: `FND-01@GOLD-2`, `FND-02@GOLD-2`, `FND-03@GOLD-2`, `FND-04@GOLD-2`, `FND-05@GOLD-2`, `FND-06@GOLD-2`, `FND-07@GOLD-2`, `FND-08@GOLD-2`, `findings.md`.
- Evidence and reference lineage: `paper-map.md`, `records.md`, `findings.md`, and `reference-map.md`.
- Review contract: current bundled `references/review-contract.md` and `references/quality-contracts.md` in this skill.
- Handoff time: 2026-10-19T16:10:23Z; revision GOLD-2 was frozen before the independent review runs.
- Source gaps: final journal version comparison not in scope; no SI identified in the supplied accepted manuscript; no other source gaps are asserted.
- Reviewer context: the eval runner is instructed to use a fresh context that has not created or edited this fixture.

## Blind-order note

At review start, read this manifest and the approved PDF/Markdown only. Complete the source inventory before opening `paper-map.md`, `records.md`, or `findings.md`. Then compare the producer objects and perform a final reread of their fixture revisions and the two source hashes before deciding.
