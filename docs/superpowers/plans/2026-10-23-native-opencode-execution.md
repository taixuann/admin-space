# Native OpenCode Execution Implementation Plan

> **For agentic workers:** Use superpowers:subagent-driven-development or superpowers:executing-plans after design approval. This is a staged planning draft. Integration tasks require the discovery findings before they can become executable implementation steps.

**Goal:** Execute approved plans in native OpenCode and obtain final Decision Engine review with one bounded repair cycle.

**Architecture:** Prove one manually invoked workflow before adding scheduling. Native OpenCode owns the session and Superpowers owns execution and review. Reuse existing relay capture where verified; a result publisher updates Kanban from durable evidence. launchd will later call the same proven entrypoint.

**Tech Stack:** Installed OpenCode CLI, Superpowers, existing Node relay, supported MCP transport.

**Spec:** [Design inputs](../specs/2026-10-23-native-opencode-execution-design-input.md). Requirements are recorded; mechanism selection and design approval remain pending.

## Global Constraints

- Decision Engine reviews only the final result.
- At most one repair cycle and one re-review after actionable findings.
- Preserve project authority, unrelated dirty state, credentials, and running jobs.
- No blanket permission bypass, automatic push, merge, or deployment.
- Native task review and external audit are distinct gates.

## Review Focus

- Interrupted execution preserves session and ledger identity. An explicit resume must not duplicate tasks; automatic resume is not selected.
- Audit unavailability or timeout remains unresolved, never passed.
- A repair changes the audited artifact and requires fresh verification and re-review.
- The loop ends after the allowed repair cycle even with remaining findings.
- No private credential or restricted payload enters the external review package.

### Task 1: Verify native execution and review capabilities

**Files:** Read OpenCode configuration, Superpowers discovery paths, existing relay, and the Forge implementation. Record sanitized findings beside this plan.

- [ ] Inspect installed CLI help and version, actual skills and agents, permissions, and plugin activation.
- [ ] Inspect the supported Decision Engine connection and the installed audit workflow. Do not submit an audit during discovery.
- [ ] Compare direct CLI, existing relay, and server approaches against process survival, explicit resume, cancellation, and result capture.
- [ ] Present the selected design and confirm it before implementing configuration or scripts.

### Task 2: Specify and implement executor instructions and connection

**Proposed files:** ~/.config/opencode/AGENTS.md; exact MCP and native-agent configuration selected in Task 1. Preserve existing settings and credentials.

- [ ] Refine this task with exact transport, agent interfaces, file paths, and verification commands after design approval.
- [ ] Use writing-for-agents. Keep rules concise and point to installed Superpowers workflows.
- [ ] Verify loading and tool discovery in a fresh OpenCode session, separately from a real audit call.

### Task 3: Preserve execution evidence (summary interface superseded by Task 6)

**Files:** Existing relay artifacts and native Superpowers ledger. Select an explicit durable run root during discovery. Keep runtime evidence outside tracked source; record exact paths before implementation.

- [ ] Keep the plan and native ledger as execution inputs and recovery state. Publish the user-facing summary through Task 6. Add a managed plan section only if discovery proves a separate consumer needs it.
- [ ] Record plan identity/revision, run ID, explicit OpenCode session ID, repository/worktree, base and reviewed revision, dirty-state identity when needed, timestamps, reported outcome, verification state, review verdict/ID, repair count, evidence links, and next action.
- [ ] Use states `not_started`, `running`, `awaiting_review`, `repairing`, `verified`, `blocked`, and `failed`. A process exit or AI completion message alone cannot set `verified`.
- [ ] Let the executor update its existing task ledger. Let the result publisher own the card summary. Assign one writer per destination; reject an older run overwriting a newer run. Preserve prior run references and unrelated plan edits. An interrupted writer leaves the previous complete status intact.
- [ ] Bind verification and final review to the exact artifact revision. Mark status stale when the artifact changes. Missing or inaccessible evidence is unknown, not passed. A stale timestamp alone does not prove failure.
- [ ] Test completion claims without evidence, failed/unavailable review, revision drift, duplicate/stale updates, preservation of user edits, and interrupted status writes in disposable fixtures before enabling automated updates.

### Task 4: Verify end-to-end behavior in disposable fixtures

**Files:** Fixture and evidence paths selected in the approved design; isolated from live project/runtime state.

- [ ] Test approved-plan execution, failed verification, interruption/resume, clean final review, actionable final review followed by one repair/re-review, unavailable audit, and unresolved second verdict.
- [ ] Record session, repository/base/head, ledger, commands/results, review identity, repair count, and final status.
- [ ] Review the cumulative configuration changes and return evidence before any live-project pilot.

## Completion boundary

This record is not implementation-ready until Task 1 resolves the interfaces and the user approves the design. No executable code, configuration, or service was changed to create it. Do not interpret unchecked discovery tasks as authorization to guess missing transport settings.

