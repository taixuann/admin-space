# Admin docs instructions

Scope: `docs/` and its subfolders. Read the root [AGENTS.md](../AGENTS.md) first. For profile work, also read [profiles/AGENTS.md](profiles/AGENTS.md).

## Choose the lifecycle

Use one Superpowers lifecycle per deliverable:

1. `superpowers:brainstorming` while the design is unsettled.
2. `superpowers:writing-plans` once Tai accepts the design. Save the plan in `superpowers/plans/` and the spec in `superpowers/specs/`.
3. Executor runs the plan (see [Executor](profiles/executor/README.md)). The plan header names requester, space, base, branch, scope, checks, engine, and report.
4. `superpowers:verification-before-completion` before any claim of completion.

Keep an existing task on its chosen lifecycle. State a replacement before switching. Read a skill before using it. If a named skill is missing from the host catalog, report the gap.

## Plan or direct

Route work by whether a written plan exists.

| Situation | Who runs it | Where | Tracking |
| --- | --- | --- | --- |
| Small, immediate, interactive, or exploratory work with no plan | The caller (Secretary, Forge) runs `/opencode` directly | The caller's own Space | The request itself; no card |
| A plan written with `superpowers:writing-plans` | Executor, through a kanban card assigned to `executor` that carries the plan path | The requester's Space, on the plan's task branch | The kanban card: who assigned, plan path, status, result |
| Executor unavailable (quota or outage) | The caller runs `/opencode` directly | The caller's own Space | The request, with the fallback noted |

Executor validates the plan header: requester, space, base, branch, scope, checks, engine, and report. A missing or ambiguous plan, a missing header field, a requester without authority over the Space, or a dirty tree sets the card blocked with the reason. Executor commits on the task branch, reports, and waits for Tai's review; it merges only on Tai's approval. There is no separate tracking-only mode.

To hand a plan to Executor, create a kanban card assigned to `executor`: the title names the task, the body holds the plan path, `workspace_kind` is `dir`, and `workspace_path` is the requester's own Space. The card's workspace is where Executor works; a requester never points it at another Space's directory. Forge calls Executor the same way for `~/development-space`.

See [Executor](profiles/executor/README.md) for the model, plan contract, permissions, and workflow.

## Pick the owning method

| Task | Use |
| --- | --- |
| Skill create or revise | `skill-creator`, `writing-for-agents` |
| `AGENTS.md` or `CLAUDE.md` change | `writing-for-agents`; check loading paths and references |
| Profile create, update, maintain, delete | `hermes-fleet-admin`; rules in [profiles/AGENTS.md](profiles/AGENTS.md) |
| Scheduled job | `launchd-automation`; rules in [automation/AGENTS.md](../automation/AGENTS.md) |
| Tool use or tool problem | [tools/AGENTS.md](../tools/AGENTS.md) |
| Process or architecture diagram | `archify` |

## Keep records

- Link derived specs, plans, and evidence back to the request.
- Keep one active plan per deliverable.
- Treat old plans in `superpowers/plans/` as history. Leave their links unchanged.
- Link to owning sources instead of copying their content.

## Memory

- Check recalled claims against the live owning source before acting. The live source wins.
- Correct a fact at its owning source first.
- Keep credentials, raw data, full documents, and run logs out of memory.
- Each profile's memory setup is in its profile README.

## Approval gates

Tai approves commits to base branches, merges, pushes, publication, external sharing, issue filing, destructive actions, scientific acceptance, and Hermes configuration changes. A skill's default commit or publish step grants none of these.
