---
id: CODEX-LOCAL-ENVIRONMENT
version: 1
scope: local-machine
status: active
updated: 2026-08-09
---

# Connected workspaces

This file is a compact availability map for fresh Codex orientation. Paths are
local to this machine. Each named owner remains authoritative for its own
state, instructions, validation, and mutations.

## Control plane

- **Root:** `/Users/tai/.codex`
- **Purpose:** Codex runtime adapters, reusable skills, general lifecycle, and
  cloud coordination.
- **Start with:** `AGENTS.md`, then `documentation/CURRENT.md` and the active
  issue or plan only when relevant.
- **Do not use for:** project data, scientific interpretation, or a source of
  truth for external-workspace state.

## Source-grounded Wiki

- **Root:** `/Users/tai/workspace/wiki`
- **Purpose:** local literature evidence retrieval, source provenance, and
  human-reviewed knowledge.
- **Entrypoint:** `AGENTS.md`; stable caller interface: `.rag/wiki.py` and
  `.rag/runtime.py`.
- **Use when:** an answer, mechanism, method, or scientific claim materially
  needs source-grounded literature evidence.
- **Do not use for:** pure computation, routine local data analysis, or as an
  automatic prerequisite for all research work.
- **Owner boundary:** Wiki returns an evidence packet; the consuming workspace
  owns reasoning, conclusions, and any Research Ticket.

## Shared executable tools

- **Root:** `/Users/tai/workspace/tools`
- **Purpose:** reusable executable capabilities extracted from project-local
  behavior.
- **Entrypoint:** `AGENTS.md`, then `CAPABILITIES.md`; inspect a selected
  tool's own `README.md` and capability contract only when it is material.
- **Known candidate:** `scientific-plot` at
  `/Users/tai/workspace/tools/scientific-plot`; its current maturity is
  `extract_candidate`, not `promote_shared`.
- **Use when:** a task matches a tool's declared contract and maturity permits
  reuse.
- **Do not use for:** scientific data selection, fitting decisions,
  interpretation, or project registry execution unless the owning project
  explicitly provides that contract.

## Research projects

- **Root:** `/Users/tai/workspace/projects`
- **Active research checkout presently mapped:**
  `/Users/tai/workspace/projects/active-projects/res_volatile-pda`
- **Project entrypoints:** `README.md`,
  `documentation/project-state.yaml`, and the nearest scoped `AGENTS.md`.
- **Use for:** project-owned data, methods, analysis selection, outputs,
  provenance, and scientific acceptance gates.
- **Caution:** both `active-projects` and `active_projects` exist. Resolve the
  live checkout and scoped instructions before any mutation; never infer one
  from the other.

## Memory planes

| Plane | What it may answer | Authority |
| --- | --- | --- |
| Canonical artifacts | what is accepted or true now | owning repository/project |
| This environment map | what connected system is locally available | local configuration only |
| Codex thread/history | what happened in the current logical interaction | context, not current truth |
| AgentMemory | prior observations and recurring patterns | historical context only |
| Wiki/RAG | source-grounded scientific evidence | source/provenance bounded |

AgentMemory is configured as an MCP and lifecycle-hook integration. A bounded
manual save-and-recall probe succeeded on 2026-08-09. Automatic lifecycle
capture remains **unproven**: the runtime has not yet produced a verified
captured session or audit event. Do not use either path to locate projects or
decide current state.

## Orientation rule

```text
identify current repository and scope
→ apply its scoped AGENTS instructions
→ read its canonical current state
→ read this map
→ decide whether an external capability is material
→ inspect only that owner's entrypoint
→ execute and validate under the owner's contract
```

An environment-map entry is a discovery hint, never an implicit invocation,
authorization, or acceptance claim.
