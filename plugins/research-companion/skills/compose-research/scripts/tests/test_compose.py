#!/usr/bin/env python3
"""Unit tests for compose.py in compose-research skill."""

from __future__ import annotations

import json
import shutil
import tempfile
import unittest
import json
from contextlib import redirect_stderr
from io import StringIO
from unittest.mock import patch
from pathlib import Path

# Add scripts directory to path
import sys
SCRIPTS_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS_DIR))

import compose  # noqa: E402


class TestCompose(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix="test-compose-")
        self.project = Path(self.test_dir)
        self.study = self.project / "study-test"
        self.study.mkdir(parents=True)

        # Create spec
        spec_dir = self.study / "spec"
        spec_dir.mkdir()
        (spec_dir / "reasoning.md").write_text(
            "# Study Reasoning\n\n## 1. Scientific Question\nDoes threshold voltage shift predictably with pulse count?\n",
            encoding="utf-8"
        )

        # Create synthetic run
        self.run_id = "run-20261019-test01"
        self.run_dir = self.study / "runs" / self.run_id
        self.fig_dir = self.run_dir / "figures" / "primary" / "vt_shift"
        self.fig_dir.mkdir(parents=True)

        # Write dummy figure file
        self.fig_file = self.fig_dir / "vt_shift.png"
        self.fig_file.write_bytes(b"PNG_FAKE_IMAGE_DATA_12345")
        self.fig_hash = compose.sha256_file(self.fig_file)

        self._write_contract_lock([{"path": "figures/primary/vt_shift/vt_shift.png", "object_id": "fig:vt_shift", "role": "figure", "sha256": self.fig_hash}])

    def _write_contract_lock(self, outputs):
        project = self.project
        raw = project / "data" / "raw" / "synthetic.csv"
        raw.parent.mkdir(parents=True, exist_ok=True)
        raw.write_bytes(b"synthetic input")
        plan = self.study / "plans" / "synthetic.html"
        plan.parent.mkdir(parents=True, exist_ok=True)
        plan.write_text("<html>synthetic plan</html>", encoding="utf-8")
        input_manifest = self.study / "input.yaml"
        input_manifest.write_text(json.dumps({"schema_version": 1, "owner": "implement-research", "inputs": [{"object_id": "synthetic-input", "role": "raw-input", "files": [{"path": "data/raw/synthetic.csv", "sha256": compose.sha256_file(raw)}]}]}), encoding="utf-8")
        code = self.study / "scripts" / "run.py"
        code.parent.mkdir(parents=True, exist_ok=True)
        code.write_text("# synthetic", encoding="utf-8")
        for relative, source in ((f"runs/{self.run_id}/plan/synthetic.html", plan), (f"runs/{self.run_id}/inputs/input.yaml", input_manifest), (f"runs/{self.run_id}/code/scripts/run.py", code)):
            target = self.study / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(source.read_bytes())
        lock = {"schema_version": 1, "owner": "implement-research", "run_id": self.run_id, "status": "COMPLETED", "scientific_acceptance": "NOT_ASSESSED", "started_at": "2026-01-01T00:00:00+00:00", "finished_at": "2026-01-01T00:00:01+00:00", "question": "synthetic", "plan": {"path": "plans/synthetic.html", "revision": 1, "sha256": compose.sha256_file(plan), "snapshot_path": f"runs/{self.run_id}/plan/synthetic.html", "authorization": "Synthetic fixture authorization"}, "input_manifest": {"path": "input.yaml", "sha256": compose.sha256_file(input_manifest), "snapshot_path": f"runs/{self.run_id}/inputs/input.yaml"}, "inputs": [{"object_id": "synthetic-input", "role": "raw-input", "files": [{"path": "data/raw/synthetic.csv", "sha256": compose.sha256_file(raw)}]}], "parameters": {}, "validation": {"inputs_unchanged": True, "protected_files_unchanged": True, "required_outputs_valid": True}, "code": {"files": [{"path": "scripts/run.py", "sha256": compose.sha256_file(code), "snapshot_path": f"runs/{self.run_id}/code/scripts/run.py"}]}, "environment": {"interpreter": "synthetic", "packages": {}}, "command": ["synthetic"], "exit_code": 0, "outputs": outputs}
        (self.run_dir / "run.lock.yaml").write_text(json.dumps(lock), encoding="utf-8")

    def _write_result_plan(self, *, assessments=None):
        evidence = f"{self.run_id}/fig:vt_shift"
        plan = self.study / "plans" / "result-plan.json"
        plan.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "schema_version": 1,
            "plan_id": "synthetic-result-plan",
            "revision": 1,
            "decision_source": "synthetic-review",
            "run_bindings": [{"run_id": self.run_id, "lock_sha256": compose.sha256_file(self.run_dir / "run.lock.yaml")}],
            "assessments": assessments if assessments is not None else {evidence: "ACCEPTED"},
            "questions": [{"question_id": "Q1", "text": "Does threshold voltage shift predictably with pulse count?", "source_heading": "1. Scientific Question", "evidence_ids": [evidence]}],
            "views": [{"view_id": "V1", "evidence_id": evidence, "label": "Synthetic view"}],
            "observations": [],
        }
        plan.write_text(json.dumps(payload), encoding="utf-8")
        return plan, evidence

    def _plan_api_kwargs(self, plan, p_data):
        content = plan.read_text(encoding="utf-8")
        digest = compose.hashlib.sha256(content.encode("utf-8")).hexdigest()
        return {
            "plan_identity": {"plan_id": p_data["plan_id"], "revision": p_data["revision"], "decision_source": p_data["decision_source"], "path": str(plan), "sha256": digest},
            "plan_snapshot": {"path": str(plan), "sha256": digest, "content": content},
            "interpret": p_data["interpretation"] or None,
            "interpretation_source": p_data["interpretation_source"],
        }

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_compose_success(self):
        result_md = compose.compose_result(
            study_root=self.study,
            project_root=self.project,
            run_ids=[self.run_id],
            assessments={f"{self.run_id}/fig:vt_shift": "ACCEPTED"},
            authorization="Synthetic test authorization",
            replace_result=False,
            interpret="Linear Vt shift observed up to 100 pulses.",
        )
        self.assertTrue(result_md.is_file())

        content = result_md.read_text(encoding="utf-8")
        self.assertIn("Does threshold voltage shift predictably with pulse count?", content)
        self.assertIn(self.run_id, content)
        self.assertIn("RE-01", content)
        self.assertIn("Linear Vt shift observed up to 100 pulses.", content)

        # Check evidence ledger
        ledger_file = self.study / "results" / "evidence-ledger.json"
        self.assertTrue(ledger_file.is_file())
        ledger_data = json.loads(ledger_file.read_text(encoding="utf-8"))
        self.assertEqual(len(ledger_data["records"]), 1)
        self.assertEqual(ledger_data["records"][0]["re_id"], "RE-01")
        self.assertEqual(ledger_data["records"][0]["disposition"], "ACCEPTED")

        # Check staged artifact
        staged_artifact = self.study / "results" / "artifacts" / self.run_id / "figures/primary/vt_shift/vt_shift.png"
        self.assertTrue(staged_artifact.is_file())
        self.assertEqual(compose.sha256_file(staged_artifact), self.fig_hash)

    def test_compose_replace_guard(self):
        # First compose
        compose.compose_result(
            study_root=self.study,
            project_root=self.project,
            run_ids=[self.run_id],
            assessments={f"{self.run_id}/fig:vt_shift": "ACCEPTED"},
            authorization="Synthetic test authorization",
            replace_result=False,
        )
        # Second compose without replace_result should fail
        with self.assertRaises(FileExistsError):
            compose.compose_result(
                study_root=self.study,
            project_root=self.project,
                run_ids=[self.run_id],
                assessments={f"{self.run_id}/fig:vt_shift": "ACCEPTED"},
            authorization="Synthetic test authorization",
                replace_result=False,
            )
        # With replace_result=True it should succeed
        res = compose.compose_result(
            study_root=self.study,
            project_root=self.project,
            run_ids=[self.run_id],
            assessments={f"{self.run_id}/fig:vt_shift": "ACCEPTED"},
            authorization="Synthetic test authorization",
            replace_result=True,
        )
        self.assertTrue(res.is_file())

    def test_replacement_exception_after_backup_move_preserves_prior_results(self):
        results = self.study / "results"
        results.mkdir(parents=True)
        marker = results / "RESULT.md"
        marker.write_text("prior result", encoding="utf-8")
        real_replace = compose.os.replace
        calls = 0
        def move_then_raise_once(source, target):
            nonlocal calls
            calls += 1
            result = real_replace(source, target)
            if calls == 1:
                raise OSError("synthetic failure after results backup move")
            return result

        with patch.object(compose.os, "replace", side_effect=move_then_raise_once):
            with self.assertRaisesRegex(OSError, "after results backup move"):
                compose.compose_result(
                    study_root=self.study,
                    project_root=self.project,
                    run_ids=[self.run_id],
                    assessments={f"{self.run_id}/fig:vt_shift": "ACCEPTED"},
                    authorization="Synthetic test authorization",
                    replace_result=True,
                )

        self.assertEqual(marker.read_text(encoding="utf-8"), "prior result")

    def test_replace_preserves_package_unknown_children_and_results_directory(self):
        compose.compose_result(
            study_root=self.study, project_root=self.project, run_ids=[self.run_id],
            assessments={f"{self.run_id}/fig:vt_shift": "ACCEPTED"},
            authorization="Synthetic test authorization",
        )
        results = self.study / "results"
        package_marker = results / "package" / "sentinel.txt"
        package_marker.parent.mkdir(parents=True)
        package_marker.write_text("package stays", encoding="utf-8")
        unknown_marker = results / "user-notes" / "notes.txt"
        unknown_marker.parent.mkdir()
        unknown_marker.write_text("unknown child stays", encoding="utf-8")

        real_replace = compose.os.replace
        def forbid_results_root_move(source, target):
            if Path(source) == results or Path(target) == results:
                raise AssertionError("Compose must not replace the results directory itself")
            return real_replace(source, target)

        with patch.object(compose.os, "replace", side_effect=forbid_results_root_move):
            result = compose.compose_result(
                study_root=self.study, project_root=self.project, run_ids=[self.run_id],
                assessments={f"{self.run_id}/fig:vt_shift": "ACCEPTED"},
                authorization="Synthetic test authorization", replace_result=True,
            )
        self.assertTrue(result.is_file())
        self.assertEqual(package_marker.read_text(encoding="utf-8"), "package stays")
        self.assertEqual(unknown_marker.read_text(encoding="utf-8"), "unknown child stays")

    def test_failed_owned_output_replacement_rolls_back_without_touching_unknown_children(self):
        results = self.study / "results"
        results.mkdir()
        (results / "RESULT.md").write_text("old result", encoding="utf-8")
        (results / "evidence-ledger.json").write_text('{"records":[]}', encoding="utf-8")
        (results / "artifacts").mkdir()
        (results / "artifacts" / "old.txt").write_text("old artifact", encoding="utf-8")
        (results / "package").mkdir()
        (results / "package" / "keep.txt").write_text("package", encoding="utf-8")
        (results / "unknown.txt").write_text("unknown", encoding="utf-8")
        real_replace = compose.os.replace
        calls = 0
        def fail_after_first_owned_backup(source, target):
            nonlocal calls
            calls += 1
            result = real_replace(source, target)
            if calls == 1:
                raise OSError("synthetic owned-output replacement failure")
            return result
        with patch.object(compose.os, "replace", side_effect=fail_after_first_owned_backup):
            with self.assertRaisesRegex(OSError, "owned-output replacement failure"):
                compose.compose_result(
                    study_root=self.study, project_root=self.project, run_ids=[self.run_id],
                    assessments={f"{self.run_id}/fig:vt_shift": "ACCEPTED"},
                    authorization="Synthetic test authorization", replace_result=True,
                )
        self.assertEqual((results / "RESULT.md").read_text(encoding="utf-8"), "old result")
        self.assertEqual((results / "evidence-ledger.json").read_text(encoding="utf-8"), '{"records":[]}')
        self.assertEqual((results / "artifacts" / "old.txt").read_text(encoding="utf-8"), "old artifact")
        self.assertEqual((results / "package" / "keep.txt").read_text(encoding="utf-8"), "package")
        self.assertEqual((results / "unknown.txt").read_text(encoding="utf-8"), "unknown")

    def test_compose_hash_mismatch_fails(self):
        # Corrupt file
        self.fig_file.write_bytes(b"CORRUPTED_DATA")
        with self.assertRaises(ValueError):
            compose.compose_result(
                study_root=self.study,
            project_root=self.project,
                run_ids=[self.run_id],
                assessments={f"{self.run_id}/fig:vt_shift": "ACCEPTED"},
            authorization="Synthetic test authorization",
                replace_result=True,
            )

    def test_compose_dry_run(self):
        preview = compose.compose_result(
            study_root=self.study,
            project_root=self.project,
            run_ids=[self.run_id],
            assessments={f"{self.run_id}/fig:vt_shift": "ACCEPTED"},
            authorization="Synthetic test authorization",
            dry_run=True,
        )
        self.assertIsInstance(preview, dict)
        self.assertEqual(preview["study"], "study-test")
        self.assertEqual(len(preview["records"]), 1)
        # Ensure RESULT.md was NOT written
        self.assertFalse((self.study / "results" / "RESULT.md").exists())

    def test_plan_based_write_requires_explicit_authorization_evidence(self):
        plan, _ = self._write_result_plan()

        with patch("sys.argv", ["compose.py", str(self.study), "--project-root", str(self.project), "--plan", str(plan)]):
            result = compose.main()

        self.assertEqual(result, 1)
        self.assertFalse((self.study / "results" / "RESULT.md").exists())

    def test_plan_assessment_conflict_is_rejected_instead_of_silently_overridden(self):
        plan, evidence = self._write_result_plan(assessments={f"{self.run_id}/fig:vt_shift": "ACCEPTED"})
        error = StringIO()

        with redirect_stderr(error), patch("sys.argv", ["compose.py", str(self.study), "--project-root", str(self.project), "--plan", str(plan), "--assess", f"{evidence}=REJECTED", "--authorization", "Synthetic explicit authorization"]):
            result = compose.main()

        self.assertEqual(result, 1)
        self.assertIn("--assess cannot be combined with --plan", error.getvalue())
        self.assertFalse((self.study / "results" / "RESULT.md").exists())

    def test_plan_run_override_is_rejected_with_explicit_conflict(self):
        plan, _ = self._write_result_plan()
        error = StringIO()

        with redirect_stderr(error), patch("sys.argv", ["compose.py", str(self.study), "--project-root", str(self.project), "--plan", str(plan), "--run-id", "different-run", "--authorization", "Synthetic authorization"]):
            result = compose.main()

        self.assertEqual(result, 1)
        self.assertIn("CLI --run-id selection conflicts with the selected result plan", error.getvalue())
        self.assertFalse((self.study / "results" / "RESULT.md").exists())

    def test_plan_authorization_is_recorded_with_plan_identity(self):
        plan, _ = self._write_result_plan()
        authorization = "Synthetic explicit plan authorization"

        with patch("sys.argv", ["compose.py", str(self.study), "--project-root", str(self.project), "--plan", str(plan), "--authorization", authorization]):
            result = compose.main()

        self.assertEqual(result, 0)
        ledger = json.loads((self.study / "results" / "evidence-ledger.json").read_text(encoding="utf-8"))
        self.assertEqual(ledger["authorization"], authorization)
        self.assertEqual(ledger["plan"]["plan_id"], "synthetic-result-plan")
        self.assertEqual(ledger["plan"]["revision"], 1)
        self.assertEqual(ledger["plan"]["decision_source"], "synthetic-review")
        plan_path = self.study / "plans" / "result-plan.json"
        self.assertEqual(ledger["plan"]["sha256"], compose.sha256_file(plan_path))
        self.assertEqual(ledger["plan_snapshot"]["sha256"], compose.sha256_file(plan_path))
        self.assertEqual(ledger["plan_snapshot"]["content"], plan_path.read_text(encoding="utf-8"))

    def test_compose_from_plan(self):
        # Create synthetic HTML result plan
        plan_html = self.study / "plans" / "2026-10-19_result_plan.html"
        plan_html.parent.mkdir(parents=True, exist_ok=True)
        lock_digest = compose.sha256_file(self.run_dir / "run.lock.yaml")
        html_content = f"""<!DOCTYPE html>
<html><body><textarea id="am-source">
---
schema_version: 1
plan_id: synthetic-result-plan
revision: 1
decision_source: scientist-review
run_bindings:
  - run_id: {self.run_id}
    lock_sha256: {lock_digest}
assessments:
  '{self.run_id}/fig:vt_shift': ACCEPTED
questions:
  - question_id: Q1
    text: Does threshold voltage shift predictably with pulse count?
    source_heading: 1. Scientific Question
    evidence_ids: ['{self.run_id}/fig:vt_shift']
views:
  - view_id: V1
    evidence_id: '{self.run_id}/fig:vt_shift'
    label: Threshold shift figure
observations:
  - observation_id: O1
    question_id: Q1
    evidence_ids: ['{self.run_id}/fig:vt_shift']
    label: Supplied threshold shift
    value: '0.125'
    unit: V
    method: User-reported from approved analysis
    limits: Synthetic fixture only
interpretation: |
  Threshold shift confirmed to follow power law.
interpretation_source: human
---
# Result Synthesis Plan
</textarea></body></html>
"""
        plan_html.write_text(html_content, encoding="utf-8")

        p_data = compose.extract_plan_data(plan_html)
        self.assertEqual(p_data["run_ids"], [self.run_id])
        self.assertEqual(p_data["assessments"].get(f"{self.run_id}/fig:vt_shift"), "ACCEPTED")
        self.assertIn("Threshold shift confirmed", p_data["interpretation"])
        self.assertEqual(p_data["questions"][0]["question_id"], "Q1")
        self.assertEqual(p_data["observations"][0]["value"], "0.125")

        # Execute compose with plan data
        res = compose.compose_result(
            study_root=self.study,
            project_root=self.project,
            run_ids=p_data["run_ids"],
            assessments=p_data["assessments"],
            authorization="Synthetic test authorization",
            lock_bindings=p_data["lock_digests"],
            plan_identity={"plan_id": p_data["plan_id"], "revision": p_data["revision"], "decision_source": p_data["decision_source"], "path": str(plan_html), "sha256": compose.sha256_file(plan_html)},
            plan_snapshot={"path": str(plan_html), "sha256": compose.sha256_file(plan_html), "content": plan_html.read_text(encoding="utf-8")},
            interpret=p_data["interpretation"],
            interpretation_source=p_data["interpretation_source"],
            result_plan={field: p_data[field] for field in ("questions", "views", "observations")},
            replace_result=True,
        )
        self.assertTrue(res.is_file())
        md_text = res.read_text(encoding="utf-8")
        self.assertIn("Threshold shift confirmed to follow power law.", md_text)
        self.assertIn("Q1: Does threshold voltage shift predictably with pulse count?", md_text)
        self.assertIn("V1", md_text)
        self.assertIn('<a href="artifacts/', md_text)
        self.assertIn(">Threshold shift figure</a>", md_text)
        self.assertIn("Supplied threshold shift", md_text)
        self.assertIn("= 0.125 V; method: User-reported from approved analysis", md_text)
        with patch.object(sys, "argv", ["compose.py", str(self.study), "--project-root", str(self.project), "--plan", str(plan_html), "--authorization", "Synthetic test authorization", "--interpret", p_data["interpretation"], "--replace-result"]):
            self.assertEqual(compose.main(), 0)
        ledger = json.loads((self.study / "results/evidence-ledger.json").read_text(encoding="utf-8"))
        self.assertEqual(ledger["result_plan"]["observations"][0]["value"], "0.125")
        self.assertEqual(ledger["interpretation_source"], p_data["interpretation_source"])

    def test_result_plan_view_unknown_evidence_rejected(self):
        plan = self.study / "result-plan.yaml"
        known = f"{self.run_id}/fig:vt_shift"
        unknown = f"{self.run_id}/missing-output"
        data = {
            "schema_version": 1, "plan_id": "test", "revision": 1, "decision_source": "review",
            "run_bindings": [{"run_id": self.run_id, "lock_sha256": compose.sha256_file(self.run_dir / "run.lock.yaml")}],
            "assessments": {known: "ACCEPTED"},
            "questions": [{"question_id": "Q1", "text": "Does threshold voltage shift predictably with pulse count?", "source_heading": "1. Scientific Question", "evidence_ids": [known]}],
            "views": [{"view_id": "V1", "evidence_id": unknown, "label": "View"}],
            "observations": [],
        }
        plan.write_text(json.dumps(data), encoding="utf-8")
        p_data = compose.extract_plan_data(plan)
        with self.assertRaisesRegex(ValueError, "View V1 references unknown evidence_id"):
            compose.compose_result(self.study, p_data["run_ids"], p_data["assessments"], authorization="Synthetic test authorization", lock_bindings=p_data["lock_digests"], **self._plan_api_kwargs(plan, p_data), result_plan={field: p_data[field] for field in ("questions", "views", "observations")}, project_root=self.project)

    def test_result_plan_observation_evidence_must_match_question(self):
        second_run = "run-20261019-test02"
        second_dir = self.study / "runs" / second_run
        shutil.copytree(self.run_dir, second_dir)
        second_file = second_dir / "figures" / "primary" / "vt_shift" / "vt_shift.png"
        second_file.write_bytes(b"other synthetic output")
        second_hash = compose.sha256_file(second_file)
        second_lock = json.loads((second_dir / "run.lock.yaml").read_text(encoding="utf-8"))
        second_lock["run_id"] = second_run
        second_lock["outputs"][0]["sha256"] = second_hash
        second_lock["plan"]["snapshot_path"] = second_lock["plan"]["snapshot_path"].replace(self.run_id, second_run)
        second_lock["input_manifest"]["snapshot_path"] = second_lock["input_manifest"]["snapshot_path"].replace(self.run_id, second_run)
        for code_file in second_lock["code"]["files"]:
            code_file["snapshot_path"] = code_file["snapshot_path"].replace(self.run_id, second_run)
        (second_dir / "run.lock.yaml").write_text(json.dumps(second_lock), encoding="utf-8")

        first_evidence = f"{self.run_id}/fig:vt_shift"
        second_evidence = f"{second_run}/fig:vt_shift"
        plan = self.study / "result-plan.yaml"
        data = {
            "schema_version": 1, "plan_id": "test", "revision": 1, "decision_source": "review",
            "run_bindings": [
                {"run_id": self.run_id, "lock_sha256": compose.sha256_file(self.run_dir / "run.lock.yaml")},
                {"run_id": second_run, "lock_sha256": compose.sha256_file(second_dir / "run.lock.yaml")},
            ],
            "assessments": {first_evidence: "ACCEPTED", second_evidence: "ACCEPTED"},
            "questions": [{"question_id": "Q1", "text": "Does threshold voltage shift predictably with pulse count?", "source_heading": "1. Scientific Question", "evidence_ids": [first_evidence]}],
            "views": [{"view_id": "V1", "evidence_id": first_evidence, "label": "View"}],
            "observations": [{"observation_id": "O1", "question_id": "Q1", "evidence_ids": [second_evidence], "label": "Value", "value": "1", "unit": "V", "method": "supplied", "limits": "synthetic"}],
        }
        plan.write_text(json.dumps(data), encoding="utf-8")
        p_data = compose.extract_plan_data(plan)
        with self.assertRaisesRegex(ValueError, "evidence_ids must be bound to question Q1"):
            compose.compose_result(self.study, p_data["run_ids"], p_data["assessments"], authorization="Synthetic test authorization", lock_bindings=p_data["lock_digests"], **self._plan_api_kwargs(plan, p_data), result_plan={field: p_data[field] for field in ("questions", "views", "observations")}, project_root=self.project)

    def _lock(self):
        return json.loads((self.run_dir / "run.lock.yaml").read_text(encoding="utf-8"))

    def _save_lock(self, data):
        (self.run_dir / "run.lock.yaml").write_text(json.dumps(data), encoding="utf-8")

    def _clone_run(self, run_id):
        run_dir = self.study / "runs" / run_id
        shutil.copytree(self.run_dir, run_dir)
        lock_path = run_dir / "run.lock.yaml"
        lock = json.loads(lock_path.read_text(encoding="utf-8"))
        lock["run_id"] = run_id
        for field in ("plan", "input_manifest"):
            lock[field]["snapshot_path"] = lock[field]["snapshot_path"].replace(self.run_id, run_id)
        for item in lock["code"]["files"]:
            item["snapshot_path"] = item["snapshot_path"].replace(self.run_id, run_id)
        lock_path.write_text(json.dumps(lock), encoding="utf-8")
        return run_dir

    def test_replacement_preserves_retired_re_id_high_watermark(self):
        run_ids = [self.run_id]
        for number in range(2, 6):
            run_id = f"run-20261019-test0{number}"
            self._clone_run(run_id)
            run_ids.append(run_id)
        assessments = {f"{rid}/fig:vt_shift": "ACCEPTED" for rid in run_ids}
        compose.compose_result(self.study, run_ids, assessments, authorization="Synthetic test authorization", project_root=self.project)
        prior = json.loads((self.study / "results/evidence-ledger.json").read_text(encoding="utf-8"))
        self.assertEqual([r["re_id"] for r in prior["records"]], [f"RE-0{n}" for n in range(1, 6)])

        compose.compose_result(self.study, [self.run_id], {f"{self.run_id}/fig:vt_shift": "ACCEPTED"}, authorization="Synthetic test authorization", replace_result=True, project_root=self.project)
        added_id = "run-20261019-test06"
        self._clone_run(added_id)
        compose.compose_result(
            self.study,
            [self.run_id, added_id],
            {f"{self.run_id}/fig:vt_shift": "ACCEPTED", f"{added_id}/fig:vt_shift": "ACCEPTED"},
            authorization="Synthetic test authorization",
            replace_result=True,
            project_root=self.project,
        )
        final = json.loads((self.study / "results/evidence-ledger.json").read_text(encoding="utf-8"))
        self.assertEqual([r["re_id"] for r in final["records"]], ["RE-01", "RE-06"])
        self.assertEqual(final["re_id_high_watermark"], 6)

    def test_failed_status_rejected_before_results(self):
        lock = self._lock(); lock["status"] = "FAILED"; self._save_lock(lock)
        with self.assertRaisesRegex(ValueError, "not COMPLETED"):
            compose.compose_result(self.study, [self.run_id], {f"{self.run_id}/fig:vt_shift": "ACCEPTED"}, authorization="Synthetic test authorization", project_root=self.project)
        self.assertFalse((self.study / "results").exists())

    def test_missing_status_rejected(self):
        lock = self._lock(); lock.pop("status"); self._save_lock(lock)
        with self.assertRaisesRegex(ValueError, "Unsupported run lock shape"):
            compose.compose_result(self.study, [self.run_id], {f"{self.run_id}/fig:vt_shift": "ACCEPTED"}, authorization="Synthetic test authorization", project_root=self.project)

    def test_missing_digest_rejected(self):
        lock = self._lock(); del lock["outputs"][0]["sha256"]; self._save_lock(lock)
        with self.assertRaisesRegex(ValueError, "Missing or malformed SHA-256"):
            compose.compose_result(self.study, [self.run_id], {f"{self.run_id}/fig:vt_shift": "ACCEPTED"}, authorization="Synthetic test authorization", project_root=self.project)

    def test_malformed_digest_rejected(self):
        lock = self._lock(); lock["outputs"][0]["sha256"] = "abc"; self._save_lock(lock)
        with self.assertRaisesRegex(ValueError, "Missing or malformed SHA-256"):
            compose.compose_result(self.study, [self.run_id], {f"{self.run_id}/fig:vt_shift": "ACCEPTED"}, authorization="Synthetic test authorization", project_root=self.project)

    def test_mismatched_run_id_rejected(self):
        lock = self._lock(); lock["run_id"] = "other-run"; self._save_lock(lock)
        with self.assertRaisesRegex(ValueError, "Run ID mismatch"):
            compose.compose_result(self.study, [self.run_id], {f"{self.run_id}/fig:vt_shift": "ACCEPTED"}, authorization="Synthetic test authorization", project_root=self.project)

    def test_unsafe_run_id_rejected_before_path_read(self):
        with self.assertRaisesRegex(ValueError, "Unsafe run ID"):
            compose.compose_result(self.study, ["../outside"], {f"{self.run_id}/fig:vt_shift": "ACCEPTED"}, authorization="Synthetic test authorization", project_root=self.project)

    def test_missing_disposition_rejected(self):
        with self.assertRaisesRegex(ValueError, "Explicit valid disposition"):
            compose.compose_result(self.study, [self.run_id], project_root=self.project)

    def test_invalid_disposition_rejected(self):
        with self.assertRaisesRegex(ValueError, "Unknown disposition"):
            compose.parse_assessments([f"{self.run_id}/fig:vt_shift=LIKELY"])

    def test_missing_is_not_an_assessment_choice(self):
        with self.assertRaisesRegex(ValueError, "Unknown disposition"):
            compose.parse_assessments([f"{self.run_id}/fig:vt_shift=MISSING"])

    def test_superseded_is_recorded_but_not_staged(self):
        result = compose.compose_result(
            study_root=self.study, project_root=self.project, run_ids=[self.run_id],
            assessments={f"{self.run_id}/fig:vt_shift": "SUPERSEDED"},
            authorization="Synthetic test authorization",
        )
        self.assertTrue(result.is_file())
        ledger = json.loads((self.study / "results" / "evidence-ledger.json").read_text(encoding="utf-8"))
        self.assertEqual(ledger["records"][0]["disposition"], "SUPERSEDED")
        self.assertFalse((self.study / "results" / "artifacts" / self.run_id / "figures/primary/vt_shift/vt_shift.png").exists())

    def test_non_string_interpretation_rejected_before_results_staging(self):
        with self.assertRaisesRegex(ValueError, "interpretation must be a string"):
            compose.compose_result(
                study_root=self.study, project_root=self.project, run_ids=[self.run_id],
                assessments={f"{self.run_id}/fig:vt_shift": "ACCEPTED"},
                authorization="Synthetic test authorization", interpret={"bad": "type"},
            )
        self.assertFalse((self.study / "results").exists())

    def test_invalid_plan_disposition_rejected(self):
        plan = self.study / "result-plan.yaml"
        plan.write_text(json.dumps({"schema_version": 1, "plan_id": "test", "revision": 1, "decision_source": "review", "run_bindings": [{"run_id": self.run_id, "lock_sha256": compose.sha256_file(self.run_dir / "run.lock.yaml")}], "assessments": {f"{self.run_id}/fig:vt_shift": "LIKELY"}, "questions": [{"question_id": "Q1", "text": "Does threshold voltage shift predictably with pulse count?", "source_heading": "1. Scientific Question", "evidence_ids": [f"{self.run_id}/fig:vt_shift"]}], "views": [{"view_id": "V1", "evidence_id": f"{self.run_id}/fig:vt_shift", "label": "View"}], "observations": []}), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "valid dispositions"):
            compose.extract_plan_data(plan)

    def test_result_plan_missing_evidence_ids_rejected(self):
        plan = self.study / "result-plan.yaml"
        data = {"schema_version": 1, "plan_id": "test", "revision": 1, "decision_source": "review", "run_bindings": [{"run_id": self.run_id, "lock_sha256": compose.sha256_file(self.run_dir / "run.lock.yaml")}], "assessments": {f"{self.run_id}/fig:vt_shift": "ACCEPTED"}, "questions": [{"question_id": "Q1", "text": "Does threshold voltage shift predictably with pulse count?", "source_heading": "1. Scientific Question"}], "views": [{"view_id": "V1", "evidence_id": f"{self.run_id}/fig:vt_shift", "label": "View"}], "observations": []}
        plan.write_text(json.dumps(data), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "requires evidence_ids"):
            compose.extract_plan_data(plan)

    def test_result_plan_unsupported_schema_version_rejected(self):
        plan = self.study / "result-plan.yaml"
        plan.write_text(json.dumps({"schema_version": 2}), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Unsupported result plan schema_version: 2"):
            compose.extract_plan_data(plan)

    def test_result_plan_question_text_must_match_heading_section(self):
        plan = self.study / "result-plan.yaml"
        evidence = f"{self.run_id}/fig:vt_shift"
        data = {
            "schema_version": 1, "plan_id": "test", "revision": 1, "decision_source": "review",
            "run_bindings": [{"run_id": self.run_id, "lock_sha256": compose.sha256_file(self.run_dir / "run.lock.yaml")}],
            "assessments": {evidence: "ACCEPTED"},
            "questions": [{"question_id": "Q1", "text": "A completely unrelated question?", "source_heading": "1. Scientific Question", "evidence_ids": [evidence]}],
            "views": [], "observations": [],
        }
        plan.write_text(json.dumps(data), encoding="utf-8")
        p_data = compose.extract_plan_data(plan)
        with self.assertRaisesRegex(ValueError, "text does not match content under source_heading"):
            compose.compose_result(self.study, p_data["run_ids"], p_data["assessments"], authorization="Synthetic test authorization", lock_bindings=p_data["lock_digests"], **self._plan_api_kwargs(plan, p_data), result_plan={field: p_data[field] for field in ("questions", "views", "observations")}, project_root=self.project)

    def test_result_plan_unknown_question_evidence_rejected(self):
        plan = self.study / "result-plan.yaml"
        evidence = f"{self.run_id}/missing-output"
        data = {"schema_version": 1, "plan_id": "test", "revision": 1, "decision_source": "review", "run_bindings": [{"run_id": self.run_id, "lock_sha256": compose.sha256_file(self.run_dir / "run.lock.yaml")}], "assessments": {f"{self.run_id}/fig:vt_shift": "ACCEPTED"}, "questions": [{"question_id": "Q1", "text": "Does threshold voltage shift predictably with pulse count?", "source_heading": "1. Scientific Question", "evidence_ids": [evidence]}], "views": [{"view_id": "V1", "evidence_id": f"{self.run_id}/fig:vt_shift", "label": "View"}], "observations": []}
        plan.write_text(json.dumps(data), encoding="utf-8")
        p_data = compose.extract_plan_data(plan)
        with self.assertRaisesRegex(ValueError, "references unknown evidence_id"):
            compose.compose_result(self.study, p_data["run_ids"], p_data["assessments"], authorization="Synthetic test authorization", lock_bindings=p_data["lock_digests"], **self._plan_api_kwargs(plan, p_data), result_plan={field: p_data[field] for field in ("questions", "views", "observations")}, project_root=self.project)

    def test_duplicate_output_identity_rejected(self):
        lock = self._lock(); lock["outputs"].append(dict(lock["outputs"][0])); self._save_lock(lock)
        with self.assertRaisesRegex(ValueError, "Duplicate output identity"):
            compose.compose_result(self.study, [self.run_id], {f"{self.run_id}/fig:vt_shift": "ACCEPTED"}, authorization="Synthetic test authorization", project_root=self.project)

    def test_symlinked_output_rejected(self):
        outside = self.study / "outside.png"; outside.write_bytes(self.fig_file.read_bytes())
        self.fig_file.unlink(); self.fig_file.symlink_to(outside)
        with self.assertRaisesRegex(ValueError, "Symlinked evidence"):
            compose.compose_result(self.study, [self.run_id], {f"{self.run_id}/fig:vt_shift": "ACCEPTED"}, authorization="Synthetic test authorization", project_root=self.project)

    def test_symlinked_input_rejected(self):
        input_path = self.project / "data/raw/synthetic.csv"
        target = self.project / "replacement.csv"
        target.write_bytes(input_path.read_bytes())
        input_path.unlink()
        input_path.symlink_to(target)
        with self.assertRaisesRegex(ValueError, "Symlinked evidence"):
            compose.compose_result(self.study, [self.run_id], {f"{self.run_id}/fig:vt_shift": "ACCEPTED"}, authorization="Synthetic test authorization", project_root=self.project)

    def test_malformed_plan_rejected_without_heuristics(self):
        path = self.study / "plans" / "malformed.yaml"; path.write_text("Selected Runs:\n - run-x\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "missing required field"):
            compose.extract_plan_data(path)

    def test_missing_yaml_dependency_is_actionable(self):
        path = self.run_dir / "run.lock.yaml"
        with patch.dict("sys.modules", {"yaml": None}):
            with self.assertRaisesRegex(RuntimeError, "PyYAML is required"):
                compose.load_yaml_lock(path)

    def test_unscoped_assessment_is_rejected_across_runs(self):
        other_id = "run-20261019-test02"
        other_dir = self.study / "runs" / other_id
        shutil.copytree(self.run_dir, other_dir)
        lock_path = other_dir / "run.lock.yaml"
        lock = json.loads(lock_path.read_text(encoding="utf-8")); lock["run_id"] = other_id
        for field in ("plan", "input_manifest"):
            lock[field]["snapshot_path"] = lock[field]["snapshot_path"].replace(self.run_id, other_id)
        for code in lock["code"]["files"]:
            code["snapshot_path"] = code["snapshot_path"].replace(self.run_id, other_id)
        lock_path.write_text(json.dumps(lock), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Unscoped assessment"):
            compose.compose_result(self.study, [self.run_id, other_id], {"fig:vt_shift": "ACCEPTED"}, authorization="Synthetic test authorization", project_root=self.project)

    def test_result_plan_stale_lock_digest_is_rejected(self):
        old_digest = compose.sha256_file(self.run_dir / "run.lock.yaml")
        data = self._lock(); data["question"] = "updated synthetic question"; self._save_lock(data)
        plan = self.study / "plans" / "stale.html"
        plan.write_text(json.dumps({"schema_version": 1, "plan_id": "test", "revision": 1, "decision_source": "review", "run_bindings": [{"run_id": self.run_id, "lock_sha256": old_digest}], "assessments": {f"{self.run_id}/fig:vt_shift": "ACCEPTED"}, "questions": [{"question_id": "Q1", "text": "Does threshold voltage shift predictably with pulse count?", "source_heading": "1. Scientific Question", "evidence_ids": [f"{self.run_id}/fig:vt_shift"]}], "views": [{"view_id": "V1", "evidence_id": f"{self.run_id}/fig:vt_shift", "label": "View"}], "observations": []}), encoding="utf-8")
        plan_data = compose.extract_plan_data(plan)
        with self.assertRaisesRegex(ValueError, "lock binding mismatch"):
            compose.compose_result(self.study, [self.run_id], plan_data["assessments"], authorization="Synthetic test authorization", lock_bindings=plan_data["lock_digests"], project_root=self.project)


    def test_results_root_and_all_owned_symlinks_are_rejected(self):
        outside = self.project / "outside"
        outside.mkdir()
        results = self.study / "results"
        results.symlink_to(outside, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "results root.*symlink|Symlinked results root"):
            compose.compose_result(self.study, [self.run_id], {f"{self.run_id}/fig:vt_shift": "ACCEPTED"}, authorization="Synthetic", project_root=self.project)
        results.unlink()
        results.mkdir()
        for name in ("RESULT.md", "evidence-ledger.json", "artifacts"):
            with self.subTest(name=name):
                link = results / name
                target = self.project / f"outside-{name}"
                if name == "artifacts":
                    target.mkdir()
                else:
                    target.write_text("outside", encoding="utf-8")
                link.symlink_to(target, target_is_directory=name == "artifacts")
                with self.assertRaisesRegex(ValueError, "symlink"):
                    compose.compose_result(self.study, [self.run_id], {f"{self.run_id}/fig:vt_shift": "ACCEPTED"}, authorization="Synthetic", replace_result=True, project_root=self.project)
                link.unlink()
                if target.is_dir():
                    target.rmdir()
                else:
                    target.unlink()

    def test_any_owned_output_requires_replace_and_success_cleans_backup(self):
        results = self.study / "results"
        results.mkdir()
        (results / "artifacts").mkdir()
        with self.assertRaisesRegex(FileExistsError, "replace_result"):
            compose.compose_result(self.study, [self.run_id], {f"{self.run_id}/fig:vt_shift": "ACCEPTED"}, authorization="Synthetic", project_root=self.project)
        compose.compose_result(self.study, [self.run_id], {f"{self.run_id}/fig:vt_shift": "ACCEPTED"}, authorization="Synthetic", replace_result=True, project_root=self.project)
        self.assertEqual(list(results.glob(".compose-owned-backup-*")), [])

    def test_partial_install_failure_rolls_back_and_interruption_is_re_raised(self):
        results = self.study / "results"
        results.mkdir()
        (results / "RESULT.md").write_text("old result", encoding="utf-8")
        (results / "evidence-ledger.json").write_text('{"records": []}', encoding="utf-8")
        (results / "artifacts").mkdir()
        (results / "artifacts" / "old.txt").write_text("old artifact", encoding="utf-8")
        real_replace = compose.os.replace
        calls = 0
        def fail_after_first_install(source, target):
            nonlocal calls
            calls += 1
            result = real_replace(source, target)
            if calls == 4:
                raise KeyboardInterrupt("synthetic install interruption")
            return result
        with patch.object(compose.os, "replace", side_effect=fail_after_first_install):
            with self.assertRaisesRegex(KeyboardInterrupt, "install interruption"):
                compose.compose_result(self.study, [self.run_id], {f"{self.run_id}/fig:vt_shift": "ACCEPTED"}, authorization="Synthetic", replace_result=True, project_root=self.project)
        self.assertEqual((results / "RESULT.md").read_text(encoding="utf-8"), "old result")
        self.assertEqual((results / "evidence-ledger.json").read_text(encoding="utf-8"), '{"records": []}')
        self.assertEqual((results / "artifacts" / "old.txt").read_text(encoding="utf-8"), "old artifact")
        self.assertEqual(list(results.glob(".compose-owned-backup-*")), [])

    def test_every_backup_and_install_replace_failure_restores_prior_outputs(self):
        results = self.study / "results"
        results.mkdir()
        (results / "RESULT.md").write_text("old result", encoding="utf-8")
        (results / "evidence-ledger.json").write_text('{"records": []}', encoding="utf-8")
        (results / "artifacts").mkdir()
        (results / "artifacts" / "old.txt").write_text("old artifact", encoding="utf-8")
        real_replace = compose.os.replace
        for failed_call in range(1, 7):
            with self.subTest(failed_call=failed_call):
                calls = 0
                def fail_after_move(source, target):
                    nonlocal calls
                    calls += 1
                    result = real_replace(source, target)
                    if calls == failed_call:
                        raise OSError(f"synthetic replace failure {failed_call}")
                    return result
                with patch.object(compose.os, "replace", side_effect=fail_after_move):
                    with self.assertRaisesRegex(OSError, f"replace failure {failed_call}"):
                        compose.compose_result(self.study, [self.run_id], {f"{self.run_id}/fig:vt_shift": "ACCEPTED"}, authorization="Synthetic", replace_result=True, project_root=self.project)
                self.assertEqual((results / "RESULT.md").read_text(encoding="utf-8"), "old result")
                self.assertEqual((results / "evidence-ledger.json").read_text(encoding="utf-8"), '{"records": []}')
                self.assertEqual((results / "artifacts" / "old.txt").read_text(encoding="utf-8"), "old artifact")
                self.assertEqual(list(results.glob(".compose-owned-backup-*")), [])

    def test_rollback_failure_keeps_prior_results_in_recovery_path(self):
        results = self.study / "results"
        results.mkdir()
        (results / "RESULT.md").write_text("recoverable result", encoding="utf-8")
        real_replace = compose.os.replace
        calls = 0
        def fail_install_and_restore(source, target):
            nonlocal calls
            calls += 1
            if calls == 2:
                result = real_replace(source, target)
                raise OSError("install failed after move")
            if calls == 3:
                raise OSError("rollback failed")
            return real_replace(source, target)
        with patch.object(compose.os, "replace", side_effect=fail_install_and_restore):
            with self.assertRaisesRegex(RuntimeError, "recovery path") as error:
                compose.compose_result(self.study, [self.run_id], {f"{self.run_id}/fig:vt_shift": "ACCEPTED"}, authorization="Synthetic", replace_result=True, project_root=self.project)
        recovery = Path(str(error.exception).split("recovery path ", 1)[1].split(":", 1)[0])
        self.assertEqual((recovery / "RESULT.md").read_text(encoding="utf-8"), "recoverable result")

    def test_plan_api_cannot_diverge_from_digest_bound_snapshot(self):
        plan, evidence = self._write_result_plan()
        content = plan.read_text(encoding="utf-8")
        p_data = compose.extract_plan_data(plan, source_text=content)
        digest = compose.hashlib.sha256(content.encode()).hexdigest()
        snapshot = {"path": str(plan), "sha256": digest, "content": content}
        identity = {"plan_id": p_data["plan_id"], "revision": p_data["revision"], "decision_source": p_data["decision_source"], "path": str(plan), "sha256": digest}
        params = dict(assessments=p_data["assessments"], authorization="Synthetic", lock_bindings=p_data["lock_digests"], plan_identity=identity, result_plan={field: p_data[field] for field in ("questions", "views", "observations")}, plan_snapshot=snapshot, project_root=self.project, interpret=p_data["interpretation"], interpretation_source=p_data["interpretation_source"])
        for field, value in (("assessments", {}), ("lock_bindings", {}), ("result_plan", {"questions": [], "views": [], "observations": []}), ("plan_identity", {**identity, "plan_id": "forged"}), ("interpret", "forged interpretation"), ("interpretation_source", "model")):
            with self.subTest(field=field):
                (self.study / "results").mkdir(exist_ok=True)
                before = list((self.study / "results").iterdir())
                altered = dict(params); altered[field] = value
                with self.assertRaisesRegex(ValueError, "snapshot|digest-bound|plan"):
                    compose.compose_result(self.study, p_data["run_ids"], **altered)
                self.assertEqual(list((self.study / "results").iterdir()), before)

    def test_plan_question_matching_accepts_normalized_exact_paragraph(self):
        plan, _ = self._write_result_plan()
        reasoning = self.study / "spec" / "reasoning.md"
        reasoning.write_text("# Study Reasoning\n\n## 1. Scientific Question\n> **Does threshold voltage shift predictably with pulse count?**\n", encoding="utf-8")
        p_data = compose.extract_plan_data(plan)
        kwargs = self._plan_api_kwargs(plan, p_data)
        result = compose.compose_result(self.study, p_data["run_ids"], p_data["assessments"], authorization="Synthetic", lock_bindings=p_data["lock_digests"], **kwargs, result_plan={field: p_data[field] for field in ("questions", "views", "observations")}, project_root=self.project)
        self.assertTrue(result.is_file())

    def test_plan_question_matching_is_exact_after_normalization(self):
        plan, evidence = self._write_result_plan()
        data = json.loads(plan.read_text(encoding="utf-8"))
        data["questions"][0]["text"] = "Does threshold voltage shift predictably"
        plan.write_text(json.dumps(data), encoding="utf-8")
        p_data = compose.extract_plan_data(plan)
        with self.assertRaisesRegex(ValueError, "does not match"):
            compose.compose_result(self.study, p_data["run_ids"], p_data["assessments"], authorization="Synthetic", lock_bindings=p_data["lock_digests"], plan_identity={"plan_id": p_data["plan_id"], "revision": p_data["revision"], "decision_source": p_data["decision_source"], "path": str(plan), "sha256": compose.sha256_file(plan)}, plan_snapshot={"path": str(plan), "sha256": compose.sha256_file(plan), "content": plan.read_text()}, result_plan={field: p_data[field] for field in ("questions", "views", "observations")}, project_root=self.project)

    def test_markdown_escapes_plan_strings_but_preserves_ledger_values(self):
        plan, evidence = self._write_result_plan()
        data = json.loads(plan.read_text(encoding="utf-8"))
        data["questions"][0]["question_id"] = "Q|1"
        data["questions"][0]["text"] = "Does threshold voltage shift predictably with pulse count?"
        data["questions"][0]["source_heading"] = "1. Scientific Question"
        data["views"][0]["label"] = "plot [x](javascript:bad) | line\nnext"
        data["observations"] = [{"observation_id": "O|1", "question_id": "Q|1", "evidence_ids": [evidence], "label": "[value]", "value": "1 | (2)", "unit": "V", "method": "method\nnext", "limits": "synthetic"}]
        plan.write_text(json.dumps(data), encoding="utf-8")
        content = plan.read_text()
        p_data = compose.extract_plan_data(plan, source_text=content)
        result = compose.compose_result(self.study, p_data["run_ids"], p_data["assessments"], authorization="Synthetic", lock_bindings=p_data["lock_digests"], plan_identity={"plan_id": p_data["plan_id"], "revision": p_data["revision"], "decision_source": p_data["decision_source"], "path": str(plan), "sha256": compose.sha256_file(plan)}, plan_snapshot={"path": str(plan), "sha256": compose.sha256_file(plan), "content": content}, result_plan={field: p_data[field] for field in ("questions", "views", "observations")}, project_root=self.project)
        rendered = result.read_text()
        self.assertIn("plot &#91;x&#93;", rendered)
        self.assertNotIn('href="javascript:bad', rendered)
        self.assertIn("Q&#124;1", rendered)
        self.assertIn("&#124; line<br>next", rendered)
        ledger = json.loads((self.study / "results" / "evidence-ledger.json").read_text())
        self.assertEqual(ledger["result_plan"]["views"][0]["label"], "plot [x](javascript:bad) | line\nnext")
        self.assertEqual(ledger["result_plan"]["observations"][0]["value"], "1 | (2)")
        self.assertIn("1 &#124; &#40;2&#41;", rendered)
        self.assertIn("method<br>next", rendered)

    def test_existing_ledger_rejects_malformed_or_duplicate_re_identity_bindings(self):
        compose.compose_result(self.study, [self.run_id], {f"{self.run_id}/fig:vt_shift": "ACCEPTED"}, authorization="Synthetic", project_root=self.project)
        ledger_path = self.study / "results" / "evidence-ledger.json"
        ledger = json.loads(ledger_path.read_text())
        ledger["records"][0]["re_id"] = "not-an-RE-id"
        ledger_path.write_text(json.dumps(ledger))
        with self.assertRaisesRegex(ValueError, "RE identity"):
            compose.compose_result(self.study, [self.run_id], {f"{self.run_id}/fig:vt_shift": "ACCEPTED"}, authorization="Synthetic", replace_result=True, project_root=self.project)
        ledger["records"][0]["re_id"] = "RE-01"
        ledger["records"].append(dict(ledger["records"][0], path="other.png", re_id="RE-01"))
        ledger_path.write_text(json.dumps(ledger))
        with self.assertRaisesRegex(ValueError, "duplicate.*binding|duplicate.*RE"):
            compose.compose_result(self.study, [self.run_id], {f"{self.run_id}/fig:vt_shift": "ACCEPTED"}, authorization="Synthetic", replace_result=True, project_root=self.project)


if __name__ == "__main__":
    unittest.main()
