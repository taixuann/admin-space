"""Scanner utility to inspect Git status, remotes, branches, and commits across workspaces,
and manage dedicated Google Drive sync profiles.
"""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional


def run_cmd(args: List[str], cwd: Optional[str] = None, timeout: int = 5) -> tuple[int, str, str]:
    try:
        res = subprocess.run(
            args,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
        return res.returncode, res.stdout.strip(), res.stderr.strip()
    except subprocess.TimeoutExpired:
        return -1, "", "Command timed out"
    except Exception as exc:
        return -1, "", str(exc)


def fetch_github_repos() -> List[Dict[str, Any]]:
    """Retrieve full list of repositories under the current user's GitHub account via gh CLI."""
    code, out, _ = run_cmd(
        ["gh", "repo", "list", "--json", "name,nameWithOwner,description,visibility,updatedAt,defaultBranchRef,isArchived", "--limit", "100"],
        timeout=10,
    )
    if code == 0 and out:
        try:
            return json.loads(out)
        except Exception:
            return []
    return []


def inspect_git_workspace(path_str: str, target_branch: Optional[str] = None) -> Dict[str, Any]:
    if not path_str:
        return {
            "path": "",
            "exists": False,
            "is_git": False,
            "branch": None,
            "available_branches": ["main"],
            "target_branch": target_branch or "main",
            "is_on_target_branch": False,
            "remote_url": None,
            "dirty": False,
            "uncommitted_count": 0,
            "uncommitted_files": [],
            "ahead": 0,
            "behind": 0,
            "last_commit": None,
            "status_code": "remote_only",
            "status_label": "Remote Only",
            "error": None,
        }

    path = Path(os.path.expanduser(path_str)).resolve()
    
    info: Dict[str, Any] = {
        "path": str(path),
        "exists": path.exists() and path.is_dir(),
        "is_git": False,
        "branch": None,
        "available_branches": ["main"],
        "target_branch": target_branch or "main",
        "is_on_target_branch": True,
        "remote_url": None,
        "dirty": False,
        "uncommitted_count": 0,
        "uncommitted_files": [],
        "ahead": 0,
        "behind": 0,
        "last_commit": None,
        "status_code": "unknown",
        "status_label": "Unknown",
        "error": None,
    }

    if not info["exists"]:
        info["status_code"] = "missing"
        info["status_label"] = "Directory Missing"
        return info

    # Check git presence
    code, out, _ = run_cmd(["git", "rev-parse", "--is-inside-work-tree"], str(path))
    if code != 0 or out != "true":
        info["status_code"] = "no_git"
        info["status_label"] = "No Git Repo"
        return info

    info["is_git"] = True

    # Current branch
    code, branch, _ = run_cmd(["git", "branch", "--show-current"], str(path))
    if code == 0 and branch:
        info["branch"] = branch
    else:
        # Detached head or unborn branch
        code, head_ref, _ = run_cmd(["git", "rev-parse", "--short", "HEAD"], str(path))
        info["branch"] = head_ref if code == 0 else "HEAD"

    # All local available branches for pill toggle
    code, branches_out, _ = run_cmd(["git", "branch", "--format=%(refname:short)"], str(path))
    if code == 0 and branches_out:
        branches = [b.strip() for b in branches_out.split("\n") if b.strip()]
        info["available_branches"] = branches if branches else [info["branch"] or "main"]
    else:
        info["available_branches"] = [info["branch"] or "main"]

    expected_branch = target_branch or ("master" if info["branch"] == "master" else "main")
    info["target_branch"] = expected_branch
    info["is_on_target_branch"] = (info["branch"] == expected_branch)

    # Remote URL
    code, remote, _ = run_cmd(["git", "config", "--get", "remote.origin.url"], str(path))
    if code == 0 and remote:
        info["remote_url"] = remote

    # Dirty / uncommitted files
    code, status_out, _ = run_cmd(["git", "status", "--porcelain"], str(path))
    if code == 0:
        lines = [line.strip() for line in status_out.split("\n") if line.strip()]
        info["uncommitted_count"] = len(lines)
        info["dirty"] = len(lines) > 0
        info["uncommitted_files"] = lines[:50]  # preview up to 50 files

    # Last commit info on target branch or HEAD
    code, log_out, _ = run_cmd(["git", "log", "-1", "--format=%h|%an|%ar|%s"], str(path))
    if code == 0 and log_out:
        parts = log_out.split("|", 3)
        if len(parts) == 4:
            info["last_commit"] = {
                "hash": parts[0],
                "author": parts[1],
                "time": parts[2],
                "message": parts[3],
            }

    # Ahead / Behind count focused strictly on origin/<target_branch>
    ref_target = f"origin/{expected_branch}"
    code, check_ref, _ = run_cmd(["git", "rev-parse", "--verify", ref_target], str(path))
    if code == 0:
        code, ab_out, _ = run_cmd(
            ["git", "rev-list", "--left-right", "--count", f"{ref_target}...HEAD"],
            str(path),
        )
        if code == 0 and ab_out:
            try:
                behind_str, ahead_str = ab_out.split()
                info["behind"] = int(behind_str)
                info["ahead"] = int(ahead_str)
            except Exception:
                pass
    elif info["branch"]:
        code, ab_out, _ = run_cmd(
            ["git", "rev-list", "--left-right", "--count", f"@{'{u}'}...HEAD"],
            str(path),
        )
        if code == 0 and ab_out:
            try:
                behind_str, ahead_str = ab_out.split()
                info["behind"] = int(behind_str)
                info["ahead"] = int(ahead_str)
            except Exception:
                pass

    # Compute high-level badge status
    if not info["remote_url"]:
        info["status_code"] = "no_remote"
        info["status_label"] = "No Remote"
    elif info["dirty"]:
        info["status_code"] = "dirty"
        info["status_label"] = f"{info['uncommitted_count']} uncommitted"
    elif info["ahead"] > 0 and info["behind"] > 0:
        info["status_code"] = "diverged"
        info["status_label"] = f"{info['ahead']} ahead, {info['behind']} behind"
    elif info["ahead"] > 0:
        info["status_code"] = "ahead"
        info["status_label"] = f"{info['ahead']} unpushed"
    elif info["behind"] > 0:
        info["status_code"] = "behind"
        info["status_label"] = f"{info['behind']} behind"
    else:
        info["status_code"] = "synced"
        info["status_label"] = "In Sync"

    return info


def scan_drive_profiles(profiles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    results = []
    for p in profiles:
        source = Path(os.path.expanduser(p.get("source_path", "")))
        exists = source.exists() and source.is_dir()
        
        git_clean = True
        uncommitted_count = 0
        is_git = False
        
        if exists:
            code, out, _ = run_cmd(["git", "rev-parse", "--is-inside-work-tree"], cwd=str(source))
            if code == 0 and out == "true":
                is_git = True
                code, stat_out, _ = run_cmd(["git", "status", "--porcelain"], cwd=str(source))
                if code == 0 and stat_out:
                    lines = [l for l in stat_out.split("\n") if l.strip()]
                    uncommitted_count = len(lines)
                    git_clean = (uncommitted_count == 0)
                else:
                    git_clean = True

        status_label = "Ready to Sync" if (exists and git_clean) else ("Commit Required" if (exists and not git_clean) else "Source Missing")
        
        item = {
            **p,
            "exists": exists,
            "is_git": is_git,
            "git_clean": git_clean,
            "uncommitted_count": uncommitted_count,
            "status_label": status_label,
        }
        results.append(item)
    return results


def scan_all_workspaces(config_path: Optional[Path] = None) -> Dict[str, Any]:
    workspaces: List[Dict[str, Any]] = []
    drive_profiles: List[Dict[str, Any]] = []

    try:
        from config_manager import load_github_config, load_drive_config, DEFAULT_GITHUB_CONFIG, DEFAULT_DRIVE_CONFIG
        if DEFAULT_GITHUB_CONFIG.exists() or DEFAULT_DRIVE_CONFIG.exists():
            workspaces = list(load_github_config().get("workspaces", []))
            drive_profiles = list(load_drive_config().get("profiles", []))
        elif config_path and Path(config_path).exists():
            with open(config_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                workspaces = data.get("workspaces", [])
                drive_profiles = data.get("drive_profiles", [])
    except Exception:
        if config_path and Path(config_path).exists():
            with open(config_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                workspaces = data.get("workspaces", [])
                drive_profiles = data.get("drive_profiles", [])

    # Auto-discover full list of GitHub repositories
    gh_repos = fetch_github_repos()
    
    # Track which repos are archived
    archived_remotes = set()
    for gr in gh_repos:
        if gr.get("isArchived", False):
            if gr.get("nameWithOwner"):
                archived_remotes.add(gr.get("nameWithOwner").lower())
            if gr.get("name"):
                archived_remotes.add(gr.get("name").lower())

    known_repos = set()
    for ws in workspaces:
        if ws.get("remote_repo"):
            known_repos.add(ws.get("remote_repo").lower())
        if ws.get("id"):
            known_repos.add(ws.get("id").lower())

    for gr in gh_repos:
        # Do not include archived repositories in untracked/discovered repos
        if gr.get("isArchived", False):
            continue

        name_with_owner = gr.get("nameWithOwner", "")
        name = gr.get("name", "")
        if name_with_owner.lower() not in known_repos and name.lower() not in known_repos:
            workspaces.append({
                "id": name,
                "name": name.replace("-", " ").title(),
                "category": "Discovered Repos",
                "path": "",
                "remote_repo": name_with_owner,
                "default_branch": gr.get("defaultBranchRef", {}).get("name", "main"),
                "tracked": False,
                "track_automation": False,
                "visibility": gr.get("visibility", "PUBLIC"),
                "is_archived": False,
            })

    ws_results = []
    for ws in workspaces:
        remote = (ws.get("remote_repo") or "").lower()
        ws_id = (ws.get("id") or "").lower()
        is_archived = (remote in archived_remotes) or (ws_id in archived_remotes) or ws.get("is_archived", False)

        # Never display untracked repos that are archived
        if not ws.get("tracked", False) and is_archived:
            continue

        target_branch = ws.get("default_branch", "main")
        git_info = inspect_git_workspace(ws.get("path", ""), target_branch=target_branch)
        merged = {**ws, "is_archived": is_archived, "git": git_info}
        ws_results.append(merged)

    drive_results = scan_drive_profiles(drive_profiles)

    return {
        "workspaces": ws_results,
        "drive_profiles": drive_results,
    }


def fetch_gdrive_remote_tree(remote: str = "gdrive:") -> List[str]:
    """Retrieve directory list on Google Drive up to depth 3."""
    code, out, _ = run_cmd(["rclone", "lsf", "--dirs-only", "-R", "--max-depth", "3", remote], timeout=15)
    if code == 0 and out:
        dirs = [d.rstrip("/") for d in out.split("\n") if d.strip()]
        return dirs
    return []


def build_gdrive_remote_hierarchy(remote: str = "gdrive:") -> Dict[str, Any]:
    """Construct a nested tree structure from remote Google Drive directories."""
    dirs = fetch_gdrive_remote_tree(remote)
    dirs = sorted(dirs, key=lambda d: d.lower())

    root = {"name": remote, "path": remote, "rel_path": "", "children": []}
    node_map = {"": root}

    for d in dirs:
        parts = d.split("/")
        cur_p = ""
        for p in parts:
            prev_p = cur_p
            cur_p = f"{prev_p}/{p}" if prev_p else p
            if cur_p not in node_map:
                node = {"name": p, "path": f"{remote}{cur_p}/", "rel_path": cur_p, "children": []}
                parent = node_map.get(prev_p, root)
                parent["children"].append(node)
                node_map[cur_p] = node

    return root


def build_folder_tree(path_str: str, max_depth: int = 2) -> Dict[str, Any]:
    root_path = Path(os.path.expanduser(path_str)).resolve()
    if not root_path.exists() or not root_path.is_dir():
        return {"name": root_path.name, "rel_path": "", "is_dir": True, "children": [], "exists": False}

    modified_map = {}
    ignored_prefixes = {".git", ".DS_Store"}
    
    code, status_out, _ = run_cmd(["git", "status", "--ignored", "--porcelain=v1"], cwd=str(root_path), timeout=5)
    if code == 0 and status_out:
        for line in status_out.split("\n"):
            line = line.rstrip()
            if not line:
                continue
            flag = line[:2].strip()
            item_path = line[3:].strip()
            if flag == "!!":
                ignored_prefixes.add(item_path.rstrip("/"))
            else:
                modified_map[item_path] = flag

    def is_ignored(rel_p: str) -> bool:
        for ign in ignored_prefixes:
            if rel_p == ign or rel_p.startswith(ign + "/") or rel_p.startswith(ign + "\\"):
                return True
        return False

    def get_status(rel_p: str) -> Optional[str]:
        if rel_p in modified_map:
            return modified_map[rel_p]
        for p, flag in modified_map.items():
            if p.startswith(rel_p + "/"):
                return "M"
        return None

    def scan_node(cur_path: Path, current_depth: int, parent_ignored: bool = False) -> Dict[str, Any]:
        rel = str(cur_path.relative_to(root_path))
        if rel == ".":
            rel = ""
        
        is_dir = cur_path.is_dir()
        ignored = parent_ignored or (is_ignored(rel) if rel else False)
        status = get_status(rel) if rel else None

        node = {
            "name": cur_path.name,
            "rel_path": rel,
            "is_dir": is_dir,
            "is_ignored": ignored,
            "status": status,
            "children": [],
        }

        # ONLY DIRECTORIES AND MAXIMUM DEPTH = 2
        if is_dir and current_depth < max_depth:
            try:
                sub_dirs = sorted([p for p in cur_path.iterdir() if p.is_dir()], key=lambda p: p.name.lower())
                for sub in sub_dirs:
                    if sub.name == ".git":
                        continue
                    child_node = scan_node(sub, current_depth + 1, parent_ignored=ignored)
                    node["children"].append(child_node)
            except PermissionError:
                pass

        return node

    tree = scan_node(root_path, 0, False)
    tree["root_name"] = root_path.name
    tree["exists"] = True
    return tree


if __name__ == "__main__":
    res = scan_all_workspaces()
    print(f"Total workspaces: {len(res['workspaces'])}")
    print(f"Total Drive profiles: {len(res['drive_profiles'])}")
    for d in res['drive_profiles']:
        print(f"  - Drive: {d['name']} -> git_clean={d.get('git_clean')}, uncommitted={d.get('uncommitted_count')}")
    t = build_folder_tree("/Users/tai/personal-space", max_depth=2)
    print(f"Tree root: {t['name']} has {len(t['children'])} top-level subfolders")
