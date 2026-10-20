#!/usr/bin/env python3
"""Compose study results from completed run locks into RESULT.md and evidence ledger.

Strictly read-only on computations. Never reruns analysis or alters raw inputs.
Follows the scientific immutability and transactional delivery contracts.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import re
import shutil
import sys
import tempfile
from pathlib import Path
from urllib.parse import quote
from typing import Any

PLUGIN_ROOT = Path(__file__).resolve().parents[3]
if str(PLUGIN_ROOT) not in sys.path:
    sys.path.insert(0, str(PLUGIN_ROOT))
from references.publication_contract import validate_run, yaml_load

DISPOSITIONS = {"ACCEPTED", "REJECTED", "AMBIGUOUS", "SUPERSEDED", "MISSING"}
ASSESSMENT_DISPOSITIONS = DISPOSITIONS - {"MISSING"}


def sha256_file(path: Path) -> str:
    """Compute hex SHA-256 checksum of a file."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def safe_path(base: Path, rel: str | Path) -> Path:
    p = (base / rel).resolve()
    base_res = base.resolve()
    if p != base_res and base_res not in p.parents:
        raise ValueError(f"Path traversal detected: {rel}")
    return p


def remove_results_path(path: Path) -> None:
    if path.is_dir() and not path.is_symlink():
        shutil.rmtree(path)
    elif path.exists() or path.is_symlink():
        path.unlink()


