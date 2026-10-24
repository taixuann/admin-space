#!/usr/bin/env python3
"""Reusable Notion Ticket Submission and Deduplication module via ntn CLI."""
from __future__ import annotations

import argparse
import datetime
import json
import os
import shutil
import subprocess
import sys
from typing import Any, Dict, List, Optional, Tuple

DEFAULT_DATABASE_ID = "3ff0a859-ed1f-8072-8ae0-fdb996889173"
DEFAULT_DATASOURCE_ID = "3ff0a859-ed1f-80c4-b3b1-000b9c10da55"


def find_ntn() -> str:
    found = shutil.which("ntn")
    if found:
        return found
    candidate_paths = [
        "/Users/tai/.local/bin/ntn",
        "/usr/local/bin/ntn",
        "/opt/homebrew/bin/ntn",
    ]
    for p in candidate_paths:
        if os.path.isfile(p) and os.access(p, os.X_OK):
            return p
    return "ntn"


def run_ntn_command(args: List[str], input_data: Optional[str] = None) -> Tuple[int, str, str]:
    ntn_bin = find_ntn()
    cmd = [ntn_bin] + args
    try:
        proc = subprocess.run(
            cmd,
            input=input_data,
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
        return proc.returncode, proc.stdout, proc.stderr
    except Exception as exc:
        raise RuntimeError(f"Error executing {' '.join(cmd)}: {exc}") from exc


def query_open_ticket(
    signature: str,
    data_source_id: str = DEFAULT_DATASOURCE_ID,
) -> Optional[str]:
    """Query data source for open tickets matching the signature in title."""
    filter_payload = {
        "filter": {
            "and": [
                {
                    "property": "Ticket",
                    "title": {"contains": signature},
                },
                {
                    "property": "Status",
                    "status": {"does_not_equal": "Done"},
                },
                {
                    "property": "Status",
                    "status": {"does_not_equal": "Canceled"},
                },
            ]
        }
    }
    code, stdout, stderr = run_ntn_command(
        ["api", "-X", "POST", f"v1/data_sources/{data_source_id}/query", "-d", json.dumps(filter_payload)]
    )
    if code != 0:
        raise RuntimeError(f"ntn query failed (exit {code}): {stderr.strip() or stdout.strip()}")

    try:
        data = json.loads(stdout)
        results = data.get("results", [])
        if results:
            return results[0].get("id")
    except Exception as exc:
        raise RuntimeError(f"Failed to parse query response: {exc}") from exc

    return None


def append_ticket_comment(page_id: str, comment_text: str) -> bool:
    """Append a comment to an existing ticket page."""
    payload = {
        "parent": {"page_id": page_id},
        "rich_text": [{"text": {"content": comment_text}}],
    }
    code, stdout, stderr = run_ntn_command(
        ["api", "-X", "POST", "v1/comments", "-d", json.dumps(payload)]
    )
    if code != 0:
        raise RuntimeError(f"ntn comment failed (exit {code}): {stderr.strip() or stdout.strip()}")
    return True


def create_ticket(
    title: str,
    target_space: str = "Development",
    system_component: str = "Automations & Runtime",
    request_type: str = "Fix",
    status: str = "Blocked",
    current_step: Optional[str] = None,
    body: Optional[str] = None,
    database_id: str = DEFAULT_DATABASE_ID,
) -> Optional[str]:
    """Create a new ticket page in the database."""
    spaces = [s.strip() for s in target_space.split(",") if s.strip()]
    components = [c.strip() for c in system_component.split(",") if c.strip()]

    properties: Dict[str, Any] = {
        "Ticket": {
            "title": [{"text": {"content": title}}]
        },
        "Status": {
            "status": {"name": status}
        },
        "Request Type": {
            "select": {"name": request_type}
        },
        "Target Space": {
            "multi_select": [{"name": s} for s in spaces]
        },
        "System Component": {
            "multi_select": [{"name": c} for c in components]
        },
    }

    if current_step:
        properties["Current Step"] = {
            "rich_text": [{"text": {"content": current_step[:2000]}}]
        }

    children: List[Dict[str, Any]] = []
    if body:
        # Bounded body block
        trimmed = body[:2000]
        children.append({
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": trimmed}}]
            },
        })

    payload: Dict[str, Any] = {
        "parent": {"database_id": database_id},
        "properties": properties,
    }
    if children:
        payload["children"] = children

    code, stdout, stderr = run_ntn_command(
        ["api", "-X", "POST", "v1/pages", "-d", json.dumps(payload)]
    )
    if code != 0:
        raise RuntimeError(f"ntn page creation failed (exit {code}): {stderr.strip() or stdout.strip()}")

    try:
        data = json.loads(stdout)
        return data.get("id")
    except Exception as exc:
        raise RuntimeError(f"Failed to parse page creation response: {exc}") from exc


