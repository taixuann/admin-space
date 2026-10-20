"""Strict plan-led v1 evidence validation shared by publication commands."""
from __future__ import annotations

import hashlib
import re
from pathlib import Path
from typing import Any

RUN_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")
DIGEST = re.compile(r"^[0-9a-f]{64}$")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def yaml_load(path: Path) -> Any:
    try:
        import yaml
    except ImportError as exc:
        raise RuntimeError("PyYAML is required to read publication evidence; install it in the supported project environment.") from exc
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise ValueError(f"Malformed YAML in {path}: {exc}") from exc


def checked_path(base: Path, value: str, *, allow_absolute: bool = False) -> Path:
    if not isinstance(value, str) or not value.strip():
        raise ValueError("Evidence path must be a non-empty string")
    raw = Path(value)
    if raw.is_absolute():
        if not allow_absolute:
            raise ValueError(f"Absolute evidence path is not allowed: {value}")
        candidate = raw
    else:
        candidate = base / raw
    current = candidate
    while current != current.parent:
        if current.is_symlink():
            raise ValueError(f"Symlinked evidence is not allowed: {current}")
        current = current.parent
    resolved = candidate.resolve(strict=False)
    resolved_base = base.resolve()
    if resolved != resolved_base and resolved_base not in resolved.parents:
        raise ValueError(f"Path traversal detected: {value}")
    return resolved


def verify_file(path: Path, expected: Any, label: str) -> str:
    if not isinstance(expected, str) or not DIGEST.fullmatch(expected):
        raise ValueError(f"Missing or malformed SHA-256 for {label}")
    if not path.is_file():
        raise FileNotFoundError(f"Selected evidence missing for {label}: {path}")
    actual = sha256_file(path)
    if actual != expected:
        raise ValueError(f"SHA-256 mismatch for {label}: expected {expected}, got {actual}")
    return actual


