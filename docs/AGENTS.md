# Admin docs instructions

Scope: `docs/` and its subfolders. Read the root [AGENTS.md](../AGENTS.md) first. For profile work, also read [profiles/AGENTS.md](profiles/AGENTS.md).

## Choose the lifecycle

Use one Superpowers lifecycle per deliverable:

1. `superpowers:brainstorming` while the design is unsettled.
2. `superpowers:writing-plans` once Tai accepts the design. Save the plan in `superpowers/plans/` and the spec in `superpowers/specs/`.
3. Executor runs the plan (see [Executor](profiles/executor/README.md)). The plan header names requester, space, base, branch, scope, checks, and report.
4. `superpowers:verification-before-completion` before any claim of completion.

Keep an existing task on its chosen lifecycle. State a replacement before switching. Read a skill before using it. If a named skill is missing from the host catalog, report the gap.

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
