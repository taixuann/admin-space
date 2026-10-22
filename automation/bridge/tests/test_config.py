"""Tests for Bridge configuration management (YAML loading, saving, updates)."""
import unittest
import tempfile
import shutil
from pathlib import Path
import yaml

from backend.config_manager import (
    load_github_config,
    save_github_config,
    load_drive_config,
    save_drive_config,
    get_tracked_workspaces,
    get_enabled_drive_profiles,
    update_workspace,
    update_drive_profile,
)


class TestConfigManager(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.gh_path = Path(self.test_dir) / "github-track.yaml"
        self.drive_path = Path(self.test_dir) / "drive-track.yaml"

        self.sample_gh = {
            "version": 1,
            "settings": {"auto_refresh_seconds": 30, "github_owner": "testuser"},
            "workspaces": [
                {
                    "id": "repo-a",
                    "name": "Repo A",
                    "category": "Tools",
                    "path": "/path/to/a",
                    "remote_repo": "testuser/repo-a",
                    "default_branch": "main",
                    "tracked": True,
                },
                {
                    "id": "repo-b",
                    "name": "Repo B",
                    "category": "Personal",
                    "path": "/path/to/b",
                    "remote_repo": "testuser/repo-b",
                    "default_branch": "main",
                    "tracked": False,
                },
            ],
        }

        self.sample_drive = {
            "version": 1,
            "settings": {"remote_prefix": "gdrive:"},
            "profiles": [
                {
                    "id": "hub-sync",
                    "name": "Hub Sync",
                    "category": "Personal",
                    "source_path": "/path/to/hub",
                    "remote_target": "gdrive:hub/",
                    "include_folders": "*",
                    "exclude_patterns": ".git, .venv",
                    "enabled": True,
                },
                {
                    "id": "inactive-sync",
                    "name": "Inactive Sync",
                    "category": "Archive",
                    "source_path": "/path/to/arch",
                    "remote_target": "gdrive:arch/",
                    "include_folders": "*",
                    "exclude_patterns": ".git",
                    "enabled": False,
                },
            ],
        }

        with open(self.gh_path, "w", encoding="utf-8") as f:
            yaml.dump(self.sample_gh, f)
        with open(self.drive_path, "w", encoding="utf-8") as f:
            yaml.dump(self.sample_drive, f)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_load_and_save_github_config(self):
        cfg = load_github_config(self.gh_path)
        self.assertEqual(cfg["version"], 1)
        self.assertEqual(len(cfg["workspaces"]), 2)

        # Update and save
        cfg["workspaces"][0]["name"] = "Updated Repo A"
        save_github_config(cfg, self.gh_path)

        reloaded = load_github_config(self.gh_path)
        self.assertEqual(reloaded["workspaces"][0]["name"], "Updated Repo A")

    def test_load_and_save_drive_config(self):
        cfg = load_drive_config(self.drive_path)
        self.assertEqual(cfg["version"], 1)
        self.assertEqual(len(cfg["profiles"]), 2)

        cfg["profiles"][0]["remote_target"] = "gdrive:custom/"
        save_drive_config(cfg, self.drive_path)

        reloaded = load_drive_config(self.drive_path)
        self.assertEqual(reloaded["profiles"][0]["remote_target"], "gdrive:custom/")

    def test_get_tracked_workspaces(self):
        tracked = get_tracked_workspaces(self.gh_path)
        self.assertEqual(len(tracked), 1)
        self.assertEqual(tracked[0]["id"], "repo-a")

    def test_get_enabled_drive_profiles(self):
        enabled = get_enabled_drive_profiles(self.drive_path)
        self.assertEqual(len(enabled), 1)
        self.assertEqual(enabled[0]["id"], "hub-sync")

    def test_update_workspace(self):
        ok = update_workspace("repo-a", {"tracked": False, "category": "Dev"}, config_path=self.gh_path)
        self.assertTrue(ok)
        reloaded = load_github_config(self.gh_path)
        ws = next(w for w in reloaded["workspaces"] if w["id"] == "repo-a")
        self.assertFalse(ws["tracked"])
        self.assertEqual(ws["category"], "Dev")

    def test_update_drive_profile(self):
        ok = update_drive_profile("hub-sync", {"exclude_patterns": ".git, node_modules"}, config_path=self.drive_path)
        self.assertTrue(ok)
        reloaded = load_drive_config(self.drive_path)
        prof = next(p for p in reloaded["profiles"] if p["id"] == "hub-sync")
        self.assertEqual(prof["exclude_patterns"], ".git, node_modules")


if __name__ == "__main__":
    unittest.main()
