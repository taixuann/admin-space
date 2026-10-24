"""Tests for update_plugins-mcp-skills backend."""
import fcntl
import json
import os
import sys
import tempfile
import time
import unittest

BACKEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend"))
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from main import cleanup_old_records, run_maintenance
from skills_updater import detect_and_report_failures, reconcile_skill_lock


class TestUpdatePluginsMcpSkills(unittest.TestCase):
    def test_dry_run(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            exit_code = run_maintenance(report_root=tmpdir, dry_run=True)
            self.assertEqual(exit_code, 0)

            result_file = os.path.join(tmpdir, "latest-result.json")
            self.assertTrue(os.path.isfile(result_file))

            with open(result_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            self.assertEqual(data["outcome"], "cached")
            self.assertEqual(data["exit_code"], 0)
            self.assertEqual(data["label"], "com.tai.update-plugins-mcp-skills")
            self.assertIn("superpowers", data["details"])

    def test_lock_skips_concurrent(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            lock_file = os.path.join(tmpdir, ".lock")
            lock_fd = open(lock_file, "w")
            fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)

            try:
                exit_code = run_maintenance(report_root=tmpdir, dry_run=True)
                self.assertEqual(exit_code, 0)

                result_file = os.path.join(tmpdir, "latest-result.json")
                self.assertTrue(os.path.isfile(result_file))

                with open(result_file, "r", encoding="utf-8") as f:
                    data = json.load(f)

                self.assertEqual(data["outcome"], "skipped_locked")
                self.assertEqual(data["exit_code"], 0)
            finally:
                fcntl.flock(lock_fd, fcntl.LOCK_UN)
                lock_fd.close()

    def test_retention_cleanup(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            runs_dir = os.path.join(tmpdir, "runs")
            os.makedirs(runs_dir, exist_ok=True)

            old_file = os.path.join(runs_dir, "run_old.json")
            new_file = os.path.join(runs_dir, "run_new.json")

            with open(old_file, "w") as f:
                f.write("{}")
            with open(new_file, "w") as f:
                f.write("{}")

            # Set old_file mtime to 35 days ago
            old_time = time.time() - (35 * 86400)
            os.utime(old_file, (old_time, old_time))

            removed = cleanup_old_records(tmpdir, retention_days=30)
            self.assertEqual(removed, 1)
            self.assertFalse(os.path.exists(old_file))
            self.assertTrue(os.path.exists(new_file))

    def test_failure_detection_404(self):
        sample_output = """
Checking for skill updates…
Checking skills from source: unknown-user/missing-skill
fatal: repository 'https://github.com/unknown-user/missing-skill.git' not found
Updating skill-foo…
✓ Updated skill-foo
"""
        failures = detect_and_report_failures(sample_output)
        self.assertTrue(len(failures) > 0)
        target_found = any("missing-skill" in f["target"] or "https://github.com" in f["target"] for f in failures)
        self.assertTrue(target_found)


if __name__ == "__main__":
    unittest.main()