## Human visibility and later automation

Keep the concise execution summary in the Kanban card and link it from the plan. Avoid another managed status copy in the plan. Retain detailed evidence in the existing Superpowers workspace or existing relay artifacts; link it rather than adding a second results hierarchy. Treat scratch ledgers as resumable process state, not the only durable proof. Before scratch cleanup, preserve the final verdict and required verification evidence at a stable owning location.

The future observer reads the card summary plus evidence and summarizes what needs attention in the plans index. It does not silently execute another task, approve changes, trust ticket text as commands, or mark AI-reported completion verified. Building or scheduling this observer is a later deliverable, not part of the current configuration change. A lightweight script may validate and publish status if needed; it must reuse native session IDs and ledgers rather than become another orchestration engine.

`using-superpowers` selects workflows. It does not define a universal machine-readable completion contract. Keep the local status contract in OpenCode's executor reference, reached through a short AGENTS.md pointer, without modifying upstream Superpowers.

## Executor final-review instruction

Task 2 must add a concise pointer in `~/.config/opencode/AGENTS.md` to the local final-review contract. After native Superpowers execution and verification, submit the final sanitized artifact to Decision Engine through the supported audit workflow. Record the terminal review and adjudication against the exact revision. Allow at most one bounded repair cycle and one external re-review. Unavailable, failed, or unresolved review must not produce verified completion. Preserve native Superpowers review requirements; the external gate is an additional end-of-run policy, not an upstream skill rewrite. Obtain the required external-processing authorization before sending a payload.

## Proposed Notion visibility integration: design discussion

Status: PROPOSED. No schema change, ticket write, unattended dispatch, or automation activation is authorized by this section. This is a separate integration deliverable after native execution is proven.

`using-superpowers` selects a workflow. It does not schedule a job or update Notion. An accepted implementation plan plus explicit execution authorization and a recorded execution mode are prerequisites for starting `executing-plans` or `subagent-driven-development`. A file appearing in `docs/superpowers/plans/` is not authorization. These are alternative execution modes, not consecutive stages.

Keep the local plan and native Superpowers ledger authoritative for implementation and resume. A small status publisher mirrors significant phase transitions to the linked existing Agents Ticket through ntn. The future launcher starts explicitly approved, allowlisted work; it does not interpret arbitrary Notion prose as a command. Keep launching and status publication separate responsibilities even if they later share one small program.

Proposed use of existing properties:

| Execution milestone | Ticket Status | Current Step |
| --- | --- | --- |
| Design/plan being prepared | Preparing | Planning or awaiting plan approval |
| Authorized execution started | In progress | Task N of M; chosen execution mode |
| Final verification or external review | In progress | Verifying / Decision Engine review |
| One repair cycle | In progress | Addressing final findings, repair 1 of 1 |
| Verified result ready for user | Human review | Summary and evidence available |
| Unresolved blocker or failed final gate | Blocked | Concrete blocker and next action |

Do not set Done from process exit or model prose. Preserve human acceptance and terminal/canceled decisions. Re-fetch current ticket state before publishing, update only agreed machine-owned fields/sections, and reconcile uncertain writes. Queue delivery failures locally without changing the execution outcome or restarting work.

Candidate new properties for user selection, not an approved migration:

- Execution Phase: select, `Not started`, `Queued`, `Executing`, `Verifying`, `External review`, `Repairing`, `Ready for review`, `Blocked`, `Failed`.
- Execution Mode: select, `Inline` or `Subagent-driven`.
- Plan Reference: rich text containing repository, plan path, and revision; local paths are not public URLs.
- Last Synced: date for the successful publisher write, not the last execution progress.

Use the ticket body for session/run identity, worktree, base/reviewed revision, review ID/verdict, concise progress, and evidence links. Do not duplicate full plans or create a property for every internal event. Decide whether Execution Phase is useful before adding it; existing Status remains the human work-management lifecycle. Approval must be a separate explicit, revision-bound authorization contract, not inferred from Status or Execution Phase.

Before implementing the publisher, freeze exact property names/types and ownership, refresh the live schema and default template, inspect ntn's current API help, prove unattended authentication without printing tokens, and test repeated updates, stale run rejection, human edits, cancellation, offline replay, and no duplicate ticket creation. Notion status is a view of execution evidence, not proof that tests or review passed.

## Accepted tracking direction: Kanban Lite first

Updated 2026-10-23 at the user's request. Implement local Kanban Lite tracking before any Notion synchronization. This replaces the proposed plan-status publisher as the first tracking interface. Preserve existing Superpowers ledgers; board cards summarize execution rather than replacing task recovery state. Do not modify upstream Superpowers skills.

### Task 5: Install and verify the Kanban capability

