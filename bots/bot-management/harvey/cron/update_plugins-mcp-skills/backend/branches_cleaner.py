"""Merged-branch pruning for the ~/.agents repository.

Deletes local branches already merged into the base branch. Never merges,
never touches remotes, never force-deletes (git branch -d only).
"""
from __future__ import annotations

import os
import subprocess
from typing import TypedDict


class BranchPruneResult(TypedDict):
    success: bool
    deleted: list[str]
    skipped: dict[str, str]  # branch -> reason ("current", "worktree", "protected")
    output: str


DEFAULT_REPO_DIR = os.path.expanduser("~/.agents")
PROTECTED_BRANCHES = {"master", "main"}


def _git(repo_dir: str, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", "-C", repo_dir, *args],
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )


def _is_squash_merged(repo_dir: str, base: str, branch: str) -> bool:
    """True when merging branch into base would leave base's tree unchanged.

    Squash merges never make the branch an ancestor of base, so --merged misses
    them. A clean merge whose tree equals base's tree proves the branch's content
    is already in base. Conflicts, errors (including git < 2.38), and any tree
    mismatch keep the branch.
    """
    merge = _git(repo_dir, "merge-tree", "--write-tree", base, branch)
    if merge.returncode != 0:
        return False
    merged_tree = merge.stdout.split()[0] if merge.stdout.split() else ""
    base_tree = _git(repo_dir, "rev-parse", "--verify", "--quiet", f"{base}^{{tree}}")
    return base_tree.returncode == 0 and merged_tree == base_tree.stdout.strip()


def prune_merged_branches(
    repo_dir: str = DEFAULT_REPO_DIR,
    base: str = "master",
    dry_run: bool = False,
) -> BranchPruneResult:
    """Deletes local branches merged into base, including squash-merged ones.

    Regular merges use `git branch -d`. Squash-merged branches are proven by tree
    equality and removed with `-D`, since git refuses `-d` for them.
    Dry run lists them without deleting.
    """
    result: BranchPruneResult = {"success": False, "deleted": [], "skipped": {}, "output": ""}

    def fail(message: str) -> BranchPruneResult:
        result["output"] = message
        return result

    verify = _git(repo_dir, "rev-parse", "--verify", "--quiet", f"{base}^{{commit}}")
    if verify.returncode != 0:
        return fail(f"base branch not found: {base}")

    # Full refnames: a detached HEAD appears as a pseudo-entry without refs/heads/.
    merged = _git(repo_dir, "branch", "--merged", base, "--format=%(refname)")
    if merged.returncode != 0:
        return fail(f"git branch --merged failed: {merged.stderr.strip()}")
    merged_names = [
        line[len("refs/heads/"):]
        for line in merged.stdout.splitlines()
        if line.startswith("refs/heads/")
    ]

    current = _git(repo_dir, "symbolic-ref", "--short", "-q", "HEAD").stdout.strip()

    worktree_list = _git(repo_dir, "worktree", "list", "--porcelain")
    if worktree_list.returncode != 0:
        return fail(f"git worktree list failed: {worktree_list.stderr.strip()}")
    in_worktree = {
        line[len("branch refs/heads/"):]
        for line in worktree_list.stdout.splitlines()
        if line.startswith("branch refs/heads/")
    }

    for name in merged_names:
        if name in PROTECTED_BRANCHES or name == base:
            result["skipped"][name] = "protected"
        elif name == current:
            result["skipped"][name] = "current"
        elif name in in_worktree:
            result["skipped"][name] = "worktree"
        elif dry_run:
            result["deleted"].append(name)
        else:
            delete = _git(repo_dir, "branch", "-d", name)
            if delete.returncode != 0:
                return fail(f"git branch -d {name} failed: {delete.stderr.strip()}")
            result["deleted"].append(name)

    unmerged = _git(repo_dir, "branch", "--no-merged", base, "--format=%(refname)")
    if unmerged.returncode != 0:
        return fail(f"git branch --no-merged failed: {unmerged.stderr.strip()}")
    for line in unmerged.stdout.splitlines():
        if not line.startswith("refs/heads/"):
            continue
        name = line[len("refs/heads/"):]
        if name in PROTECTED_BRANCHES or name == base:
            result["skipped"][name] = "protected"
        elif name == current:
            result["skipped"][name] = "current"
        elif name in in_worktree:
            result["skipped"][name] = "worktree"
        elif not _is_squash_merged(repo_dir, base, name):
            continue
        elif dry_run:
            result["deleted"].append(name)
        else:
            delete = _git(repo_dir, "branch", "-D", name)
            if delete.returncode != 0:
                return fail(f"git branch -D {name} failed: {delete.stderr.strip()}")
            result["deleted"].append(name)

    result["success"] = True
    return result
