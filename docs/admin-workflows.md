# Admin workflows

## Select the workflow

Identify the requested outcome, owning component, and authorized scope. Read the
selected skill before acting. Use one main lifecycle for the work. Specialist
skills can support it without creating another plan or execution authority.

`brainstorming` runs before a design is settled. `writing-plans` runs after the
user accepts a design. `executing-plans` or `subagent-driven-development` runs
the plan. `verification-before-completion` gates any claim of completion.

Improve provides a read-only advisory workflow and handoff plans. Use it when
asked, or when the task is a pure advisory survey of an unfamiliar codebase. It
is not required as the entrypoint for every Admin task, and it is not the Admin
planning profile.

Preserve an explicitly selected lifecycle for existing work. A replacement
workflow must be stated before changing the task's lifecycle or artifacts. Do not
run two competing planning or execution lifecycles for the same deliverable.

## Reach the owner

| Task | Material to read |
| --- | --- |
| Refine an unclear request | `brainstorming`; `step-back` when patches keep accumulating |
| Define scope and acceptance | `writing-plans`, then `verification-planning` |
| Break an agreed specification into tasks | `writing-plans` |
| Migrate existing source or runtime paths | The component instructions and the selected migration workflow |
| Add logs or diagnose unattended behavior | The component contract and the owning automation runbook |
| Create or revise a skill | `skill-creator`; `writing-for-agents` for instructions |
| Create or revise a plugin | The target host manifest and maintained package instructions; `skill-creator` for included skills |
| Change a macOS scheduled job | `launchd-automation`; inspect source, installed configuration, and recovery first. Placement rules: [Automation](automation.md) |
| Explain an automation process | `archify`; distinguish proposed paths from observed behavior |
| Create or revise `AGENTS.md` or `CLAUDE.md` | `writing-for-agents`; verify hierarchy, loading paths, and references |
| Develop a tool | The tool repository `AGENTS.md`, the Development Space small-tool contract, and [Admin tool handoff](tools.md) |

Skill identifiers name capabilities, not commands or launchable agent
configurations. Resolve them from the current host's skill catalog. If the named
capability is unavailable, report the gap before depending on it.

## Profiles

A profile defines responsibilities, decision boundaries, and handoffs. A skill
supplies a method for a task. A runtime configuration loads a profile on a
specific host. Keep these distinct.

The Admin planning profile is [Admin Architect & Planning](profiles/admin-architect-planning.md).
It is a draft definition: no host loads it, no configuration file references it,
and it grants no execution authority. Its Notion source is
[TBD · Architect & Planning Profile (Draft)](https://app.notion.com/p/4020a859ed1f813d8d5acc6d1676a247),
read on 2026-10-23.

Do not treat the profile page as a deployed runtime. The final name,
configuration format, attached skill set, ticket trigger, and independent-review
threshold remain open. Preserve existing Admin identity and user preferences
while evaluating it.

## Keep one record of the work

Admin request IDs describe intent, scope, and success criteria. Link derived
design, task plans, and execution evidence back to that request. Keep request
briefs in `plans/`, indexed by `plans/README.md`. Preserve existing artifacts and
task tracking when selecting a new workflow. Establish the artifact locations in
the task handoff rather than creating a second active plan through a skill's
default path.

## Distinguish policy from pending migration

Requests 008, 009, and 010 describe the automation, independent-tool-repository,
Development Space, and Admin planning changes. Read their current status in the
plan index before relying on them. Source location, installed discovery, and
verified runtime behavior are separate facts.

A workflow reference does not create an agent profile, start a background job,
dispatch another agent, install a package, or grant publication authority.
Configure launchable profiles only when their intended host and behavior are
specified.

## Known capability gaps

Resolved against the host skill catalog on 2026-10-23:

- The `agent-skills` phase skills (`using-agent-skills`, `interview-me`,
  `idea-refine`, `spec-driven-development`, `planning-and-task-breakdown`,
  `observability-and-instrumentation`) are not installed here. Earlier Admin
  routing text named them. Use the installed Superpowers and local skills listed
  above instead, and record the gap when a request genuinely needs one of them.
- No dedicated plugin-authoring skill is installed. Inspect the target host
  manifest and existing package conventions, then select an available capability.
- `cli-developer` and `agent-rules` are not installed here. The profile names
  `cli-developer` as a method for command-line surfaces; neither capability can
  be evaluated or installed until its source is supplied. Use the owning tool
  repository's contract in the meantime.
