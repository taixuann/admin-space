# Native OpenCode execution: design inputs

Status: Recorded requirements and proposed approach, 2026-10-23. Not an approved design or deployed executor.

## Accepted requirements

Use native OpenCode as the execution host. Use Superpowers as the main workflow. Keep durable executor guidance in ~/.config/opencode/AGENTS.md, written with writing-for-agents. Receive an approved plan, repository/worktree identity, scope, verification criteria, and integration limits. Execute without routine human check-ins.

Decision Engine reviews only the final result, not every task. If actionable findings require changes, allow one bounded repair cycle, rerun affected verification, then one final re-review. Stop with evidence if findings remain. Do not create an unbounded loop. Unavailable review is not approval. This review policy does not silently remove the task reviews required if subagent-driven-development is selected.

No automatic merge, publication, deployment, credential changes, or unrestricted permissions are granted. Preserve host/project approval boundaries. Do not send secrets or restricted material to external review.

## Proposed execution mechanism

Begin with native OpenCode plus a thin launcher only if it adds necessary process supervision. Reuse the existing opencode-delegate relay for CLI invocation, explicit session IDs, timeout, and result capture before introducing another wrapper. The launcher must not duplicate Superpowers planning, task ledgers, or review orchestration.

AGENTS.md describes behavior. Native agents provide execution/review roles. MCP connects Decision Engine. A directory at ~/.decision-engine is not itself an MCP connection. Inspect the actual installed server or supported endpoint before defining configuration.

For a first pilot, prefer foreground CLI execution with durable artifacts. If unattended survival after the launching chat exits is required, verify that host lifecycle explicitly before promising it. A persistent server/SDK client is an alternative only when CLI supervision proves insufficient.

## Evidence and sources

- OpenCode CLI: https://opencode.ai/docs/cli/ supports programmatic run and explicit session selection.
- OpenCode server: https://opencode.ai/docs/server/ exposes headless HTTP APIs.
- MCP: https://opencode.ai/docs/mcp-servers/ supports local and remote integrations.
- Existing relay: ~/.agents/skills/opencode-delegate/scripts/relay.mjs and references/dispatch-and-poll.md. Installed behavior must be verified against OpenCode's actual version.
- Example pipeline: ~/development-space/automation/linear-notion-tracking/README.md. Describes phase routing and human gates; implementation is not yet audited or approved for reuse.

## Open design decisions

Select CLI supervision versus server lifecycle. Verify Superpowers discovery and native task delegation in OpenCode. Locate Decision Engine's actual transport and credentials without copying secrets. Define the final result package, stable audit identity, and resume behavior. Confirm one repair cycle and one re-review are represented in the chosen audit workflow rather than bypassing its own requirements.

## Plan-local result visibility

Kanban owns the visible summary. Link the card from the plan. Keep native ledgers
for recovery and durable run evidence for verification. Add a managed plan status
section only if a separate consumer is demonstrated.

## Notion observation follow-up

The user requests a proposed schema and transition design so execution progress is visible in Agents Ticket. Keep native Superpowers as the executor. The plan records candidate fields and transitions for discussion only. Database modification and launch approval semantics are not selected yet.

## Accepted Kanban-first scope

Use Kanban Lite as the local progress view paired with native Superpowers through OpenCode AGENTS.md. Install and verify its skill and runtime without modifying Superpowers. Keep native ledgers for recovery. Defer Notion synchronization and schema changes. Board movement does not authorize or start execution. Installation and instruction changes remain implementation tasks in the plan, not completed facts.


## Accepted result-publisher role

The user selected Codex or Claude to read results and update the existing Kanban
card. It does not add a second review gate or execute repairs. The runner owns
execution and review. The publisher validates identity and evidence, preserves
human edits, and reports uncertainty. Keep one machine writer per card.

Deliver local Kanban first, then prove the full manual workflow and publisher.
Only after its stability gate passes, design scheduling and outward Notion sync. A future inbound Notion edit is a validated request, separate
from observed execution state. Launch still requires explicit authorization for
the exact plan revision. Inbound mapping and conflict handling remain open.


## Accepted manual-first boundary

One manually invoked workflow owns locking, execution, evidence capture, and
publication. Reuse existing relay capture before adding machinery. OpenCode owns
the native session store. Each run records the exact session ID and keeps attempt
history, process output, final report, verification, review, and publication
receipts outside tracked source. A latest-result pointer is not the history.

An interrupted run preserves partial work and awaits explicit recovery. Automatic
resume remains undecided. A workspace lock prevents concurrent writers; stale
lock recovery requires checking the prior process and session.

Prove clean completion, failure, interruption, duplicate invocation, explicit
resume, and publication retry in fixtures, then a scoped accepted pilot. Record
verification evidence. Set up automation only after the manual workflow is stable.
launchd will call the same entrypoint and capture streams. Scheduling, retention,
missing-run observation, and unattended survival are later automation work.
