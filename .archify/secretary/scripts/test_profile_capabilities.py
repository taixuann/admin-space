#!/usr/bin/env python3
"""Focused tests for profile capability rendering."""

import hashlib
import json
import shutil
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys_path = str(HERE)
import sys
sys.path.insert(0, sys_path)

import profile_capabilities as pc

SCRATCH_ROOT = Path.home() / ".hermes" / "cache" / "scratch"


class SchemaTests(unittest.TestCase):
    def test_valid_minimal(self):
        data = {
            "skills": [],
            "plugins": [],
            "mcps": [],
            "external_tools": [],
            "automation": [],
        }
        self.assertEqual(pc.validate(data), data)

    def test_missing_section_rejected(self):
        data = {
            "skills": [],
            "plugins": [],
            "mcps": [],
            "external_tools": [],
        }
        with self.assertRaises(ValueError):
            pc.validate(data)

    def test_unknown_section_rejected(self):
        data = {
            "skills": [],
            "plugins": [],
            "mcps": [],
            "external_tools": [],
            "automation": [],
            "extra": [],
        }
        with self.assertRaises(ValueError):
            pc.validate(data)

    def test_duplicate_key_rejected(self):
        text = """
skills: []
plugins: []
mcps: []
external_tools: []
automation: []
skills: []
"""
        with self.assertRaises(pc.DuplicateKeyError):
            pc.load_yaml_text(text)

    def test_non_list_section_rejected(self):
        data = {
            "skills": "nope",
            "plugins": [],
            "mcps": [],
            "external_tools": [],
            "automation": [],
        }
        with self.assertRaises(ValueError):
            pc.validate(data)

    def test_bad_entry_rejected(self):
        data = {
            "skills": [123],
            "plugins": [],
            "mcps": [],
            "external_tools": [],
            "automation": [],
        }
        with self.assertRaises(ValueError):
            pc.validate(data)

    def test_mapping_entry_valid(self):
        data = {
            "skills": [{"name": "x", "note": "y"}],
            "plugins": [],
            "mcps": [],
            "external_tools": [],
            "automation": [],
        }
        pc.validate(data)
        self.assertIn("x (y)", pc.entry_text(data["skills"][0]))

    def test_profile_mismatch_rejected(self):
        data = {
            "profile": "coordinator",
            "skills": [],
            "plugins": [],
            "mcps": [],
            "external_tools": [],
            "automation": [],
        }
        with self.assertRaises(ValueError):
            pc.validate(data, "secretary")


class RenderTests(unittest.TestCase):
    def test_all_five_sections_in_candidate(self):
        data = {
            "profile": "secretary",
            "skills": ["a"],
            "plugins": [],
            "mcps": [],
            "external_tools": ["b"],
            "automation": [],
        }
        candidate = pc.render_candidate(data, "secretary")
        for section in pc.SECTIONS:
            self.assertIn(f"## {section.replace('_', ' ').title()} {{#{section}}}", candidate)
        self.assertIn("(none)", candidate)

    def test_escaping_user_data(self):
        evil = "x | y <script> `code`"
        data = {
            "skills": [evil],
            "plugins": [],
            "mcps": [],
            "external_tools": [],
            "automation": [],
        }
        candidate = pc.render_candidate(data, "secretary")
        # Should not contain raw angle bracket outside code; entry is wrapped in inline code.
        self.assertIn("\\|", candidate)
        self.assertNotIn("<script>", candidate)

    def test_hindsight_visible(self):
        data = {
            "skills": [],
            "plugins": [{"name": "hindsight", "detail": "target bank admin; desired only, not applied or health claim"}],
            "mcps": [],
            "external_tools": [],
            "automation": [],
        }
        candidate = pc.render_candidate(data, "secretary")
        self.assertIn("hindsight", candidate)
        self.assertIn("target bank admin", candidate)
        self.assertIn("desired only, not applied or health claim", candidate)


class BuildTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="profile-cap-", dir=str(SCRATCH_ROOT)))
        self.repo = self.tmp / "repo"
        (self.repo / "docs" / "profiles" / "secretary").mkdir(parents=True)
        self.yaml = self.repo / "docs" / "profiles" / "secretary" / "capabilities.yaml"
        self.yaml.write_text(
            "skills: [one]\nplugins: []\nmcps: []\nexternal_tools: []\nautomation: []\n",
            encoding="utf-8",
        )
        self.cli = pc.resolve_archify_cli(pc.REPO_ROOT)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_build_generates_candidate_and_html(self):
        result = pc.build_profile("secretary", self.repo, str(self.cli))
        self.assertTrue(Path(result["candidate"]).is_file())
        self.assertTrue(Path(result["output"]).is_file())
        html = Path(result["output"]).read_text(encoding="utf-8")
        self.assertIn("one", html)
        # receipts
        stage = self.repo / ".archify" / "profile-capabilities-secretary"
        self.assertTrue((stage / "capabilities.finalize.json").is_file())

    def test_changing_yaml_changes_candidate_and_html(self):
        r1 = pc.build_profile("secretary", self.repo, str(self.cli))
        cand1 = Path(r1["candidate"]).read_text()
        html1 = Path(r1["output"]).read_text()
        self.yaml.write_text(
            "skills: [two]\nplugins: []\nmcps: []\nexternal_tools: []\nautomation: []\n",
            encoding="utf-8",
        )
        r2 = pc.build_profile("secretary", self.repo, str(self.cli))
        cand2 = Path(r2["candidate"]).read_text()
        html2 = Path(r2["output"]).read_text()
        self.assertNotEqual(cand1, cand2)
        self.assertNotEqual(html1, html2)
        self.assertIn("two", cand2)
        self.assertIn("two", html2)

    def test_empty_sections_still_render(self):
        self.yaml.write_text(
            "skills: []\nplugins: []\nmcps: []\nexternal_tools: []\nautomation: []\n",
            encoding="utf-8",
        )
        result = pc.build_profile("secretary", self.repo, str(self.cli))
        html = Path(result["output"]).read_text(encoding="utf-8")
        # all five headings present in candidate at least
        cand = Path(result["candidate"]).read_text(encoding="utf-8")
        for section in pc.SECTIONS:
            self.assertIn(f"## {section.replace('_', ' ').title()} {{#{section}}}", cand)

    def test_malformed_yaml_preserves_last_good(self):
        pc.build_profile("secretary", self.repo, str(self.cli))
        html_path = pc.output_path(self.repo, "secretary")
        before = html_path.read_text(encoding="utf-8")
        self.yaml.write_text("skills: [\n", encoding="utf-8")
        with self.assertRaises(Exception):
            pc.build_profile("secretary", self.repo, str(self.cli))
        after = html_path.read_text(encoding="utf-8")
        self.assertEqual(before, after)

    def test_render_failure_preserves_last_good(self):
        pc.build_profile("secretary", self.repo, str(self.cli))
        html_path = pc.output_path(self.repo, "secretary")
        before = html_path.read_text(encoding="utf-8")
        # bad archify cli path to force render failure
        with self.assertRaises(Exception):
            pc.build_profile("secretary", self.repo, "/nonexistent/archify.mjs")
        after = html_path.read_text(encoding="utf-8")
        self.assertEqual(before, after)

    def test_render_failure_nonzero_cli(self):
        # Use main() with bad cli env to ensure nonzero exit
        import os
        os.environ["ARCHIFY_CLI"] = "/nonexistent/archify.mjs"
        # reset by calling build_all
        _results, errors = pc.build_all(["secretary"], self.repo, "/nonexistent/archify.mjs")
        del os.environ["ARCHIFY_CLI"]
        self.assertTrue(errors)
        self.assertIn("secretary", errors)


class WatcherTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="profile-cap-", dir=str(SCRATCH_ROOT)))
        self.repo = self.tmp / "repo"
        (self.repo / "docs" / "profiles" / "secretary").mkdir(parents=True)
        self.yaml = self.repo / "docs" / "profiles" / "secretary" / "capabilities.yaml"
        self.yaml.write_text(
            "skills: [one]\nplugins: []\nmcps: []\nexternal_tools: []\nautomation: []\n",
            encoding="utf-8",
        )
        self.cli = pc.resolve_archify_cli(pc.REPO_ROOT)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_watcher_observes_edit_and_recovery(self):
        state = {"digests": {}}
        # initial
        pc.run_watch_iteration(["secretary"], state, self.repo, str(self.cli))
        # edit
        self.yaml.write_text(
            "skills: [two]\nplugins: []\nmcps: []\nexternal_tools: []\nautomation: []\n",
            encoding="utf-8",
        )
        pc.run_watch_iteration(["secretary"], state, self.repo, str(self.cli))
        cand = (self.repo / ".archify" / "profile-capabilities-secretary" / "candidate.archify.md").read_text()
        self.assertIn("two", cand)
        # malformed
        self.yaml.write_text("skills: [\n", encoding="utf-8")
        pc.run_watch_iteration(["secretary"], state, self.repo, str(self.cli))
        # html preserved
        html = pc.output_path(self.repo, "secretary").read_text()
        self.assertIn("two", html)
        # recovery
        self.yaml.write_text(
            "skills: [three]\nplugins: []\nmcps: []\nexternal_tools: []\nautomation: []\n",
            encoding="utf-8",
        )
        pc.run_watch_iteration(["secretary"], state, self.repo, str(self.cli))
        cand = (self.repo / ".archify" / "profile-capabilities-secretary" / "candidate.archify.md").read_text()
        self.assertIn("three", cand)


class IntervalTests(unittest.TestCase):
    def test_interval_rejects_nonpositive_and_nonfinite(self):
        for bad in ("0", "-1", "nan", "inf", "-0.5"):
            with self.subTest(value=bad):
                with self.assertRaises(SystemExit):
                    pc.main(["--once", "--interval", bad])

    def test_interval_accepts_positive_finite(self):
        self.assertEqual(pc.validate_interval("1.5"), 1.5)
        self.assertEqual(pc.validate_interval("0.25"), 0.25)


if __name__ == "__main__":
    unittest.main()
