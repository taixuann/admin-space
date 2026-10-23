# Request 008: Reliable OpenCode model refresh

## Status and purpose

- Status: IN PROGRESS 2026-10-23. Source implemented in `tools/opencode-free-router/automation/model-refresh/` and `tools/automation-incidents/`; 65 tests pass across model selection, runner, and incidents. The label is not installed; the legacy job still owns the schedule. Activation remains blocked on old-runner continuity and unattended Notion authentication. Evidence: [batch 7](execution-2026-10-23/batch-7-verification.md).
- Priority: P1. Effort: M. Risk: MED.
- Base inspected: `40e9d38238e487744ec216f5a57617e3c09cfb3e`, 2026-10-23.
- This is the Admin request brief: intent, accepted boundaries, proposals, evidence, and acceptance criteria. It is not the final implementation plan.
- Plan 007 remains deferred.

The identifier `008` traces this request across tool repositories and implementation artifacts. Start the full Superpowers workflow from this brief: inspect current state, brainstorm remaining design choices, approve a design, use writing-plans, execute in isolated worktrees with the selected Superpowers execution workflow, review, verify, and finish under the owning repository's integration rules. Keep links back to this request. Do not treat draft snippets below as permission to install, restart, publish, or create live tickets.

## Accepted outcome and boundaries

Refresh the OpenCode default model through the existing model tool. Preserve provider priority, free-quota constraints, the last valid model on failure, and the midnight schedule. Do not update the OpenCode binary or upstream package in this request.

Each tool is an independent Git repository at `~/.agents/tools/<tool-name>/`. Admin Git ignores the complete tools subtree after the reviewed extraction in plan 009. Development Space hosts worktrees; it does not become the canonical source home.

Automation source follows its owner:

- A job dedicated to one tool lives in that tool repository under `automation/<job-name>/`, beside its implementation and tests.
- A job that coordinates several independently owned tools or applies Space policy lives under Admin `automation/<job-name>/`.
- Calling a shared incident reporter does not by itself turn a tool-specific job into Space orchestration. Classify by the primary responsibility and independent lifecycle.
- Runtime reports for both kinds live at `~/.agents/automation/<job-name>/logs/`. They are ignored by Admin Git. An optional short Admin README may point to the source; it does not duplicate runner, plist, or runbook authority.

OpenCode model refresh is tool-owned. Keep its source in `tools/opencode-free-router/automation/model-refresh/`, and report runs at `~/.agents/automation/opencode-model-refresh/logs/`.

## Repository and source map

```text
~/.agents/                                  # Admin repository
  automation/opencode-model-refresh/
    logs/                                   # Ignored reports, no duplicate runner
  tools/                                    # Ignored by Admin Git
    opencode-free-router/                   # Independent tool repository
      backend/
      tests/                                # Or existing backend test location
      docs/
      automation/model-refresh/
        README.md
        AGENTS.md
        run.sh                              # Only if orchestration requires it
        launchd.plist
        docs/                               # Archify source and workflow
~/development-space/worktrees/admin/
  opencode-free-router_008/                  # Linked tool worktree
```

Tool branch: `admin/opencode-free-router_008`. Shared incident tool, if selected, has its own repository and branch `admin/automation-incidents_008`. Admin source changes for a genuinely Space-owned automation use `automation/<job-name>` in Admin Git. Do not create an extra automation branch for the model tool's own job. Skill changes follow their owning repository's rules and have a separate bounded deliverable.

## Dependencies and deliverables