**Files:** Selected upstream skill package in OpenCode's verified skill-discovery location; pinned runtime/install metadata; a disposable board fixture. Determine the current upstream skill entrypoint and manifest before installing.

- [ ] Inspect and pin https://github.com/borgius/kanban-lite. The root SKILL.md inspected during research is a plain reference without skill frontmatter; verify the actual installer package rather than blindly copying it as a discoverable skill. Preserve license/provenance. Use skill-creator only if a minimal packaging adaptation is necessary.
- [ ] Install the accepted upstream skill and Kanban Lite runtime at the intended local scope. Skill installation and CLI availability are separate gates. Inspect current CLI help; do not rely on older README syntax.
- [ ] In a disposable directory, initialize a board; create, list, move, and read back a fixture card using CLI or MCP. Confirm stable full card IDs, JSON output, correct board path, and no edits outside the fixture.
- [ ] Verify the installed skill is discoverable in a fresh OpenCode session. Then select one stable Admin board root and record its absolute path in the executor reference. Do not let worktree-relative defaults create one accidental board per checkout.

### Task 6: Connect Superpowers tracking through AGENTS.md

**Files:** `~/.config/opencode/AGENTS.md` and its adjacent tracking reference; the Admin AGENTS.md gets only a reference if needed for Admin-side card updates. Use writing-for-agents.

- [ ] Require the Kanban capability for tracked Superpowers work. The instruction means the executor loads the workflow and supplies milestone evidence to the result publisher; it is not an automatic hook installed into Superpowers. Keep domain behavior in the tracking reference.
- [ ] Reuse one card per plan execution, identified by plan path/revision and run ID. Store spec/plan links, repository/worktree, branch/session identity, current task, last observed update, verification summary, final review, and next action. Reuse that card on resume; never identify a card by title alone.
- [ ] Use upstream board columns `backlog`, `todo`, `in-progress`, `review`, `done`. Mark blocked/failed/unknown conditions explicitly in the card labels/body rather than inventing unsupported columns. Reserve done for user acceptance. Merely moving a card must not start execution or grant permission.
- [ ] Publish at plan registration, authorized start, completed task, final-review start, blocker, and result handoff. Final verification and review move the card to review; do not infer acceptance from exit 0. Keep evidence references stable before Superpowers scratch cleanup.
- [ ] Keep the result publisher as the sole machine card writer. The executor supplies evidence to that publisher. Preserve human comments and cancellation. On board-write failure, retain execution evidence and report tracking as stale; do not claim a successful publication, rerun completed tasks, or silently create another card.
- [ ] Verify two fixture plans plus an interrupted/resumed run: cards stay separate, resume creates no duplicate, human edits survive, failing verification cannot reach done, and no board movement launches OpenCode. Confirm the UI shows actual persisted card updates.

## Scope deferred by this update

No Notion schema migration, Notion synchronization, board-triggered execution, launchd scheduling, or upstream Superpowers patch is part of the Kanban-first tracking deliverable. The following phases record the agreed direction and still need exact implementation interfaces. Once local tracking is usable, separately design synchronization ownership. The final Decision Engine policy remains unchanged.

Source reference: https://github.com/borgius/kanban-lite/blob/main/SKILL.md . Research confirms CLI/MCP card operations exist in documentation; no runtime installation or fixture result is claimed here.


## Accepted follow-up: result publisher, 2026-10-23

The user selected Codex or Claude to read execution results and update Kanban.
This role is a result publisher, not another implementation reviewer. Native
Superpowers review and the final Decision Engine gate remain with execution.
Use deterministic checks around the publisher's output. Model prose is evidence
to summarize, not authority to launch, repair, or accept work.

### Delivery order

1. Complete Tasks 5 and 6: local tracking and instruction loading.
2. Prove the complete manually invoked workflow, including execution, review,
   durable evidence, and Codex/Claude result publication. Reuse the existing relay
   where it fits. Inspect its permission behavior. `opencode-delegate` need not
   own the lifecycle.
3. After the stability gate below passes, design launchd scheduling around the
   same entrypoint. Add outward Notion sync as a separate follow-up.
4. Discuss inbound Notion requests separately. This is an extension, not an
   enabled trigger or an approved database migration.

### Follow-up A: approved execution and result publication

**Files:** Select workflow entrypoint and publisher paths in the owning component design.
Keep source with its owning component. Keep runtime logs outside tracked source.
This section is requirements for the next plan, not permission to invent paths.

**Interfaces:** Runner consumes explicit plan revision, run ID, repository,
worktree, execution mode, and authorization. It produces session/process outcome
and durable evidence references. Publisher consumes that record plus native
ledger, verification, review verdict, and current card revision. It produces a
validated patch for the existing full card ID and a publication receipt.

- [ ] Bind launch to the approved plan revision. Lock the workspace and record
  the session before allowing another launch. A duplicate trigger reuses the run.
