# Admin Space

Admin Space lives at `~/.agents`. It maintains the agent environment and coordinates work across Spaces.

This is the first working edition. Refine these documents as actual use reveals missing guidance.

## Read the right document

| Document | Purpose |
| --- | --- |
| [AGENTS.md](AGENTS.md) | Operating instructions for agents |
| [SOUL.md](SOUL.md) | Admin identity and conduct |
| [USER.md](USER.md) | Collaboration preferences |
| [ARCHITECTURE.md](ARCHITECTURE.md) | Components, ownership, and information flow |
| [CLAUDE.md](CLAUDE.md) | Claude entrypoint for the same operating instructions |

## Workspace

- `skills/` contains reusable instructions.
- `plugins/` contains maintained plugin sources.
- `automation/` contains local automation assets. Read each component's README before use.
- `memories/` provides access to existing memory locations. Preserve its links and contents.
- `plans/` holds existing plans and execution evidence.
- `managed-links/` records links maintained by external tooling.
- `bin/` contains existing executable entrypoints.

`tools/` provides entrypoints and runbooks for existing capabilities. Implementations stay with their owning runtimes.

## Connected sources

[Admin Home](https://www.notion.so/4010a859ed1f81789613e07d67b7880e) contains the Notion design and links to its seven aspects.
[Admin design ticket](https://www.notion.so/4010a859ed1f8120b5e0f1a2496e4edc) records the design discussion.

Notion holds intent, decisions, and process history. Local files hold the working instructions and implementation.
There is no automatic synchronization between them. Reconcile conflicting instructions against the user's latest decision before an affected change.

Hindsight provides the shared Admin memory bank for Codex and Claude. See [memory ownership](ARCHITECTURE.md#memory).

## Explore Admin

Open [docs/README.md](docs/README.md) for interactive memory and skill views, source inventory, and coverage limits.

## Tools

[Admin tools](tools/README.md) includes the native Hindsight memory explorer.
