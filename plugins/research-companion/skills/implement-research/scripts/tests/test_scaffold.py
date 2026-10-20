#!/usr/bin/env python3
"""Unit tests for scaffold.py in implement-research skill."""

from __future__ import annotations

import shutil
import tempfile
import unittest
from pathlib import Path

# Add scripts directory to path
import sys
SCRIPTS_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS_DIR))

import scaffold  # noqa: E402


class TestScaffold(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix="test-scaffold-")
        self.study = Path(self.test_dir) / "study-scaffold-test"
        self.study.mkdir(parents=True)

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_scaffold_creates_structure(self):
        scaffold.scaffold_study_scripts(self.study)

        # Check required directories
        self.assertTrue((self.study / "scripts" / "modules").is_dir())
        self.assertTrue((self.study / "scripts" / "specific").is_dir())
        self.assertTrue((self.study / "scripts" / "tests").is_dir())

        # Check files
        self.assertTrue((self.study / "scripts" / "run.py").is_file())
        self.assertTrue((self.study / "scripts" / "tests" / "test_reader.py").is_file())
        self.assertTrue((self.study / "scripts" / "tests" / "test_analysis.py").is_file())


if __name__ == "__main__":
    unittest.main()