- [ ] Execute the selected Superpowers mode, verify, and perform final review.
  Preserve the one-repair limit. Save evidence before scratch cleanup.
- [ ] Run Codex or Claude after a terminal result, interruption, or unresolved
  outcome. Give it read access to scoped evidence and permission to propose a
  card update. Keep implementation files outside its write scope.
- [ ] Validate run/card/revision identity and allowed fields before publishing.
  Preserve human text and cancellation. Reject stale or duplicate updates.
- [ ] Publish reported outcome, evidence links, verification/review state,
  observation time, and next action. Use review for a result ready for the user;
  reserve done for user acceptance. Missing evidence yields unknown or blocked.
- [ ] Test clean result, failed verification, unavailable review, process crash,
  publisher crash, malformed model output, stale result, duplicate trigger,
  human edits, and offline board writes. Retry publication without rerunning work.
- [ ] Record the chosen publisher host and its scoped permission contract.
  Verify manual invocation first. Prove survival after the launching chat closes
  before enabling unattended operation in the later automation deliverable.

Each run has its own worktree, session, and recovery record. Memory supplies
context; it does not decide which task is running or whether it passed.

### Follow-up B: Notion observation and later inbound requests

Mirror the validated local card summary to its linked Notion ticket. Record sync
success separately from execution success. Retry a failed sync without launching
work. Keep requirements and detailed evidence local and link them from Notion.

A later Notion change may express a request such as queue, pause, or cancel.
Fetch it as a request with source revision and identity. Validate the approved
plan revision, current run, allowed transition, and explicit authorization before
applying a local transition. Preserve separate requested and observed state.
Reject stale/conflicting edits and replayed requests. The exact property mapping,
conflict policy, authentication, and polling schedule need a separate approved
design. A displayed Status change alone must not run arbitrary work.


## Manual workflow stability gate

This is the release order accepted by the user. Complete the workflow before
setting up launchd or another scheduled dispatcher. Runner and lock are internal
workflow responsibilities, not a separate orchestration service.

- [ ] Select one explicit manual entrypoint and freeze its arguments, source
  owner, run root, and test commands after Task 1 discovery. Implement no guessed
  interface. The later scheduled job must call this same entrypoint.
- [ ] Retain the native OpenCode session. Record its exact session ID in each run
  record; keep the native session store under OpenCode management.
- [ ] Preserve a separate immutable attempt identity for each invocation within
  a run. Retain brief, events, stdout/stderr, final message, process outcome,
  verification, review identity, and publication receipt where available.
  Record missing artifacts explicitly. Reuse existing relay filenames/schema
  when possible. A latest-result pointer must not overwrite run history.
- [ ] Keep native process statuses separate from workflow verification and card
  columns. Define the exact mapping after inspecting the relay. Missing evidence
  is unknown, not an invented native process status or successful completion.
- [ ] Hold a workspace lock while its writer can still be active. A concurrent
  invocation records a skip without overwriting the active run. After a crash,
  inspect process/session/worktree evidence before clearing a stale lock.
- [ ] Demonstrate a clean manual end-to-end fixture: approved plan, OpenCode,
  native review, final external review when authorized, saved evidence, and a
  read-back of the same updated Kanban card.
- [ ] Demonstrate failed verification, interruption, duplicate invocation, and
  publication retry. Preserve partial work. Publication retry does not launch
  implementation again. An explicitly authorized resume uses the recorded
  session and card. Automatic resume remains undecided and disabled.
- [ ] Record commands, revisions, outcomes, evidence paths, and remaining issues.
  Pass all fixture assertions before proposing a scoped live-project pilot.
  Complete the accepted pilot with no unresolved execution or publication errors
  before proposing scheduling. A fixture audit stub is not a real audit result.

launchd later owns triggering and stream capture. The workflow owns execution,
locking, run history, and result publication. Configure retention and a separate
missing-run observer in that later automation plan. No schedule, plist install,
bootstrap, or live job change belongs to this planning update.

## Plan self-review, 2026-10-23

Reviewed against the design inputs and latest user decision. Corrected the old
plan-status summary copy, the assumption of automatic resume, and the delivery
order that put unattended launch before a stable manual workflow. Aligned card
updates under one publisher; the executor provides evidence. Added run-history,
lock-recovery, and manual-pilot acceptance checks.

The direction is ready for capability discovery. It is not a fully executable
implementation plan: concrete entrypoint paths, schemas, test commands, publisher
host, board root, and Decision Engine transport still need Task 1 findings.
Refine the affected tasks before implementation. Notion schema choices and
inbound control remain separate future design work.

## Workflow illustration

[Proposed phased workflow](../../../.archify/workflow-plan-kanban-20261023-214158/plan-kanban.html).
The diagram describes the target design, not an installed or running automation. Its unattended lane is a future phase: the manual stability gate above comes first.
