---
requester: secretary
space: ~/.agents
base: master
branch: none (Tai approved inline execution; tree holds unrelated uncommitted work, so no branch switch)
scope: docs/profiles/, docs/AGENTS.md, ~/.hermes skills `opencode`, runtime config of profiles forge and executor
checks: see Verify
engine: self
report: chat
approval: Tai, 2026-10-25 ("triển khai thật luôn")
---

# Simplify profile docs, align Forge, make `/opencode` run-only

Tai's decisions: drop `capabilities.yaml` everywhere (keep README + SOUL + workflow); Forge enables all three plugins, MCPs linear + xerj + open-design (open-design moves from Executor to Forge), keeps global skills; Forge workflow is ticket → plan → review → Executor → review → merge; the `opencode` skill only runs `opencode run ... --auto` in the right directory, never picks a model.

## Tasks

1. **opencode skill.** Patch global `~/.hermes/skills/autonomous-ai-agents/opencode/SKILL.md`: one-shot example and flags use `--auto`; no model flag in examples. Back up, then copy to the `forge` and `executor` profile copies. Enable `opencode` for Forge (it was disabled).
2. **Forge runtime.** Back up `config.yaml`. Add MCP `open-design` (copied from Executor, minus session-specific socket variables) and `xerj`; confirm `linear` enabled. Skills and plugins unchanged (`external_dirs` keeps the global dir).
3. **Executor runtime.** Set `mcp_servers.open-design.enabled false`.
4. **Forge identity.** Make `docs/profiles/forge/SOUL.md` canonical (copy of runtime SOUL, then runtime SOUL becomes a symlink, old one backed up).
5. **Docs.** Move every `docs/profiles/*/capabilities.yaml` to `backups/`; fix every reference (profile index, `docs/profiles/AGENTS.md`, READMEs). Forge README: drop router text, state MCPs/plugins inline. Executor README: open-design off.
6. **Forge workflow diagram.** Archify lifecycle in `.archify/forge/`, symlinked as `forge-workflow.html`, same layout as Executor. Remove "YAML" from the Secretary diagram text and rebuild.
7. **hermes-fleet-admin.** Replace the manifest rule with: README states intent, runtime config is the truth, Verify reads the runtime and reports drift.

## Verify

- `hermes -p forge config get mcp_servers` lists linear, xerj, open-design enabled; Executor shows open-design disabled.
- Fresh read-only Forge session: role, cwd, MCP/plugin visibility, `opencode` skill loads.
- `cmp` runtime SOUL vs docs SOUL; all Markdown links resolve; Archify finalize passes for Forge and Secretary.
- No `capabilities.yaml` left under `docs/profiles/`.

## Rollback

Backups: `~/.agents/backups/profile-simplify-*` (YAML files, old SOULs, skill copies); `config.yaml.admin-backup-*` in each profile.
