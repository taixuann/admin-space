#!/usr/bin/env python3
"""Scaffold a standard-compliant Study scripts directory from templates.

Usage:
    python .agents/skills/implement-research/scripts/scaffold.py <study-root> [--force]

Creates:
    <study-root>/scripts/
      ├── modules/
      │   ├── __init__.py
      │   ├── data.py
      │   ├── theme.py
      │   └── plot.py
      ├── specific/
      │   ├── __init__.py
      │   └── analysis.py
      ├── tests/
      │   ├── __init__.py
      │   ├── test_reader.py
      │   └── test_analysis.py
      └── run.py
"""

from __future__ import annotations

import argparse
from pathlib import Path
import shutil
import sys

SKILL_DIR = Path(__file__).resolve().parents[1]
TEMPLATES_DIR = SKILL_DIR / "assets" / "templates" / "scripts"


def scaffold_study_scripts(study_root: Path, force: bool = False) -> None:
    study_root = study_root.resolve()
    if not study_root.is_dir():
        raise FileNotFoundError(f"Study root directory does not exist: {study_root}")

    scripts_dir = study_root / "scripts"
    if scripts_dir.exists() and not force:
        print(f"scripts/ already exists in {study_root}. Use --force to overwrite existing files.")

    template_mapping = [
        ("modules/__init__.py.tmpl", "modules/__init__.py"),
        ("modules/data.py.tmpl", "modules/data.py"),
        ("modules/theme.py.tmpl", "modules/theme.py"),
        ("modules/plot.py.tmpl", "modules/plot.py"),
        ("specific/__init__.py.tmpl", "specific/__init__.py"),
        ("specific/analysis.py.tmpl", "specific/analysis.py"),
        ("tests/__init__.py.tmpl", "tests/__init__.py"),
        ("tests/test_reader.py.tmpl", "tests/test_reader.py"),
        ("tests/test_analysis.py.tmpl", "tests/test_analysis.py"),
        ("run.py.tmpl", "run.py"),
    ]

    for tmpl_rel, dest_rel in template_mapping:
        src = TEMPLATES_DIR / tmpl_rel
        if not src.is_file():
            raise FileNotFoundError(f"Template missing: {src}")

        dest = scripts_dir / dest_rel
        dest.parent.mkdir(parents=True, exist_ok=True)

        if dest.exists() and not force:
            print(f"  [skipped] {dest.relative_to(study_root)} (already exists)")
            continue

        shutil.copy2(src, dest)
        # Ensure executable permission for run.py
        if dest.name == "run.py":
            dest.chmod(dest.stat().st_mode | 0o111)
        print(f"  [created] {dest.relative_to(study_root)}")

    print(f"Scaffolding complete for {study_root.name}/scripts/")


def main() -> int:
    parser = argparse.ArgumentParser(description="Scaffold study scripts layout.")
    parser.add_argument("study_root", type=Path, help="Path to study root directory")
    parser.add_argument("--force", "-f", action="store_true", help="Overwrite existing files")
    args = parser.parse_args()

    try:
        scaffold_study_scripts(args.study_root, force=args.force)
        return 0
    except Exception as exc:
        print(f"Error scaffolding scripts: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
