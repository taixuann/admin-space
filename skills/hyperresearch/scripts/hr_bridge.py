#!/usr/bin/env python3
"""
HyperResearch Multi-Level Bridge
Deterministic Python helper for AutoSci and Study skills.
Exposes clean sub-pipeline functions:
  Level 0: Instant Vault & Claims Retrieval (<2s)
  Level 1: Targeted Scholar & Adversarial Lookup (10-45s)
  Level 2: Light Bounded Synthesis (~15-30m)
  Level 3: Full Deep Pipeline (~1.5-2.5h)
"""

import sys
import json
import argparse
import subprocess
from pathlib import Path

HR_BIN = Path("/Users/tai/hyperresearch/.venv/bin/hyperresearch")
if not HR_BIN.exists():
    local_bin = Path("/Users/tai/research-projects/hyperresearch/.venv/bin/hyperresearch")
    if local_bin.exists():
        HR_BIN = local_bin

VAULT_DIR = Path("/Users/tai/hyperresearch")

def _run_cmd(args):
    try:
        res = subprocess.run(
            [str(HR_BIN)] + args,
            capture_output=True,
            text=True,
            cwd=str(VAULT_DIR),
            check=False
        )
        if res.returncode == 0:
            try:
                return json.loads(res.stdout)
            except json.JSONDecodeError:
                return {"ok": True, "output": res.stdout.strip()}
        else:
            return {"ok": False, "error": res.stderr.strip() or res.stdout.strip()}
    except Exception as e:
        return {"ok": False, "error": str(e)}

# --- LEVEL 0: Instant Vault & Claims (<2s) ---

def level0_search(query: str):
    """Full-text search across existing markdown notes in vault."""
    return _run_cmd(["search", query, "--json"])

def level0_claims(query: str):
    """Search indexed claims across vault sources."""
    return _run_cmd(["claims", "search", query, "--json"])

def level0_read_note(note_id: str):
    """Read a specific note from the vault."""
    return _run_cmd(["note", "show", note_id, "--json"])

# --- LEVEL 1: Targeted Scholar & Adversarial (10-45s) ---

def level1_scholar(query: str, limit: int = 10, scope: str = "papers"):
    """Query OpenAlex, Crossref, CORE, DOAB, PubMed, deduplicated."""
    args = ["scholar", "search", query, "--limit", str(limit), "-j"]
    if scope:
        args.extend(["--scope", scope])
    return _run_cmd(args)

def level1_adversarial(idea_or_claim: str, limit: int = 5):
    """Run adversarial searches for criticisms, limitations, and prior art."""
    queries = [
        f"prior art {idea_or_claim}",
        f"limitations of {idea_or_claim}",
        f"criticism {idea_or_claim}"
    ]
    results = {}
    for q in queries:
        res = _run_cmd(["scholar", "search", q, "--limit", str(limit), "-j"])
        results[q] = res
    return {"ok": True, "adversarial_results": results}

def level1_fetch(url_or_doi: str):
    """Fetch URL or DOI into persistent Markdown note with PDF text extraction."""
    return _run_cmd(["fetch", url_or_doi, "-j"])

# --- LEVEL 2 & 3: Pipeline Runs ---

def run_pipeline(query: str, profile: str = "light", budget: float = None):
    """Scaffold and launch a pipeline run (Level 2: light, Level 3: full)."""
    # 1. Mint tag
    slug = "-".join(query.lower().split()[:4]).replace("/", "-")
    tag_res = _run_cmd(["vault-tag", slug, "--json"])
    if not tag_res.get("ok", True) and "error" in tag_res:
        return tag_res
    vault_tag = tag_res.get("data", {}).get("vault_tag") or tag_res.get("vault_tag", f"{slug}-run")
    
    # 2. Init run workspace
    cmd = ["run", "init", vault_tag, "--profile", profile, "--json"]
    if budget:
        cmd.extend(["--budget", str(budget)])
    init_res = _run_cmd(cmd)
    return {
        "ok": True,
        "vault_tag": vault_tag,
        "profile": profile,
        "init": init_res
    }

def main():
    parser = argparse.ArgumentParser(description="HyperResearch Tiered Bridge")
    subparsers = parser.add_subparsers(dest="command")

    # Level 0
    p_s0 = subparsers.add_parser("level0-search", help="Instant search across vault notes")
    p_s0.add_argument("query", help="Search query")

    p_c0 = subparsers.add_parser("level0-claims", help="Search indexed claims")
    p_c0.add_argument("query", help="Claim query")

    p_r0 = subparsers.add_parser("level0-read", help="Read note by ID")
    p_r0.add_argument("note_id", help="Note ID")

    # Level 1
    p_s1 = subparsers.add_parser("level1-scholar", help="Live academic search across OpenAlex/Crossref/CORE")
    p_s1.add_argument("query", help="Scholar query")
    p_s1.add_argument("--limit", type=int, default=10, help="Max results")

    p_adv1 = subparsers.add_parser("level1-adversarial", help="Adversarial prior art and criticism search")
    p_adv1.add_argument("idea", help="Idea or claim to test")
    p_adv1.add_argument("--limit", type=int, default=5, help="Max results per angle")

    p_f1 = subparsers.add_parser("level1-fetch", help="Fetch paper URL or DOI into note")
    p_f1.add_argument("target", help="URL or DOI")

    # Self-test
    subparsers.add_parser("test", help="Test bridge connectivity")

    args = parser.parse_args()

    if args.command == "level0-search":
        print(json.dumps(level0_search(args.query), indent=2))
    elif args.command == "level0-claims":
        print(json.dumps(level0_claims(args.query), indent=2))
    elif args.command == "level0-read":
        print(json.dumps(level0_read_note(args.note_id), indent=2))
    elif args.command == "level1-scholar":
        print(json.dumps(level1_scholar(args.query, limit=args.limit), indent=2))
    elif args.command == "level1-adversarial":
        print(json.dumps(level1_adversarial(args.idea, limit=args.limit), indent=2))
    elif args.command == "level1-fetch":
        print(json.dumps(level1_fetch(args.target), indent=2))
    elif args.command == "test":
        print("Testing HyperResearch CLI connection...")
        status = _run_cmd(["status", "--json"])
        sources = _run_cmd(["scholar", "sources", "--json"])
        print(json.dumps({"binary": str(HR_BIN), "status": status.get("ok", False), "scholar_sources": sources.get("ok", False)}, indent=2))
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
