```yaml
requester: secretary
space: ~/.agents
base: master
branch: automation/update_plugins-mcp-skills
scope: [automation/update_plugins-mcp-skills/backend/, automation/update_plugins-mcp-skills/tests/, automation/update_plugins-mcp-skills/README.md]
checks:
  - /opt/miniconda3/envs/core/bin/python3 -m unittest discover -s automation/update_plugins-mcp-skills/tests -v
  - plutil -lint automation/update_plugins-mcp-skills/launchd.plist
  - python3 ~/.agents/skills/launchd-automation/scripts/verify_automation.py "/Users/tai/.agents/automation/update_plugins-mcp-skills" --static --report-root "/Users/tai/.agents/automation/update_plugins-mcp-skills/logs"
  - /opt/miniconda3/envs/core/bin/python3 automation/update_plugins-mcp-skills/backend/main.py --dry-run --report-root $(mktemp -d)   # exit 0, details contains branch_prune
  - git status shows no changes outside scope
engine: opencode
report: kanban card comment + kanban_complete summary to Secretary, including the list of branches the job WOULD delete today
```

# Prune merged branches (new phase in the daily Admin maintenance job) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans. Steps use checkbox syntax.

**Goal:** The existing 03:00 job also deletes local branches of `~/.agents` that are already merged into `master`. It never merges anything.

**Architecture:** One new module `backend/branches_cleaner.py` with one function, called as Phase 5 from `run_maintenance` in `backend/main.py`, reusing the job's lock, run records, `latest-result.json`, and `report_incident`. No new launchd label, no plist change: the installed plist already runs this source path, so a merge to `master` takes effect at the next 03:00 run.

**Tech Stack:** Python 3 stdlib (`subprocess`, `unittest`, `tempfile`), git CLI.

