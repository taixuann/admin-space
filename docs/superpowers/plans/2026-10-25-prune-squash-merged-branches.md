```yaml
requester: secretary
space: ~/.agents
base: master
branch: executor/prune-squash-merged
scope: [automation/update_plugins-mcp-skills/backend/branches_cleaner.py, automation/update_plugins-mcp-skills/tests/test_branches_cleaner.py, automation/update_plugins-mcp-skills/README.md]
checks:
  - /opt/miniconda3/envs/core/bin/python3 -m unittest discover -s automation/update_plugins-mcp-skills/tests -v
  - python3 ~/.agents/skills/launchd-automation/scripts/verify_automation.py "/Users/tai/.agents/automation/update_plugins-mcp-skills" --static --report-root "/Users/tai/.agents/automation/update_plugins-mcp-skills/logs"
  - live dry run of prune_merged_branches(dry_run=True) lists exactly `automation/update_plugins-mcp-skills` and `executor/supervisor-profile`, deletes nothing
  - git status shows no changes outside scope
engine: self
report: kanban card comment + kanban_complete summary to Secretary
```

# Prune squash-merged branches Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans.

**Goal:** Tai merges with squash, so `git branch --merged` never lists those branches. Phase 5 must also delete a local branch whose content is already in `master`, without ever deleting unreviewed work.

**Architecture:** Extend `prune_merged_branches` in `backend/branches_cleaner.py`. A branch not listed by `--merged` counts as squash-merged when `git merge-tree --write-tree <base> <branch>` exits 0 and prints a tree id equal to `git rev-parse <base>^{tree}`: merging it would change nothing. Delete such branches with `git branch -D` (`-d` refuses squash-merged branches); the tree proof replaces git's own check. Regular merged branches keep `-d`.

**Spec:** Tai, 2026-10-25: prefers squash-merge; the job must still clean up. Builds on [2026-10-25-prune-merged-branches.md](2026-10-25-prune-merged-branches.md) (already on master). Requires git >= 2.38 (`merge-tree --write-tree`); installed is 2.50.1.

## Global Constraints

- Same skip rules as before: never delete `master`/`main`, the base, the current branch, or a branch checked out in a worktree. Local branches only; no remote, merge, or push.
- `-D` only after the tree-equality proof. Conflict (exit 1), any other nonzero exit, or a tree mismatch means keep the branch.
- Tests use temp repos only. Do not edit `main.py`, `launchd.plist`, or `AGENTS.md`.

## Review Focus

- Squash branch whose files master later changed again: tree differs or conflicts, branch kept (false negative is acceptable).
- Branch with real unmerged work: kept.
- Multi-commit branch squashed into one commit: deleted.
- Dry-run lists squash-merged branches without deleting.
- Git too old for `--write-tree` (nonzero, usage error): branch kept, job does not fail.

### Task 1: Detect and delete squash-merged branches

**Files:**
- Modify: `automation/update_plugins-mcp-skills/backend/branches_cleaner.py`
- Test: `automation/update_plugins-mcp-skills/tests/test_branches_cleaner.py`
- Modify: `automation/update_plugins-mcp-skills/README.md` (Phase 5 note: squash detection by tree equality, `-D` after proof, recovery via `git reflog`)

**Interfaces:**
- Consumes: existing `prune_merged_branches(repo_dir, base, dry_run) -> BranchPruneResult` and its `_git` helper.
- Produces: same signature and result shape; `deleted` also includes squash-merged branches. New private helper `_is_squash_merged(repo_dir: str, base: str, branch: str) -> bool`.

- [ ] **Step 1: Write failing tests** in `test_branches_cleaner.py`:
  - `test_deletes_squash_merged_multi_commit_branch`: branch `s/squash` with two commits, squashed into master with `git merge --squash` plus commit; result `deleted == ["s/squash"]` and the branch is gone.
  - `test_keeps_unmerged_work`: branch with a commit not in master is kept (existing test may already cover; add a squash-neighbor case).
  - `test_keeps_squash_branch_when_master_changed_same_file_later`: after the squash, master edits the same file again; branch is kept.
  - `test_dry_run_lists_squash_merged_without_deleting`.
- [ ] **Step 2: Run** `/opt/miniconda3/envs/core/bin/python3 -m unittest automation/update_plugins-mcp-skills/tests/test_branches_cleaner.py` → the new tests FAIL.
- [ ] **Step 3: Implement** `_is_squash_merged` and use it in `prune_merged_branches` for branches from `git branch --no-merged <base> --format=%(refname)` that pass the skip rules; delete with `git branch -D` unless `dry_run`.
- [ ] **Step 4: Run** the full test directory → PASS; run the live dry run and report the exact list.
- [ ] **Step 5: Commit** on the task branch and stop for Tai's review. Do not merge, push, or deploy.
