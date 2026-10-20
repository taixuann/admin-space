#!/usr/bin/env python3
"""Synthetic end-to-end checks for the generated execution template."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

import yaml

PLUGIN_ROOT = Path(__file__).resolve().parents[4]
if str(PLUGIN_ROOT) not in sys.path:
    sys.path.insert(0, str(PLUGIN_ROOT))
from references.publication_contract import validate_run

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))
import scaffold  # noqa: E402


ANALYSIS_SOURCE = '''from pathlib import Path

def run_study_analysis(data, params=None):
    params = params or {}
    if params.get("fail"):
        raise RuntimeError("synthetic analysis failure")
    if params.get("system_exit"):
        raise SystemExit(0)
    if params.get("interrupt"):
        raise KeyboardInterrupt()
    return {"status": "SUCCESS", "required_outputs": ["tables/summary.csv"]}

def render_figures(analyzed, palette, run_dir, **kwargs):
    if not (kwargs.get("params") or {}).get("omit_output"):
        output = Path(run_dir) / "tables" / "summary.csv"
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text("metric,value\\ncount,1\\n", encoding="utf-8")
'''


class TestExecutionContract(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="test-execution-contract-")).resolve()
        self.project = self.tmp / "project"
        self.study = self.project / "analysis"
        self.study.mkdir(parents=True)
        (self.study / "spec").mkdir()
        (self.study / "plans").mkdir()
        (self.study / "spec" / "reasoning.md").write_text("Synthetic question.\n", encoding="utf-8")
        self.plan = self.study / "plans" / "run-plan.html"
        self.plan.write_text("---\nrevision: 1\n---\nSynthetic plan", encoding="utf-8")
        self.input_file = self.project / "data" / "raw" / "input.csv"
        self.input_file.parent.mkdir(parents=True)
        self.input_file.write_text("time,current\n0,1\n", encoding="utf-8")
        self.manifest = self.study / "input.yaml"
        self._write_manifest()
        scaffold.scaffold_study_scripts(self.study)
        (self.study / "scripts" / "specific" / "analysis.py").write_text(ANALYSIS_SOURCE, encoding="utf-8")
        self.runner = self.study / "scripts" / "run.py"
        sys.path.insert(0, str(self.study / "scripts"))

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _sha256(self, path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def _write_manifest(self, *, include_digest=True):
        item = {"path": "data/raw/input.csv"}
        if include_digest:
            item["sha256"] = self._sha256(self.input_file)
        doc = {
            "schema_version": 1,
            "owner": "implement-research",
            "inputs": [{"object_id": "synthetic-input", "role": "raw-input", "files": [item]}],
        }
        self.manifest.write_text(json.dumps(doc), encoding="utf-8")

    def _run(self, run_id="synthetic-r1", *, params=None, extra=(), runner=None):
        env = os.environ.copy()
        env.pop("PYTHONDONTWRITEBYTECODE", None)
        params_path = self.tmp / "params.json"
        params_path.write_text(json.dumps(params or {}), encoding="utf-8")
        command = [
            sys.executable, str(runner or self.runner),
            "--study-root", str(self.study),
            "--project-root", str(self.project),
            "--plan", str(self.plan),
            "--authorization", "Synthetic test authorization",
            "--params-json", str(params_path),
            *extra,
        ]
        if "--out" not in extra:
            command.extend(["--run-id", run_id])
        return subprocess.run(command, cwd=self.study, env=env, text=True, capture_output=True, check=False)

    def _lock(self, run_id="synthetic-r1"):
        return yaml.safe_load((self.study / "runs" / run_id / "run.lock.yaml").read_text(encoding="utf-8"))

    def test_existing_output_sentinel_is_untouched(self):
        occupied = self.study / "runs" / "occupied"
        occupied.mkdir(parents=True)
        sentinel = occupied / "sentinel.txt"
        sentinel.write_text("preserve", encoding="utf-8")
        result = self._run(extra=("--out", str(occupied)))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("exist", result.stderr.lower())
        self.assertEqual(sentinel.read_text(encoding="utf-8"), "preserve")
        self.assertFalse((occupied / "run.lock.yaml").exists())

    def test_same_time_allocation_collision_is_rejected(self):
        from run import spawn_run_dir

        moment = datetime(2026, 1, 2, 3, 4, 5, tzinfo=timezone.utc)
        first = spawn_run_dir(self.study, "same-time", now=moment)
        self.assertTrue(first.is_dir())
        with self.assertRaises(FileExistsError):
            spawn_run_dir(self.study, "same-time", now=moment)

    def test_missing_input_hash_is_recorded_as_failed_allocation(self):
        self._write_manifest(include_digest=False)
        result = self._run()
        self.assertNotEqual(result.returncode, 0)
        lock = self._lock()
        self.assertEqual(lock["status"], "FAILED")
        self.assertIn("SHA-256", lock["error"])

    def test_changed_input_is_recorded_as_failed_allocation(self):
        self.input_file.write_text("time,current\n0,999\n", encoding="utf-8")
        result = self._run()
        self.assertNotEqual(result.returncode, 0)
        lock = self._lock()
        self.assertEqual(lock["status"], "FAILED")
        self.assertIn("SHA-256", lock["error"])

    def test_absolute_input_paths_are_confined_to_project_root_in_loader_and_validator(self):
        from modules.data import checked_input_path
        from references.publication_contract import checked_path

        external = self.tmp / "outside.csv"
        external.write_text("time,current\n0,9\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "escapes selected project root"):
            checked_input_path(self.project, str(external))
        with self.assertRaisesRegex(ValueError, "Path traversal detected"):
            checked_path(self.project, str(external), allow_absolute=True)

        self.assertEqual(checked_input_path(self.project, str(self.input_file)), self.input_file.resolve())
        self.assertEqual(checked_path(self.project, str(self.input_file), allow_absolute=True), self.input_file.resolve())

    def test_optional_input_name_is_validated_and_preserved_in_run_record(self):
        doc = json.loads(self.manifest.read_text(encoding="utf-8"))
        doc["inputs"][0]["name"] = "Selected synthetic input"
        self.manifest.write_text(json.dumps(doc), encoding="utf-8")

        result = self._run()

        self.assertEqual(result.returncode, 0, result.stderr)
        lock = self._lock()
        self.assertEqual(lock["inputs"][0]["name"], "Selected synthetic input")

        self._write_manifest()
        doc = json.loads(self.manifest.read_text(encoding="utf-8"))
        doc["inputs"][0]["name"] = 42
        self.manifest.write_text(json.dumps(doc), encoding="utf-8")
        invalid = self._run(run_id="synthetic-r2")
        self.assertNotEqual(invalid.returncode, 0)
        self.assertIn("name", self._lock("synthetic-r2")["error"].lower())

    def test_analysis_receives_staged_input_copy_and_cannot_modify_original(self):
        self._write_manifest()
        original = self.input_file.read_bytes()
        (self.study / "scripts" / "specific" / "analysis.py").write_text(
            '''from pathlib import Path\ndef run_study_analysis(data, params=None):\n    Path(data["series"][0]["path"]).write_text("changed by analysis", encoding="utf-8")\n    return {"status": "SUCCESS", "required_outputs": ["tables/summary.csv"]}\ndef render_figures(analyzed, palette, run_dir, **kwargs):\n    output = Path(run_dir) / "tables" / "summary.csv"\n    output.parent.mkdir(parents=True, exist_ok=True)\n    output.write_text("metric,value\\ncount,1\\n", encoding="utf-8")\n''',
            encoding="utf-8",
        )

        result = self._run()

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.input_file.read_bytes(), original)
        lock = self._lock()
        self.assertEqual(lock["inputs"][0]["files"][0]["path"], "data/raw/input.csv")
        self.assertEqual(lock["inputs"][0]["files"][0]["sha256"], self._sha256(self.input_file))

    def test_modified_recovery_snapshot_seals_run_as_failed(self):
        (self.study / "scripts" / "specific" / "analysis.py").write_text(
            '''import os
from pathlib import Path

def run_study_analysis(data, params=None):
    snapshot = Path(os.environ["STUDY_RUN_DIR"]) / "plan" / "run-plan.html"
    snapshot.write_text("changed by analysis", encoding="utf-8")
    return {"status": "SUCCESS", "required_outputs": ["tables/summary.csv"]}

def render_figures(analyzed, palette, run_dir, **kwargs):
    output = Path(run_dir) / "tables" / "summary.csv"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("metric,value\\ncount,1\\n", encoding="utf-8")
''',
            encoding="utf-8",
        )

        result = self._run()

        self.assertNotEqual(result.returncode, 0)
        lock = self._lock()
        self.assertEqual(lock["status"], "FAILED")
        self.assertIn("Recovery snapshots changed", lock["error"])
        snapshot = self.study / lock["plan"]["snapshot_path"]
        self.assertNotEqual(self._sha256(snapshot), lock["plan"]["sha256"])

    def test_execution_exception_preserves_failed_lock(self):
        result = self._run(params={"fail": True})
        self.assertNotEqual(result.returncode, 0)
        lock = self._lock()
        self.assertEqual(lock["status"], "FAILED")
        self.assertEqual(lock["error"], "synthetic analysis failure")
        self.assertEqual(lock["scientific_acceptance"], "NOT_ASSESSED")

    def test_protected_tree_symlink_is_recorded_as_failed_before_analysis(self):
        link = self.study / "spec" / "external.md"
        link.symlink_to(self.input_file)

        result = self._run()

        self.assertNotEqual(result.returncode, 0)
        lock = self._lock()
        self.assertEqual(lock["status"], "FAILED")
        self.assertIn("Symlinked protected file is not allowed", lock["error"])
        self.assertFalse((self.study / "runs" / "synthetic-r1" / "tables" / "summary.csv").exists())

    def test_symlinked_protected_root_is_rejected_and_records_failed_run(self):
        from run import path_inside

        plans_target = self.study / "plans-target"
        (self.study / "plans").rename(plans_target)
        (self.study / "plans").symlink_to(plans_target, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "Symlinked execution path"):
            path_inside(self.study, self.study / "plans" / "run-plan.html", "Selected plan")

        (self.study / "plans").unlink()
        plans_target.rename(self.study / "plans")
        scripts_target = self.study / "scripts-target"
        (self.study / "scripts").rename(scripts_target)
        (self.study / "scripts").symlink_to(scripts_target, target_is_directory=True)

        result = self._run()

        self.assertNotEqual(result.returncode, 0)
        lock = self._lock()
        self.assertEqual(lock["status"], "FAILED")
        self.assertIn("Symlinked protected directory is not allowed", lock["error"])
        self.assertFalse((self.study / "runs" / "synthetic-r1" / "tables" / "summary.csv").exists())

    def test_environment_record_captures_all_installed_distributions_deterministically(self):
        from run import environment_record

        first = environment_record()["packages"]
        second = environment_record()["packages"]

        self.assertTrue(first)
        self.assertEqual(first, second)
        self.assertEqual(first, sorted(first, key=lambda item: (item["name"].casefold(), item["name"], item["version"])))
        self.assertTrue(all(item["name"] and item["version"] for item in first))

    def test_invalid_utf8_question_seals_failed_run_and_keeps_partial_output(self):
        (self.study / "spec" / "reasoning.md").write_bytes(b"Synthetic question: \xff\xfe\n")

        result = self._run()

        self.assertNotEqual(result.returncode, 0)
        lock = self._lock()
        self.assertEqual(lock["status"], "FAILED")
        self.assertIn("UTF-8", lock["error"])
        self.assertEqual(lock["exit_code"], 1)
        self.assertTrue((self.study / "runs" / "synthetic-r1" / "tables" / "summary.csv").is_file())
        self.assertEqual(lock["outputs"][0]["path"], "tables/summary.csv")

    def test_missing_required_output_cannot_be_completed(self):
        result = self._run(params={"omit_output": True})
        self.assertNotEqual(result.returncode, 0)
        lock = self._lock()
        self.assertEqual(lock["status"], "FAILED")
        self.assertIn("required output", lock["error"].lower())

    def test_completed_run_recovers_exact_code_and_input_and_is_plan022_compatible(self):
        result = self._run()
        self.assertEqual(result.returncode, 0, result.stderr)
        lock, _, _ = validate_run(self.study, "synthetic-r1", self.project)
        self.assertEqual(lock["status"], "COMPLETED")
        self.assertEqual(lock["inputs"][0]["files"][0]["path"], "data/raw/input.csv")
        code = lock["code"]["files"]
        self.assertTrue(code)
        for item in code:
            source = self.study / item["path"]
            snapshot = self.study / item["snapshot_path"]
            self.assertEqual(self._sha256(source), item["sha256"])
            self.assertEqual(self._sha256(snapshot), item["sha256"])
        self.assertTrue((self.study / lock["input_manifest"]["snapshot_path"]).is_file())
        self.assertTrue((self.study / lock["plan"]["snapshot_path"]).is_file())
        self.assertEqual(list((self.study / "scripts").rglob("__pycache__")), [])

    def test_runner_outside_scripts_root_is_rejected_before_allocation(self):
        external_runner = self.tmp / "external-run.py"
        external_runner.write_bytes(self.runner.read_bytes())
        result = self._run(run_id="outside-runner", runner=external_runner)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("must be located under study_root/scripts", result.stderr)
        self.assertFalse((self.study / "runs" / "outside-runner").exists())

    def test_system_exit_seals_failed_run_not_completed(self):
        result = self._run(run_id="system-exit-run", params={"system_exit": True})
        self.assertNotEqual(result.returncode, 0)
        lock = yaml.safe_load((self.study / "runs" / "system-exit-run" / "run.lock.yaml").read_text(encoding="utf-8"))
        self.assertEqual(lock["status"], "FAILED")
        self.assertIn("SystemExit", lock["error"])

    def test_keyboard_interrupt_seals_failed_run_then_propagates(self):
        result = self._run(run_id="interrupt-run", params={"interrupt": True})
        self.assertNotEqual(result.returncode, 0)
        lock = yaml.safe_load((self.study / "runs" / "interrupt-run" / "run.lock.yaml").read_text(encoding="utf-8"))
        self.assertEqual(lock["status"], "FAILED")
        self.assertIn("KeyboardInterrupt", lock["error"])


    def test_shared_run_validator_rejects_boolean_schema_exit_and_empty_role(self):
        result = self._run()
        self.assertEqual(result.returncode, 0, result.stderr)
        lock_path = self.study / "runs" / "synthetic-r1" / "run.lock.yaml"
        original = yaml.safe_load(lock_path.read_text(encoding="utf-8"))
        for field, value in (("schema_version", True), ("exit_code", False)):
            with self.subTest(field=field):
                lock = dict(original); lock[field] = value
                lock_path.write_text(yaml.safe_dump(lock, sort_keys=False), encoding="utf-8")
                with self.assertRaisesRegex(ValueError, "schema_version|exit_code|execution metadata"):
                    validate_run(self.study, "synthetic-r1", self.project)
        lock = dict(original)
        lock["outputs"] = [dict(lock["outputs"][0], role=" ")]
        lock_path.write_text(yaml.safe_dump(lock, sort_keys=False), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "role"):
            validate_run(self.study, "synthetic-r1", self.project)


if __name__ == "__main__":
    unittest.main()
