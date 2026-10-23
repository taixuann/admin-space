# Plan 005: git baseline at ~/.agents + codex candidate rewrite (writing-for-agents)

> **Operator decisions 2026-10-02, Stage E preparation turn:**
> 1. "set 1 cái git ở .agents là được mà? đâu cần để folder baseline" —
>    a git repo at `~/.agents` replaces the folder-baseline workflow for
>    drift checking and recovery.
> 2. "codex /agents.md thì xài /writing-for-agents + /simple-english để
>    triển khai" — the codex global candidate gets a full authoring pass
>    with the writing-for-agents discipline and the simple-english register
>    before Stage E.
> Both deployed the same day.

## Status

- **Status**: DONE (git baseline live; candidate rewritten; Stage E install still awaiting the operator's final authorization)
- **Priority**: P1
- **Effort**: S
- **Depends on**: plan 002 (done), plan 003/004 (done)
- **Category**: dx
- **Planned at**: 2026-10-02

## Change 1: git repo at ~/.agents (recovery layer)

- `git init` at `/Users/tai/.agents`, baseline commit
  `ac5af95` ("pre-install baseline: live skills + plans + workspaces (before
  GI Stage E install)") taken BEFORE any live file changed. Working tree
  clean at commit time.
- Effect: every future install or skill edit here is visible as
  `git diff` and recoverable with `git checkout -- <path>`; the folder
  `baseline/` copies stay only as historical A–C checkpoint evidence (they
  back the evidence-structure check that already passed and are not needed
  for future flows).
- Known quirk: `skills/prompt-refine` is an embedded git repo; git recorded
  it as a gitlink. It stays functional as a skill; do not re-clone it
  through the outer repo.
- Rollback for Stage E install is now: `git checkout -- <file>` (or the
  whole tree) — simpler than hash reconciliation.

## Change 2: codex candidate AGENTS.md authored via /writing-for-agents + /simple-english

- Full rewrite of
  `global-guidance-workspace/candidate/codex/AGENTS.md`
  (79 → 72 lines, diff 45 insertions / 51 deletions against the previous
  candidate).
- Structural moves per writing-for-agents (context-load reduction):
  - The Prometheus / Franky / Athena role-definition bullets (long inline
    prose) became a pointer: governed tasks read `agents/ROLE-CONTRACT.md`
    in the checkout, which owns role definitions. The dual-role file keeps
    conditional framing ("applies only when the task edits `/Users/tai/.codex`").
  - Retained as compressed rules: override precedence, skills/tools trigger
    discipline ("availability alone is not a reason"), lifecycle line,
    scientific baseline, delegated-execution batches, OpenCode model
    allowlist table (unchanged), persistent-instructions checklist, memory
    and evidence separation (OBSERVE → PROPOSE → REVIEW → ACCEPT → UPDATE),
    simplicity, blocked-turns convention, environment map.
  - Dropped as duplicates or staleness: role-definition prose (owned by
    ROLE-CONTRACT.md), Franky workflow-YAML history notes (repo-side
    detail), the "portrait" of every role, redundant Git-lifecycle repeats.
- Register applied (simple-english Plain): semicolons split into sentences
  (0 remaining), one instruction per sentence, condition before command,
  no em-dashes.

## Verification

- `git -C ~/.agents log --oneline` → `ac5af95` baseline + this candidate in
  working tree (`git diff --stat`: 1 file, +46/−52).
- Line count 72 ≤ 90 budget. Semicolon/em-dash count: 0.
- Key rules present (grep-verified): override precedence, ROLE-CONTRACT
  pointer, OBSERVE → PROPOSE chain, `Say hi` live check, ENVIRONMENT.md
  hint, blocked-turns convention, no-automatic-push, stop-and-escalate.

## Boundary

Nothing installed yet. Live files under `~/.agents/skills/` and
`~/.codex/AGENTS.md` are unchanged (the baseline commit is the snapshot of
that untouched state). Stage E install replaces live files only after the
operator's explicit authorization; recovery is then `git checkout`.
