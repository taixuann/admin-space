---
name: launchd-automation
description: Plan, create, migrate, inspect, and troubleshoot macOS launchd automations. Owns the tools and automation boundary, per-job documentation, Archify workflow, logs, incident recovery, and safe service verification. Use for scheduled macOS jobs, LaunchAgents, launchctl problems, or automation lifecycle plans.
compatibility: macOS (darwin)
---

# Launchd automation

Own the automation contract. Other planning skills refer here for domain rules. Follow the owning workspace's instructions and the user's authorized scope. Write maintained artifacts in English.

## Inspect before changing

Identify the owning workspace, job name, launchd label, source and installed plist, runner, called tool, schedule, environment, side effects, logs, and recovery path. Read component instructions. Compare installed files with maintained source. Preserve running jobs and unrelated edits.

For discussion or planning, inspect without installing, restarting, scaffolding, or switching branches. Distinguish confirmed facts, assumptions, proposed behavior, and unresolved decisions.

## Source layout and branch

Classify source by its primary responsibility. A job dedicated to one tool lives under that independent tool repository's `automation/<job-name>/`. A job coordinating several independently owned tools or enforcing Space policy lives under the owning Space's `automation/<job-name>/`. A shared incident reporter alone does not change ownership. Keep reusable business logic in the tool backend and call existing entrypoints.

Each source automation contains README.md, AGENTS.md, its source plist, an optional thin runner, and docs/ with the Archify workflow. Write runtime reports to an explicit report root, which can be outside the source repository. In Admin, use `~/.agents/automation/<stable-job-name>/logs/` and ignore reports in Git. An optional README there points to source without duplicating its runbook.

For an Admin tool request, develop in a tool worktree on `admin/<tool-name>_<request-id>`, including that tool's automation source. For a Space-owned Admin job, use `automation/<job-name>` in the Admin repository. Follow the tool-handoff docs for worktree naming. Planning alone changes no branch. Verify collisions and dirty state before selecting a worktree; preserve unrelated work.

Treat the numbered Admin request as intent and acceptance criteria. Use the full Superpowers pipeline to derive and execute the implementation plan after design approval. Do not infer deployment or integration authority from a request ID or branch name.

## Explain before activation

Use Archify alongside the plan before deploying or changing the service. During planning, keep outputs with the plan. During implementation, keep the maintained diagram in the automation's `docs/` and link it from README. Follow Archify's validation workflow.

Show trigger, schedule and timezone, runner, tool, inputs, outputs, logs, and recovery. Show success, cached/no-change, lock contention, execution failure, reporting failure, queued replay, and interrupted/missing runs where applicable. Mark non-applicable cases with a reason. Label observed and proposed paths. Do not invent runtimes or claim the runner can detect its own absence.

README explains purpose, trigger, local-time or explicit timezone behavior, sleep/wake behavior, tool entrypoint, inputs and outputs, manual execution, logs, failure handling, rerun, and rollback. AGENTS defines scope, safe inspection, mutation authority, credential boundaries, and completion checks. Keep detailed tool policy with the tool.

## Runtime and evidence

Use absolute executable paths and an explicit minimal environment. A wrapper is optional when the plist can call the tool directly. Do not implicitly load shell profiles, version managers, or `.env` files. Use only the approved credential mechanism. Never print secrets.

Define a run ID, source repository/revision and dirty state, timestamps, terminal outcome, exit code, duration, and sanitized error context. Use temporary report and state roots for worktree tests. Keep stdout/stderr available for diagnosis. Use structured per-run evidence and a latest-result summary when the job needs machine-readable status. Define bounded retention and rotation. Ignore logs, locks, queues, credentials, and mutable runtime state in Git.

Prevent overlapping mutations. Record lock contention as a skipped run. Do not kill the existing run to force a check. Define timeout, interruption, stale-lock recovery, and preservation of the last valid tool state.

When the job has Notion incident reporting, use the owning incident tool and verify the live database schema. Save the sanitized event before delivery. Reuse an unresolved ticket under the agreed grouping rule. Preserve human fields and status. Report recovery without automatically closing the ticket. Keep pending events separate from rotated logs. Reconcile uncertain deliveries before retrying, and bound retry time and attempts. Reporting failure must not recursively create incidents. Chat connector access does not prove unattended credentials work.

Success normally stays in local evidence. A missing run requires a separate observer if alerting is required. Do not silently add one.

## Deploy and verify

Before deployment, validate plist syntax, executable and working-directory paths, permissions, environment, documentation links, and diagram validation. Inspect bundled scaffold, templates, and verifier before using them; they must match this contract. Do not run older helpers that source implicit environment or force restarts.

Use modern `launchctl bootstrap`, `bootout`, and `print` with the correct user domain. Changing or stopping a live service must fall within the user's authorization. Preserve the previous plist and record rollback. Do not suppress lifecycle errors without examining them.

A successful dispatch is not a completed run. For an authorized live check, trigger without `-k`, wait with a bounded limit, and verify a fresh run ID, terminal result, exit code, and expected output or side effect. Empty stderr alone is insufficient. Use `-k` only when interruption is explicitly authorized and safe.

Validate failure, overlap, and reporting recovery with isolated fixtures before any live side effect. Do not create a real ticket merely to test documentation. Report configuration validation separately from runtime validation, including any checks not performed.
