# Planning review, 2026-10-23

Scope: requests/plans 008, 009, 010, tools handoff draft, launchd candidate, and skill adaptation notes. Base: `40e9d38238e487744ec216f5a57617e3c09cfb3e`. Planning review only; no implementation acceptance.

## Reconciled issues

- Request 008 mixed intent, executable steps, revisions, and multiple source owners. It is now one request brief with separate deliverables, dependencies, and remaining design choices. Superpowers derives the implementation plan after design approval.
- Tool-specific automation was forced into Admin source and a second branch. It now stays in the tool repository; only Space orchestration uses the Admin automation branch convention.
- Source and runtime report ownership were ambiguous. Both job types use explicit ignored Admin report roots; worktree fixtures use temporary reports and fake state.
- Replacing the old runner risked silently removing unrelated scheduled behavior. Its continuity is now an explicit prerequisite to replacement.
- The older Improve candidate and evaluation expectations were stale. The candidate is marked superseded for installation; fixtures now reflect request tracing and source ownership.

## Fresh-context review

The reviewer found two actionable P2 issues, both corrected:

1. Plan 009 activated skill packages before behavioral acceptance. Inspection now stays staged; installation and fresh-session loading follow evaluated acceptance.
2. Plan 009's worktree tree contradicted the Admin naming contract. The tree now uses `worktrees/admin/<tool-name>_<plan-number>/`.

## Result

The reviewed planning model is ready for Superpowers design. This is not approval to execute, deploy, or install. Incident grouping, unattended Notion transport, report retention and timeout values, and the old runner's unrelated task continuity remain explicit design/activation decisions. Plan 007 stays deferred.

Archify request-008 preview passed validation, delivery, artifact checks, and browser checks. Structural checks do not prove skill behavior, scheduler health, model routes, or Notion delivery. No paired behavior evaluation or live runtime test ran in this review.
