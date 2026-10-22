"""Bridge Configuration Manager: Loads, saves, and updates YAML track files."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict, List, Optional
import yaml

DEFAULT_CONFIG_DIR = Path(__file__).resolve().parent.parent / "config"
DEFAULT_GITHUB_CONFIG = DEFAULT_CONFIG_DIR / "github-track.yaml"
DEFAULT_DRIVE_CONFIG = DEFAULT_CONFIG_DIR / "drive-track.yaml"


def load_github_config(path: Optional[Path] = None) -> Dict[str, Any]:
    cfg_path = Path(path) if path else DEFAULT_GITHUB_CONFIG
    if cfg_path.exists():
        with open(cfg_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
            return data

    return {"version": 1, "settings": {}, "workspaces": []}


def save_github_config(data: Dict[str, Any], path: Optional[Path] = None) -> None:
    cfg_path = Path(path) if path else DEFAULT_GITHUB_CONFIG
    cfg_path.parent.mkdir(parents=True, exist_ok=True)
    with open(cfg_path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)


def load_drive_config(path: Optional[Path] = None) -> Dict[str, Any]:
    cfg_path = Path(path) if path else DEFAULT_DRIVE_CONFIG
    if cfg_path.exists():
        with open(cfg_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
            return data

    return {"version": 1, "settings": {}, "profiles": []}


def save_drive_config(data: Dict[str, Any], path: Optional[Path] = None) -> None:
    cfg_path = Path(path) if path else DEFAULT_DRIVE_CONFIG
    cfg_path.parent.mkdir(parents=True, exist_ok=True)
    with open(cfg_path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)


def get_tracked_workspaces(path: Optional[Path] = None) -> List[Dict[str, Any]]:
    cfg = load_github_config(path)
    workspaces = cfg.get("workspaces", [])
    return [w for w in workspaces if w.get("tracked", True) is not False]


def get_enabled_drive_profiles(path: Optional[Path] = None) -> List[Dict[str, Any]]:
    cfg = load_drive_config(path)
    profiles = cfg.get("profiles", [])
    return [p for p in profiles if p.get("enabled", True) is not False]


def update_workspace(ws_id: str, updates: Dict[str, Any], config_path: Optional[Path] = None) -> bool:
    cfg = load_github_config(config_path)
    workspaces = cfg.get("workspaces", [])
    found = False
    for ws in workspaces:
        if ws.get("id") == ws_id:
            ws.update(updates)
            found = True
            break

    if not found and "id" in updates:
        workspaces.append(updates)
        found = True

    if found:
        cfg["workspaces"] = workspaces
        save_github_config(cfg, config_path)
        return True
    return False


def update_drive_profile(profile_id: str, updates: Dict[str, Any], config_path: Optional[Path] = None) -> bool:
    cfg = load_drive_config(config_path)
    profiles = cfg.get("profiles", [])
    found = False
    for p in profiles:
        if p.get("id") == profile_id:
            p.update(updates)
            found = True
            break

    if not found and "id" in updates:
        profiles.append(updates)
        found = True

    if found:
        cfg["profiles"] = profiles
        save_drive_config(cfg, config_path)
        return True
    return False
