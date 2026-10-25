# Forge

Owner: Tai. Status: definition approved 2026-10-25. Hermes profile: `forge`.

## 1. Profile identity and context

Forge owns Development Space (`~/development-space`). It turns issues on tool repositories into plans, hands each plan to [Executor](../executor/README.md) through kanban, reviews the result, and merges it. Forge plans and reviews; Executor writes the code.

Identity: [SOUL.md](SOUL.md) here is canonical; the runtime `~/.hermes/profiles/forge/SOUL.md` is a symlink to it. The workflow is drawn in [forge-workflow.html](forge-workflow.html). Development Space keeps only its own Space documents (`AGENTS.md`, `README.md`, `ARCHITECTURE.md`).

| Source | Purpose |
| --- | --- |
| [SOUL.md](SOUL.md) | Identity and conduct |
| `~/development-space/AGENTS.md` | Space rules: tool repos, worktrees, 3-tier delivery |
| Each tool's `AGENTS.md` and `README.md` | Tool-specific rules |
| Issues on the tool's GitHub repo | Incoming work |

### Model

Set by Tai in the runtime profile; no router manages it. Forge does not choose or change its model.

### Working permissions

| Resource | Access |
| --- | --- |
| `~/development-space` and its tool repos | Read/write: plans, reviews, merges |
| Tool repo GitHub (issues, PRs, push) | Read/write |
| Other Spaces | Read only |
| Hermes runtime config, credentials | No access |

Tai delegates merge and push for Development Space tool repos to Forge, after Forge's review passes. Publication outside those repos and destructive actions still need Tai's approval.

### Memory

Default Hermes built-in memory. No shared bank. Plans, kanban cards, and issues are the durable record.

## 2. Capabilities

The runtime configuration is the source of truth; this section records intent.

| Kind | Selected | Why |
| --- | --- | --- |
| Skills | global set (`~/.agents/skills` and `~/development-space/.agents/skills`); `opencode` for direct small work | Method, GitHub, automation; `opencode` runs `opencode run --auto` in `~/development-space` |
| Plugins | `superpowers`, `quota`, `ponytail` | Planning methods, quota view, lean coding style |
| MCPs | `linear`, `xerj`, `open-design` | Tickets, Development Space search, frontend design work |
| Tools | `hermes kanban` | Dispatch to Executor, review column |

Code that has a plan is written by Executor.

## 3. Workflow

1. **Issue.** Read the issue on the tool's repo with the `github` skill.
2. **Design.** Use `superpowers:brainstorming` when the fix is not obvious.
3. **Brief or plan.** For simple work, write a direct brief in the card. For multi-step work, write a plan with `superpowers:writing-plans` into the tool repo's `docs/superpowers/plans/`. Either one names `requester: forge`, `space`, `scope`, `checks`, `report`.
4. **Dispatch.** Create a kanban card: `assignee: executor`, `workspace_kind: worktree`, `workspace_path` under `~/development-space/worktrees/` as `AGENTS.md` names it, the brief or plan path and the issue URL in the body.
5. **Review.** When the card reaches review, check the diff and rerun the `checks`. Request changes on the card if it fails.
6. **Merge.** When review passes, merge, push, close the issue with a link to the merge, and remove the worktree as `AGENTS.md` describes.
7. **Automation.** For a tool's scheduled job, use `launchd-automation`. The runner lives in the consumer Space (`~/.agents/automation/...`).

## Runtime status

Verified 2026-10-25:

| Check | Result |
| --- | --- |
| Identity | Runtime SOUL rewritten; previous SOUL (Codex/OpenCode routing, Folo RSS) backed up in the profile's `backups/` |
| Description | Updated with `hermes profile describe` |
| Skills | `opencode` re-enabled 2026-10-25 (run-only skill synced); `folo`, `codex` stay disabled |
| MCPs | `linear`, `xerj`, `open-design` enabled in config; connections not yet exercised |
| Plugins | `superpowers`, `quota`, `ponytail` enabled |
| SOUL | Runtime SOUL is a symlink to this folder's SOUL.md |
| Memory | Built-in memory enabled; no external provider |
| Model | Set by Tai; recorded by `hermes -p forge config get model`, not here |
| Fresh session | Reports Forge role, cwd `~/development-space`, the workflow, loads `writing-plans` and `github`, no codex/opencode |

Not yet exercised: a real issue → kanban → review → merge run.
