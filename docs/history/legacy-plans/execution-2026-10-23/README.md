# Execution record: Admin upgrade 008 / 009 / 010

Started 2026-10-23. This record holds the reconciled execution order, the actual
repository boundaries, and the evidence produced by each batch. It does not
replace the request briefs.

Source requests:

- [008 · Reliable OpenCode model refresh](../008-opencode-model-refresh.md)
- [009 · Development Space and independent tools](../009-development-space-cli-tools.md)
- [010 · Admin planning profile and docs](../010-admin-workflow-composition.md)

## Reconciliation against the current direction

The 2026-10-23 direction supersedes three proposals in the briefs. These are the
binding readings used here.

| Brief proposal | Current direction | Effect on this execution |
| --- | --- | --- |
| 010 rewrites Improve into an Admin advisor skill | Establish an Architect & Planning Profile from selected Agent Skills plus concise docs references | Improve is left unchanged and stays available. No rewrite was performed. The profile is written as a draft definition, not a deployed runtime. |
| 008/010 install a replacement Improve candidate | Keep Improve until the replacement passes representative behavior checks and references migrate | The old candidate under `plans/008-skill-adaptation/candidate/improve/` stays a record. It is not installed. |
| 008 owns generic report and Notion logic inside model selection | Split: model tool + its own automation in the tool repo; shared incident delivery in its own tool repo | Implemented as two repositories plus one tool-owned job. |
| 010 packages an `admin-workflows` plugin | Plugin packaging is a later step after the format is demonstrated | No plugin was created. `docs/admin-workflows.md` remains the single routing authority. |

The drafts in `plans/010-admin-workflow-draft/` are design inputs. `review.md`
there is a planning review only; it does not accept installation.

## Repository boundaries as executed

| Boundary | Location | Git owner |
| --- | --- | --- |
| Admin contract, docs, Space orchestration, skills | `~/.agents/` | Admin repository |
| Independent tools | `~/.agents/tools/<tool-name>/` | Each tool's own repository; ignored by Admin Git |
| Engineering workshop | `~/development-space/` | Development Space repository |
| Tool development worktrees | `~/development-space/worktrees/admin/<tool-name>_<request-id>/` | The tool repository; ignored by Development Space Git |
| Tool-owned automation source | `<tool>/automation/<job-name>/` | The tool repository, on the tool task branch |
| Space-owned automation source | `~/.agents/automation/<job-name>/` | Admin repository, branch `automation/<job-name>` |
| Runtime reports (both kinds) | `~/.agents/automation/<job-name>/logs/` | Ignored by Admin Git |

A shared incident reporter dependency does not change source ownership. The
model-refresh job stays tool-owned even though it calls `automation-incidents`.

## Execution order

Order is dependency-bound, not priority-bound. Each batch ends with its own
checks; the cumulative diff is reviewed once at the end.

| # | Batch | Request | Why it must be here |
| --- | --- | --- | --- |
| 0 | Reconcile plans, record boundaries | 008/009/010 | Prevents two competing plans for one deliverable |
| 1 | Workshop path migration and consumer repair | 009 | Tool worktrees live under the moved path |
| 2 | Independent tool repositories and Admin index transition | 009 | 008 cannot branch or use a worktree before this |
| 3 | Documentation and planning-profile format | 010 | Defines the handoff used by batches 4-5 |
| 4 | Model tool + tool-owned automation | 008 | Needs the tool repository and the handoff contract |
| 5 | Shared Notion incident tool | 008 | Needs the report contract from batch 4 |
| 6 | launchd-automation rewrite and validation | 008 | Independent capability; validated against the layouts from batches 4-5 |
| 7 | Cumulative review and verification | all | Single final validation |

Batch 3 was ordered before 4 because the tool handoff fields are an input to the
worktree task, not an output of it.

## Preserved runtime behavior

Recorded before any mutation. Nothing in this execution changes a schedule.

| Live surface | State at start | Action taken |
| --- | --- | --- |
| `com.tai.model-control-sync` | Loaded, daily 00:00, `RunAtLoad` false | Not booted out, not replaced, not kickstarted |
| `com.tai.linear-notion-sync` | Loaded, daily 00:00, runner under the old workshop path | Path reference repaired; job reloaded; not kickstarted |
| `com.tai.bridge.sync` | Loaded | Untouched |
| OpenCode default model | `opencode/deepseek-v4.1-flash-free` | Unchanged by this execution |
| Notion | No ticket created | No test ticket created |

## Open decisions carried forward

Not silently resolved. Each is reported with a recommendation.

1. Incident grouping: `job + stage + stable error category` versus one unresolved
   incident per job.
2. Unattended Notion authentication source for a LaunchAgent.
3. Final profile name, runtime configuration format, attached skill set, ticket
   trigger, and independent-review threshold.
4. Old `run-sync.sh` continuity: it calls model sync and a PaperQA index helper.
   The helper is unrelated scheduled behavior.
5. Report retention and timeout values are proposed, not measured.
6. `bin/sync-skills` drift: 55 missing links and 43 absolute paths across the
   Claude Code and Gemini mirrors. Unrelated to this execution; unrepaired.

## Status after batch 7

All seven batches are complete as scoped work. Cumulative state: 83 tests
passing, plists lint, no broken links in the changed surfaces, no secret
strings, and no live schedule or model default changed. Four deliverables are
implemented but deliberately inactive — the replacement job is not loaded, the
Notion transport has no credentials, the profile is a draft, and the incident
grouping policy has no value. Levels and gates are itemized in
[batch-7-verification.md](batch-7-verification.md).

## Evidence index

| Batch | Evidence file |
| --- | --- |
| 1 | [batch-1-workshop-migration.md](batch-1-workshop-migration.md) |
| 2 | [batch-2-tool-repositories.md](batch-2-tool-repositories.md) |
| 3 | [batch-3-docs-profile.md](batch-3-docs-profile.md) |
| 4 | [batch-4-model-refresh.md](batch-4-model-refresh.md) |
| 5 | [batch-5-incidents.md](batch-5-incidents.md) |
| 6 | [batch-6-launchd-skill.md](batch-6-launchd-skill.md) |
| 7 | [batch-7-verification.md](batch-7-verification.md) |