**Spec:** Tai, 2026-10-25: delete merged branches only; merging stays with Tai. Placement: extend `update_plugins-mcp-skills` (Tai's suggestion; reuse of lock/report outweighs the mild responsibility mismatch, README description is updated).

## Global Constraints

- Delete only local branches, with `git branch -d` (safe delete, refuses unmerged). Never `-D`, never touch remotes, never merge, push, or rebase.
- Base branch is `master` (the repo's integration branch; `main` too if it ever exists, never deleted).
- Never delete: the base branch, `master`, `main`, the currently checked-out branch, any branch checked out in any worktree (`git worktree list --porcelain`).
- Repo path is `/Users/tai/.agents`, passed as a parameter so tests use temp repos. Tests never touch the live repo or live report root.
- Match module style of `plugins_updater.py` (TypedDict result, `subprocess.run` with timeout, no raising on git failure).
- Do not edit `launchd.plist` or `AGENTS.md` (protected / unchanged schedule).

## Review Focus

- Detached HEAD in the repo: must not crash; no branch is "current".
- Branch checked out in a linked worktree (exists today: `admin-native-opencode-execution-stage-1`): kept and reported as skipped.
- Squash-merged or rebased branches are not detected as merged: left alone (non-goal), never force-deleted.
- Branch names with slashes (`executor/x`, `automation/y`): deleted correctly.
- Base branch missing or git failure: result `success=False`, nothing deleted, incident reported, job outcome `failed` like other phases.
- Dry-run: lists would-delete branches, deletes nothing.

### Task 1: `prune_merged_branches`

**Files:**
- Create: `automation/update_plugins-mcp-skills/backend/branches_cleaner.py`
- Test: `automation/update_plugins-mcp-skills/tests/test_branches_cleaner.py`

**Interfaces:**
- Produces:
  ```python
  class BranchPruneResult(TypedDict):
      success: bool
      deleted: list[str]
      skipped: dict[str, str]   # branch -> reason ("current", "worktree", "protected")
      output: str               # error text when success is False, else ""

  def prune_merged_branches(repo_dir: str = DEFAULT_REPO_DIR, base: str = "master", dry_run: bool = False) -> BranchPruneResult
  ```
  `DEFAULT_REPO_DIR = os.path.expanduser("~/.agents")`. With `dry_run=True`, `deleted` holds the branches that would be deleted.

- [ ] **Step 1: Write failing tests** in `tests/test_branches_cleaner.py` using a helper that builds a temp git repo (`git init -b master`, one commit) and these tests:
  - `test_deletes_merged_branch_keeps_unmerged`: branch `a/merged` merged into master and branch `b/unmerged` with an extra commit; result `deleted == ["a/merged"]`, `b/unmerged` still exists.
  - `test_never_deletes_base_or_current`: checked out on a merged branch `c/current`; it and `master` remain; `skipped["c/current"] == "current"`.
  - `test_skips_branch_checked_out_in_worktree`: merged branch `d/wt` added via `git worktree add`; it remains with `skipped["d/wt"] == "worktree"`.
  - `test_dry_run_deletes_nothing`: merged branch listed in `deleted`, still exists afterward.
  - `test_missing_base_fails_safely`: `base="nope"` gives `success False`, no branch deleted, `output` non-empty.
  - `test_detached_head_does_not_crash`: `git checkout --detach`; merged branch is deleted, `success True`.
- [ ] **Step 2: Run** `/opt/miniconda3/envs/core/bin/python3 -m unittest automation/update_plugins-mcp-skills/tests/test_branches_cleaner.py` → FAIL (module missing).
- [ ] **Step 3: Implement** `prune_merged_branches` in `branches_cleaner.py`: verify base with `git rev-parse --verify <base>`; list `git branch --merged <base> --format=%(refname:short)`; read current via `git symbolic-ref --short -q HEAD` (empty when detached); collect worktree branches from `git worktree list --porcelain` (`branch refs/heads/<name>` lines); skip as above; delete each remaining with `git branch -d <name>` (skip the call when `dry_run`). Any git failure returns `success False` with stderr text and keeps already-recorded deletions in `deleted`.
- [ ] **Step 4: Run** the test file → PASS.
- [ ] **Step 5: Commit** `feat(automation): prune merged branches helper` on the task branch.

### Task 2: Wire Phase 5 into the job and document it

**Files:**
- Modify: `automation/update_plugins-mcp-skills/backend/main.py` (import; dry-run `details`; Phase 5 after Phase 4; `all_ok`; `details`)
- Modify: `automation/update_plugins-mcp-skills/README.md` (description line and a "Phases" note that Phase 5 prunes merged local branches of `~/.agents`, never merges, skips current/worktree branches; recovery: `git reflog` / `git branch <name> <sha>`)
- Test: `automation/update_plugins-mcp-skills/tests/test_backend.py`

**Interfaces:**
- Consumes: `prune_merged_branches(repo_dir, base, dry_run) -> BranchPruneResult` from Task 1.
- Produces: `details["branch_prune"]` in `latest-result.json` (the full `BranchPruneResult`; `{"dry_run": True}` in dry-run mode).

- [ ] **Step 1: Extend `test_dry_run`** in `test_backend.py` to `assertIn("branch_prune", data["details"])`; run, expect FAIL.
- [ ] **Step 2: Implement** Phase 5 in `run_maintenance`: log start; call `prune_merged_branches()`; on failure `log_err` and `report_incident(title="[Auto-Sync] Merged-branch prune failure", error_details=..., component="Automations & Runtime")`; include `prune_res["success"]` in `all_ok`; add `"branch_prune": prune_res` to `details`. On success log the deleted and skipped branch names. Dry-run `details` gets `"branch_prune": {"dry_run": True}`.
- [ ] **Step 3: Update README** as listed above, keeping the schedule text unchanged.
- [ ] **Step 4: Run all checks** from the header; paste actual output. Also run `python3 -c` calling `prune_merged_branches(dry_run=True)` against the live repo and report the would-delete and skipped lists (nothing is deleted).
- [ ] **Step 5: Commit** `feat(automation): phase 5 prune merged branches` on the task branch, then stop for Tai's review. Do not merge, push, or deploy.
