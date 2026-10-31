# Admin Space docs

Admin Space (`~/.agents`) is the shared workspace for agent operating rules, profiles, and plans. It is not one agent. Tai sets direction and keeps final authority.

## Roles

| Role | Does | Does not |
| --- | --- | --- |
| Tai | Directs work, approves, reviews and accepts | |
| [Secretary](profiles/secretary/README.md) | Develops requests with Tai, manages profiles, writes plans, verifies, records, reports | Own other Spaces' domain work |
| [Executor](profiles/executor/README.md) | Runs plans from any authorized profile on a task branch in the owning Space; merges after Tai approves | Write plans or set direction |
| [Coordinator](profiles/coordinator/README.md) (Asura) | Carries scoped handoffs to bots in other Spaces and returns their answers | Transfer ownership or publish |
| Bots in other Spaces | Do their Space's work | |

## How work flows

1. Tai gives direction to Secretary.
2. Secretary inspects current state and settles the scope with Tai (`superpowers:brainstorming` when unclear).
3. Secretary writes the plan in `superpowers/plans/` (`superpowers:writing-plans`).
4. Executor runs the plan on a task branch, verifies, commits, and reports.
5. Tai reviews. Executor merges after approval.
6. Secretary checks the evidence, updates records, and reports what changed, what was verified, and what remains open.

When another Space is involved, Secretary hands the request to Coordinator. That Space keeps its artifacts and authority.

## What lives where

| Path | Holds |
| --- | --- |
| [`AGENTS.md`](AGENTS.md) | How agents work in this Space |
| [`superpowers/`](superpowers/plans/README.md) | Specs (`specs/`) and plans (`plans/`); historical plans and evidence |
| [`../automation/`](../automation/README.md) | Admin-owned scheduled jobs |
| [`../skills/`](../skills/) | Admin-maintained skill sources |
| `~/development-space/repos/` | Internal tool source (Development Space) |
| `~/.hermes/` | Hermes runtime: profiles, sessions, installed capabilities, native memory |

A path tells you where to look. It does not grant permission to change it.

## Sources

| Source | Tells you |
| --- | --- |
| Tai's latest decision | What is authorized |
| Live files, config, command output | What actually exists and works |
| Plans | What was intended, not proof it ran |
| [Notion Admin Home](https://www.notion.so/4010a859ed1f81789613e07d67b7880e) | Design intent and history; not synced with local files |
| Memory (Hindsight) | Recall to check against the live source |