def validate_run(study_root: Path, requested_id: str, project_root: Path, *, verify_inputs: bool = True) -> tuple[dict[str, Any], Path, str]:
    if not isinstance(requested_id, str) or not RUN_ID.fullmatch(requested_id) or requested_id in {".", ".."}:
        raise ValueError(f"Unsafe run ID: {requested_id!r}")
    project_root = project_root.resolve()
    if not project_root.is_dir():
        raise FileNotFoundError(f"Selected project root not found: {project_root}")
    run_dir = checked_path(study_root, f"runs/{requested_id}")
    lock_path = checked_path(study_root, f"runs/{requested_id}/run.lock.yaml")
    if not lock_path.is_file():
        raise FileNotFoundError(f"Run lock not found: {lock_path}")
    lock = yaml_load(lock_path)
    required = {"schema_version", "owner", "run_id", "status", "scientific_acceptance", "started_at", "finished_at", "question", "plan", "input_manifest", "inputs", "parameters", "validation", "code", "environment", "command", "exit_code", "outputs"}
    if not isinstance(lock, dict) or required - lock.keys():
        raise ValueError(f"Unsupported run lock shape; missing {sorted(required - lock.keys()) if isinstance(lock, dict) else 'mapping'}")
    if type(lock["schema_version"]) is not int or lock["schema_version"] != 1 or lock["owner"] != "implement-research":
        raise ValueError("Unsupported run lock schema or owner; expected schema_version 1 owner implement-research")
    if lock["run_id"] != requested_id:
        raise ValueError(f"Run ID mismatch: requested {requested_id}, lock records {lock['run_id']}")
    if lock["status"] != "COMPLETED":
        raise ValueError(f"Run {requested_id} is not COMPLETED")
    if lock["scientific_acceptance"] not in {"NOT_ASSESSED", "ACCEPTED", "REJECTED"}:
        raise ValueError("Invalid scientific_acceptance")
    for field in ("plan", "input_manifest"):
        item = lock[field]
        if not isinstance(item, dict) or not isinstance(item.get("snapshot_path"), str):
            raise ValueError(f"Malformed {field} recovery record")
        if field == "plan" and (type(item.get("revision")) is not int or item["revision"] < 1 or not isinstance(item.get("authorization"), str) or not item["authorization"].strip()):
            raise ValueError("Plan recovery record requires a positive revision and actual authorization")
        checked_path(study_root, item.get("path", ""))
        snapshot = checked_path(study_root, item["snapshot_path"])
        verify_file(snapshot, item.get("sha256"), f"{field} snapshot")
    validation = lock["validation"]
    if not isinstance(validation, dict) or any(validation.get(k) is not True for k in ("inputs_unchanged", "protected_files_unchanged", "required_outputs_valid")):
        raise ValueError("Run validation checks are incomplete")
    if not isinstance(lock["started_at"], str) or not isinstance(lock["finished_at"], str) or not isinstance(lock["question"], str) or not isinstance(lock["parameters"], dict) or not isinstance(lock["environment"], dict) or not isinstance(lock["command"], list) or type(lock["exit_code"]) is not int or lock["exit_code"] != 0:
        raise ValueError("Run lock execution metadata is incomplete or inconsistent")
    if not isinstance(lock["inputs"], list) or not lock["inputs"] or not isinstance(lock["outputs"], list) or not lock["outputs"]:
        raise ValueError("Run inputs and outputs must be non-empty lists")
    manifest_path = checked_path(study_root, lock["input_manifest"]["snapshot_path"])
    manifest = yaml_load(manifest_path)
    if not isinstance(manifest, dict) or manifest.get("schema_version") != 1 or manifest.get("owner") != "implement-research" or not isinstance(manifest.get("inputs"), list):
        raise ValueError("Unsupported input manifest shape; expected schema_version 1 owner implement-research")
    if any(not isinstance(item, dict) or not isinstance(item.get("object_id"), str) or not item["object_id"] or not isinstance(item.get("files"), list) for item in manifest["inputs"]):
        raise ValueError("Malformed input manifest object record")
    if len({item["object_id"] for item in manifest["inputs"]}) != len(manifest["inputs"]):
        raise ValueError("Duplicate input object identity in manifest")
    if {item["object_id"] for item in manifest["inputs"]} != {item.get("object_id") for item in lock["inputs"] if isinstance(item, dict)}:
        raise ValueError("Run input records do not match the input manifest")
    def input_signature(records: list[Any]) -> set[tuple[str, str, str | None, tuple[tuple[str, str], ...]]]:
        result = set()
        for record in records:
            if not isinstance(record, dict) or not isinstance(record.get("object_id"), str) or not isinstance(record.get("role"), str) or not isinstance(record.get("files"), list):
                raise ValueError("Malformed nested input record")
            name = record.get("name")
            if "name" in record and (not isinstance(name, str) or not name.strip()):
                raise ValueError(f"Input {record['object_id']} name must be a non-empty string when supplied")
            files = []
            for item in record["files"]:
                if not isinstance(item, dict) or not isinstance(item.get("path"), str) or not isinstance(item.get("sha256"), str):
                    raise ValueError("Malformed nested input file record")
                files.append((item["path"], item["sha256"]))
            if not files:
                raise ValueError("Input object has no declared files")
            result.add((record["object_id"], record["role"], name.strip() if isinstance(name, str) else None, tuple(sorted(files))))
        return result
    if input_signature(manifest["inputs"]) != input_signature(lock["inputs"]):
        raise ValueError("Run input files do not match the hashed input manifest")
    if verify_inputs:
        for inp in lock["inputs"]:
            if not isinstance(inp, dict) or not isinstance(inp.get("object_id"), str) or not isinstance(inp.get("files"), list) or not inp["files"]:
                raise ValueError("Malformed nested input record")
            for file_info in inp["files"]:
                if not isinstance(file_info, dict):
                    raise ValueError("Malformed input file record")
                path = checked_path(project_root, file_info.get("path", ""), allow_absolute=True)
                verify_file(path, file_info.get("sha256"), "input")
    if not isinstance(lock["code"], dict) or not isinstance(lock["code"].get("files"), list) or not lock["code"]["files"]:
        raise ValueError("Malformed code recovery records")
    for item in lock["code"]["files"]:
        if not isinstance(item, dict) or not isinstance(item.get("snapshot_path"), str):
            raise ValueError("Malformed code recovery record")
        checked_path(study_root, item.get("path", ""))
        snapshot = checked_path(study_root, item["snapshot_path"])
        verify_file(snapshot, item.get("sha256"), "code snapshot")
    identities = set()
    paths = set()
    for output in lock["outputs"]:
        if not isinstance(output, dict) or not isinstance(output.get("object_id"), str) or not isinstance(output.get("path"), str):
            raise ValueError("Malformed output record")
        if not isinstance(output.get("role"), str) or not output["role"].strip():
            raise ValueError("Output role must be a non-empty string")
        if output["object_id"] in identities:
            raise ValueError(f"Duplicate output identity: {output['object_id']}")
        identities.add(output["object_id"])
        if output["path"] in paths:
            raise ValueError(f"Duplicate output path: {output['path']}")
        paths.add(output["path"])
        out_path = checked_path(run_dir, output["path"])
        verify_file(out_path, output.get("sha256"), f"output {output['object_id']}")
    return lock, lock_path, sha256_file(lock_path)
