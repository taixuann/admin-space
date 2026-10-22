"""Unit tests for Track Automation Scanner."""
import sys
import tempfile
import unittest
from pathlib import Path

# Add track-automation to path
TRACK_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(TRACK_DIR))

from scan_automations import (
    classify_category,
    format_bytes,
    humanize_cron,
    humanize_schedule,
    inspect_file,
    run_full_scan,
    scan_model_control_details,
)


class TestTrackAutomationScanner(unittest.TestCase):
    def test_format_bytes(self):
        self.assertEqual(format_bytes(500), "500 B")
        self.assertEqual(format_bytes(2048), "2.0 KB")
        self.assertEqual(format_bytes(1048576 * 3), "3.0 MB")

    def test_humanize_schedule(self):
        # Calendar daily
        cal_daily = {"StartCalendarInterval": {"Hour": 1, "Minute": 0}}
        msg, s_type = humanize_schedule(cal_daily)
        self.assertEqual(msg, "Daily at 01:00")
        self.assertEqual(s_type, "calendar")

        # Calendar weekly
        cal_weekly = {"StartCalendarInterval": {"Hour": 9, "Minute": 30, "Weekday": 1}}
        msg, s_type = humanize_schedule(cal_weekly)
        self.assertEqual(msg, "Every Mon at 09:30")
        self.assertEqual(s_type, "calendar")

        # Interval seconds
        int_30m = {"StartInterval": 1800}
        msg, s_type = humanize_schedule(int_30m)
        self.assertEqual(msg, "Every 30m")
        self.assertEqual(s_type, "interval")

        # Daemon
        daemon = {"KeepAlive": True}
        msg, s_type = humanize_schedule(daemon)
        self.assertEqual(msg, "Always Running (Daemon)")
        self.assertEqual(s_type, "daemon")

        # Login
        login = {"RunAtLoad": True}
        msg, s_type = humanize_schedule(login)
        self.assertEqual(msg, "Runs once at Login / Boot")
        self.assertEqual(s_type, "login")

        # Manual
        manual = {}
        msg, s_type = humanize_schedule(manual)
        self.assertEqual(msg, "Manual / On-demand")
        self.assertEqual(s_type, "manual")

    def test_humanize_cron(self):
        self.assertEqual(humanize_cron("0 9 * * 1"), "Every Mon at 09:00")
        self.assertEqual(humanize_cron("0 1 * * *"), "Daily at 01:00")
        self.assertEqual(humanize_cron("*/15 * * * *"), "Every 15 minutes")
        self.assertEqual(humanize_cron("* * * * *"), "Every minute")

    def test_classify_category(self):
        self.assertEqual(classify_category("com.tai.bridge.sync", "/bin/bash"), "sync")
        self.assertEqual(classify_category("com.tai.zotero-oakreader-sync", "python"), "sync")
        self.assertEqual(classify_category("com.tai.notion-pulse", "/bin/bash"), "lifeos")
        self.assertEqual(classify_category("com.tai.model-control-sync", "/bin/bash"), "ai")
        self.assertEqual(classify_category("ai.hermes.gateway", "node"), "ai")
        self.assertEqual(classify_category("sh.brew.ollama", "ollama"), "ai")
        self.assertEqual(classify_category("com.google.GoogleUpdater.wake", "updater"), "system")

    def test_inspect_file(self):
        with tempfile.NamedTemporaryFile("w+", delete=False) as tf:
            tf.write("line 1\nline 2\nline 3\n")
            tf.flush()
            info = inspect_file(tf.name)
            self.assertTrue(info["exists"])
            self.assertGreater(info["size"], 0)
            self.assertIn("line 3", info["snippet"])

        # Non-existing file
        info_none = inspect_file("/tmp/non_existing_log_xyz.log")
        self.assertFalse(info_none["exists"])
        self.assertEqual(info_none["size"], 0)

    def test_scan_model_control_details(self):
        details = scan_model_control_details()
        if details:
            self.assertIn("hyperresearch", details)
            self.assertIn("pqa_kb", details)
            self.assertEqual(details["hyperresearch"]["policy"], "LOCKED")
            self.assertEqual(details["pqa_kb"]["target_cost"], "$0.00")

    def test_run_full_scan(self):
        res = run_full_scan()
        self.assertIn("timestamp", res)
        self.assertIn("stats", res)
        self.assertIn("automations", res)
        self.assertGreater(res["stats"]["total"], 0)


if __name__ == "__main__":
    unittest.main()
