# Tools

Tools used by Admin Space are owned by **Development Space**. Their source lives in `~/development-space/tools/<space>/<tool-name>/`, each an independent Git repository. Admin launches and uses them. Each tool's own `README.md` is its runbook.

This folder is ignored by Admin Git except for this README and [AGENTS.md](AGENTS.md).

| Tool | Purpose | Source | Issues |
| --- | --- | --- | --- |
| `opencode-model-router` | OpenCode model routing for registered consumers | Installed from GitHub with `uv tool`; source `~/development-space/tools/admin/opencode-model-router` (symlinked here for the dashboard). Admin registry: `~/.agents/config/opencode-model-router/register.yaml` | [GitHub](https://github.com/taixuann/opencode-model-router/issues) |
| `hindsight` | Open the Hindsight memory explorer for bank `admin` | Local repo here; **not yet migrated** | No remote |
| `automation-incidents` | Shared incident reporter for scheduled jobs | Local repo here; **not yet migrated** | No remote |

The two local repos were extracted from Admin revision `40e9d38238e487744ec216f5a57617e3c09cfb3e` on 2026-10-23. Moving them into Development Space and giving them remotes is Development Space's work. The retired `opencode-free-router` is archived at `~/.hermes/backups/opencode-free-router-20261025-174918.tar.gz`.