1. Request/design preparation can proceed before repository extraction. Plan 009 must establish the selected tool's independent repository and usable Development Space worktree before tool implementation. Other tools need not all be migrated first.
2. Define model-result and report contracts. Implement the model tool plus its own automation source together. This is one coherent deliverable in the model tool repository.
3. Shared Notion incident delivery is a separate tool deliverable with a versioned CLI contract and fake transport fixtures. A consumer records which version or revision it was checked against.
4. Rewrite launchd-automation helpers and skill as a separate capability deliverable through skill-creator. It must support both source layouts. Do not use the older helpers as if that rewrite were installed.
5. Plan 010 owns the Admin-focused Improve rewrite and docs routing. Its later plugin packaging is not a prerequisite for this model job.
6. Activate the integrated job only after source review, fixture checks, incident grouping selection, and verified unattended Notion authentication. A blocked Notion transport does not block isolated development or fake-transport tests.

## Current evidence to refresh during design

The following was inspected against the base above. Recheck before implementation:

- `automation/model-control/run-sync.sh` calls the model backend and also includes an unrelated command. Preserve that existing unrelated behavior until its separate ownership and schedule are resolved; do not silently retire it by replacing the old plist. This request does not redesign that work.
- `tools/opencode-free-router/backend/model_sync.py` owns model discovery, ranking, probes, state, and OpenCode default updates. It writes state atomically, uses a lock, and preserves the previous selection on failure. Keep existing standard-library Python conventions.
- The current public failure text reports exception class but does not identify a useful failing stage. Add safe stage attribution without leaking raw provider output.
- Benchmark cache reuse must remain distinguishable from fresh benchmark retrieval and model probing.
- Installed plist: `~/Library/LaunchAgents/com.tai.model-control-sync.plist`. Observed Label: `com.tai.model-control-sync`; calendar Hour 0, Minute 0; RunAtLoad false. Preserve label and schedule unless a separately reviewed change is needed.
- Legacy model-control compatibility assets and automation scanner references need consumer checks. Keep them until verified replacements exist.
- Plan 009 recorded 42 Admin-tracked tool paths. Adding an ignore rule alone does not untrack them. Preserve files and recoverability during extraction.

## Report and runtime contract

Source and reports are separate. Pass an explicit absolute report destination to the stable scheduled entrypoint. In a worktree, use a temporary report root and fake state/configuration. Tests must not write to the live Admin reports, OpenCode configuration, credential store, or incident queue.

The automation runner owns run lifecycle and report files. The model tool emits structured stage/result information and can work without an automation report destination. Avoid implementing generic scheduling or Notion transport inside model selection. Reuse the existing tool lock so manual and scheduled calls cannot overlap configuration mutation.

Use one writer per run log and atomic latest-result updates. Record schema version, run ID, stable job ID, request ID 008, timestamp, stage, outcome, exit code, duration, source repository and exact revision. Record dirty state when relevant; a revision alone must not misrepresent uncommitted runtime code. Record selected model before/after and whether configuration changed.

Outcomes: success, cached, failed, skipped_locked, and incomplete when observed later without a terminal result. A lock skip must not overwrite an active run's latest status. Missing starts require a separate observer, which is deferred. A runner cannot report its own absence.

Keep diagnostic stdout/stderr and per-run JSONL. Proposed retention: 30 days and at most 100 completed runs; proposed size bound: 1 MiB per run with terminal summary preserved. Confirm these values during design. Pending incident events live separately from rotated reports and never expire through report cleanup. Sanitize all report fields. Exclude secrets, raw headers, provider response bodies, prompt text, environment dumps, and arbitrary exception strings.

## Notion incident requirements and design inputs

Confirmed: local reports plus Agents Ticket on failure, repeated occurrences update an unresolved ticket, human state is preserved, later success may append recovery without closing the ticket.

Unresolved design choice: incident grouping by job plus stage plus stable error category, or one unresolved incident per job. Do not choose silently. The following detailed contract is retained for Superpowers design and fresh schema verification.

### Verified Notion destination and template

Database: https://app.notion.com/p/3ff0a859ed1f80728ae0fdb996889173
Data source: collection://3ff0a859-ed1f-80c4-b3b1-000b9c10da55
Existing default template: https://app.notion.com/p/3ff0a859ed1f80d4af62c0419119fa88 (New Intent).

The schema was fetched in this conversation. Re-fetch it before implementation and before activation. Use exact values:

- Ticket title: `[Automation] opencode-model-refresh · <stable error category>`.
- Request Type: `Fix`.
- System Component: `Automations & Runtime`.
- Target Space: `Admin`.
- Status on creation: `Captured`.
- Current Step on creation: a concise observed failure and next triage action.

The existing template contains Init tabs for Process log, Intent, Context & Sources, plus Spec & Plan. Preserve this structure. Add an automation incident summary and occurrence history. Do not overwrite human plans, decisions, status, Current Step, or existing body text on later occurrences. Use an application-owned block or section for machine updates.

No Incident Key, First Seen, Last Seen, or Count database properties currently exist. Do not invent them or change the database schema. Store these values in the owned incident section and local delivery state. A local file path is evidence on this Mac, not an externally accessible attachment.

### Shared ownership and command contract

Proposed home: `tools/automation-incidents/`. This tool owns Notion schema mapping, incident identity, delivery, replay, and ticket reconciliation. It must not contain model selection logic. The model tool emits a sanitized result envelope. The automation runner reports new terminal failures and flushes pending events on later invocations, including successful runs.

Proposed CLI contract, not an existing command:

```sh
python3 tools/automation-incidents/backend/incidents.py report --event-file <sanitized-event.json>
python3 tools/automation-incidents/backend/incidents.py flush
python3 tools/automation-incidents/backend/incidents.py status
```

`report` persists the event before attempting delivery. `flush` retries pending deliveries. `status` is read-only and includes the ticket URL, pending count, oldest pending timestamp, and last delivery error category. Do not accept shell command strings as event payloads or execute ticket text.

Before adding a Notion transport, inspect existing installed CLI/native integrations, including `skills/notion-cli/SKILL.md`. Prefer an existing supported noninteractive integration. Chat-session connector access does not prove a LaunchAgent has authentication. Do not extract desktop connector tokens. Stop activation if no approved unattended credential source exists. Use private runtime storage and minimum database access. Do not embed credentials in plist, plans, metadata, logs, or events.

### Incident lifecycle and duplicate handling

Use a stable job identity independent of folder names. Do not put timestamps, run IDs, raw URLs, or arbitrary provider text into the grouping key. Each occurrence has its own stable event ID and run ID.

On failure, query for the exact machine incident marker and an unresolved ticket. Unresolved statuses are Captured, Preparing, In progress, Human review, and Blocked. Done and Canceled are terminal. Reuse an unresolved match without resetting its status. If several exact matches exist, stop creating tickets and flag reconciliation locally. If the only previous ticket is terminal, create a new incident episode and reference the previous one.

Append one occurrence with time, stage, safe error category, exit code, effect on the current model, and local evidence path. Update first seen, last seen, and count in the machine-owned summary. Keep immutable occurrence evidence. Never replace the full page with a reconstructed copy.

Notion create/append operations are not assumed exactly once. Persist intent, serialize delivery, embed event markers, and reconcile after an unknown timeout before retrying. A lost response after successful creation must not cause a second ticket. Count unique event IDs, not send attempts. Re-fetch status immediately before updating. Respect terminal tickets and preserve user edits.

A later successful run can append recovery evidence to the existing episode. Do not automatically close or reopen a ticket. Ticket capture does not authorize an agent to repair the system autonomously.

### Offline delivery and failure containment

Keep pending envelopes and ticket mappings in ignored private runtime state under the incident tool, separate from rotating logs. Pending events must not expire with log retention. Flush pending events on subsequent scheduled invocations, including successful model runs. Bound each flush by request timeout, attempt count, and total elapsed time. Honor rate-limit retry guidance and retain permanent authentication/schema failures for human action.

A reporting failure must never recursively report itself through the same failing path. Write local delivery status and preserve the original model error. Do not count a failure to send a ticket as a successful refresh. A runner that never starts cannot report its own absence. Missing-run detection requires a separate observer and is deferred, with that limit stated in the runbook.

