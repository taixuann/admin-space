# Plan 006: Clean the ~/.codex repo — drop dead index, role contract, CI

> **Executor instructions**: Follow this plan step by step. Run every
> verification command and confirm the expected result before moving on. If
> anything in the "STOP conditions" section occurs, stop and report; do not
> improvise. Update the status row in `/Users/tai/.agents/plans/README.md`
> when done.
>
> **Drift check (run first)**: `git -C /Users/tai/.codex log --oneline -1`
> → `e7c5b71`; `git -C /Users/tai/.codex diff --quiet AGENTS.md` → exit 0
> (AGENTS.md untouched since install); `git -C /Users/tai/.codex status
> --porcelain | grep -c '^ D'` → 64. On any mismatch, STOP.

## Status

- **Priority**: P1
- **Effort**: S
- **Risk**: LOW (deletions only; every byte stays in git history)
- **Depends on**: none
- **Category**: tech-debt
- **Planned at**: 2026-10-02, `~/.codex` at `e7c5b71`
- **Issue**: omit

## Why this matters

The `~/.codex` repo index claims 72 tracked files. 64 of them no longer
exist on disk, the CI guards their dead paths, and the role contract has
exactly one referrer. Every future `git status` is noise, and the repo
misdescribes itself (README lists skills that are gone). After this plan
6 files remain tracked and every one exists.

## Current state

Target repo `/Users/tai/.codex` at `e7c5b71`, working tree (verified
2026-10-02):

- 64 tracked paths deleted on disk: all of `skills/agent-creator/`,
  `skills/agents-md/`, `skills/athena-review/`, `skills/harness-worker/`,
  `skills/issue-execution/`, `skills/skill-creator/`.
- 3 modified tracked files: `.github/workflows/skill-validate.yml` (2-line
  workflow tweak), `agents/ROLE-CONTRACT.md` (2-line wording tweak),
  `agents/prometheus.toml` (6-line delegation-boundary rewording, already
  on disk).
- `AGENTS.md` (72 lines) clean at `5e9ca977…`. Its workbench section
  (lines 19-21) points at the contract being deleted:

```text
1. Read `agents/ROLE-CONTRACT.md` in that checkout. It owns the role definitions and boundaries (Prometheus, Franky, Athena). This file does not redefine them. Do not invent or merge roles.
2. Select exactly one canonical parent role and workflow. Bounded leaf adapters serve under it. Do not cross role boundaries or protected scopes. Changes to role policy require explicit human approval.
3. Delegate only bounded steps within the active role contract. Conflicts in role, scope, plan, or worktree state are stop-and-escalate conditions.
```

- `README.md` "Start here" items 2-4 link dead files (`ROLE-CONTRACT.md`,
  three deleted skills).
- `.gitignore` carries dead negations for every removed skills path plus
  `!agents/ROLE-CONTRACT.md`.

## Commands you will need

| Purpose | Command | Expected on success |
|---|---|---|
| Drift | `git -C /Users/tai/.codex log --oneline -1` | `e7c5b71 …` |
| Count deletions | `git -C /Users/tai/.codex status --porcelain \| grep -c '^ D'` | `64` |
| Final tree | `git -C /Users/tai/.codex ls-files \| wc -l` | `6` |
| No dangling refs | `git -C /Users/tai/.codex grep -rn 'ROLE-CONTRACT\|agent-creator\|agents-md\|athena-review\|harness-worker\|issue-execution' -- . ':!*.sqlite*'` | exit 1 (no match) |

## Scope

**In scope** (only files to change, all inside `/Users/tai/.codex`):
- Remove from index: the 64 already-deleted `skills/*` paths, plus
  `agents/ROLE-CONTRACT.md`, plus `.github/workflows/skill-validate.yml`
  (then `rmdir .github/workflows .github`).
- Edit `AGENTS.md` workbench items 1-3 only.
- Edit `README.md` "Start here" list only.
- Edit `.gitignore` dead negations only.
- One commit. No push.

**Out of scope** (do NOT touch):
- All runtime state: `sessions/`, `archived_sessions/`, `*.sqlite*`,
  `packages/`, `logs*/`, `cache/`, `.tmp/`, `memories/`, `computer-use/`.
- `skills/.system/` (Codex-managed runtime), `WORKFLOW.md`,
  `agents/templates/` (both untracked), `agents/*.toml` content.
- `~/.agents/` files, `~/.config/opencode/`, `~/.claude/`.
- Push, remote changes, GitHub repo archive or delete.

## Steps

### Step 1: Record the deletions in the index

