# Plan 005: Fork AutoSci to your account and push the local work

> **Executor instructions**: Follow this plan step by step. Run every
> verification command and confirm the expected result before moving to the
> next step. If anything in the "STOP conditions" section occurs, stop and
> report — do not improvise. When done, update the status row for this plan
> in the index (`/Users/tai/.opencode/plan/README.md`).
>
> **Drift check (run first)**: In `/Users/tai/workspace/research-projects/autosci`,
> run `git log --oneline -1` — expect `feca5e0` on branch `autosci-codex`,
> and `git status -sb` — expect `## autosci-codex...origin/autosci-codex [ahead 3]`.
> If the branch, HEAD, or ahead-count differs, STOP and report.

## Status

- **Priority**: P1
- **Effort**: S
- **Risk**: LOW
- **Depends on**: none
- **Category**: dx / access
- **Planned at**: autosci `feca5e0`, 2026-10-02 (research-projects monorepo at `041d0456`)

## Why this matters

The `autosci/` checkout's only remote is `https://github.com/skyllwt/AutoSci.git`,
where the operator has READ permission (verified via `gh repo view`). Three
local commits on `autosci-codex` (wiki index/log updates, Obsidian monochrome
theme, Zotero integration) cannot be pushed anywhere. Every downstream step —
the quartz site (plan 006), any collaboration — needs a writable remote. The
fix is a fork under the operator's account with `skyllwt` kept as `upstream`.

## Current state

- Location: `/Users/tai/workspace/research-projects/autosci/` — a nested clone,
  ignored by the monorepo (`autosci/` in `/Users/tai/workspace/research-projects/.gitignore`).
  It is intentionally NOT tracked by research-projects; do not `git add` it there.
- `git remote -v` → single remote `origin https://github.com/skyllwt/AutoSci.git`.
- `git branch` → `* autosci-codex`; ahead 3 of `origin/autosci-codex`:
  `feca5e0`, `6138c77`, `a803692`.
- `gh` CLI is installed and authenticated (a `gh repo view` probe succeeded during
  planning). All `gh` commands below run as the operator.

## Commands you will need

| Purpose | Command | Expected on success |
|---|---|---|
| Fork | `gh repo fork skyllwt/AutoSci --clone=false` (cwd anywhere) | prints fork URL under the operator's account |
| Repoint | `git remote add upstream <skyllwt URL>` + set `origin` to fork (see steps) | `git remote -v` shows both |
| Push | `git push -u origin autosci-codex` (cwd `autosci/`) | 3 commits pushed, no rejection |
| Verify | `gh repo view <fork> --json nameWithOwner,viewerPermission` | `viewerPermission` is `ADMIN` or `WRITE` |

## Scope

**In scope** (the only places you may change):
- Remotes of `/Users/tai/workspace/research-projects/autosci/` (add `upstream`, repoint `origin`).
- The new fork `taixuann/AutoSci` (or whatever username the fork lands under — use the actual owner `gh` reports).

**Out of scope** (do NOT touch):
- `/Users/tai/workspace/research-projects/` itself — no commits, no `.gitignore` changes, do not track `autosci/`.
- Code or wiki content inside `autosci/` — push only, no edits.
- The monorepo `quartz/` submodule — handled in plan 006.

## Git workflow

- No branch creation needed; work on the existing `autosci-codex`.
- Do NOT push to `skyllwt/AutoSci` (it will fail anyway — READ permission).
- Do NOT open a PR unless the operator instructed it.

## Steps

### Step 1: Create the fork

```sh
gh repo fork skyllwt/AutoSci --clone=false
```

Record the exact fork path it prints (expected `taixuann/AutoSci` but use what
`gh` reports — if the operator's username differs, substitute everywhere below).

**Verify**: `gh repo view <fork-path> --json nameWithOwner,viewerPermission` →
permission is `ADMIN` (own fork).

### Step 2: Rewire remotes in the local clone

```sh
cd /Users/tai/workspace/research-projects/autosci
git remote rename origin upstream
git remote add origin https://github.com/<fork-path>.git
git remote -v
```

Expected: `origin` → fork, `upstream` → `skyllwt/AutoSci`. Fetch both:
`git fetch origin && git fetch upstream` (exit 0; no output required).

### Step 3: Push the local work

```sh
git push -u origin autosci-codex
```

Expected: the 3 commits (`feca5e0`, `6138c77`, `a803692`) upload cleanly.
Afterwards `git status -sb` → `## autosci-codex...origin/autosci-codex` with
no `ahead` count. If the fork already contains an `autosci-codex` branch that
diverges (e.g. someone pushed there first), STOP and report — do not force-push.

**Verify**: `git ls-remote origin autosci-codex` shows `feca5e0` as the tip.

## Test plan

No new tests — this plan is access plumbing. Verification is the `ls-remote`
tip check plus re-running the drift check (status shows in-sync, ahead 0).

## Done criteria

- [ ] A fork of AutoSci exists under the operator's account with WRITE/ADMIN permission
- [ ] Local `origin` → fork, `upstream` → `skyllwt/AutoSci`; both fetch cleanly
- [ ] `git ls-remote origin autosci-codex` tip is `feca5e0` (or the drift-checked HEAD if reconciled)
- [ ] No commits made to `/Users/tai/workspace/research-projects` itself (`git -C ... status` unchanged apart from pre-existing untracked skill dirs)
- [ ] Index status row updated

## STOP conditions

- `gh repo fork` fails (no permission to fork, SSO enforcement, rate limit) — report the message.
- The fork's `viewerPermission` is not WRITE/ADMIN.
- Push is rejected for any reason — report, do not `--force`.
- The drift check mismatches (different HEAD/branch/ahead-count).

## Maintenance notes

- Future autosci work branches off `autosci-codex` (or `main`) and pushes to the
  fork; `upstream` is pull-only (sync via `git fetch upstream` + merge when needed).
- Plan 006 builds on this: the quartz site work happens in the fork, not in `skyllwt`.
- Reviewer focus: confirm no push was ever attempted against `skyllwt` (check `git reflog` dates/refs if in doubt).
