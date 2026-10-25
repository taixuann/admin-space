# Coordinator

Status: Role agreement from Tai, not a deployed runtime configuration.
Owner: Tai.
Last reviewed: 2026-10-25.

## Responsibility

See [capabilities (YAML)](capabilities.yaml) and the generated [HTML view](capabilities.html) for role requirements and the unverified runtime inventory. Use the [profile index](../README.md) to compare roles.

The legacy renderer lives in `.archify/secretary/scripts/` and is not part of the current workflow.

Coordinator handles communication with bots in other Spaces. Secretary and the OpenCode team focus on Admin Space work. Tai leads both roles and retains final authority.

Secretary prepares a scoped handoff when Admin work needs another Space. Coordinator communicates with the responsible bot, follows the handoff, and returns the response and evidence pointers. The owning Space retains implementation authority and canonical artifacts. Secretary reconciles the result into the Admin record and reports to Tai.

Communication within an authorized internal handoff does not grant permission to publish, share externally, change permissions, or alter another bot's identity. Preserve session-specific exclusions and Tai's approval gates.

## Runtime status

Tai identifies Asura as the Coordinator. This documentation pass does not contact Asura, inspect credentials, rename a runtime profile, or change its SOUL.md. No Coordinator identity source is invented or copied here.

A future documented SOUL source can live in this directory after the active source is inspected and the change is authorized. The directory is documentation, not an active HERMES_HOME.

## Navigation

- [[docs/README|Admin Space roles and full flow]]
- [[docs/profiles/secretary/README|Secretary profile]]
- [[docs/profiles/coordinator/capabilities.yaml|Coordinator capability targets]]
- [[docs/profiles/coordinator/capabilities.html|Coordinator capabilities view]]
- [[docs/AGENTS|Work procedures]]

Portable links: [Admin Space](../../README.md), [Secretary](../secretary/README.md), [Work procedures](../../AGENTS.md).
