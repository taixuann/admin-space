"""Tests for Bridge CLI interface."""
import unittest
import tempfile
import shutil
import sys
from io import StringIO
from pathlib import Path
import yaml

from cli import build_parser, main as cli_main


class TestCLI(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.gh_path = Path(self.test_dir) / "github-track.yaml"
        self.drive_path = Path(self.test_dir) / "drive-track.yaml"
        self.log_dir = Path(self.test_dir) / "logs"
        self.log_dir.mkdir()

        # Minimal configs
        with open(self.gh_path, "w", encoding="utf-8") as f:
            yaml.dump({
                "version": 1,
                "workspaces": [
                    {
                        "id": "my-tool",
                        "name": "My Tool",
                        "path": self.test_dir,
                        "default_branch": "main",
                        "tracked": True,
                    }
                ]
            }, f)

        with open(self.drive_path, "w", encoding="utf-8") as f:
            yaml.dump({
                "version": 1,
                "profiles": [
                    {
                        "id": "my-drive",
                        "name": "My Drive",
                        "source_path": self.test_dir,
                        "remote_target": "gdrive:my-drive/",
                        "exclude_patterns": ".git",
                        "enabled": True,
                    }
                ]
            }, f)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_parser_help(self):
        parser = build_parser()
        with self.assertRaises(SystemExit) as cm:
            parser.parse_args(["--help"])
        self.assertEqual(cm.exception.code, 0)

    def test_cli_status(self):
        out = StringIO()
        code = cli_main(
            ["status"],
            gh_config_path=self.gh_path,
            drive_config_path=self.drive_path,
            log_dir=self.log_dir,
            stdout=out,
        )
        self.assertEqual(code, 0)
        output = out.getvalue()
        self.assertIn("My Tool", output)
        self.assertIn("My Drive", output)

    def test_cli_track_toggle(self):
        out = StringIO()
        code = cli_main(
            ["track", "github", "my-tool", "--disable"],
            gh_config_path=self.gh_path,
            drive_config_path=self.drive_path,
            log_dir=self.log_dir,
            stdout=out,
        )
        self.assertEqual(code, 0)
        with open(self.gh_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        self.assertFalse(data["workspaces"][0]["tracked"])

    def test_cli_sync_github_dry_run(self):
        out = StringIO()
        code = cli_main(
            ["sync", "github", "--dry-run"],
            gh_config_path=self.gh_path,
            drive_config_path=self.drive_path,
            log_dir=self.log_dir,
            stdout=out,
        )
        self.assertEqual(code, 0)
        self.assertIn("Dry Run", out.getvalue())


if __name__ == "__main__":
    unittest.main()
