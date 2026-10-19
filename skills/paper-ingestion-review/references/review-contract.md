# Review contract reference

This file records the review rules fetched from Notion page **Paper Ingestion Review** (page ID `3da0a859-ed1f-8188-9874-ce403277d90e`, fetched 2026-10-19; page last edited 2026-09-14) and the currently exposed **Ingestion Reviews** database schema. The live Notion page and source-specific approved packet remain authoritative. This copy makes the local skill runnable when a linked page is unavailable; it does not silently resolve a live conflict.

## Scope and ownership

Review one paper packet containing its Paper map, material Experimental Records, active Paper Findings, approved sources, and frozen manifest. The producer owns content creation and repair. The reviewer reads the frozen content, inventories the source, records review state and anchored issues, and routes the packet. The reviewer is read-only on scientific content while adjudicating.

Content objects are Paper, Experimental Records, and Paper Findings. The Paper's Records tab is an inspection surface, not another store. One Ingestion Reviews row represents one review run. A Review Issue is an audit defect, not a Paper Finding. Do not create a second issue database or a second content flow.

Only a qualifying independent reviewer may finalize `PASS` and downstream readiness. A same-context challenge can improve the contract but cannot qualify the packet.

## Active ledger

Create one row per review run. The current exposed database identifies these operational fields:

- Identity and scope: `Review`, `Review ID`, `Paper`, `Route`, `Scope`.
- Snapshot and independence: `Frozen Revision`, `Reviewer Qualification`, `Reviewer Context`, `Reviewed At`.
- Six dimensions: `Source & Identity`, `Paper Coverage`, `Record Coverage`, `Figure/Table Coverage`, `Finding Fidelity`, and `Traceability & Lineage`.
- Outcome: `Verdict`, `Issue Summary`.

`Route` is `FULL`, `SCOPED`, or `NO_REVIEW`. `Reviewer Qualification` is `QUALIFYING_INDEPENDENT`, `NON_QUALIFYING_SAME_CONTEXT`, `UNAVAILABLE`, or `NOT_ASSESSED`. Each dimension is `NOT_ASSESSED`, `PASS`, or `FAIL`. `Verdict` is `NOT_ASSESSED`, `PASS`, `REPAIR`, or `BLOCKED`.

Fields prefixed `Legacy` are retained for history. Do not use them to infer readiness or write new decisions into them. The current database has no active `Target` property. The page's older phrase “legacy Target = INGESTION_PACKET” conflicts with its active-field statement and the live schema; represent full packet scope in `Route = FULL` and `Scope` instead. Do not create or populate a legacy field to satisfy the older phrase.

## Review route

- `FULL`: first review; changed source, Paper map, Record inventory, Finding universe, or material conditions; material source identity, attribution, reference-lineage, figure/table, or coverage defect; stale or unproven prior review; or a request to qualify downstream readiness.
- `SCOPED`: a reviewer has established a local/minor repair, unchanged source and frozen snapshot, and bounded blast radius. Review the repaired target, its direct dependencies, relevant source context, and affected dimensions. Escalate if any of those facts are uncertain.
- `NO_REVIEW`: metadata-only changes that cannot alter scientific meaning, provenance, routing, coverage, or lifecycle. It never creates readiness or object `PASS`.

## Frozen packet and independence

The manifest records:

1. Paper ID and revision, including the Paper-map revision.
2. Every material Experimental Record ID and revision.
3. Every active Paper Finding ID and revision.
4. Approved PDF and Markdown stable identities, plus provider version/revision or hashes when available.
5. Source-access results and an explicit missing-source list.
6. Review contract and skill version, with handoff time.
7. Any producer self-audit marked as non-qualifying challenge input.

A URL alone does not identify immutable bytes. Record missing provider tokens or hashes as a limitation. Fresh-context qualification means the reviewer has a separate context and has not read producer conclusions before completing the source inventory. The reviewer may read packet IDs and revisions before the inventory to admit and freeze the packet.

Newly handed-off material Records and Findings start at `NEEDS_REVIEW`. Object lifecycle and review dimensions are different state systems. Only the reviewer/finalizer writes object lifecycle states. Producers may not self-PASS.

## Snapshot race

Record the manifest at admission. Re-read packet revisions and source identities immediately before the verdict and lifecycle writes. A material source-byte, Paper, Record, Finding, relation, locator, condition, or review-contract change invalidates the pending decision. Record `BLOCKED`, add a `stale_revision` issue, withhold PASS, re-freeze, and run a fresh full review unless the change is proven outside scope. Reviewer comments and ledger writes do not invalidate scientific content.

## Outcome and readiness

`PASS` requires qualifying independence, all applicable dimensions passing, accessible approved sources, every material object passing, zero unresolved blocker/major issues, and a final manifest that matches. `REPAIR` means source evidence is sufficient and the producer can make a bounded correction. `BLOCKED` means source, identity, provenance, visuals, snapshot integrity, or qualifying review is unavailable. Missing evidence is not a failed scientific result.

Set `READY_FOR_DOWNSTREAM` only when approved sources remain accessible; Paper coverage is adequate for the stated downstream use; the full review qualifies and passes; all applicable dimensions and material objects pass; Experimental Record Coverage passes when material processes exist; no blocker/major issue remains; and the final revisions match. Otherwise return `REPAIR`, `BLOCKED`, or `NOT_READY` with gates.

## Source page

Canonical Notion skill: [Paper Ingestion Review](https://app.notion.com/p/3da0a859ed1f81889874ce403277d90e). The source page names the Paper Ingestion producer skill, review ledger, Review Issue schema, Paper Map, Experimental Record, Finding, Reference Map, and evaluation cases. Several linked pages were returned as deleted on fetch, so their retrieved contents are summarized in `quality-contracts.md` and `eval-cases.md`. Re-fetch them when available and reconcile any change before relying on this copy.
