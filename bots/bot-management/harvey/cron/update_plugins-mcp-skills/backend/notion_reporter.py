"""Notion incident reporter delegating to shared ticket_submit module with fail-soft resilience."""
from __future__ import annotations

import os
import sys
from typing import Any, Dict

# Add ticket-submit script location
TICKET_SUBMIT_DIR = os.path.expanduser("~/.agents/skills/ticket-submit/scripts")
if TICKET_SUBMIT_DIR not in sys.path:
    sys.path.insert(0, TICKET_SUBMIT_DIR)

try:
    from ticket_submit import submit_or_update_ticket
except ImportError:
    submit_or_update_ticket = None


def report_incident(
    title: str,
    error_details: str,
    component: str = "Automations & Runtime",
    status: str = "Blocked",
) -> Dict[str, Any]:
    """Reports an incident via ticket-submit skill with fail-soft resilience."""
    if not submit_or_update_ticket:
        sys.stderr.write("ticket_submit module not available, skipping Notion escalation.\n")
        return {"success": False, "action": "skipped_no_module"}

    try:
        res = submit_or_update_ticket(
            title=title,
            target_space="Admin",
            system_component=component,
            request_type="Fix",
            status=status,
            body=error_details,
            signature=title,
        )
        return res
    except Exception as exc:
        # Must fail softly: log to stderr and never mask underlying automation exit code
        sys.stderr.write(f"Notion ticket escalation warning (soft fail): {exc}\n")
        return {"success": False, "error": str(exc), "action": "soft_failed"}