def submit_or_update_ticket(
    title: str,
    target_space: str = "Development",
    system_component: str = "Automations & Runtime",
    request_type: str = "Fix",
    status: str = "Blocked",
    current_step: Optional[str] = None,
    body: Optional[str] = None,
    signature: Optional[str] = None,
    database_id: str = DEFAULT_DATABASE_ID,
    data_source_id: str = DEFAULT_DATASOURCE_ID,
) -> Dict[str, Any]:
    """Submit a ticket or update an existing open ticket with deduping."""
    sig = signature or title
    now_iso = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    try:
        existing_page_id = query_open_ticket(sig, data_source_id=data_source_id)
        if existing_page_id:
            comment_content = f"[{now_iso}] Recurring failure in {target_space}:\n{body or 'No log provided.'}"
            # Trim comment to 2000 chars for Notion limit
            append_ticket_comment(existing_page_id, comment_content[:2000])
            return {
                "success": True,
                "action": "commented",
                "page_id": existing_page_id,
            }
        else:
            new_id = create_ticket(
                title=title,
                target_space=target_space,
                system_component=system_component,
                request_type=request_type,
                status=status,
                current_step=current_step or f"Automated escalation at {now_iso}",
                body=body,
                database_id=database_id,
            )
            return {
                "success": True,
                "action": "created",
                "page_id": new_id,
            }
    except Exception as exc:
        return {
            "success": False,
            "action": "failed",
            "error": str(exc),
        }


def main() -> None:
    parser = argparse.ArgumentParser(description="Submit or update tickets in Notion Agent Tickets via ntn.")
    parser.add_argument("--title", required=True, help="Ticket title")
    parser.add_argument("--space", default="Development", help="Target Space (e.g. Development, Admin, Research)")
    parser.add_argument("--component", default="Automations & Runtime", help="System Component")
    parser.add_argument("--type", default="Fix", help="Request Type (Fix, Build, Improve, Evaluate, Operate)")
    parser.add_argument("--status", default="Blocked", help="Ticket Status (Captured, Blocked, Human review, etc.)")
    parser.add_argument("--step", default=None, help="Current step description")
    parser.add_argument("--body", default=None, help="Details or log snippet for ticket body/comment")
    parser.add_argument("--signature", default=None, help="Signature to search for existing open tickets (defaults to title)")
    parser.add_argument("--database-id", default=DEFAULT_DATABASE_ID, help="Notion Database ID")
    parser.add_argument("--datasource-id", default=DEFAULT_DATASOURCE_ID, help="Notion Data Source ID")

    args = parser.parse_args()
    res = submit_or_update_ticket(
        title=args.title,
        target_space=args.space,
        system_component=args.component,
        request_type=args.type,
        status=args.status,
        current_step=args.step,
        body=args.body,
        signature=args.signature,
        database_id=args.database_id,
        data_source_id=args.datasource_id,
    )

    print(json.dumps(res, indent=2))
    if not res["success"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
