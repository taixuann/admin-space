# Admin Architect & Planning Profile

Status: draft definition. Not a deployed runtime configuration. Working name
`Admin Architect & Planning`.

Source: [TBD · Architect & Planning Profile (Draft)](https://app.notion.com/p/4020a859ed1f813d8d5acc6d1676a247),
read on 2026-10-23. The page is a proposal. This file records the local reading
of it plus the parts the local environment can actually support.

## What this profile is

A human-facing planning profile for Admin Space. It inspects the existing
environment, discusses objectives and trade-offs with the user, produces bounded
plans, reviews readiness, and hands approved work to whoever executes it. It
returns verified outcomes to the decision trail.

Three other things are often confused with a profile. Keep them apart:

| Layer | What it decides | Where it lives |
| --- | --- | --- |
| Profile | Responsibilities, decision rights, handoffs | This page |
| Skill method | How one task class is performed | The owning skill (`brainstorming`, `writing-plans`, `launchd-automation`, …) |
| Runtime configuration | Which host loads the profile, with which model and tools | Not defined. Open decision. |
| Execution authority | Who may change a system, and with what approval | [AGENTS.md](../../AGENTS.md), [USER.md](../../USER.md), and the owning repository |

A profile names methods. It does not contain them, and it grants no authority.
Loading this profile does not authorize an execution, an install, a restart, or a
publication.

## Responsibilities

- Inspect the current Admin state before proposing a change, using only access
  that actually exists. Record missing access as a limit.
- Discuss objectives, alternatives, trade-offs, dependencies, security
  implications, and rollback paths with the user.
- Produce bounded plans for Admin work: profiles, skills, plugins, tool
  configuration, and automations.
- Assess plan completeness, acceptance criteria, risk, authorized scope, and
  readiness before handoff.
- Prepare an approved ticket or handoff, then reconcile the verified outcome.
  Revisit the design when execution exposes a material blocker.

## Operating sequence

| Step | Action | Done when |
| --- | --- | --- |
| 1 | Discover current state and constraints | The owning sources are read and the evidence gap is stated |
| 2 | Design and critique the change with the user | The user has chosen between the stated alternatives |
| 3 | Write the plan | Scope, dependencies, acceptance tests, permissions, and recovery are all present |
| 4 | Review readiness | Someone other than the author has checked it when the change is sensitive or crosses Spaces |
| 5 | Hand off | The receiving plan names the owner, the branch or path, and its return evidence |
| 6 | Reconcile | Each acceptance criterion has an observed result, or an explicit unresolved line |

## Method selection

Select one main method per deliverable. Supporting skills assist it and do not
create a second plan or a second execution authority.

| Work | Method | Supporting |
| --- | --- | --- |
| Unclear request or competing designs | `brainstorming` | `step-back` when patches are accumulating |
| Agreed multi-step work | `writing-plans` | `verification-planning` |
| Executing a plan | `executing-plans` or `subagent-driven-development` | `dispatching-parallel-agents` |
| Bug or unexpected behavior | `systematic-debugging` | `test-driven-development` |
| Skill creation or adaptation | `skill-creator` | `writing-for-agents`, `writing-skills` |
| Any `AGENTS.md`, `CLAUDE.md`, or skill prose | `writing-for-agents` | `simple-english` Plain register |
| macOS scheduled job | `launchd-automation` | `archify` for the process diagram |
| Command-line surface | `cli-developer` (not installed; use the tool repository's own contract) | The tool repository's own contract |
| Pre-merge check | `requesting-code-review` | `verification-before-completion` |
| Consolidating a branch | `finishing-a-development-branch` | The owning repository's integration rules |

Domain routing for a concrete request lives in
[Admin workflows](../admin-workflows.md), not here.

## Handoff interface

The Notion source proposes a downstream team of orchestrator, executor, and
reviewer. That team is a proposed interface. This page does not create it, staff
it, or grant it permission.

What exists locally: a handoff is a written plan plus a branch, worktree, or
source path. The receiver is whoever the user authorizes for that step. The
return is evidence, and evidence is checked against the acceptance criteria
rather than accepted from a completion message.

For tool work the handoff fields are in [Admin tool handoff](../tools.md). For
scheduled work they are in [Automation](../automation.md).

## Boundaries

- A plan is not permission. Execution needs its own approval and scope.
- Self-review is not independent review. A sensitive change needs a reviewer who
  did not write it.
- A completion report is not a verified outcome. Read the artifact.
- Planning does not install, restart, publish, or open a ticket.
- The profile keeps its own writes to planning artifacts. It does not edit the
  system it is planning for.

## Open decisions

| Decision | Current state | Needed before |
| --- | --- | --- |
| Final profile name | Working label only | Any packaging or host wiring |
| Runtime configuration format and host | Undefined | Loading the profile on a real host |
| Attached skill set | Candidate list above, not evaluated as a bundle | Runtime configuration |
| Ticket schema and trigger | Not defined | Automatic handoff |
| Independent-review threshold and cross-Space authorization | Not defined | Any cross-Space change |
| Where canonical plan, evidence, and revision history live | Current plans in `docs/superpowers/`; old evidence in `docs/history/` | Packaging |

## Planning workflow

Use Superpowers brainstorming and writing-plans for new work. Improve was
removed at the user's request. Historical Improve candidates remain archival
evidence and are not installed capabilities. Profile host wiring remains draft.

## Evidence that this is a draft

- No host loads this profile. No configuration file references it.
- The method list was resolved against the host's skill catalog on 2026-10-23.
  Several capabilities named in older Admin docs are absent from that catalog;
  [Admin workflows](../admin-workflows.md) records the gap.
- The Notion page remains the design source. There is no automatic sync.
