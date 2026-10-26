"""Tests for merged-branch pruning. Each test uses a temporary git repo."""
import os
import subprocess
import sys
import tempfile
import unittest

BACKEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend"))
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from branches_cleaner import prune_merged_branches


def git(repo, *args):
    return subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True, check=True).stdout


def commit(repo, name):
    with open(os.path.join(repo, name), "w") as f:
        f.write(name)
    git(repo, "add", name)
    git(repo, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-m", name)


def branches(repo):
    return set(git(repo, "for-each-ref", "--format=%(refname:short)", "refs/heads").split())


class PruneTestCase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.repo = self._tmp.name
        git(self.repo, "init", "-b", "master")
        commit(self.repo, "base.txt")

    def tearDown(self):
        self._tmp.cleanup()

    def make_merged_branch(self, name):
        git(self.repo, "branch", name)  # points at master tip: merged

    def make_unmerged_branch(self, name):
        git(self.repo, "checkout", "-q", "-b", name)
        commit(self.repo, name.replace("/", "_") + ".txt")
        git(self.repo, "checkout", "-q", "master")


class TestPruneMergedBranches(PruneTestCase):
    def test_deletes_merged_branch_keeps_unmerged(self):
        self.make_merged_branch("a/merged")
        self.make_unmerged_branch("b/unmerged")

        res = prune_merged_branches(repo_dir=self.repo, base="master")

        self.assertTrue(res["success"])
        self.assertEqual(res["deleted"], ["a/merged"])
        self.assertEqual(branches(self.repo), {"master", "b/unmerged"})

    def test_never_deletes_base_or_current(self):
        self.make_merged_branch("c/current")
        git(self.repo, "checkout", "-q", "c/current")

        res = prune_merged_branches(repo_dir=self.repo, base="master")

        self.assertTrue(res["success"])
        self.assertEqual(res["deleted"], [])
        self.assertEqual(res["skipped"]["c/current"], "current")
        self.assertEqual(branches(self.repo), {"master", "c/current"})

    def test_skips_branch_checked_out_in_worktree(self):
        self.make_merged_branch("d/wt")
        wt = os.path.join(self.repo + "-wt")
        self.addCleanup(lambda: __import__("shutil").rmtree(wt, ignore_errors=True))
        git(self.repo, "worktree", "add", "-q", wt, "d/wt")

        res = prune_merged_branches(repo_dir=self.repo, base="master")

        self.assertTrue(res["success"])
        self.assertEqual(res["skipped"]["d/wt"], "worktree")
        self.assertIn("d/wt", branches(self.repo))

    def test_dry_run_deletes_nothing(self):
        self.make_merged_branch("a/merged")

        res = prune_merged_branches(repo_dir=self.repo, base="master", dry_run=True)

        self.assertTrue(res["success"])
        self.assertEqual(res["deleted"], ["a/merged"])
        self.assertIn("a/merged", branches(self.repo))

    def test_missing_base_fails_safely(self):
        self.make_merged_branch("a/merged")

        res = prune_merged_branches(repo_dir=self.repo, base="nope")

        self.assertFalse(res["success"])
        self.assertEqual(res["deleted"], [])
        self.assertTrue(res["output"])
        self.assertIn("a/merged", branches(self.repo))

    def test_detached_head_does_not_crash(self):
        self.make_merged_branch("a/merged")
        git(self.repo, "checkout", "-q", "--detach")

        res = prune_merged_branches(repo_dir=self.repo, base="master")

        self.assertTrue(res["success"])
        self.assertEqual(res["deleted"], ["a/merged"])


class TestSquashMergedBranches(PruneTestCase):
    def make_squash_branch(self, name, files):
        """Branch with several commits, squashed into master as one commit."""
        git(self.repo, "checkout", "-q", "-b", name)
        for f in files:
            commit(self.repo, f)
        git(self.repo, "checkout", "-q", "master")
        git(self.repo, "merge", "-q", "--squash", name)
        git(self.repo, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "-m", "squash " + name)

    def test_deletes_squash_merged_multi_commit_branch(self):
        self.make_squash_branch("s/squash", ["one.txt", "two.txt"])
        self.assertIn("s/squash", branches(self.repo))

        res = prune_merged_branches(repo_dir=self.repo, base="master")

        self.assertTrue(res["success"])
        self.assertEqual(res["deleted"], ["s/squash"])
        self.assertEqual(branches(self.repo), {"master"})

    def test_keeps_unmerged_work_next_to_squash_branch(self):
        self.make_squash_branch("s/squash", ["one.txt"])
        self.make_unmerged_branch("s/unmerged")

        res = prune_merged_branches(repo_dir=self.repo, base="master")

        self.assertEqual(res["deleted"], ["s/squash"])
        self.assertEqual(branches(self.repo), {"master", "s/unmerged"})

    def test_keeps_squash_branch_when_master_changed_same_file_later(self):
        git(self.repo, "checkout", "-q", "-b", "s/later")
        with open(os.path.join(self.repo, "shared.txt"), "w") as f:
            f.write("branch")
        git(self.repo, "add", "shared.txt")
        git(self.repo, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "-m", "b")
        git(self.repo, "checkout", "-q", "master")
        git(self.repo, "merge", "-q", "--squash", "s/later")
        git(self.repo, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "-m", "squash")
        with open(os.path.join(self.repo, "shared.txt"), "w") as f:
            f.write("master again")
        git(self.repo, "add", "shared.txt")
        git(self.repo, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "-m", "later")

        res = prune_merged_branches(repo_dir=self.repo, base="master")

        self.assertTrue(res["success"])
        self.assertEqual(res["deleted"], [])
        self.assertIn("s/later", branches(self.repo))

    def test_dry_run_lists_squash_merged_without_deleting(self):
        self.make_squash_branch("s/squash", ["one.txt"])

        res = prune_merged_branches(repo_dir=self.repo, base="master", dry_run=True)

        self.assertEqual(res["deleted"], ["s/squash"])
        self.assertIn("s/squash", branches(self.repo))

    def test_squash_branch_checked_out_in_worktree_is_skipped(self):
        self.make_squash_branch("s/wt", ["one.txt"])
        wt = self.repo + "-wt"
        self.addCleanup(lambda: __import__("shutil").rmtree(wt, ignore_errors=True))
        git(self.repo, "worktree", "add", "-q", wt, "s/wt")

        res = prune_merged_branches(repo_dir=self.repo, base="master")

        self.assertEqual(res["skipped"]["s/wt"], "worktree")
        self.assertIn("s/wt", branches(self.repo))


if __name__ == "__main__":
    unittest.main()