### Ticket body example

```text
Automation incident
Job: opencode-model-refresh
Incident key: <stable key>
First seen: <ISO timestamp>
Last seen: <ISO timestamp>
Occurrences: <unique count>
Impact: <observed effect, including whether the old default remains usable>

Occurrence history
Time | Event ID | Run ID | Stage | Error category | Exit code | Local evidence

Recovery evidence
Time | Run ID | Observed successful outcome
```

No raw provider errors, auth material, prompts, environment dumps, or guessed root causes may enter this template.


## Skill and documentation deliverable

Launchd-automation owns source classification, scheduler lifecycle, run evidence, failure recovery, and validation rules. Its scaffold, templates, and verifier must support tool-owned source and Space-owned source with an explicit report root. Prefer direct absolute executable invocation when a wrapper adds no value. Remove implicit shell-profile/version-manager/.env loading and forced restarts. Static validation must not execute the job. Read plist Label from contents.

Each source automation includes a human runbook, concise AGENTS.md, and an Archify workflow covering schedule/timezone, sleep/wake limits, tools, reports, success/cache, lock contention, tool failure, delivery failure, replay, and recovery. Use writing-for-agents for each AGENTS.md edit. Keep the report root as runtime evidence, with at most a navigation pointer to the owning runbook.

The drafts in [skill adaptation](008-skill-adaptation/README.md) are not installed. Skill-creator owns paired behavior evaluation and feedback. Plan 010 supersedes the earlier generic Improve candidate framing. Do not install that older Improve draft as the final Admin workflow.

## Verification and acceptance

Superpowers writing-plans must derive exact file changes and commands from the current owner repositories. Existing model fixtures use standard-library unittest under backend; reuse them rather than creating a parallel test layout merely to match the sketch.

Required model/report cases: new selection, cached result, benchmark fallback and stale rejection, catalog failure, all probes failed, apply failure, manual/scheduled overlap, interrupted run, disk-write failure, secret redaction, retention of active/pending evidence, and bounded report truncation.

Required incident cases: first create, repeat unresolved incident, preserved human fields, terminal recurrence, multiple matches, concurrent delivery, create/append timeout after remote success, durable queue restart, rate limiting, revoked auth, schema drift, recovery without auto-close, and no recursive reporting. Use fake Notion fixtures and isolated state.

Required source-layout cases: dedicated-tool job stays inside the tool repository; Space-coordinating job stays in Admin; a reporter dependency alone does not change ownership; worktree tests write only temporary reports; installed runner targets the stable checkout and explicit report root.

Before activation, record the exact stable tool revision and incident CLI revision, lint the source and installed plist, compare installed paths and schedule, preserve previous configuration for rollback, and verify no duplicate scheduler. An approved live run must produce a fresh run ID, terminal outcome, and expected model effect. Successful launchctl dispatch or old exit 0 is insufficient.

A real Notion smoke event requires explicit approval and a clearly labeled test record. No silent operational ticket creation. If the old runner contains unrelated scheduled behavior, resolve its continuity before replacement. Rollback restores the reviewed prior job configuration without overwriting unrelated OpenCode settings or tool runtime state.

## Review state and remaining decisions

This brief is ready for Superpowers design, not source execution. Incident grouping, approved unattended Notion transport, measured timeouts, retention values, and unrelated old-runner continuity remain design/activation inputs. They do not invalidate the accepted source ownership model.

[Plan 009](009-development-space-cli-tools.md) owns independent tool repositories, the workshop rename, and worktrees. [Plan 010](010-admin-workflow-composition.md) owns Admin workflow docs and the Improve rewrite. [Tools handoff draft](010-admin-workflow-draft/docs/tools.md) defines traceability.

[Workflow preview](008-automation-visual/automation.html) is a proposal. Its validation receipts establish rendered output only, not job runtime or implementation readiness. The written ownership and report contract in this brief is authoritative if an older preview differs.
