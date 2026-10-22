"""Tests for Bridge Google Drive Engine (1:1 mirror sync, exclude rules, git gatekeeper)."""
import unittest
import tempfile
import shutil
import subprocess
from pathlib import Path

from backend.drive_engine import (
    build_rclone_exclude_flags,
    check_drive_gatekeeper,
    sync_drive_profile,
    check_drive_diff,
)


class TestDriveEngine(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.source_dir = Path(self.test_dir) / "source"
        self.source_dir.mkdir()
        self.log_file = Path(self.test_dir) / "drive-sync.log"

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_build_rclone_exclude_flags(self):
        excludes = ".git, .venv, node_modules, .DS_Store, subfolder/*"
        flags = build_rclone_exclude_flags(excludes)
        # Should include .git/**
        self.assertIn("--exclude", flags)
        self.assertIn(".git/**", flags)
        self.assertIn(".venv/**", flags)
        self.assertIn("node_modules/**", flags)
        self.assertIn(".DS_Store", flags)

    def test_check_drive_gatekeeper_clean(self):
        # Create git repo that is clean
        subprocess.run(["git", "init"], cwd=str(self.source_dir), check=True, capture_output=True)
        subprocess.run(["git", "config", "user.name", "Test"], cwd=str(self.source_dir), check=True, capture_output=True)
        subprocess.run(["git", "config", "user.email", "test@test.com"], cwd=str(self.source_dir), check=True, capture_output=True)
        (self.source_dir / "file.txt").write_text("hello")
        subprocess.run(["git", "add", "."], cwd=str(self.source_dir), check=True, capture_output=True)
        subprocess.run(["git", "commit", "-m", "init"], cwd=str(self.source_dir), check=True, capture_output=True)

        is_clean, uncommitted_count = check_drive_gatekeeper(str(self.source_dir))
        self.assertTrue(is_clean)
        self.assertEqual(uncommitted_count, 0)

    def test_check_drive_gatekeeper_dirty(self):
        subprocess.run(["git", "init"], cwd=str(self.source_dir), check=True, capture_output=True)
        (self.source_dir / "dirty.txt").write_text("changes")

        is_clean, uncommitted_count = check_drive_gatekeeper(str(self.source_dir))
        self.assertFalse(is_clean)
        self.assertGreater(uncommitted_count, 0)

    def test_sync_blocked_by_dirty_gatekeeper(self):
        subprocess.run(["git", "init"], cwd=str(self.source_dir), check=True, capture_output=True)
        (self.source_dir / "dirty.txt").write_text("uncommitted")

        profile = {
            "id": "test-sync",
            "name": "Test Sync",
            "source_path": str(self.source_dir),
            "remote_target": "gdrive:test-target/",
            "exclude_patterns": ".git",
            "enabled": True,
        }

        # Should be blocked when auto_commit is False and not forced
        res = sync_drive_profile(profile, dry_run=True, force=False, auto_commit=False, log_path=self.log_file)
        self.assertEqual(res["status"], "blocked_by_git")
        self.assertFalse(res["success"])
        self.assertIn("Git commit required", res["error"])

        # Should be allowed when forced
        res_forced = sync_drive_profile(profile, dry_run=True, force=True, auto_commit=False, log_path=self.log_file)
        self.assertEqual(res_forced["status"], "dry_run")
        self.assertTrue(res_forced["success"])

    def test_sync_auto_commit_when_dirty(self):
        subprocess.run(["git", "init"], cwd=str(self.source_dir), check=True, capture_output=True)
        subprocess.run(["git", "config", "user.name", "Test"], cwd=str(self.source_dir), check=True, capture_output=True)
        subprocess.run(["git", "config", "user.email", "test@test.com"], cwd=str(self.source_dir), check=True, capture_output=True)
        (self.source_dir / "dirty.txt").write_text("changes to auto commit")

        profile = {
            "id": "test-sync",
            "name": "Test Sync",
            "source_path": str(self.source_dir),
            "remote_target": "gdrive:test-target/",
            "exclude_patterns": ".git",
            "enabled": True,
        }

        # Dry run with auto_commit=True
        res_dry = sync_drive_profile(profile, dry_run=True, auto_commit=True, date_str="2026-10-18", log_path=self.log_file)
        self.assertTrue(res_dry["would_commit"])
        self.assertEqual(res_dry["commit_message"], "automation: 2026-10-18 commit automatically")

        # Live run with auto_commit=True
        res_live = sync_drive_profile(profile, dry_run=True, auto_commit=True, date_str="2026-10-18", log_path=self.log_file)
        self.assertTrue(res_live["would_commit"])


if __name__ == "__main__":
    unittest.main()