def publish_results(staging: Path, destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    backup = Path(tempfile.mkdtemp(prefix=".compose-owned-backup-", dir=destination))
    owned = ("RESULT.md", "evidence-ledger.json", "artifacts")
    try:
        for name in owned:
            old = destination / name
            if old.exists() or old.is_symlink():
                os.replace(old, backup / name)
        for name in owned:
            source = staging / name
            if source.exists() or source.is_symlink():
                os.replace(source, destination / name)
    except BaseException as exc:  # aqg: top-level boundary - result replacement rollback must preserve prior outputs
        failures = []
        for name in reversed(owned):
            target, saved, source = destination / name, backup / name, staging / name
            try:
                if saved.exists() or saved.is_symlink():
                    if target.exists() or target.is_symlink():
                        remove_results_path(target)
                    os.replace(saved, target)
                elif not source.exists() and not source.is_symlink() and (target.exists() or target.is_symlink()):
                    remove_results_path(target)
            except BaseException as restore_exc:  # aqg: top-level boundary - recovery backup retains any unrestored prior output
                failures.append(f"{name}: {restore_exc}")
        if failures:
            raise RuntimeError(f"Result replacement failed; prior owned outputs remain at recovery path {backup}: {'; '.join(failures)}") from exc
        shutil.rmtree(backup)
        raise
    else:
        shutil.rmtree(backup)


def markdown_text(value: Any) -> str:
    text = html.escape(str(value), quote=False)
    text = text.replace("|", "&#124;").replace("[", "&#91;").replace("]", "&#93;").replace("(", "&#40;").replace(")", "&#41;")
    text = text.replace(chr(96), "&#96;").replace("*", "&#42;").replace("_", "&#95;").replace("~", "&#126;")
    return text.replace(chr(13) + chr(10), chr(10)).replace(chr(10), "<br>")


def markdown_link(label: Any, destination: str) -> str:
    href = html.escape(quote(destination, safe="/._-"), quote=True)
    return f'<a href="{href}">{markdown_text(label)}</a>'


def read_question(study_root: Path) -> str:
    reasoning_path = study_root / "spec" / "reasoning.md"
    if not reasoning_path.is_file():
        return f"Study: {study_root.name}"
    content = reasoning_path.read_text(encoding="utf-8")
    # Search for question section
    m = re.search(r"##\s*1\.\s*Scientific Question\s*\n+(.*?)(?=\n##|\Z)", content, re.DOTALL)
    if m and m.group(1).strip():
        return m.group(1).strip()
    # Fallback to first paragraph
    lines = [line.strip() for line in content.splitlines() if line.strip() and not line.startswith("#")]
    return lines[0] if lines else f"Study: {study_root.name}"


def load_yaml_lock(lock_path: Path) -> dict[str, Any]:
    data = yaml_load(lock_path)
    if not isinstance(data, dict):
        raise ValueError(f"Run lock must contain a YAML mapping: {lock_path}")
    return data


def extract_plan_data(plan_path: Path, *, source_text: str | None = None) -> dict[str, Any]:
    """Load the explicit result-plan contract; malformed data never falls back to heuristics."""
    text = source_text if source_text is not None else plan_path.read_text(encoding="utf-8")
    match = re.search(r'<textarea id="am-source"[^>]*>(.*?)</textarea>', text, re.DOTALL)
    if match:
        text = match.group(1).strip()
    frontmatter = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    payload = frontmatter.group(1) if frontmatter else text
    try:
        import yaml  # type: ignore
    except ImportError as exc:
        raise RuntimeError("PyYAML is required to read result plans; install it in the supported project environment.") from exc
    try:
        parsed = yaml.safe_load(payload)
    except yaml.YAMLError as exc:
        raise ValueError(f"Malformed result plan YAML: {exc}") from exc
    if not isinstance(parsed, dict):
        raise ValueError("Result plan must contain a YAML mapping")
    if "schema_version" not in parsed:
        raise ValueError("Result plan is missing required field: schema_version")
    if type(parsed.get("schema_version")) is not int or parsed["schema_version"] != 1:
        raise ValueError(f"Unsupported result plan schema_version: {parsed.get('schema_version')!r}; expected 1")
    required = {"schema_version", "plan_id", "revision", "decision_source", "run_bindings", "assessments", "questions", "views", "observations"}
    if required - parsed.keys():
        raise ValueError(f"Result plan is missing required fields: {sorted(required - parsed.keys())}")
    if not isinstance(parsed["plan_id"], str) or not parsed["plan_id"].strip() or type(parsed["revision"]) is not int or parsed["revision"] < 1:
        raise ValueError("Result plan requires a non-empty plan_id and positive integer revision")
    if not isinstance(parsed["decision_source"], str) or not parsed["decision_source"].strip():
        raise ValueError("Result plan requires a decision_source")
    if not isinstance(parsed["run_bindings"], list) or not parsed["run_bindings"]:
        raise ValueError("Result plan requires run_bindings")
    bindings = {}
    for item in parsed["run_bindings"]:
        if not isinstance(item, dict) or not isinstance(item.get("run_id"), str) or not isinstance(item.get("lock_sha256"), str) or not re.fullmatch(r"[0-9a-f]{64}", item["lock_sha256"]):
            raise ValueError("Malformed result plan run binding")
        if item["run_id"] in bindings:
            raise ValueError(f"Duplicate result plan run binding: {item['run_id']}")
        bindings[item["run_id"]] = item["lock_sha256"]
    assessments = parsed["assessments"]
    if not isinstance(assessments, dict) or not assessments or any(not isinstance(k, str) or not isinstance(v, str) or v not in ASSESSMENT_DISPOSITIONS for k, v in assessments.items()):
        raise ValueError("Result plan assessments must explicitly map scoped evidence IDs to valid dispositions")
    questions = parsed["questions"]
    if not isinstance(questions, list) or not questions:
        raise ValueError("Result plan questions must be a non-empty list")
    question_ids = set()
    for question in questions:
        if not isinstance(question, dict) or any(not isinstance(question.get(field), str) or not question[field].strip() for field in ("question_id", "text", "source_heading")):
            raise ValueError("Each result-plan question requires question_id, text, and source_heading")
        if question["question_id"] in question_ids:
            raise ValueError(f"Duplicate result-plan question ID: {question['question_id']}")
        question_ids.add(question["question_id"])
        if not isinstance(question.get("evidence_ids"), list) or not question["evidence_ids"] or any(not isinstance(ref, str) or not ref.strip() for ref in question["evidence_ids"]) or len(set(question["evidence_ids"])) != len(question["evidence_ids"]):
            raise ValueError(f"Result-plan question {question['question_id']} requires evidence_ids")
    views = parsed["views"]
    if not isinstance(views, list):
        raise ValueError("Result plan views must be a list; use [] when none are selected")
    view_ids = set()
    for view in views:
        if not isinstance(view, dict) or any(not isinstance(view.get(field), str) or not view[field].strip() for field in ("view_id", "evidence_id", "label")):
            raise ValueError("Each result-plan view requires view_id, evidence_id, and label")
        if view["view_id"] in view_ids:
            raise ValueError(f"Duplicate result-plan view ID: {view['view_id']}")
        view_ids.add(view["view_id"])
    observations = parsed["observations"]
    if not isinstance(observations, list):
        raise ValueError("Result plan observations must be a list; use [] when none are supplied")
    observation_ids = set()
    for observation in observations:
        fields = ("observation_id", "question_id", "label", "value", "unit", "method", "limits")
        if not isinstance(observation, dict) or any(not isinstance(observation.get(field), str) or not observation[field].strip() for field in fields):
            raise ValueError(f"Each supplied observation requires non-empty fields: {', '.join(fields)}")
        if observation["observation_id"] in observation_ids:
            raise ValueError(f"Duplicate result-plan observation ID: {observation['observation_id']}")
        observation_ids.add(observation["observation_id"])
        if observation["question_id"] not in question_ids:
            raise ValueError(f"Observation {observation['observation_id']} references unknown question_id {observation['question_id']}")
        if not isinstance(observation.get("evidence_ids"), list) or not observation["evidence_ids"] or any(not isinstance(ref, str) or not ref.strip() for ref in observation["evidence_ids"]):
            raise ValueError(f"Observation {observation['observation_id']} requires evidence_ids")
    interpretation = parsed.get("interpretation", "")
    interpretation_source = parsed.get("interpretation_source")
    if interpretation and (not isinstance(interpretation_source, str) or interpretation_source not in {"human", "model"}):
        raise ValueError("Result plan interpretation requires interpretation_source: human or model")
    return {"run_ids": list(bindings), "lock_digests": bindings, "assessments": assessments,
            "interpretation": interpretation, "interpretation_source": interpretation_source, "plan_id": parsed["plan_id"],
            "revision": parsed["revision"], "decision_source": parsed["decision_source"],
            "questions": questions, "views": views, "observations": observations}


def parse_assessments(assess_args: list[str] | None) -> dict[str, str]:
    res: dict[str, str] = {}
    if not assess_args:
        return res
    for item in assess_args:
        if "=" not in item:
            raise ValueError(f"Invalid assessment format: {item}. Expected key=DISPOSITION")
        k, v = item.split("=", 1)
        k, v = k.strip(), v.strip().upper()
        if k in res:
            raise ValueError(f"Duplicate assessment key: {k}")
        if v not in ASSESSMENT_DISPOSITIONS:
            raise ValueError(f"Unknown disposition '{v}'. Allowed: {', '.join(sorted(ASSESSMENT_DISPOSITIONS))}")
        res[k] = v
    return res


def compose_result(
    study_root: Path,
    run_ids: list[str],
    assessments: dict[str, str] | None = None,
    replace_result: bool = False,
    interpret: str | None = None,
    dry_run: bool = False,
    authorization: str | None = None,
    lock_bindings: dict[str, str] | None = None,
    plan_identity: dict[str, Any] | None = None,
    interpretation_source: str | None = None,
    result_plan: dict[str, Any] | None = None,
    plan_snapshot: dict[str, str] | None = None,
    project_root: Path | None = None,
) -> Path | dict[str, Any]:
    study_root = study_root.resolve()
    if project_root is None:
        raise ValueError("Explicit project_root is required to validate declared input paths")
    project_root = project_root.resolve()
    if not study_root.is_dir():
        raise FileNotFoundError(f"Study root not found: {study_root}")
    if not run_ids:
        raise ValueError("At least one run ID is required")
    if interpret is not None and not isinstance(interpret, str):
        raise ValueError("interpretation must be a string")
    if plan_identity is not None or result_plan is not None or plan_snapshot is not None:
        if not isinstance(plan_identity, dict) or not isinstance(plan_snapshot, dict) or not isinstance(plan_snapshot.get("content"), str):
            raise ValueError("Plan-based Compose requires identity and text snapshot of the selected plan")
        snapshot_digest = hashlib.sha256(plan_snapshot["content"].encode("utf-8")).hexdigest()
        if snapshot_digest != plan_snapshot.get("sha256") or snapshot_digest != plan_identity.get("sha256"):
            raise ValueError("Selected result plan snapshot digest mismatch")
        snapshot_path = plan_snapshot.get("path")
        if not isinstance(snapshot_path, str) or snapshot_path != plan_identity.get("path"):
            raise ValueError("Plan identity path does not match digest-bound snapshot")
        parsed_plan = extract_plan_data(Path(snapshot_path), source_text=plan_snapshot["content"])
        expected_identity = {"plan_id": parsed_plan["plan_id"], "revision": parsed_plan["revision"], "decision_source": parsed_plan["decision_source"], "path": snapshot_path, "sha256": snapshot_digest}
        if plan_identity != expected_identity:
            raise ValueError("Plan identity does not match digest-bound snapshot")
        if run_ids != parsed_plan["run_ids"] or lock_bindings != parsed_plan["lock_digests"]:
            raise ValueError("Selected runs or lock bindings do not match digest-bound plan snapshot")
        if assessments != parsed_plan["assessments"]:
            raise ValueError("Assessments do not match digest-bound plan snapshot")
        expected_result_plan = {field: parsed_plan[field] for field in ("questions", "views", "observations")}
        if result_plan != expected_result_plan:
            raise ValueError("Result plan questions, views, or observations do not match digest-bound snapshot")
        expected_interpretation = parsed_plan["interpretation"] or None
        if interpret != expected_interpretation:
            raise ValueError("Interpretation does not match digest-bound plan snapshot")
        if interpretation_source != parsed_plan["interpretation_source"]:
            raise ValueError("Interpretation source does not match digest-bound plan snapshot")

    assess_map = assessments or {}
    if (plan_identity is not None or result_plan is not None) and not (authorization and authorization.strip()):
        raise ValueError("Explicit human authorization is required for plan-based Compose")
    if assess_map and not (authorization and authorization.strip()):
        raise ValueError("Explicit human authorization is required for artifact dispositions")
    if len(set(run_ids)) != len(run_ids):
        raise ValueError("Duplicate selected run ID")
    results_dir = study_root / "results"
    result_md = results_dir / "RESULT.md"
    ledger_json = results_dir / "evidence-ledger.json"
    if results_dir.is_symlink():
        raise ValueError(f"Symlinked results root is not allowed: {results_dir}")
    owned_paths = [results_dir / name for name in ("RESULT.md", "evidence-ledger.json", "artifacts")]
    for path in owned_paths:
        if path.is_symlink():
            raise ValueError(f"symlinked Compose-owned output is not allowed: {path}")
    if not dry_run and not replace_result and any(path.exists() for path in owned_paths):
        raise FileExistsError(f"Compose-owned results already exist under {results_dir}. Pass replace_result=True to overwrite.")

    # 1. Load run locks
    selected_locks = []
    for rid in run_ids:
        lock_data, lock_path, lock_digest = validate_run(study_root, rid, project_root)
        if lock_bindings is not None and lock_bindings.get(rid) != lock_digest:
            raise ValueError(f"Result plan lock binding mismatch for run {rid}")
        selected_locks.append((lock_data, lock_path, lock_digest))
    if lock_bindings is not None and set(lock_bindings) != set(run_ids):
        raise ValueError("Result plan run bindings must exactly match selected runs")

    # 2. Collect outputs and verify hashes
    records = []
    scoped_keys = set()
    for lock, _, lock_digest in selected_locks:
        rid = lock["run_id"]
        run_dir = study_root / "runs" / rid
        for out in lock.get("outputs", []):
            if out.get("role") == "log":
                continue
            path_rel = out.get("path")
            if not path_rel:
                continue
            expected_hash = out.get("sha256")
            actual_file = safe_path(run_dir, path_rel)
            if not actual_file.is_file():
                raise FileNotFoundError(f"Output file missing for run {rid}: {actual_file}")
            actual_hash = sha256_file(actual_file)
            if expected_hash and actual_hash != expected_hash:
                raise ValueError(f"SHA-256 hash mismatch for {actual_file}: expected {expected_hash}, got {actual_hash}")

            obj_id = out.get("object_id") or path_rel
            scoped_key = f"{rid}/{obj_id}"
            scoped_keys.add(scoped_key)

            # Determine disposition
            decision = assess_map.get(scoped_key)
            if decision is None and obj_id in assess_map:
                raise ValueError(f"Unscoped assessment for {obj_id}; use {scoped_key}")
            if decision not in DISPOSITIONS - {"MISSING"}:
                raise ValueError(f"Explicit valid disposition required for {scoped_key}")
            records.append({
                "run_id": rid,
                "output": out,
                "path": path_rel,
                "object_id": obj_id,
                "role": out.get("role", "analysis-output"),
                "sha256": actual_hash,
                "lock_sha256": lock_digest,
                "decision_source": plan_identity["decision_source"] if plan_identity else "CLI authorization",
                "scientific_acceptance": lock.get("scientific_acceptance", "NOT_ASSESSED"),
                "disposition": decision,
                "file_path": actual_file,
            })

    # Validate assess keys
    for k in assess_map:
        if k not in scoped_keys:
            raise ValueError(f"Assessment key '{k}' matches no output in selected runs.")

    records_by_evidence = {f"{r['run_id']}/{r['object_id']}": r for r in records}
    if result_plan is not None:
        question_evidence = {}
        reasoning = study_root / "spec" / "reasoning.md"
        reasoning_text = reasoning.read_text(encoding="utf-8") if reasoning.is_file() else ""
        for question in result_plan["questions"]:
            heading = question["source_heading"].lstrip("# ").strip()
            section_lines = []
            heading_level = None
            found_heading = False
            for line in reasoning_text.splitlines():
                heading_match = re.match(r"^\s*(#{1,6})\s+(.+?)\s*#*\s*$", line)
                if heading_match:
                    level = len(heading_match.group(1))
                    title = heading_match.group(2).strip()
                    if found_heading and level <= heading_level:
                        break
                    if not found_heading and title == heading:
                        found_heading = True
                        heading_level = level
                        continue
                if found_heading:
                    section_lines.append(line)
            if not found_heading:
                raise ValueError(f"Question {question['question_id']} source_heading not found in spec/reasoning.md: {question['source_heading']}")
            def normalized_plan_text(value: str) -> str:
                value = re.sub("[" + chr(96) + "*_~]", "", value)
                value = re.sub(r"^\s*>\s?", "", value, flags=re.MULTILINE)
                value = re.sub(r"^\s*[-+*]\s+", "", value, flags=re.MULTILINE)
                return " ".join(value.split()).casefold()
            question_text = normalized_plan_text(question["text"])
            paragraphs = re.split(r"\n\s*\n", "\n".join(section_lines))
            if not question_text or question_text not in {normalized_plan_text(part) for part in paragraphs}:
                raise ValueError(f"Question {question['question_id']} text does not match content under source_heading {question['source_heading']}")
            missing = [ref for ref in question["evidence_ids"] if ref not in records_by_evidence]
            if missing:
                raise ValueError(f"Question {question['question_id']} references unknown evidence_id(s): {', '.join(missing)}")
            question_evidence[question["question_id"]] = set(question["evidence_ids"])
        for view in result_plan["views"]:
            record = records_by_evidence.get(view["evidence_id"])
            if record is None:
                raise ValueError(f"View {view['view_id']} references unknown evidence_id: {view['evidence_id']}")
            if not any(view["evidence_id"] in refs for refs in question_evidence.values()):
                raise ValueError(f"View {view['view_id']} evidence_id is not bound to a selected question: {view['evidence_id']}")
            if record["disposition"] != "ACCEPTED":
                raise ValueError(f"View {view['view_id']} must reference ACCEPTED evidence: {view['evidence_id']}")
        for observation in result_plan["observations"]:
            if not set(observation["evidence_ids"]).issubset(records_by_evidence):
                missing = sorted(set(observation["evidence_ids"]) - records_by_evidence.keys())
                raise ValueError(f"Observation {observation['observation_id']} references unknown evidence_id(s): {', '.join(missing)}")
            if not set(observation["evidence_ids"]).issubset(question_evidence[observation["question_id"]]):
                raise ValueError(f"Observation {observation['observation_id']} evidence_ids must be bound to question {observation['question_id']}")

    # 3. Assign stable RE identities
    existing_re_map: dict[tuple[str, str], str] = {}
    re_id_high_watermark = 0
    if ledger_json.is_file():
        prior = json.loads(ledger_json.read_text(encoding="utf-8"))
        if not isinstance(prior, dict) or not isinstance(prior.get("records"), list):
            raise ValueError("Existing evidence ledger has an unsupported shape")
        stored_watermark = prior.get("re_id_high_watermark", 0)
        if type(stored_watermark) is not int or stored_watermark < 0:
            raise ValueError("Existing evidence ledger has an invalid re_id_high_watermark")
        re_id_high_watermark = stored_watermark
        seen_re_ids = set()
        for rec in prior["records"]:
            if not isinstance(rec, dict):
                raise ValueError("Existing evidence ledger contains a malformed record")
            prior_re_id = rec.get("re_id")
            match = re.fullmatch(r"RE-(\d+)", prior_re_id) if isinstance(prior_re_id, str) else None
            if not match or int(match.group(1)) < 1 or not isinstance(rec.get("run_id"), str) or not rec["run_id"] or not isinstance(rec.get("path"), str) or not rec["path"]:
                raise ValueError("Existing evidence ledger contains a malformed RE identity or run/path binding")
            key = (rec["run_id"], rec["path"])
            numeric_re_id = int(match.group(1))
            if numeric_re_id in seen_re_ids or key in existing_re_map:
                raise ValueError("Existing evidence ledger contains duplicate RE identity or run/path binding")
            seen_re_ids.add(numeric_re_id)
            existing_re_map[key] = prior_re_id
            re_id_high_watermark = max(re_id_high_watermark, numeric_re_id)

    next_num = re_id_high_watermark + 1

    for rec in records:
        key = (rec["run_id"], rec["path"])
        if key in existing_re_map:
            rec["re_id"] = existing_re_map[key]
        else:
            rec["re_id"] = f"RE-{next_num:02d}"
            existing_re_map[key] = rec["re_id"]
            next_num += 1

    question_text = "\n".join(q["text"] for q in result_plan["questions"]) if result_plan else read_question(study_root)

    # If dry-run requested, output preview without writing files
    if dry_run:
        print("=== COMPOSE PREVIEW (DRY-RUN) ===")
        print(f"Study: {study_root.name}")
        print(f"Question: {question_text}")
        print(f"Selected Runs: {', '.join(run_ids)}")
        print("Planned Output Dispositions:")
        for rec in records:
            dest = f"artifacts/{rec['run_id']}/{rec['path']}" if rec['disposition'] == 'ACCEPTED' else "(not staged)"
            print(f"  - [{rec['re_id']}] {rec['object_id']} -> {rec['disposition']} -> {dest}")
        print(f"Summary: {sum(1 for r in records if r['disposition'] == 'ACCEPTED')} ACCEPTED, {sum(1 for r in records if r['disposition'] != 'ACCEPTED')} OTHER")
        print("All SHA-256 hashes verified successfully.")
        return {
            "study": study_root.name,
            "question": question_text,
            "run_ids": run_ids,
            "records": records,
            "result_plan": result_plan,
        }

    # 4. Stage only Compose-owned outputs; unrelated result children remain in place.
    with tempfile.TemporaryDirectory(prefix=".compose-transaction-", dir=study_root) as tmp:
        staging_dir = Path(tmp) / "owned-results"
        staging_dir.mkdir()
        artifacts_dir = staging_dir / "artifacts"
        artifacts_dir.mkdir()

        # Stage accepted artifacts
        for rec in records:
            if rec["disposition"] == "ACCEPTED":
                dest = safe_path(artifacts_dir, f"{rec['run_id']}/{rec['path']}")
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(rec["file_path"], dest)
                if sha256_file(dest) != rec["sha256"]:
                    raise ValueError(f"Staged artifact hash mismatch: {dest}")

        # Render RESULT.md
        md_lines = ["# Result", ""]
        if result_plan:
            md_lines.extend(["## Selected Questions", "", "> From [spec/reasoning.md](../spec/reasoning.md).", ""])
            for question in result_plan["questions"]:
                refs = ", ".join(f"`{records_by_evidence[ref]['re_id']}`" for ref in question["evidence_ids"])
                md_lines.extend([
                    f"### {markdown_text(question['question_id'])}: {markdown_text(question['text'])}",
                    "",
                    f"Source heading {markdown_text(question['source_heading'])}. Evidence: {refs}.",
                    "",
                ])
        else:
            md_lines.extend(["## Question", "", "> From [spec/reasoning.md](../spec/reasoning.md).", "", f"**{markdown_text(question_text)}**", ""])
        md_lines.extend(["## Selected Scope", ""])
        for rid in run_ids:
            md_lines.append(f"- Run `{rid}` ([run.lock.yaml](../runs/{rid}/run.lock.yaml), status verified: COMPLETED).")
        md_lines.extend(["", "## Summary", "", "Artifact dispositions select evidence for use; they do not imply scientific acceptance.", "", "| Evidence ID | View / Stem | Run | Disposition | Scientific Acceptance | File Link |", "|---|---|---|---|---|---|"])

        for rec in records:
            dest_rel = f"artifacts/{rec['run_id']}/{rec['path']}" if rec["disposition"] == "ACCEPTED" else f"../runs/{rec['run_id']}/{rec['path']}"
            md_lines.append(f"| {markdown_text(rec['re_id'])} | {markdown_text(Path(rec['path']).name)} | {markdown_text(rec['run_id'])} | {markdown_text(rec['disposition'])} | {markdown_text(rec['scientific_acceptance'])} | {markdown_link(Path(rec['path']).name, dest_rel)} |")

        if result_plan:
            md_lines.extend(["", "## Selected Views", "", "| View | Evidence | Label |", "|---|---|---|"])
            for view in result_plan["views"]:
                record = records_by_evidence[view["evidence_id"]]
                view_path = f"artifacts/{record['run_id']}/{record['path']}"
                md_lines.append(f"| {markdown_text(view['view_id'])} | {markdown_text(record['re_id'])} | {markdown_link(view['label'], view_path)} |")
            md_lines.extend(["", "## Supplied Observations", ""])
            if result_plan["observations"]:
                for observation in result_plan["observations"]:
                    refs = ", ".join(f"`{records_by_evidence[ref]['re_id']}`" for ref in observation["evidence_ids"])
                    md_lines.append(f"- {markdown_text(observation['observation_id'])} ({markdown_text(observation['question_id'])}): **{markdown_text(observation['label'])}** = {markdown_text(observation['value'])} {markdown_text(observation['unit'])}; method: {markdown_text(observation['method'])}; limits: {markdown_text(observation['limits'])}; evidence: {refs}.")
            else:
                md_lines.append("No quantitative or qualitative observations were supplied in the Result Plan.")

        md_lines.extend([
            "",
            "## Limits & Dispositions",
            "",
            f"- Total outputs evaluated: {len(records)}.",
            f"- Accepted artifacts staged: {sum(1 for r in records if r['disposition'] == 'ACCEPTED')}.",
            f"- Ambiguous / Rejected: {sum(1 for r in records if r['disposition'] in ('AMBIGUOUS', 'REJECTED'))}.",
            "- Process note: Materialized strictly from immutable run locks. No recalculation performed.",
        ])

        if interpret and interpret.strip():
            md_lines.extend([
                "",
                "## Interpretation",
                "",
                f"> Source: {interpretation_source or 'CLI-provided; authorship not independently verified'}. Scientific acceptance remains NOT_ASSESSED unless separately recorded in the run lock.",
                "",
                markdown_text(interpret.strip()),
            ])

        (staging_dir / "RESULT.md").write_text("\n".join(md_lines) + "\n", encoding="utf-8")

        # Render evidence-ledger.json
        ledger = {
            "ledger_version": 1,
            "re_id_high_watermark": max(re_id_high_watermark, next_num - 1),
            "study": study_root.name,
            "plan": plan_identity,
            "plan_snapshot": plan_snapshot,
            "result_plan": result_plan,
            "authorization": authorization,
            "interpretation_source": interpretation_source or ("CLI-provided; authorship not independently verified" if interpret else None),
            "runs": [{"run_id": rid, "lock": f"runs/{rid}/run.lock.yaml", "lock_sha256": digest} for rid, _, digest in selected_locks],
            "records": [
                {
                    "re_id": r["re_id"],
                    "run_id": r["run_id"],
                    "path": r["path"],
                    "object_id": r["object_id"],
                    "role": r["role"],
                    "sha256": r["sha256"],
                    "lock_sha256": r["lock_sha256"],
                    "decision_source": r["decision_source"],
                    "disposition": r["disposition"],
                    "scientific_acceptance": r["scientific_acceptance"],
                }
                for r in records
            ],
            "interpretation": interpret.strip() if interpret else None,
        }
        (staging_dir / "evidence-ledger.json").write_text(json.dumps(ledger, indent=2) + "\n", encoding="utf-8")

        publish_results(staging_dir, results_dir)

    return result_md


def main() -> int:
    parser = argparse.ArgumentParser(description="Compose study results into RESULT.md and evidence ledger.")
    parser.add_argument("study_root", help="Path to study root directory")
    parser.add_argument("--project-root", required=True, help="Explicit project root used to resolve declared input paths")
    parser.add_argument("--plan", help="Path to Result Synthesis Plan (HTML or YAML)")
    parser.add_argument("--run-id", action="append", dest="run_ids", help="Run ID(s) to include; with --plan they must exactly match its selected runs")
    parser.add_argument("--assess", action="append", help="Disposition: key=ACCEPTED|REJECTED|AMBIGUOUS|SUPERSEDED")
    parser.add_argument("--replace-result", action="store_true", help="Replace existing Compose-owned results")
    parser.add_argument("--interpret", help="Verbatim scientist interpretation note")
    parser.add_argument("--authorization", help="Required for plan-based Compose and artifact dispositions; recorded in evidence-ledger.json")
    parser.add_argument("--check", action="store_true", help="Preview composition and verify hashes without writing")

    args = parser.parse_args()
    try:
        run_ids = list(args.run_ids or [])
        assessments = parse_assessments(args.assess)
        interpret = args.interpret
        interpretation_source = None
        lock_bindings = None
        plan_identity = None
        authorization = args.authorization
        result_plan = None
        plan_snapshot = None

        if args.plan:
            if args.assess:
                raise ValueError("--assess cannot be combined with --plan; use the selected plan assessments")
            plan_path = Path(args.plan)
            if not plan_path.is_file():
                raise FileNotFoundError(f"Result plan not found: {plan_path}")
            plan_bytes = plan_path.read_bytes()
            plan_text = plan_bytes.decode("utf-8")
            plan_digest = hashlib.sha256(plan_bytes).hexdigest()
            p_data = extract_plan_data(plan_path, source_text=plan_text)
            plan_run_ids = p_data["run_ids"]
            if run_ids and run_ids != plan_run_ids:
                raise ValueError("CLI --run-id selection conflicts with the selected result plan")
            if not run_ids:
                run_ids = plan_run_ids
            lock_bindings = p_data["lock_digests"]
            plan_identity = {"plan_id": p_data["plan_id"], "revision": p_data["revision"], "decision_source": p_data["decision_source"], "path": str(plan_path), "sha256": plan_digest}
            plan_snapshot = {"path": str(plan_path), "sha256": plan_digest, "content": plan_text}
            result_plan = {field: p_data[field] for field in ("questions", "views", "observations")}
            assessments = p_data["assessments"]
            if args.interpret and p_data.get("interpretation") and args.interpret.strip() != p_data["interpretation"].strip():
                raise ValueError("CLI interpretation conflicts with selected result plan")
            if p_data.get("interpretation"):
                interpret = p_data["interpretation"]
                interpretation_source = p_data.get("interpretation_source")

        if args.plan and not (authorization and authorization.strip()):
            raise ValueError("Explicit --authorization is required for plan-based Compose")

        if not run_ids:
            raise ValueError("No run IDs provided. Pass --run-id <id> or specify run_ids in --plan.")

        res = compose_result(
            Path(args.study_root),
            run_ids,
            assessments=assessments,
            replace_result=args.replace_result,
            interpret=interpret,
            dry_run=args.check,
            authorization=authorization,
            lock_bindings=lock_bindings,
            plan_identity=plan_identity,
            interpretation_source=interpretation_source,
            result_plan=result_plan,
            plan_snapshot=plan_snapshot,
            project_root=Path(args.project_root),
        )
        if args.check:
            print("COMPOSE_CHECK_OK")
        else:
            print(f"COMPOSE_SUCCESS {res}")
        return 0
    except Exception as exc:
        print(f"COMPOSE_ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
