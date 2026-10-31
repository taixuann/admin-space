---
name: ticket-submit
description: Submit, query, and deduplicate incident or task tickets in the Notion Agent Tickets database via the ntn CLI. Use when an automation, agent, or workflow encounters a failure, unhandled error, drift, or actionable task that needs escalation or tracking in Notion.
---

# ticket-submit

Submit actionable tickets to the central Notion **Agent Tickets** database via `ntn`. Automatically deduplicates against existing open tickets by appending recurrence logs instead of creating spam tickets.

## Notion Database Contract

- **Database URL**: `https://app.notion.com/p/3ff0a859ed1f80728ae0fdb996889173`
- **Database ID**: `3ff0a859-ed1f-8072-8ae0-fdb996889173`
- **Data Source ID**: `3ff0a859-ed1f-80c4-b3b1-000b9c10da55`

Transport: `ntn` (notion-cli) is the first and only path for this skill. All Notion API calls go through `ntn api`.

### Valid Properties

| Property | Type | Options / Format | Default |
| --- | --- | --- | --- |
| `Ticket` | Title | Brief error or issue title | (Required) |
| `Status` | Status | `Captured`, `Human review`, `Done`, `Canceled` | `Captured` |
| `Request Type` | Select | `Build`, `Fix`, `Improve`, `Evaluate`, `Operate` | `Fix` (for incidents) |
| `Target Space` | Multi-select | `Admin`, `Development`, `Study`, `Research`, `Personal`, `Cross-space` | Resolved from workspace root |
| `System Component` | Multi-select | `Profiles & Identity`, `Memory & Knowledge`, `Skills & Integrations`, `Agents & Models`, `Workflows & Architecture`, `Automations & Runtime` | `Automations & Runtime` (for launchd) |

Step text is written as the first paragraph of the page body, not as a property.

## Deduplication & Recurrence Policy

1. Before creating a new ticket, the reporter queries the data source for open tickets whose `Ticket` title contains the issue signature (e.g. `[Auto-Sync] Error skill <name>`) and whose `Status` is neither `Done` nor `Canceled`.
2. **If an open ticket exists**: Do NOT create a duplicate ticket. Call `ntn api -X POST v1/comments` to append a recurrence log entry with current UTC timestamp and error excerpt.
3. **If no open ticket exists**: Call `ntn api -X POST v1/pages` to create a new ticket in `Status: Captured` with the initial error body (step text as the first paragraph of the page body).
4. **Soft-failure guarantee**: If `ntn` is not installed, unauthenticated, or the network is unreachable, log to `stderr` and continue without crashing the caller.

## Usage

### 1. CLI Execution

```bash
python3 ~/.agents/skills/ticket-submit/scripts/ticket_submit.py \
    --title "[Auto-Sync] Maintenance failure in development-space" \
    --space "Development" \
    --component "Automations & Runtime" \
    --type "Fix" \
    --status "Captured" \
    --step "Skills updater 404" \
    --body "Detailed error log or stack trace..."
```

### 2. Python Import

```python
import sys
sys.path.insert(0, "/Users/tai/.agents/skills/ticket-submit/scripts")
from ticket_submit import submit_or_update_ticket

result = submit_or_update_ticket(
    title="[Auto-Sync] Error updating skill: foo",
    target_space="Development",
    system_component="Automations & Runtime",
    request_type="Fix",
    status="Captured",
    current_step="Phase 1: Skills update",
    body="Detailed stderr log output...",
)
# Returns: {"success": True, "action": "created" | "commented", "page_id": "..."}
```
