#!/usr/bin/env python3
"""Unit tests for package_crate.py in ro-crate-research skill."""

from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from datetime import datetime
from unittest.mock import patch
from pathlib import Path

# Add scripts directory to path
import sys
SCRIPTS_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS_DIR))

import package_crate  # noqa: E402


class TestPackageCrate(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix="test-crate-")
        self.project = Path(self.test_dir)
        self.study = self.project / "study-crate-test"
        self.study.mkdir(parents=True)

        # Create spec
        spec_dir = self.study / "spec"
        spec_dir.mkdir()
        (spec_dir / "reasoning.md").write_text(
            "# Study Reasoning\n\n## 1. Scientific Question\nIs the memristive filament formation reversible?\n",
            encoding="utf-8"
        )

        # Create synthetic run
        self.run_id = "run-20261019-crate01"
        self.run_dir = self.study / "runs" / self.run_id
        self.out_dir = self.run_dir / "figures" / "primary" / "retention"
        self.out_dir.mkdir(parents=True)

        self.fig_file = self.out_dir / "retention.png"
        self.fig_file.write_bytes(b"RO_CRATE_TEST_IMAGE_DATA_54321")
        self.fig_hash = package_crate.sha256_file(self.fig_file)

        self._write_contract_lock([{"path": "figures/primary/retention/retention.png", "object_id": "fig:retention", "role": "figure", "sha256": self.fig_hash}])

    def _write_contract_lock(self, outputs):
        project = self.project
        raw = project / "data" / "raw" / "synthetic.csv"
        raw.parent.mkdir(parents=True, exist_ok=True)
        raw.write_bytes(b"synthetic input")
        plan = self.study / "plans" / "synthetic.html"
        plan.parent.mkdir(parents=True, exist_ok=True)
        plan.write_text("<html>synthetic plan</html>", encoding="utf-8")
        input_manifest = self.study / "input.yaml"
        input_manifest.write_text(json.dumps({"schema_version": 1, "owner": "implement-research", "inputs": [{"object_id": "synthetic-input", "role": "raw-input", "files": [{"path": "data/raw/synthetic.csv", "sha256": package_crate.sha256_file(raw)}]}]}), encoding="utf-8")
        code = self.study / "scripts" / "run.py"
        code.parent.mkdir(parents=True, exist_ok=True)
        code.write_text("# synthetic", encoding="utf-8")
        for relative, source in ((f"runs/{self.run_id}/plan/synthetic.html", plan), (f"runs/{self.run_id}/inputs/input.yaml", input_manifest), (f"runs/{self.run_id}/code/scripts/run.py", code)):
            target = self.study / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(source.read_bytes())
        lock = {"schema_version": 1, "owner": "implement-research", "run_id": self.run_id, "status": "COMPLETED", "scientific_acceptance": "NOT_ASSESSED", "started_at": "2026-01-01T00:00:00+00:00", "finished_at": "2026-01-01T00:00:01+00:00", "question": "synthetic", "plan": {"path": "plans/synthetic.html", "revision": 1, "sha256": package_crate.sha256_file(plan), "snapshot_path": f"runs/{self.run_id}/plan/synthetic.html", "authorization": "Synthetic fixture authorization"}, "input_manifest": {"path": "input.yaml", "sha256": package_crate.sha256_file(input_manifest), "snapshot_path": f"runs/{self.run_id}/inputs/input.yaml"}, "inputs": [{"object_id": "synthetic-input", "role": "raw-input", "files": [{"path": "data/raw/synthetic.csv", "sha256": package_crate.sha256_file(raw)}]}], "parameters": {}, "validation": {"inputs_unchanged": True, "protected_files_unchanged": True, "required_outputs_valid": True}, "code": {"files": [{"path": "scripts/run.py", "sha256": package_crate.sha256_file(code), "snapshot_path": f"runs/{self.run_id}/code/scripts/run.py"}]}, "environment": {"interpreter": "synthetic", "packages": {}}, "command": ["synthetic"], "exit_code": 0, "outputs": outputs}
        (self.run_dir / "run.lock.yaml").write_text(json.dumps(lock), encoding="utf-8")

    def _set_input_files(self, files):
        manifest_path = self.study / "input.yaml"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["inputs"][0]["files"] = files
        manifest_bytes = json.dumps(manifest).encode("utf-8")
        manifest_path.write_bytes(manifest_bytes)
        snapshot = self.study / f"runs/{self.run_id}/inputs/input.yaml"
        snapshot.write_bytes(manifest_bytes)
        lock_path = self.run_dir / "run.lock.yaml"
        lock = json.loads(lock_path.read_text(encoding="utf-8"))
        lock["input_manifest"]["sha256"] = package_crate.sha256_file(manifest_path)
        lock["inputs"][0]["files"] = files
        lock_path.write_text(json.dumps(lock), encoding="utf-8")

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_ro_crate_13_requires_license_and_valid_root_metadata(self):
        destination = self.study / "results" / "preserve-license-required"
        destination.mkdir(parents=True)
        marker = destination / "preserve.txt"
        marker.write_text("existing package", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "explicit.*license"):
            package_crate.package_study(
                study_root=self.study,
                project_root=self.project,
                run_ids=[self.run_id],
                output_dir=destination,
                replace_package=True,
            )
        self.assertEqual(marker.read_text(encoding="utf-8"), "existing package")

        crate_path = self._package(
            study_root=self.study,
            project_root=self.project,
            run_ids=[self.run_id],
            output_dir=self.study / "results" / "required-metadata",
            output_scope="all-selected",
            license="https://example.org/licenses/synthetic-test",
        )
        graph = json.loads((crate_path / "ro-crate-metadata.json").read_text(encoding="utf-8"))["@graph"]
        root = graph[1]
        self.assertEqual(root["license"], "https://example.org/licenses/synthetic-test")
        self.assertIsInstance(datetime.fromisoformat(root["datePublished"]), datetime)
        output = next(entity for entity in graph if entity.get("@id", "").endswith("retention.png"))
        self.assertNotIn("sourceRun", output)
        self.assertNotIn("role", output)
        property_ids = {item["@id"] for item in output["additionalProperty"]}
        properties = {
            item["name"]: item["value"]
            for item in graph
            if item.get("@id") in property_ids
        }
        self.assertEqual(properties, {"sourceRun": self.run_id, "role": "figure", "disposition": "ACCEPTED"})
        self.assertTrue(all(set(item) == {"@id"} for item in output["additionalProperty"]))

    def test_package_crate_success(self):
        out_pkg = self.study / "results" / "package"
        pkg_path = self._package(
            study_root=self.study,
            project_root=self.project,
            run_ids=[self.run_id],
            output_dir=out_pkg,
            replace_package=False,
        )
        self.assertTrue(pkg_path.is_dir())
        # Check metadata
        meta_file = pkg_path / "ro-crate-metadata.json"
        self.assertTrue(meta_file.is_file())
        crate = json.loads(meta_file.read_text(encoding="utf-8"))
        self.assertEqual(crate["@context"], package_crate.CRATE_CONTEXT)

        # Validate with crate validator
        package_crate.validate_crate(pkg_path)

        # Check packaged output file
        dest_fig = pkg_path / "outputs" / self.run_id / "figures/primary/retention/retention.png"
        self.assertTrue(dest_fig.is_file())
        self.assertEqual(package_crate.sha256_file(dest_fig), self.fig_hash)

        # Check README.md
        readme = pkg_path / "README.md"
        self.assertTrue(readme.is_file())
        self.assertIn("Is the memristive filament formation reversible?", readme.read_text(encoding="utf-8"))

    def test_package_replace_guard(self):
        out_pkg = self.study / "results" / "package"
        self._package(
            study_root=self.study,
            project_root=self.project,
            run_ids=[self.run_id],
            output_dir=out_pkg,
            replace_package=False,
        )
        # Re-packaging without replace_package should fail
        with self.assertRaises(FileExistsError):
            self._package(
                study_root=self.study,
            project_root=self.project,
                run_ids=[self.run_id],
                output_dir=out_pkg,
                replace_package=False,
            )
        # With replace_package=True should succeed
        res = self._package(
            study_root=self.study,
            project_root=self.project,
            run_ids=[self.run_id],
            output_dir=out_pkg,
            replace_package=True,
        )
        self.assertTrue(res.is_dir())

    def test_package_formats_filtering(self):
        # Also create a .pdf output
        pdf_file = self.out_dir / "retention.pdf"
        pdf_file.write_bytes(b"FAKE_PDF_DATA_67890")
        pdf_hash = package_crate.sha256_file(pdf_file)

        self._write_contract_lock([
            {"path": "figures/primary/retention/retention.png", "object_id": "fig:retention_png", "role": "figure", "sha256": self.fig_hash},
            {"path": "figures/primary/retention/retention.pdf", "object_id": "fig:retention_pdf", "role": "figure", "sha256": pdf_hash},
        ])

        out_pkg = self.study / "results" / "package_pdf_only"
        pkg_path = self._package(
            study_root=self.study,
            project_root=self.project,
            run_ids=[self.run_id],
            output_dir=out_pkg,
            formats=["pdf"],
            replace_package=True,
        )
        # PDF should be present, PNG should be excluded
        self.assertTrue((pkg_path / "outputs" / self.run_id / "figures/primary/retention/retention.pdf").is_file())
        self.assertFalse((pkg_path / "outputs" / self.run_id / "figures/primary/retention/retention.png").exists())

    def test_package_preview(self):
        preview = self._package(
            study_root=self.study,
            project_root=self.project,
            run_ids=[self.run_id],
            output_dir=self.study / "results" / "package_preview",
            preview=True,
        )
        self.assertIsInstance(preview, dict)
        self.assertEqual(preview["study"], "study-crate-test")
        self.assertFalse((self.study / "results" / "package_preview").exists())

    def test_package_only_accepted_and_metadata(self):
        # Write evidence-ledger.json with one ACCEPTED and one REJECTED
        rejected = self.out_dir / "rejected.csv"
        rejected.write_bytes(b"rejected synthetic output")
        self._write_contract_lock([
            {"path": "figures/primary/retention/retention.png", "object_id": "fig:accepted", "role": "figure", "sha256": self.fig_hash},
            {"path": "figures/primary/retention/rejected.csv", "object_id": "table:rejected", "role": "table", "sha256": package_crate.sha256_file(rejected)},
        ])
        results_dir = self.study / "results"
        results_dir.mkdir(parents=True, exist_ok=True)
        ledger = {
            "runs": [{"run_id": self.run_id, "lock_sha256": package_crate.sha256_file(self.run_dir / "run.lock.yaml")}],
            "records": [
                {
                    "run_id": self.run_id,
                    "path": "figures/primary/retention/retention.png",
                    "disposition": "ACCEPTED",
                    "lock_sha256": package_crate.sha256_file(self.run_dir / "run.lock.yaml"),
                    "sha256": self.fig_hash,
                },
                {
                    "run_id": self.run_id,
                    "path": "figures/primary/retention/rejected.csv",
                    "disposition": "REJECTED",
                    "lock_sha256": package_crate.sha256_file(self.run_dir / "run.lock.yaml"),
                    "sha256": package_crate.sha256_file(rejected),
                },
            ]
        }
        (results_dir / "evidence-ledger.json").write_text(json.dumps(ledger), encoding="utf-8")

        out_pkg = self.study / "results" / "package_accepted_meta"
        pkg_path = self._package(
            study_root=self.study,
            project_root=self.project,
            run_ids=[self.run_id],
            output_dir=out_pkg,
            output_scope="accepted-only",
            ensure_ledger=False,
            author="Dr. Turing",
            license="CC-BY-4.0",
            replace_package=True,
        )
        self.assertTrue(pkg_path.is_dir())
        self.assertTrue((pkg_path / "outputs" / self.run_id / "figures/primary/retention/retention.png").is_file())
        self.assertFalse((pkg_path / "outputs" / self.run_id / "figures/primary/retention/rejected.csv").exists())
        meta = json.loads((pkg_path / "ro-crate-metadata.json").read_text(encoding="utf-8"))
        root_ds = meta["@graph"][1]
        creator = next(item for item in meta["@graph"] if item.get("@id") == root_ds["creator"]["@id"])
        self.assertEqual(creator["name"], "Dr. Turing")
        self.assertEqual(root_ds["license"], "CC-BY-4.0")
        readme = (pkg_path / "README.md").read_text(encoding="utf-8")
        self.assertIn("Output scope: accepted-only", readme)
        self.assertIn("| `figures/primary/retention/retention.png` | ACCEPTED |", readme)

    def test_accepted_only_rejects_duplicate_ledger_output_bindings(self):
        self._package(self.study, [self.run_id], output_scope="accepted-only", preview=True, project_root=self.project)
        ledger_path = self.study / "results" / "evidence-ledger.json"
        ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
        accepted = next(record for record in ledger["records"] if record["disposition"] == "ACCEPTED")
        ledger["records"].append(dict(accepted))
        ledger_path.write_text(json.dumps(ledger), encoding="utf-8")

        with self.assertRaisesRegex(ValueError, "Duplicate accepted ledger output binding"):
            self._package(self.study, [self.run_id], output_scope="accepted-only", preview=True, ensure_ledger=False, project_root=self.project)

    def test_protected_destination_roots_are_rejected_before_preview(self):
        destinations = [
            self.study,
            self.study / "results",
            self.study / "results" / "artifacts",
            self.study / "spec" / "package",
            self.study / "plans" / "package",
            self.study / "scripts" / "package",
            self.study / "runs" / "package",
        ]
        for destination in destinations:
            with self.subTest(destination=destination), self.assertRaisesRegex(ValueError, "overlaps protected study content"):
                self._package(self.study, [self.run_id], output_dir=destination, preview=True, project_root=self.project)

    def test_input_paths_preserve_project_relative_identity_for_same_basenames(self):
        first = self.project / "samples-a" / "sample.csv"
        second = self.project / "samples-b" / "sample.csv"
        first.parent.mkdir(); second.parent.mkdir()
        first.write_bytes(b"first selected sample")
        second.write_bytes(b"second selected sample")
        self._set_input_files([
            {"path": "samples-a/sample.csv", "sha256": package_crate.sha256_file(first)},
            {"path": "samples-b/sample.csv", "sha256": package_crate.sha256_file(second)},
        ])

        crate = self._package(self.study, [self.run_id], output_dir=self.study / "results" / "distinct-inputs", project_root=self.project)

        packaged_first = crate / "inputs" / self.run_id / "synthetic-input" / "samples-a" / "sample.csv"
        packaged_second = crate / "inputs" / self.run_id / "synthetic-input" / "samples-b" / "sample.csv"
        self.assertEqual(packaged_first.read_bytes(), first.read_bytes())
        self.assertEqual(packaged_second.read_bytes(), second.read_bytes())

    def test_package_staging_and_backup_are_on_destination_filesystem(self):
        destination = self.study / "results" / "same-filesystem"
        destination.parent.mkdir(parents=True)
        real_replace = package_crate.os.replace
        def replace_on_destination_fs(source, target):
            source_path = Path(source)
            target_path = Path(target)
            self.assertEqual(source_path.stat().st_dev, destination.parent.stat().st_dev)
            self.assertEqual(target_path.parent.stat().st_dev, destination.parent.stat().st_dev)
            try:
                source_path.resolve().relative_to(destination.parent.resolve())
            except ValueError:
                self.fail(f"replacement source is not staged beside destination: {source_path}")
            return real_replace(source, target)
        with patch.object(package_crate.os, "replace", side_effect=replace_on_destination_fs):
            result = self._package(self.study, [self.run_id], output_dir=destination, project_root=self.project)
        self.assertTrue(result.is_dir())

    def test_exception_after_backup_move_restores_existing_package(self):
        destination = self.study / "results" / "rollback-after-backup"
        self._package(self.study, [self.run_id], output_dir=destination, project_root=self.project)
        marker = destination / "preserve.txt"
        marker.write_text("old package", encoding="utf-8")
        real_replace = package_crate.os.replace
        calls = 0
        def move_then_raise_once(source, target):
            nonlocal calls
            calls += 1
            result = real_replace(source, target)
            if calls == 1:
                raise OSError("synthetic failure after backup move")
            return result
        with patch.object(package_crate.os, "replace", side_effect=move_then_raise_once):
            with self.assertRaisesRegex(OSError, "after backup move"):
                self._package(self.study, [self.run_id], output_dir=destination, replace_package=True, project_root=self.project)
        self.assertEqual(marker.read_text(encoding="utf-8"), "old package")

    def test_keyboard_interrupt_at_backup_and_install_boundaries_restores_package(self):
        destination = self.study / "results" / "interrupt-rollback"
        for boundary in (1, 2):
            with self.subTest(boundary=boundary):
                if destination.exists():
                    shutil.rmtree(destination)
                self._package(self.study, [self.run_id], output_dir=destination, project_root=self.project)
                marker = destination / "preserve.txt"
                marker.write_text("old package", encoding="utf-8")
                real_replace = package_crate.os.replace
                calls = 0

                def interrupt_after_boundary(source, target):
                    nonlocal calls
                    calls += 1
                    result = real_replace(source, target)
                    if calls == boundary:
                        raise KeyboardInterrupt(f"synthetic interruption at replacement boundary {boundary}")
                    return result

                with patch.object(package_crate.os, "replace", side_effect=interrupt_after_boundary):
                    with self.assertRaisesRegex(KeyboardInterrupt, "synthetic interruption"):
                        self._package(self.study, [self.run_id], output_dir=destination, replace_package=True, project_root=self.project)
                self.assertEqual(marker.read_text(encoding="utf-8"), "old package")
                self.assertEqual(list(destination.parent.glob(f".{destination.name}.backup-*")), [])

    def test_keyboard_interrupt_with_failed_rollback_preserves_recovery_path(self):
        destination = self.study / "results" / "interrupt-recovery"
        self._package(self.study, [self.run_id], output_dir=destination, project_root=self.project)
        marker = destination / "preserve.txt"
        marker.write_text("recoverable package", encoding="utf-8")
        real_replace = package_crate.os.replace
        calls = 0

        def interrupt_install_then_fail_restore(source, target):
            nonlocal calls
            calls += 1
            if calls == 3:
                raise OSError("synthetic restore failure")
            result = real_replace(source, target)
            if calls == 2:
                raise KeyboardInterrupt("synthetic install interruption")
            return result

        with patch.object(package_crate.os, "replace", side_effect=interrupt_install_then_fail_restore):
            with self.assertRaisesRegex(RuntimeError, "recovery path") as error:
                self._package(self.study, [self.run_id], output_dir=destination, replace_package=True, project_root=self.project)
        recovery = Path(str(error.exception).split("recovery path ", 1)[1].split(":", 1)[0])
        self.assertEqual((recovery / "preserve.txt").read_text(encoding="utf-8"), "recoverable package")

    def _lock(self):
        return json.loads((self.run_dir / "run.lock.yaml").read_text(encoding="utf-8"))

    def _save_lock(self, data):
        (self.run_dir / "run.lock.yaml").write_text(json.dumps(data), encoding="utf-8")

    def _package(self, *args, **kwargs):
        kwargs.setdefault("license", "https://example.org/licenses/synthetic-test")
        kwargs.setdefault("output_scope", "all-selected")
        if kwargs.pop("ensure_ledger", True):
            run_ids = kwargs.get("run_ids", args[1] if len(args) > 1 else [])
            records = []
            runs = []
            for run_id in run_ids:
                lock_path = self.study / "runs" / run_id / "run.lock.yaml"
                lock = json.loads(lock_path.read_text(encoding="utf-8"))
                lock_digest = package_crate.sha256_file(lock_path)
                runs.append({"run_id": run_id, "lock_sha256": lock_digest})
                for output in lock["outputs"]:
                    records.append({
                        "run_id": run_id,
                        "path": output["path"],
                        "disposition": "ACCEPTED",
                        "lock_sha256": lock_digest,
                        "sha256": output["sha256"],
                    })
            results = self.study / "results"
            results.mkdir(exist_ok=True)
            (results / "evidence-ledger.json").write_text(json.dumps({"runs": runs, "records": records}), encoding="utf-8")
        return package_crate.package_study(*args, **kwargs)

    def test_python_api_requires_explicit_output_scope(self):
        with self.assertRaisesRegex(ValueError, "explicit output_scope"):
            package_crate.package_study(
                study_root=self.study,
                project_root=self.project,
                run_ids=[self.run_id],
                preview=True,
                license="https://example.org/licenses/synthetic-test",
            )

    def test_all_selected_scope_binds_dispositions_to_every_output(self):
        pdf = self.out_dir / "retention.pdf"
        pdf.write_bytes(b"synthetic ambiguous output")
        csv = self.out_dir / "retention.csv"
        csv.write_bytes(b"synthetic rejected output")
        superseded = self.out_dir / "retention.sup"
        superseded.write_bytes(b"synthetic superseded output")
        outputs = [
            {"path": "figures/primary/retention/retention.png", "object_id": "fig:accepted", "role": "figure", "sha256": self.fig_hash},
            {"path": "figures/primary/retention/retention.pdf", "object_id": "fig:rejected", "role": "figure", "sha256": package_crate.sha256_file(pdf)},
            {"path": "figures/primary/retention/retention.csv", "object_id": "table:rejected", "role": "table", "sha256": package_crate.sha256_file(csv)},
            {"path": "figures/primary/retention/retention.sup", "object_id": "fig:superseded", "role": "figure", "sha256": package_crate.sha256_file(superseded)},
        ]
        self._write_contract_lock(outputs)
        lock_path = self.run_dir / "run.lock.yaml"
        lock_digest = package_crate.sha256_file(lock_path)
        ledger = {
            "runs": [{"run_id": self.run_id, "lock_sha256": lock_digest}],
            "records": [
                {"run_id": self.run_id, "path": outputs[0]["path"], "disposition": "ACCEPTED", "lock_sha256": lock_digest, "sha256": outputs[0]["sha256"]},
                {"run_id": self.run_id, "path": outputs[1]["path"], "disposition": "AMBIGUOUS", "lock_sha256": lock_digest, "sha256": outputs[1]["sha256"]},
                {"run_id": self.run_id, "path": outputs[2]["path"], "disposition": "REJECTED", "lock_sha256": lock_digest, "sha256": outputs[2]["sha256"]},
                {"run_id": self.run_id, "path": outputs[3]["path"], "disposition": "SUPERSEDED", "lock_sha256": lock_digest, "sha256": outputs[3]["sha256"]},
            ],
        }
        results = self.study / "results"
        results.mkdir(exist_ok=True)
        (results / "evidence-ledger.json").write_text(json.dumps(ledger), encoding="utf-8")

        crate = self._package(self.study, [self.run_id], output_dir=results / "all-selected", project_root=self.project, ensure_ledger=False)
        metadata = json.loads((crate / "ro-crate-metadata.json").read_text(encoding="utf-8"))["@graph"]
        root = next(entity for entity in metadata if entity.get("@id") == "./")
        scope_property = next(entity for entity in metadata if entity.get("@id") == root["additionalProperty"]["@id"])
        self.assertEqual((scope_property["name"], scope_property["value"]), ("outputScope", "all-selected"))
        property_values = {entry["@id"]: (entry["name"], entry["value"]) for entry in metadata if entry.get("@type") == "PropertyValue"}
        output_dispositions = {}
        for entity in metadata:
            if entity.get("@id", "").startswith("outputs/"):
                properties = [property_values[prop["@id"]] for prop in entity.get("additionalProperty", [])]
                output_dispositions[entity["@id"]] = dict(properties)["disposition"]
        self.assertEqual(output_dispositions, {
            f"outputs/{self.run_id}/{outputs[0]['path']}": "ACCEPTED",
            f"outputs/{self.run_id}/{outputs[1]['path']}": "AMBIGUOUS",
            f"outputs/{self.run_id}/{outputs[2]['path']}": "REJECTED",
            f"outputs/{self.run_id}/{outputs[3]['path']}": "SUPERSEDED",
        })
        readme = (crate / "README.md").read_text(encoding="utf-8")
        self.assertIn("Output scope: all selected outputs with explicit dispositions", readme)
        self.assertIn("| `figures/primary/retention/retention.pdf` | AMBIGUOUS |", readme)
        self.assertIn("| `figures/primary/retention/retention.csv` | REJECTED |", readme)
        self.assertIn("| `figures/primary/retention/retention.sup` | SUPERSEDED |", readme)

    def test_custom_existing_output_requires_recognized_crate_before_replacement(self):
        destination = self.project / "user-owned-output"
        destination.mkdir()
        sentinel = destination / "sentinel.txt"
        sentinel.write_text("preserve", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "not a recognized RO-Crate"):
            self._package(self.study, [self.run_id], output_dir=destination, replace_package=True, project_root=self.project)
        self.assertEqual(sentinel.read_text(encoding="utf-8"), "preserve")

    def test_custom_non_destructive_and_recognized_crate_replacement(self):
        destination = self.project / "custom-crate"
        crate = self._package(self.study, [self.run_id], output_dir=destination, project_root=self.project)
        self.assertTrue((crate / "README.md").is_file())
        replacement = self._package(self.study, [self.run_id], output_dir=destination, replace_package=True, project_root=self.project)
        self.assertTrue((replacement / "ro-crate-metadata.json").is_file())

    def test_tmp_alias_is_not_rejected_as_a_symlinked_parent(self):
        with tempfile.TemporaryDirectory(prefix="crate-alias-", dir="/tmp") as temp_dir:
            destination = Path("/tmp") / Path(temp_dir).name / "package"
            crate = self._package(self.study, [self.run_id], output_dir=destination, project_root=self.project)
            self.assertTrue(crate.is_dir())

    def test_all_selected_scope_requires_ledger_and_rejects_mismatched_bindings(self):
        results = self.study / "results"
        results.mkdir(exist_ok=True)
        ledger_path = results / "evidence-ledger.json"
        with self.assertRaisesRegex(FileNotFoundError, "evidence-ledger.json"):
            package_crate.package_study(
                self.study, [self.run_id], project_root=self.project,
                output_scope="all-selected", preview=True,
                license="https://example.org/licenses/synthetic-test",
            )
        lock_path = self.run_dir / "run.lock.yaml"
        ledger_path.write_text(json.dumps({
            "runs": [{"run_id": self.run_id, "lock_sha256": "0" * 64}],
            "records": [{"run_id": self.run_id, "path": "figures/primary/retention/retention.png", "disposition": "ACCEPTED", "lock_sha256": "0" * 64, "sha256": self.fig_hash}],
        }), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Stale evidence ledger binding"):
            package_crate.package_study(
                self.study, [self.run_id], project_root=self.project,
                output_scope="all-selected", preview=True,
                license="https://example.org/licenses/synthetic-test",
            )
        digest = package_crate.sha256_file(lock_path)
        ledger_path.write_text(json.dumps({
            "runs": [{"run_id": self.run_id, "lock_sha256": digest}],
            "records": [{"run_id": self.run_id, "path": "figures/primary/retention/retention.png", "disposition": "ACCEPTED", "lock_sha256": digest, "sha256": "0" * 64}],
        }), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "output hash mismatch"):
            package_crate.package_study(
                self.study, [self.run_id], project_root=self.project,
                output_scope="all-selected", preview=True,
                license="https://example.org/licenses/synthetic-test",
            )
        ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
        ledger["records"][0]["disposition"] = "MISSING"
        ledger["records"][0]["sha256"] = self.fig_hash
        ledger_path.write_text(json.dumps(ledger), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Unsupported or missing output disposition"):
            package_crate.package_study(
                self.study, [self.run_id], project_root=self.project,
                output_scope="all-selected", preview=True,
                license="https://example.org/licenses/synthetic-test",
            )

    def test_cli_requires_mutually_exclusive_output_scope(self):
        common = ["package_crate.py", str(self.study), "--project-root", str(self.project), "--run-id", self.run_id, "--license", "synthetic"]
        for scope_flags in ([], ["--only-accepted", "--include-all-selected-outputs"]):
            with self.subTest(scope_flags=scope_flags), patch.object(sys, "argv", common + scope_flags):
                with self.assertRaises(SystemExit) as error:
                    package_crate.main()
                self.assertEqual(error.exception.code, 2)

    def test_preview_rejects_wrong_output_hash(self):
        lock = self._lock(); lock["outputs"][0]["sha256"] = "0" * 64; self._save_lock(lock)
        with self.assertRaisesRegex(ValueError, "SHA-256 mismatch"):
            self._package(self.study, [self.run_id], preview=True, project_root=self.project)

    def test_missing_code_snapshot_rejected(self):
        lock = self._lock(); (self.study / lock["code"]["files"][0]["snapshot_path"]).unlink()
        with self.assertRaisesRegex(FileNotFoundError, "Selected evidence missing"):
            self._package(self.study, [self.run_id], preview=True, project_root=self.project)

    def test_protected_destination_rejected(self):
        with self.assertRaisesRegex(ValueError, "overlaps protected study content"):
            self._package(self.study, [self.run_id], output_dir=self.study / "runs", preview=True, project_root=self.project)

    def test_raw_input_destination_ancestor_rejected(self):
        external_input = self.project / "external" / "synthetic.csv"
        external_input.parent.mkdir(parents=True)
        external_input.write_bytes(b"external selected synthetic input")
        lock = self._lock()
        files = [{"path": "external/synthetic.csv", "sha256": package_crate.sha256_file(external_input)}]
        manifest = {"schema_version": 1, "owner": "implement-research", "inputs": [{"object_id": "synthetic-input", "role": "raw-input", "files": files}]}
        manifest_path = self.study / "input.yaml"
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        (self.study / lock["input_manifest"]["snapshot_path"]).write_bytes(manifest_path.read_bytes())
        lock["input_manifest"]["sha256"] = package_crate.sha256_file(manifest_path)
        lock["inputs"][0]["files"] = files
        self._save_lock(lock)
        with self.assertRaisesRegex(ValueError, "aliases selected raw input evidence"):
            self._package(self.study, [self.run_id], output_dir=external_input.parent, preview=True, project_root=self.project)

    def test_crate_uses_ro_crate_13_identifiers(self):
        self.assertEqual(package_crate.CRATE_SPEC, "https://w3id.org/ro/crate/1.3")
        self.assertEqual(package_crate.CRATE_CONTEXT, "https://w3id.org/ro/crate/1.3/context")

    def test_missing_selected_input_fails_preview(self):
        (self.project / "data/raw/synthetic.csv").unlink()
        with self.assertRaisesRegex(FileNotFoundError, "Selected evidence missing"):
            self._package(self.study, [self.run_id], preview=True, project_root=self.project)

    def test_explicit_input_exclusion_is_recorded(self):
        destination = self.study / "results" / "outputs_only"
        (self.project / "data/raw/synthetic.csv").unlink()
        result = self._package(self.study, [self.run_id], output_dir=destination, include_inputs=False, project_root=self.project)
        readme = (result / "README.md").read_text(encoding="utf-8")
        self.assertIn("outputs-only package", readme)
        self.assertFalse((result / "inputs").exists())

    def test_duplicate_run_selection_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "Duplicate run IDs"):
            self._package(self.study, [self.run_id, self.run_id], preview=True, project_root=self.project)

    def test_duplicate_input_destination_id_fails_before_replacement(self):
        project = self.project
        destination = self.study / "results" / "collision"
        self._package(self.study, [self.run_id], output_dir=destination, project_root=project)
        raw1 = project / "data/raw/synthetic.csv"
        lock = self._lock()
        inputs = [{"path": "data/raw/synthetic.csv", "sha256": package_crate.sha256_file(raw1)}, {"path": "data/raw/synthetic.csv", "sha256": package_crate.sha256_file(raw1)}]
        manifest = {"schema_version": 1, "owner": "implement-research", "inputs": [{"object_id": "synthetic-input", "role": "raw-input", "files": inputs}]}
        manifest_path = self.study / "input.yaml"
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        manifest_snapshot = self.study / lock["input_manifest"]["snapshot_path"]
        manifest_snapshot.write_bytes(manifest_path.read_bytes())
        lock["input_manifest"]["sha256"] = package_crate.sha256_file(manifest_path)
        lock["inputs"][0]["files"] = inputs
        self._save_lock(lock)
        (destination / "preserved.txt").write_text("prior package", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Duplicate package destination ID"):
            self._package(self.study, [self.run_id], output_dir=destination, replace_package=True, project_root=project)
        self.assertEqual((destination / "preserved.txt").read_text(encoding="utf-8"), "prior package")

    def test_accepted_ledger_stale_lock_binding_fails(self):
        results = self.study / "results"; results.mkdir(exist_ok=True)
        ledger = {"runs": [{"run_id": self.run_id, "lock_sha256": "0" * 64}], "records": [{"run_id": self.run_id, "path": "figures/primary/retention/retention.png", "disposition": "ACCEPTED", "lock_sha256": "0" * 64, "sha256": self.fig_hash}]}
        (results / "evidence-ledger.json").write_text(json.dumps(ledger), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Stale evidence ledger binding"):
            self._package(self.study, [self.run_id], output_scope="accepted-only", ensure_ledger=False, preview=True, project_root=self.project)

    def test_preview_inventory_matches_assembled_file_entities(self):
        preview = self._package(self.study, [self.run_id], preview=True, project_root=self.project)
        crate = self._package(self.study, [self.run_id], output_dir=self.study / "results" / "parity", project_root=self.project)
        graph = json.loads((crate / "ro-crate-metadata.json").read_text(encoding="utf-8"))["@graph"]
        packaged_files = [item for item in graph[2:] if "File" in (item.get("@type") if isinstance(item.get("@type"), list) else [item.get("@type")])]
        packaged = {(item["@id"], item["sha256"]) for item in packaged_files}
        selected = {(item["package_path"], item["sha256"]) for item in preview["inventory"]}
        self.assertEqual(selected | {("README.md", package_crate.sha256_file(crate / "README.md"))}, packaged)

    def test_replacement_failure_restores_previous_package(self):
        destination = self.study / "results" / "rollback"
        self._package(self.study, [self.run_id], output_dir=destination, project_root=self.project)
        marker = destination / "old.txt"; marker.write_text("keep", encoding="utf-8")
        real_replace = package_crate.os.replace
        calls = 0
        def replace_then_fail(source, target):
            nonlocal calls
            calls += 1
            if calls == 2:
                raise OSError("synthetic swap failure")
            return real_replace(source, target)
        with patch.object(package_crate.os, "replace", side_effect=replace_then_fail):
            with self.assertRaisesRegex(OSError, "synthetic swap failure"):
                self._package(self.study, [self.run_id], output_dir=destination, replace_package=True, project_root=self.project)
        self.assertEqual(marker.read_text(encoding="utf-8"), "keep")

    def test_missing_yaml_dependency_is_actionable(self):
        lock_path = self.run_dir / "run.lock.yaml"
        with patch.dict("sys.modules", {"yaml": None}):
            with self.assertRaisesRegex(RuntimeError, "PyYAML is required"):
                package_crate.load_yaml_file(lock_path)

    def test_two_runs_keep_distinct_code_snapshots(self):
        other_id = "run-20261019-crate02"
        other_dir = self.study / "runs" / other_id
        shutil.copytree(self.run_dir, other_dir)
        lock_path = other_dir / "run.lock.yaml"
        lock = json.loads(lock_path.read_text(encoding="utf-8")); lock["run_id"] = other_id
        for field in ("plan", "input_manifest"):
            lock[field]["snapshot_path"] = lock[field]["snapshot_path"].replace(self.run_id, other_id)
        new_source = self.study / "scripts" / "run_two.py"
        new_source.write_text("# run two", encoding="utf-8")
        new_snapshot = other_dir / "code" / "scripts" / "run_two.py"
        new_snapshot.parent.mkdir(parents=True, exist_ok=True); new_snapshot.write_bytes(new_source.read_bytes())
        lock["code"]["files"] = [{"path": "scripts/run_two.py", "sha256": package_crate.sha256_file(new_source), "snapshot_path": f"runs/{other_id}/code/scripts/run_two.py"}]
        lock_path.write_text(json.dumps(lock), encoding="utf-8")
        package = self._package(self.study, [self.run_id, other_id], output_dir=self.study / "results" / "two_runs", project_root=self.project)
        self.assertEqual((package / "code" / self.run_id / "scripts/run.py").read_text(encoding="utf-8"), "# synthetic")
        self.assertEqual((package / "code" / other_id / "scripts/run_two.py").read_text(encoding="utf-8"), "# run two")

    def test_two_versions_of_same_code_path_are_packaged_from_run_snapshots(self):
        other_id = "run-20261019-crate02"
        other_dir = self.study / "runs" / other_id
        shutil.copytree(self.run_dir, other_dir)
        lock_path = other_dir / "run.lock.yaml"
        lock = json.loads(lock_path.read_text(encoding="utf-8"))
        lock["run_id"] = other_id
        for field in ("plan", "input_manifest"):
            lock[field]["snapshot_path"] = lock[field]["snapshot_path"].replace(self.run_id, other_id)
        for record in lock["code"]["files"]:
            record["snapshot_path"] = record["snapshot_path"].replace(self.run_id, other_id)
        code = self.study / "scripts" / "run.py"
        code.write_text("# version two", encoding="utf-8")
        code_snapshot = self.study / lock["code"]["files"][0]["snapshot_path"]
        code_snapshot.write_bytes(code.read_bytes())
        lock["code"]["files"][0]["sha256"] = package_crate.sha256_file(code_snapshot)
        lock_path.write_text(json.dumps(lock), encoding="utf-8")

        package = self._package(self.study, [self.run_id, other_id], output_dir=self.study / "results" / "same_code_path", project_root=self.project)
        self.assertEqual((package / "code" / self.run_id / "scripts/run.py").read_text(encoding="utf-8"), "# synthetic")
        self.assertEqual((package / "code" / other_id / "scripts/run.py").read_text(encoding="utf-8"), "# version two")

    def test_mutated_live_plan_and_input_manifest_do_not_invalidate_snapshots(self):
        (self.study / "plans" / "synthetic.html").write_text("<html>edited later</html>", encoding="utf-8")
        (self.study / "input.yaml").write_text("schema_version: 99\ninputs: []\n", encoding="utf-8")
        preview = self._package(self.study, [self.run_id], preview=True, project_root=self.project)
        self.assertEqual(preview["outputs_count"], 1)


    def test_canonical_destination_collision_is_rejected_before_replacement(self):
        destination = self.study / "results" / "canonical-collision"
        alternate = "figures/primary/retention/../retention/retention.png"
        outputs = [
            {"path": "figures/primary/retention/retention.png", "object_id": "fig:one", "role": "figure", "sha256": self.fig_hash},
            {"path": alternate, "object_id": "fig:two", "role": "figure", "sha256": self.fig_hash},
        ]
        self._write_contract_lock(outputs)
        lock_digest = package_crate.sha256_file(self.run_dir / "run.lock.yaml")
        (self.study / "results").mkdir(exist_ok=True)
        (self.study / "results" / "evidence-ledger.json").write_text(json.dumps({
            "runs": [{"run_id": self.run_id, "lock_sha256": lock_digest}],
            "records": [
                {"run_id": self.run_id, "path": item["path"], "disposition": "ACCEPTED", "lock_sha256": lock_digest, "sha256": self.fig_hash}
                for item in outputs
            ],
        }), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Duplicate package destination ID"):
            self._package(self.study, [self.run_id], output_dir=destination, project_root=self.project)
        self.assertFalse(destination.exists())

    def test_accepted_only_requires_binding_for_zero_accepted_outputs_and_fails_clearly(self):
        results = self.study / "results"
        results.mkdir(exist_ok=True)
        lock_digest = package_crate.sha256_file(self.run_dir / "run.lock.yaml")
        ledger_path = results / "evidence-ledger.json"
        ledger_path.write_text(json.dumps({"runs": [{"run_id": self.run_id, "lock_sha256": "0" * 64}], "records": []}), encoding="utf-8")
        destination = results / "zero-accepted"
        with self.assertRaisesRegex(ValueError, "Stale evidence ledger binding"):
            self._package(self.study, [self.run_id], output_dir=destination, output_scope="accepted-only", preview=True, ensure_ledger=False, project_root=self.project)
        ledger_path.write_text(json.dumps({"runs": [{"run_id": self.run_id, "lock_sha256": lock_digest}], "records": []}), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "No ACCEPTED outputs"):
            self._package(self.study, [self.run_id], output_dir=destination, output_scope="accepted-only", preview=True, ensure_ledger=False, project_root=self.project)
        self.assertFalse(destination.exists())


if __name__ == "__main__":
    unittest.main()
