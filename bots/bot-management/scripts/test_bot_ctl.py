#!/usr/bin/env python3
import json
import os
import shutil
import tempfile
import unittest
from pathlib import Path

# Module to be implemented:
from bot_ctl import (
    observe_bot,
    apply_bot,
    verify_bot,
    pull_plugins,
    main_cli,
)


class TestBotCtl(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.bots_dir = self.tmp / "bots"
        self.profiles_dir = self.tmp / "profiles"
        self.bots_dir.mkdir()
        self.profiles_dir.mkdir()

        # Dummy models.yaml
        self.models_yaml = self.bots_dir / "models.yaml"
        self.models_yaml.write_text("""
providers:
  anthropic:
    type: subscription
    models:
      - claude-haiku-5-5

aliases:
  operation:
    high:     { model: claude-haiku-5-5,  effort: high }
    standard: { model: claude-haiku-5-5,  effort: medium }
""")

        # Dummy plugins.yaml
        self.plugins_yaml = self.bots_dir / "plugins.yaml"
        self.plugins_yaml.write_text("""
plugins:
  standalone:
    superpowers: "skills library"
memory:
  in_use:
    harvey: mnemosyne
mcps:
  seen_on_harvey: [notion]
""")

        # Dummy bot dir (harvey)
        self.bot_dir = self.bots_dir / "harvey"
        self.bot_dir.mkdir()
        (self.bot_dir / "SOUL.md").write_text("""---
name: Harvey
title: Secretary
description: Secretary bot
instruction: Follow rules
enable: true
---
## Context
Harvey context
""")

        (self.bot_dir / "config.json").write_text(json.dumps({
            "model": {
                "primary": "operation.high",
                "fallback": []
            },
            "skills": {"external_dirs": [str(self.tmp / "skills")]},
            "plugins": {
                "enable": ["superpowers"]
            },
            "mcps": {
                "enable": ["notion"]
            },
            "memory": {
                "provider": "mnemosyne"
            }
        }))

        # Skill source
        self.skills_dir = self.tmp / "skills"
        self.skills_dir.mkdir()
        (self.skills_dir / "archify").mkdir()
        (self.skills_dir / "archify" / "SKILL.md").write_text("# Archify")

        # Live profile
        self.profile_dir = self.profiles_dir / "harvey"
        self.profile_dir.mkdir()
        (self.profile_dir / "config.yaml").write_text("model:\n  default: old-model\n")
        (self.profile_dir / ".env").write_text("SECRET=xyz\n")

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_observe_bot_all_and_category_filter(self):
        def mock_hermes(*args):
            if args[0] == "config" and args[1] == "get":
                if args[2] == "model.default": return 0, "claude-haiku-5-5"
                if args[2] == "model.provider": return 0, "anthropic"
                if args[2] == "memory.provider": return 0, "mnemosyne"
                if args[2] == "skills.external_dirs": return 0, "[]"
            if args[0] == "skills" and args[1] == "list":
                return 0, "│ Name         │ Status   │\n│ hermes-agent │ enabled  │\n│ archify      │ enabled  │"
            if args[0] == "plugins" and args[1] == "list":
                return 0, "│ Name        │ Status   │\n│ superpowers │ enabled  │"
            if args[0] == "mcp" and args[1] == "list":
                return 0, "  notion   ✓ enabled"
            return 0, ""

        # Test filter by category="skills"
        rows_skills = observe_bot(self.bot_dir, self.models_yaml, self.profile_dir, mock_hermes, category="skills")
        self.assertTrue(len(rows_skills) > 0)
        for r in rows_skills:
            self.assertEqual(r["category"], "skills")

        # Test observe all
        rows_all = observe_bot(self.bot_dir, self.models_yaml, self.profile_dir, mock_hermes, category=None)
        categories = {r["category"] for r in rows_all}
        self.assertIn("soul", categories)
        self.assertIn("models", categories)
        self.assertIn("skills", categories)
        self.assertIn("plugins", categories)
        self.assertIn("mcp", categories)
        self.assertIn("memory", categories)

    def test_apply_bot_reconcile(self):
        calls = []
        def mock_hermes(*args):
            calls.append(args)
            if args[0] == "skills" and args[1] == "list":
                return 0, "│ Name         │ Status   │\n│ hermes-agent │ enabled  │\n│ old-skill    │ enabled  │"
            if args[0] == "chat":
                return 0, "Hello!"
            return 0, ""

        res = apply_bot(self.bot_dir, self.models_yaml, self.profile_dir, mock_hermes, skip_smoke=False)
        self.assertTrue(res["success"])
        # SOUL symlink created
        self.assertTrue((self.profile_dir / "SOUL.md").is_symlink())
        # Backup created without .env
        backup_dir = res["backup_dir"]
        self.assertTrue(backup_dir.exists())
        self.assertFalse((backup_dir / ".env").exists())
        # Model set
        self.assertIn(("config", "set", "model.default", "claude-haiku-5-5"), calls)
        self.assertIn(("config", "set", "model.provider", "anthropic"), calls)
        # Skills: only the external dirs are written; the live disabled list is Tai's and is never touched
        self.assertIn(("config", "set", "skills.external_dirs", json.dumps([str(self.tmp / "skills")])), calls)
        self.assertFalse(any(c[:3] == ("config", "set", "skills.disabled") for c in calls))
        self.assertFalse(any(c[:2] == ("skills", "disable") or c[:2] == ("skills", "enable") for c in calls))
        # Smoke test called
        self.assertIn(("chat", "-q", "say hi"), calls)

    def test_verify_bot(self):
        def mock_hermes(*args):
            if args[0] == "config" and args[1] == "get":
                if args[2] == "model.default": return 0, "claude-haiku-5-5"
                if args[2] == "model.provider": return 0, "anthropic"
                if args[2] == "memory.provider": return 0, "mnemosyne"
                if args[2] == "skills.external_dirs": return 0, f"  - {self.tmp / 'skills'}"
            if args[0] == "skills" and args[1] == "list":
                return 0, "│ Name         │ Status   │\n│ hermes-agent │ enabled  │"
            if args[0] == "plugins" and args[1] == "list":
                return 0, "│ Name        │ Status   │\n│ superpowers │ enabled  │"
            if args[0] == "mcp" and args[1] == "list":
                return 0, "  notion   ✓ enabled"
            return 0, ""

        (self.profile_dir / "SOUL.md").symlink_to(self.bot_dir / "SOUL.md")
        exit_code, rows = verify_bot(self.bot_dir, self.models_yaml, self.profile_dir, mock_hermes)
        self.assertEqual(exit_code, 0)
        self.assertTrue(all(r["status"] == "match" for r in rows if r["status"] != "untested"))

    def test_apply_writes_external_dirs_and_never_the_disabled_list(self):
        calls = []
        def mock_hermes(*args):
            calls.append(args)
            if args[0] == "skills" and args[1] == "list":
                return 0, "│ Name       │ Status   │\n│ live-skill │ enabled  │"
            return 0, ""

        res = apply_bot(self.bot_dir, self.models_yaml, self.profile_dir, mock_hermes, skip_smoke=True)
        self.assertTrue(res["success"])
        self.assertIn(("config", "set", "skills.external_dirs", json.dumps([str(self.tmp / "skills")])), calls)
        self.assertFalse(any(c[:3] == ("config", "set", "skills.disabled") for c in calls))

    def test_apply_only_soul_and_memory_leaves_skills_and_model(self):
        calls = []
        def mock_hermes(*args):
            calls.append(args)
            if args[0] == "skills" and args[1] == "list":
                return 0, "│ Name      │ Status   │\n│ old-skill │ enabled  │"
            return 0, ""

        res = apply_bot(self.bot_dir, self.models_yaml, self.profile_dir, mock_hermes, skip_smoke=True, only=["soul", "memory"])
        self.assertTrue(res["success"])
        self.assertTrue((self.profile_dir / "SOUL.md").is_symlink())
        self.assertTrue(any(c[:3] == ("config", "set", "memory.provider") for c in calls))
        self.assertFalse(any(c[:3] == ("config", "set", "model.default") for c in calls))
        self.assertFalse(any(c[:3] == ("config", "set", "skills.disabled") for c in calls))
        self.assertFalse(any(c[:3] == ("config", "set", "skills.external_dirs") for c in calls))

    def test_apply_rejects_unknown_step(self):
        with self.assertRaises(ValueError):
            apply_bot(self.bot_dir, self.models_yaml, self.profile_dir, lambda *a: (0, ""), skip_smoke=True, only=["bogus"])

    def test_missing_skill_dir_refuses_before_any_write(self):
        cfg = json.loads((self.bot_dir / "config.json").read_text())
        cfg["skills"]["external_dirs"] = [str(self.tmp / "no-such-folder")]
        (self.bot_dir / "config.json").write_text(json.dumps(cfg))
        calls = []
        def mock_hermes(*args):
            calls.append(args)
            return 0, ""

        with self.assertRaises(ValueError):
            apply_bot(self.bot_dir, self.models_yaml, self.profile_dir, mock_hermes, skip_smoke=True)
        self.assertEqual(calls, [])

    def test_pull_plugins(self):
        def mock_hermes(*args):
            if args[0] == "plugins" and args[1] == "list":
                return 0, "│ Name        │ Status   │ Description     │\n│ superpowers │ enabled  │ skills library  │\n│ new-plugin  │ disabled │ helpful plugin  │"
            if args[0] == "mcp" and args[1] == "list":
                return 0, "  notion   ✓ enabled\n  linear   ✗ disabled"
            if args[0] == "memory" and args[1] == "--help":
                return 0, "Available providers: mnemosyne, hindsight, built-in"
            return 0, ""

        catalog, diff = pull_plugins(mock_hermes, self.plugins_yaml)
        self.assertIn("superpowers", catalog["plugins"])
        self.assertIn("new-plugin", catalog["plugins"])
        self.assertIn("notion", catalog["mcps"])
        self.assertIn("new-plugin", diff.get("plugins_added", []))

    def test_cli_subcommands_and_flags(self):
        # Test CLI help / dispatch parsing
        with self.assertRaises(SystemExit) as cm:
            main_cli(["--help"])
        self.assertEqual(cm.exception.code, 0)


if __name__ == "__main__":
    unittest.main()
