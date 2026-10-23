# Model Refresh Remaining Gates Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans or superpowers:subagent-driven-development after the gated design is ready.

**Goal:** Preserve request 008's remaining work without repeating implemented code.

**Architecture:** Keep tool source in its independent repository and develop in its existing worktree. Qualify stable integration before separately authorized activation. Incident delivery remains independent of refresh outcome.

**Tech Stack:** Existing Python runner, launchd, automation-incidents and native Notion transport.

**Spec:** [Request 008](../../history/legacy-plans/008-opencode-model-refresh.md) and [verification record](../../history/legacy-plans/execution-2026-10-23/batch-7-verification.md).

## Global Constraints

- No tool mutation or scheduler activation is performed by this migration.
- Preserve the legacy schedule and its unrelated indexing responsibility.
- Preserve outcome/exit status when incident delivery fails.
- Keep credentials outside tracked files and use temporary state for fixtures.
- Review current evidence; archived test counts are historical.

## Review Focus

- Stable runner path must exist before installing its plist (Task 1).
- Legacy indexing must retain an owner (Task 2).
- Unresolved incident grouping must fail explicitly (Task 2).
- Failed delivery must remain replayable without another refresh (Task 2).
- Live checks must distinguish dispatch from terminal result (Task 3).

### Task 1: Qualify the existing tool branch for integration

**Files:** Existing independent opencode-free-router worktree's backend and automation/model-refresh/. Inspect its AGENTS.md before changes.

**Interfaces:** Produce the reviewed tool diff, exact revision, fixture results and integration/rollback proposal.

- [ ] Verify branch/worktree/base and current dirty state. Read the runner, tests,
  plist and runbook. Do not regenerate code from the old request.
- [ ] Run the tool's documented model and runner tests in isolated state. Record
  commands and results against the exact revision. Review cumulative changes.
- [ ] Integrate only under the tool repository's authorized workflow. Verify the
  stable runner path and source revision before proposing any live activation.

### Task 2: Resolve activation design gates

**Files:** Existing source runner/runbook/plist and the legacy indexing helper.
Freeze exact paths and commands in this task after discovery and design approval.

**Interfaces:** Produce the selected indexing owner, incident grouping config,
credential source reference, replay checks and reversible activation sequence.

- [ ] Establish how indexing continues if model-control is replaced. Review the
  replacement indexing job separately with launchd-automation before deployment.
- [ ] Select incident grouping explicitly. Verify unattended Notion authentication
  without printing secrets. Test failure and one recovery episode in fixtures.
- [ ] Test good refresh plus failed delivery: refresh outcome/exit unchanged,
  latest-delivery records failure, pending event remains, replay does not rerun
  refresh. Test missing config as a clear configuration failure.

### Task 3: Activate only after explicit live-job authorization

**Files:** The reviewed source plist, installed plist and explicit runtime root.

**Interfaces:** Produce installed/source comparison and a fresh terminal result.

- [ ] Use launchd-automation static checks. Record old schedule, backup and rollback.
- [ ] Obtain authorization for the exact labels and execute the accepted sequence.
- [ ] Verify a fresh terminal outcome, correct model effect and incident behavior.
  Roll back under the approved recovery sequence if acceptance fails.

## Readiness

This is a gated continuation, not an executable activation order. Task 2 needs
selected live configuration and exact commands. The user deferred tool work;
none is dispatched by creating this file. Self-review: all remaining batch-7
activation gates map to Tasks 1–3; completed extraction and tests are not repeated
as new feature work.
