#!/usr/bin/env python3
"""Render profile capability YAML into Archify HTML views.

This is Admin documentation build automation. It treats every capabilities.yaml
file as untrusted data: it validates the schema, escapes all values, and uses
Archify finalize to publish the HTML. Invalid input or a failed render leaves
the last successful HTML untouched.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[3]
PROFILES = ("secretary", "coordinator")
SECTIONS = ("skills", "plugins", "mcps", "external_tools", "automation")
ALLOWED_TOP_LEVEL = set(SECTIONS) | {
    "profile", "owner", "status", "scope", "notes", "last_reviewed",
}
METADATA_KEYS = ALLOWED_TOP_LEVEL - set(SECTIONS)
ENTRY_EXTRA_KEYS = {"detail", "note", "description"}


class DuplicateKeyError(ValueError):
    """Raised when a YAML mapping contains a duplicate key."""


class StrictLoader(yaml.SafeLoader):
    pass


def _construct_mapping(loader, node, deep=False):
    keys = []
    for key_node, _value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in keys:
            raise DuplicateKeyError(f"duplicate YAML key: {key!r}")
        keys.append(key)
    return yaml.SafeLoader.construct_mapping(loader, node, deep=deep)


StrictLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _construct_mapping
)


def load_yaml_text(text: str) -> Any:
    return yaml.load(text, Loader=StrictLoader)


def validate(data: Any, profile: str | None = None) -> dict[str, Any]:
    if not isinstance(data, dict):
        raise ValueError("capabilities YAML must be a mapping")
    unknown = set(data) - ALLOWED_TOP_LEVEL
    if unknown:
        raise ValueError(f"unsupported top-level section(s): {sorted(unknown)}")
    for section in SECTIONS:
        if section not in data:
            raise ValueError(f"missing required section: {section}")
        value = data[section]
        if not isinstance(value, list):
            raise ValueError(f"section {section!r} must be a list")
        for item in value:
            if isinstance(item, str):
                continue
            if isinstance(item, dict):
                if "name" not in item or not isinstance(item["name"], str):
                    raise ValueError(f"entry in {section!r} must have a string 'name'")
                for key in item:
                    if key not in ({"name"} | ENTRY_EXTRA_KEYS):
                        raise ValueError(
                            f"unsupported entry key {key!r} in {section!r}"
                        )
                    if not isinstance(item[key], str):
                        raise ValueError(
                            f"entry field {key!r} in {section!r} must be a string"
                        )
            else:
                raise ValueError(f"entry in {section!r} must be a string or mapping")
    for key in METADATA_KEYS:
        if key in data and not isinstance(data[key], str):
            raise ValueError(f"metadata field {key!r} must be a string")
    if profile is not None and "profile" in data and data["profile"] != profile:
        raise ValueError(
            f"profile metadata {data['profile']!r} does not match {profile!r}"
        )
    return data


def entry_text(item: Any) -> str:
    if isinstance(item, str):
        return item
    text = item["name"]
    extras = [item[key] for key in ("detail", "note", "description") if item.get(key)]
    if extras:
        text = f"{text} ({'; '.join(extras)})"
    return text


def _inline_code(text: str) -> str:
    text = " ".join(str(text).split())
    escaped_pipe = text.replace("|", "\\|")
    escaped_pipe = escaped_pipe.replace("<", "&lt;").replace(">", "&gt;")
    runs = re.findall(r"`+", escaped_pipe)
    fence_len = max((len(run) for run in runs), default=0) + 1
    fence = "`" * fence_len
    return f"{fence}{escaped_pipe}{fence}"


def _escape_table_cell(text: str) -> str:
    return _inline_code(text)


def render_candidate(data: dict[str, Any], profile: str) -> str:
    # Fixed, safe heading: profile is validated to secretary/coordinator.
    lines: list[str] = []
    lines.append(f"# {profile.title()} capabilities {{#{profile}-capabilities}}")
    lines.append("")
    lines.append(
        "Approved target capabilities for this profile. Generated from "
        "`capabilities.yaml`; describes desired targets, not live runtime status."
    )
    lines.append("")
    metadata_rows = []
    for key in ("profile", "status", "scope", "notes", "owner", "last_reviewed"):
        if key in data and data[key]:
            metadata_rows.append((key.replace("_", " ").title(), data[key]))
    if metadata_rows:
        lines.append("## Profile metadata {#profile-metadata}")
        lines.append("")
        lines.append("@facts id=profile-facts")
        lines.append("| Label | Value |")
        for label, value in metadata_rows:
            lines.append(f"| {_inline_code(label)} | {_escape_table_cell(value)} |")
        lines.append("")
    lines.append("@answer scope=" + json.dumps(
        f"{profile} profile · approved targets · not live runtime status",
        ensure_ascii=False,
    ))
    lines.append("")
    for section in SECTIONS:
        lines.append(f"## {section.replace('_', ' ').title()} {{#{section}}}")
        lines.append("")
        entries = [entry_text(item) for item in data[section]]
        lines.append("| Capability | Details |")
        lines.append("| --- | --- |")
        if entries:
            for entry in entries:
                lines.append(f"| {_escape_table_cell(entry)} | Approved target |")
        else:
            lines.append("| (none) | No approved targets |")
        lines.append("")
    lines.append(
        "Empty sections mean no approved targets are selected for that category."
    )
    lines.append("")
    return "\n".join(lines)


def _node_binary() -> str:
    found = shutil.which("node")
    return found or "node"


def _archify_cli(repo_root: Path) -> Path:
    candidate = repo_root / "skills" / "archify" / "bin" / "archify.mjs"
    if candidate.is_file():
        return candidate
    installed = Path("/Users/tai/.agents/skills/archify/bin/archify.mjs")
    if installed.is_file():
        return installed
    return candidate


def resolve_archify_cli(repo_root: Path, override: str | None = None) -> Path:
    if override:
        return Path(override)
    env = os.environ.get("ARCHIFY_CLI")
    if env:
        return Path(env)
    return _archify_cli(repo_root)


def yaml_path(repo_root: Path, profile: str) -> Path:
    return repo_root / "docs" / "profiles" / profile / "capabilities.yaml"


def output_path(repo_root: Path, profile: str) -> Path:
    if profile == "secretary":
        return repo_root / ".archify" / "profile-capabilities-secretary" / "capabilities.html"
    return repo_root / "docs" / "profiles" / profile / "capabilities.html"


def staging_dir(repo_root: Path, profile: str) -> Path:
    return repo_root / ".archify" / f"profile-capabilities-{profile}"


def build_profile(
    profile: str,
    repo_root: Path | str = REPO_ROOT,
    archify_cli: str | None = None,
) -> dict[str, Any]:
    repo_root = Path(repo_root)
    cli = resolve_archify_cli(repo_root, archify_cli)
    node = _node_binary()
    src = yaml_path(repo_root, profile)
    text = src.read_text(encoding="utf-8")
    data = load_yaml_text(text)
    validate(data, profile)
    candidate = render_candidate(data, profile)
    stage = staging_dir(repo_root, profile)
    stage.mkdir(parents=True, exist_ok=True)
    candidate_path = stage / "candidate.archify.md"
    candidate_path.write_text(candidate, encoding="utf-8")
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    (stage / "source.sha256").write_text(digest + "\n", encoding="utf-8")

    # Validate before finalizing.
    validate_proc = subprocess.run(
        [node, str(cli), "validate", "explainer", str(candidate_path), "--json", "--writing", "warn"],
        cwd=str(repo_root),
        capture_output=True,
        text=True,
    )
    if validate_proc.returncode != 0:
        raise RuntimeError(
            "Archify validation failed:\n"
            + (validate_proc.stdout or "")
            + (validate_proc.stderr or "")
        )

    out = output_path(repo_root, profile)
    out.parent.mkdir(parents=True, exist_ok=True)
    candidate_sha = hashlib.sha256(candidate.encode("utf-8")).hexdigest()
    finalize_proc = subprocess.run(
        [
            node, str(cli), "finalize", "explainer", str(candidate_path), str(out),
            "--json", "--out-dir", str(stage), "--candidate-sha256", candidate_sha,
            "--writing", "warn",
        ],
        cwd=str(repo_root),
        capture_output=True,
        text=True,
    )
    if finalize_proc.returncode != 0:
        raise RuntimeError(
            "Archify finalize failed:\n"
            + (finalize_proc.stdout or "")
            + (finalize_proc.stderr or "")
        )
    try:
        result = json.loads(finalize_proc.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Could not parse Archify result: {exc}") from exc
    return {
        "profile": profile,
        "candidate": str(candidate_path),
        "output": str(out),
        "source_digest": digest,
        "candidate_sha256": candidate_sha,
        "finalize": result,
    }


def build_all(profiles, repo_root=REPO_ROOT, archify_cli=None):
    results = {}
    errors = {}
    for profile in profiles:
        try:
            results[profile] = build_profile(profile, repo_root, archify_cli)
        except Exception as exc:  # noqa: BLE001 - preserve last good artifact
            errors[profile] = str(exc)
    return results, errors


def run_watch_iteration(profiles, state, repo_root=REPO_ROOT, archify_cli=None):
    """One polling iteration. Mutates and returns state dict."""
    state = dict(state or {})
    digests = state.setdefault("digests", {})
    for profile in profiles:
        src = yaml_path(repo_root, profile)
        try:
            text = src.read_text(encoding="utf-8")
            digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
        except OSError:
            digest = None
        if digests.get(profile) == digest:
            continue
        digests[profile] = digest
        try:
            build_profile(profile, repo_root, archify_cli)
            print(f"[profile-capabilities] rebuilt {profile}", flush=True)
        except Exception as exc:  # noqa: BLE001
            print(f"[profile-capabilities] {profile} build failed: {exc}", flush=True)
    return state


def validate_interval(value: Any) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError("interval must be a number") from exc
    if not math.isfinite(number) or number <= 0:
        raise ValueError("--interval must be finite and greater than zero")
    return number


def _argparse_interval(value: str) -> float:
    try:
        return validate_interval(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(str(exc)) from exc


def watch(profiles, interval=1.0, repo_root=REPO_ROOT, archify_cli=None):
    interval = validate_interval(interval)
    state = {"digests": {}}
    # Initial pass.
    run_watch_iteration(profiles, state, repo_root, archify_cli)
    while True:
        time.sleep(interval)
        run_watch_iteration(profiles, state, repo_root, archify_cli)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--once", action="store_true", help="render once (default)")
    parser.add_argument("--watch", action="store_true", help="watch YAML files and rebuild")
    parser.add_argument("--profile", choices=PROFILES, help="single profile (default: both)")
    parser.add_argument(
        "--interval", type=_argparse_interval, default=1.0,
        help="watch poll interval seconds (finite and > 0)",
    )
    parser.add_argument("--repo-root", default=None, help="override repository root")
    parser.add_argument("--archify-cli", default=None, help="override Archify CLI path")
    args = parser.parse_args(argv)

    repo_root = Path(args.repo_root) if args.repo_root else REPO_ROOT
    profiles = (args.profile,) if args.profile else PROFILES

    if args.watch:
        try:
            watch(profiles, args.interval, repo_root, args.archify_cli)
        except KeyboardInterrupt:
            return 0
        return 0

    # Default is --once.
    results, errors = build_all(profiles, repo_root, args.archify_cli)
    for profile, result in results.items():
        print(json.dumps(result, indent=2))
    if errors:
        for profile, error in errors.items():
            print(f"{profile}: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
