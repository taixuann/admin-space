"""Tests for Bridge Git Automation Engine (Automated commit & push for tracked repos)."""
import unittest
import tempfile
import shutil
import subprocess
from pathlib import Path
from datetime import datetime

from backend.git_engine import (
    sync_tracked_repo,
    sync_all_tracked_repos,
    format_automation_commit_msg,
    safe_pull_repo,
    pull_all_repos,
)


def run_cmd(args, cwd):
    res = subprocess.run(args, cwd=cwd, capture_output=True, text=True, check=True)
    return res.stdout.strip()


class TestGitEngine(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.repo_dir = Path(self.test_dir) / "test-repo"
        self.repo_dir.mkdir()
        self.log_file = Path(self.test_dir) / "github-sync.log"

        # Initialize local git repo
        run_cmd(["git", "init"], cwd=str(self.repo_dir))
        run_cmd(["git", "config", "user.name", "Test User"], cwd=str(self.repo_dir))
        run_cmd(["git", "config", "user.email", "test@example.com"], cwd=str(self.repo_dir))

        # Initial commit on main
        init_file = self.repo_dir / "README.md"
        init_file.write_text("# Test Repo\n")
        run_cmd(["git", "add", "README.md"], cwd=str(self.repo_dir))
        run_cmd(["git", "commit", "-m", "chore: initial commit"], cwd=str(self.repo_dir))
        run_cmd(["git", "branch", "-M", "main"], cwd=str(self.repo_dir))

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_format_automation_commit_msg(self):
        date_str = "2026-10-18"
        msg = format_automation_commit_msg(date_str)
        self.assertEqual(msg, "automation: 2026-10-18 commit automatically")

    def test_sync_tracked_repo_clean(self):
        ws = {
            "id": "test-repo",
            "name": "Test Repo",
            "path": str(self.repo_dir),
            "default_branch": "main",
            "tracked": True,
        }
        res = sync_tracked_repo(ws, dry_run=False, log_path=self.log_file)
        self.assertEqual(res["status"], "clean")
        self.assertFalse(res["committed"])
        self.assertFalse(res["pushed"])

    def test_sync_tracked_repo_uncommitted_dry_run(self):
        # Create uncommitted dirty file
        (self.repo_dir / "notes.txt").write_text("work in progress\n")
        ws = {
            "id": "test-repo",
            "name": "Test Repo",
            "path": str(self.repo_dir),
            "default_branch": "main",
            "tracked": True,
        }
        res = sync_tracked_repo(ws, dry_run=True, log_path=self.log_file)
        self.assertEqual(res["status"], "dry_run")
        self.assertTrue(res["would_commit"])
        self.assertIn("automation:", res["commit_message"])
        # Verify nothing actually committed
        status = run_cmd(["git", "status", "--porcelain"], cwd=str(self.repo_dir))
        self.assertIn("notes.txt", status)

    def test_sync_tracked_repo_uncommitted_actual_commit(self):
        # Create uncommitted dirty file
        (self.repo_dir / "data.csv").write_text("col1,col2\n1,2\n")
        ws = {
            "id": "test-repo",
            "name": "Test Repo",
            "path": str(self.repo_dir),
            "default_branch": "main",
            "tracked": True,
        }
        res = sync_tracked_repo(ws, dry_run=False, log_path=self.log_file, date_str="2026-10-18")
        self.assertTrue(res["committed"])
        self.assertEqual(res["commit_message"], "automation: 2026-10-18 commit automatically")

        # Verify git status is now clean
        status = run_cmd(["git", "status", "--porcelain"], cwd=str(self.repo_dir))
        self.assertEqual(status, "")

        # Verify last commit message
        last_log = run_cmd(["git", "log", "-1", "--format=%s"], cwd=str(self.repo_dir))
        self.assertEqual(last_log, "automation: 2026-10-18 commit automatically")

        # Verify log file written
        log_content = self.log_file.read_text()
        self.assertIn("automation: 2026-10-18 commit automatically", log_content)

    def test_sync_all_skips_untracked_repos(self):
        (self.repo_dir / "untracked_work.txt").write_text("do not touch\n")
        workspaces = [
            {
                "id": "test-repo",
                "name": "Test Repo",
                "path": str(self.repo_dir),
                "default_branch": "main",
                "tracked": False,  # UNTRACKED!
            }
        ]
        results = sync_all_tracked_repos(workspaces=workspaces, log_path=self.log_file)
        self.assertEqual(len(results), 0)
        # Verify file is still untouched and not committed
        status = run_cmd(["git", "status", "--porcelain"], cwd=str(self.repo_dir))
        self.assertIn("untracked_work.txt", status)

    def test_safe_pull_repo_dirty_blocked(self):
        # Create dirty uncommitted file
        (self.repo_dir / "dirty_local.txt").write_text("uncommitted edits\n")
        ws = {
            "id": "test-repo",
            "name": "Test Repo",
            "path": str(self.repo_dir),
            "default_branch": "main",
        }
        res = safe_pull_repo(ws, dry_run=False, log_path=self.log_file)
        self.assertEqual(res["status"], "dirty_blocked")
        self.assertIn("uncommitted changes", res["error"])
        self.assertEqual(res["uncommitted_count"], 1)

    def test_safe_pull_repo_fast_forward_success(self):
        # Set up a remote bare repo with main as default branch
        remote_bare = Path(self.test_dir) / "remote.git"
        run_cmd(["git", "init", "--bare", "--initial-branch=main", str(remote_bare)], cwd=self.test_dir)
        run_cmd(["git", "remote", "add", "origin", str(remote_bare)], cwd=str(self.repo_dir))
        run_cmd(["git", "push", "-u", "origin", "main"], cwd=str(self.repo_dir))

        # Clone to second workspace and push a commit
        clone_dir = Path(self.test_dir) / "clone-worker"
        run_cmd(["git", "clone", str(remote_bare), str(clone_dir)], cwd=self.test_dir)
        run_cmd(["git", "config", "user.name", "Worker"], cwd=str(clone_dir))
        run_cmd(["git", "config", "user.email", "worker@example.com"], cwd=str(clone_dir))
        (clone_dir / "wiki-page.md").write_text("# New Wiki Topic\n")
        run_cmd(["git", "add", "wiki-page.md"], cwd=str(clone_dir))
        run_cmd(["git", "commit", "-m", "feat: new wiki article"], cwd=str(clone_dir))
        run_cmd(["git", "push", "origin", "main"], cwd=str(clone_dir))

        # Test local safe pull fast-forwards cleanly
        ws = {
            "id": "test-repo",
            "name": "Test Repo",
            "path": str(self.repo_dir),
            "default_branch": "main",
        }
        res = safe_pull_repo(ws, dry_run=False, log_path=self.log_file)
        self.assertEqual(res["status"], "pulled")
        self.assertTrue(res["pulled"])
        self.assertEqual(res["behind"], 1)
        self.assertTrue((self.repo_dir / "wiki-page.md").exists())

    def test_safe_pull_repo_diverged_stops_conflict(self):
        # Set up a remote bare repo with main as default branch
        remote_bare = Path(self.test_dir) / "remote.git"
        run_cmd(["git", "init", "--bare", "--initial-branch=main", str(remote_bare)], cwd=self.test_dir)
        run_cmd(["git", "remote", "add", "origin", str(remote_bare)], cwd=str(self.repo_dir))
        run_cmd(["git", "push", "-u", "origin", "main"], cwd=str(self.repo_dir))

        # Worker pushes commit to remote
        clone_dir = Path(self.test_dir) / "clone-worker"
        run_cmd(["git", "clone", str(remote_bare), str(clone_dir)], cwd=self.test_dir)
        run_cmd(["git", "config", "user.name", "Worker"], cwd=str(clone_dir))
        run_cmd(["git", "config", "user.email", "worker@example.com"], cwd=str(clone_dir))
        (clone_dir / "worker.txt").write_text("worker edit\n")
        run_cmd(["git", "add", "worker.txt"], cwd=str(clone_dir))
        run_cmd(["git", "commit", "-m", "worker commit"], cwd=str(clone_dir))
        run_cmd(["git", "push", "origin", "main"], cwd=str(clone_dir))

        # Local makes a distinct local commit (without pushing)
        (self.repo_dir / "local.txt").write_text("local edit\n")
        run_cmd(["git", "add", "local.txt"], cwd=str(self.repo_dir))
        run_cmd(["git", "commit", "-m", "local commit"], cwd=str(self.repo_dir))

        # Test safe pull halts with diverged status
        ws = {
            "id": "test-repo",
            "name": "Test Repo",
            "path": str(self.repo_dir),
            "default_branch": "main",
        }
        res = safe_pull_repo(ws, dry_run=False, log_path=self.log_file)
        self.assertEqual(res["status"], "diverged")
        self.assertFalse(res["pulled"])
        self.assertIn("Branch diverged", res["error"])


if __name__ == "__main__":
    unittest.main()
