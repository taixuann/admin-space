"""Plugins updater module for global Superpowers and Caveman installations."""
from __future__ import annotations

import os
import subprocess
from typing import TypedDict


class SuperpowersUpdateResult(TypedDict):
    success: bool
    updated: bool
    head_sha: str | None
    output: str


class CavemanUpdateResult(TypedDict):
    success: bool
    output: str


DEFAULT_SUPERPOWERS_DIR = os.path.expanduser("~/.gemini/config/plugins/superpowers")


def update_superpowers(repo_dir: str = DEFAULT_SUPERPOWERS_DIR) -> SuperpowersUpdateResult:
    """Updates the Superpowers repository to latest origin/main."""
    if not os.path.isdir(os.path.join(repo_dir, ".git")):
        return {
            "success": False,
            "updated": False,
            "head_sha": None,
            "output": f"Directory is not a git repository: {repo_dir}",
        }

    try:
        # Fetch latest
        fetch_proc = subprocess.run(
            ["git", "-C", repo_dir, "fetch", "origin", "main"],
            capture_output=True,
            text=True,
            timeout=45,
            check=False,
        )
        if fetch_proc.returncode != 0:
            return {
                "success": False,
                "updated": False,
                "head_sha": None,
                "output": f"git fetch failed: {fetch_proc.stderr.strip()}",
            }

        # Check rev-parse
        local_head = subprocess.run(
            ["git", "-C", repo_dir, "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        ).stdout.strip()

        remote_head = subprocess.run(
            ["git", "-C", repo_dir, "rev-parse", "origin/main"],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        ).stdout.strip()

        if local_head == remote_head:
            return {
                "success": True,
                "updated": False,
                "head_sha": local_head,
                "output": f"Up to date at commit {local_head[:12]}",
            }

        # Fast-forward pull
        pull_proc = subprocess.run(
            ["git", "-C", repo_dir, "pull", "--ff-only", "origin", "main"],
            capture_output=True,
            text=True,
            timeout=45,
            check=False,
        )
        combined = (pull_proc.stdout + "\n" + pull_proc.stderr).strip()
        new_head = subprocess.run(
            ["git", "-C", repo_dir, "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        ).stdout.strip()

        return {
            "success": pull_proc.returncode == 0,
            "updated": True,
            "head_sha": new_head,
            "output": combined,
        }
    except Exception as exc:
        return {
            "success": False,
            "updated": False,
            "head_sha": None,
            "output": f"Exception updating superpowers: {exc}",
        }


def update_caveman() -> CavemanUpdateResult:
    """Installs/updates Caveman command-output rewrite hooks across all agents."""
    fnm_bin = os.path.expanduser("~/.local/share/fnm/aliases/default/bin")
    env = os.environ.copy()
    env["PATH"] = f"{fnm_bin}:{env.get('PATH', '')}"

    try:
        proc = subprocess.run(
            ["caveman", "tools", "hooks", "install"],
            env=env,
            capture_output=True,
            text=True,
            timeout=45,
            check=False,
        )
        combined = (proc.stdout + "\n" + proc.stderr).strip()
        return {
            "success": proc.returncode == 0,
            "output": combined,
        }
    except FileNotFoundError:
        return {
            "success": False,
            "output": "caveman executable not found in PATH or fnm default bin",
        }
    except Exception as exc:
        return {
            "success": False,
            "output": f"Exception updating caveman hooks: {exc}",
        }
