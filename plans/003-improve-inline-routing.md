# Plan 003: Inline skill routing mentions in improve (applied at candidate stage)

> **Deployment record.** The operator approved the placement audit (2026-10-02,
> "Option B") and ordered deployment the same day: inline mentions only, no
> structural changes, terminal-title dropped in favor of OpenCode's native
> terminal titles. This plan replaces the REJECTED
> `~/.agents/plans/001-improve-core-driver.md` and records what was applied.

## Status

- **Status**: DONE (candidate-stage apply; not installed — installation remains gated by GI-001 Stage E)
- **Priority**: P1
- **Effort**: S
- **Risk**: LOW
- **Depends on**: none at candidate stage; installation remains gated by GI-001 Stage E
- **Category**: dx
- **Planned at**: 2026-10-02, no commit SHA

## Decisions applied

Five inline mentions, one per concern, in the GI-001 candidate files
(`global-instructions/orchestration-workspace/candidate/`):

1. **/prompt-refine** — improve `SKILL.md` Phase 2, end of the subagent-brief
   bullet list: refine the finished brief for the executor model; the guard
   freezes the playbook path, verbatim Hard Rules 4 and 6, the report
   contract, and the findings-only instruction.
2. **/simple-english** — improve `SKILL.md` Phase 4, plan-prose register
   bullet (Plain mode; tables, code, and commands keep their structure;
   Strict only when named).
3. **/skill-creator** — improve `SKILL.md` Phase 4: skill-subject plans name
   /skill-creator in the executor toolkit.
4. **opencode-delegate dispatch wording** — improve
   `references/closing-the-loop.md`: the external path names the relay
   (`scripts/relay.mjs`) and its `--read-only` review-only leg (GI-001
   "User decisions added after planning" item 2); the REVISE verdict row is
   transport-neutral with exact-sessionId preference and
   `--resume-last` as the fallback (replacing the Claude-Code-only
   `SendMessage`).
5. **Ponytail register** — improve `references/closing-the-loop.md` Review
   checklist gains item 5 (bloat scan: speculative abstraction, dead
   flexibility, invented dependencies; cosmetic findings go to NOTES,
   contract-violating ones go to REVISE). Brief level: opencode-delegate
   `references/writing-the-brief.md` `<action_safety>` gains the smallest-diff
   register and the objection-in-report rule (GI-001 "User decisions added
   after planning" item 5).

## Review round (2026-10-02, same day)

A cold-read by a fresh-context subagent flagged issues; all fixed in the
candidates and this record: README row 001 now records the improve direction
as DECIDED (inline, plan 003; the old UNDECIDED wording was a live
contradiction); writing-the-brief's closing "commit it yourself" line became
the governing-workflow wording (commit-actor conflict); the REVISE row
prefers the exact sessionId; improve's report contract is stated to win for
improve-led dispatches (transport template applies only to its own); the
`review <plan>` list gained item 5 so "run execute's review unchanged" holds;
prompt-refine's guard names its referent (the playbook's Finding format,
not an undefined "report contract" in the Phase 2 context); skill-creator's
loop is named by its real shape (draft → evaluate → feedback).

Deferred (pre-existing text, not introduced here): "record rejections in the
index" before `plans/README.md` exists (Phase 3/4 ordering), the unstated
`advisor-plans/` carve-out in Phase 4's index lines, and undefined terms
"cheap" / "side-effect free" in Hard Rule 2.

## Findings verified rather than edited

- **review-and-land ponytail-review bullet (GI-001 item 6): already covered.**
  The candidate's "The implementer sweep" section contains the same checks
  (dead weight, a-second-way, speculative surface, near-duplicate tests,
  guards for impossible cases). Adding the bullet would duplicate them; the
  file was left byte-identical (hash below matches the A-C receipt).
- **terminal-title: rejected.** OpenCode sets terminal titles natively
  (`OPENCODE_DISABLE_TERMINAL_TITLE` exists in the CLI docs); a mention would
  duplicate a platform feature.
- **humanizer / playwright-cli / remotion chain: no mention**, per the
  placement audit (procedure text, verification-via-toolkit, non-workflow).

## Verification

- `quick_validate.py` on candidate `improve` → `Skill is valid!`, exit 0
- `quick_validate.py` on candidate `opencode-delegate` → `Skill is valid!`, exit 0
- Candidate hashes after this deployment (sha-256):

| Candidate file | SHA-256 |
| --- | --- |
| `skills/improve/SKILL.md` | `e6b0f2f52a1c2e49994362647aed3e67705270f9a6928f2756b2a5d7d52a2b08` |
| `skills/improve/references/closing-the-loop.md` | `8449fcd729c45e5a9d4abe08f3094292622fd11b0e86efa0c4b26f189af6001d` |
| `skills/opencode-delegate/references/writing-the-brief.md` | `33551cb08c795d0bbc6e72aba23ecf4b81eac597a54adfa559d3aa149026d7ef` |
| `skills/opencode-delegate/references/review-and-land.md` | `eff2826e6bd591c984fd798d5ac84f7835de12f5c6d4e228fb3f57bafb282011` (unchanged) |

Pre-deployment hashes are the A–C checkpoint values in
`global-instructions/orchestration-workspace/review-receipt.md`
(improve SKILL.md `6edb6dd4…`, closing-the-loop `ae915f51…`,
writing-the-brief `c53f95a1…`).

## Boundary

The installed skills under `/Users/tai/.agents/skills/` stay untouched
(hash-verified earlier today at their pre-candidate values); everything here
is candidate-stage and flows to installation through GI-001's Stage E with
its remaining Stage D cases, the isolation boundary, and the separate
install authorization.

## Maintenance

- New global skill: add one inline mention at its natural step, or skip it when a native platform feature already covers the concern (predetermined by the terminal-title verdict).
- Post-V2-upgrade refresh pass (GI-002 section "Candidate refresh pass")
  applies its teachings to the AGENTS.md candidates, not to these skills.
