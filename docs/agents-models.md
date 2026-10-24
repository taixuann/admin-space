# Agents and Models

Source: [05 · Agents & Models](https://www.notion.so/4010a859ed1f81238e0dca41eee46829)

Last reviewed: 2026-10-25. Status: Draft (not execution approval).

## Purpose

Describe cloud and local agent profiles, model and provider choices,
fallback, cost, limits, and capability boundaries. Every Space is
hybrid-capable. Choose execution based on permissions, data location,
reliability, and cost. Admin prefers cloud for planning and coordination,
not always for execution.

## Observed profiles

- Default Hermes profile is Astra. It is a front-door router across the
  research and software workspace. It owns no canonical state.
- Forge profile is the software control plane. It was formerly named dev.
  It routes product work to target repositories through Codex or OpenCode.
- Each profile has its own model and provider configuration.

## Observed configuration boundaries

- Default profile uses a custom OpenAI-compatible endpoint at a local
  proxy.
- Forge profile uses the OpenCode Go provider.
- Secrets and tokens stay in the credential store and are not recorded
  here.

## Draft planning profile

- [Admin Architect & Planning profile](profiles/admin-architect-planning.md)
  is a draft definition. No host loads it and no configuration file
  references it. It grants no execution authority.

## Proposed or pending

- Which providers and budgets are currently approved.
- How a delegated local agent returns evidence.
- Final name, host wiring, and skill set for the planning profile.

## Related sources

- [Admin workflows](admin-workflows.md)
- [ARCHITECTURE.md](../ARCHITECTURE.md)
- [AGENTS.md](../AGENTS.md)