```bash
cd /Users/tai/.codex
git rm -q skills/agent-creator skills/agents-md skills/athena-review skills/harness-worker skills/issue-execution skills/skill-creator agents/ROLE-CONTRACT.md .github/workflows/skill-validate.yml
rmdir .github/workflows .github
```

**Verify**: `git status --porcelain | grep -c '^ D'` → `0`; `ls .github`
→ exit 1 (gone).

### Step 2: Rewrite the AGENTS.md workbench items 1-3

Replace lines 19-21 (quoted in Current state) with exactly:

```text
1. When the task needs a bounded role, read the matching adapter config in `agents/` (`prometheus.toml`, `franky.toml`, `athena.toml`). Do not invent or merge roles.
2. Select exactly one parent role and workflow. Bounded leaf adapters serve under it. Do not cross role boundaries or protected scopes. Changes to role policy require explicit human approval.
3. Delegate only bounded steps within the selected role's boundaries. Conflicts in role, scope, plan, or worktree state are stop-and-escalate conditions.
```

Change no other line.

**Verify**: `grep -c 'ROLE-CONTRACT' AGENTS.md` → `0` (exit 1);
`wc -l AGENTS.md` → `72`.

### Step 3: Fix the README "Start here" list

Replace items 2-4 (quoted in Current state) with exactly:

```text
2. [`agents/`](agents/) — bounded role adapter configs (`prometheus.toml`,
   `franky.toml`, `athena.toml`).
```

Keep item 1 and all other lines.

**Verify**: every `](...)` target in README.md resolves to an existing
path.

### Step 4: Prune dead .gitignore negations

Delete these lines: `!agents/ROLE-CONTRACT.md` and the whole skills block
(`!skills/`, `!skills/skill-creator/`, `!skills/skill-creator/**`,
`!skills/agent-creator/`, `!skills/agent-creator/**`,
`!skills/issue-execution/`, `!skills/issue-execution/**`,
`!skills/harness-worker/`, `!skills/harness-worker/**`,
`!skills/athena-review/`, `!skills/athena-review/**`,
`!skills/agents-md/`, `!skills/agents-md/**`). Keep `!agents/` and
`!agents/*.toml`. Keep the `skills/**/AGENTS.md` guard line.

**Verify**: `git check-ignore skills/agent-creator/SKILL.md` → exit 0
(still ignored); `git check-ignore agents/prometheus.toml` → exit 1
(still tracked-eligible).

### Step 5: Commit without pushing

```bash
cd /Users/tai/.codex
git status --porcelain
git commit -m "chore: drop dead skills index, role contract, CI; keep toml adapters"
```

**Verify**: `git status --porcelain` → empty; `git ls-files | wc -l`
→ `6`; `git log --oneline -1` shows the new commit on top of `e7c5b71`.
Do NOT push.

## Test plan

No test suite ships with this repo. Verification is the machine checks
above plus one read-through: open the final `AGENTS.md` workbench section
and confirm it names only files that exist (`agents/*.toml`).

## Done criteria

Machine-checkable. ALL must hold:

- [ ] `git -C /Users/tai/.codex ls-files | wc -l` → `6`
- [ ] `git -C /Users/tai/.codex status --porcelain` → empty
- [ ] `git -C /Users/tai/.codex grep -rn 'ROLE-CONTRACT' -- .` → exit 1
- [ ] `wc -l /Users/tai/.codex/AGENTS.md` → `72`
- [ ] Every README link target exists
- [ ] No push performed (`git status -sb` shows `ahead 1` at most, no
      remote contact needed to verify — do not run fetch/push)
- [ ] `~/.agents/plans/README.md` row 006 updated

## STOP conditions

Stop and report back (do not improvise) if:

- The drift check fails (AGENTS.md changed since `e7c5b71`, deletion
  count is not 64).
- Any file listed as deleted-on-disk reappears (someone restored it —
  reconcile instead of re-deleting).
- `agents/*.toml` files differ from what Step 1 saw (they are keep-as-is;
  unexpected edits need operator review, not silent inclusion).
- A push, remote change, or GitHub archive/delete is requested without a
  separate explicit authorization.

## Maintenance notes

- For the reviewer: the deletions are already reality on disk; this commit
  only makes the index honest. Nothing executable is removed.
- `agents/*.toml` stay as opaque adapter configs; future role-policy
  changes need operator approval per AGENTS.md item 2.
- If CI is ever wanted back, retarget it at `~/.agents` skills via
  `quick_validate.py` instead of reviving `.github/` here.
- The operator's standing rule stands: plans touching
  `~/.codex/AGENTS.md` ask first.
