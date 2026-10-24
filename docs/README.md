# Admin documentation

This wiki organizes Admin documentation by the seven aspects defined in
[Admin Space Home](https://www.notion.so/4010a859ed1f81789613e07d67b7880e).
The operating contract stays in the root documents. This page is navigation
and context, not a second contract.

Last reviewed: 2026-10-25. Source of truth for implementation status is the
live repository, configuration, or runtime. Notion holds design intent and
may lag behind the live state.

## How to use this wiki

1. Read the root documents first: [AGENTS.md](../AGENTS.md),
   [SOUL.md](../SOUL.md), [USER.md](../USER.md),
   [ARCHITECTURE.md](../ARCHITECTURE.md), and [README.md](../README.md).
2. Open the aspect that owns the question.
3. Follow the link to the detailed runbook or source. Do not duplicate a
   runbook here.

## Table of contents

| # | Aspect | Local owner | Detailed source |
| --- | --- | --- | --- |
| 01 | [Profiles and Identity](#01-profiles-and-identity) | [SOUL.md](../SOUL.md), [USER.md](../USER.md) | [Admin Architect & Planning profile](profiles/admin-architect-planning.md) |
| 02 | [Memory and Knowledge](#02-memory-and-knowledge) | [memory.md](memory.md) | [Hindsight explorer](../tools/hindsight/README.md) |
| 03 | [Skills and Integrations](#03-skills-and-integrations) | [skills/README.md](skills/README.md) | [Skill groups view](skills/skills.html) |
| 04 | [Tools](#04-tools) | [tools.md](tools.md) | [Hindsight](../tools/hindsight/README.md), [OpenCode Free Router](../tools/opencode-free-router/README.md) |
| 05 | [Agents and Models](#05-agents-and-models) | [agents-models.md](agents-models.md) | [Admin Architect & Planning profile](profiles/admin-architect-planning.md) |
| 06 | [Workflows and Architecture](#06-workflows-and-architecture) | [AGENTS.md](../AGENTS.md), [ARCHITECTURE.md](../ARCHITECTURE.md) | [Admin workflows](admin-workflows.md), [Plans](superpowers/plans/README.md) |
| 07 | [Automations and Runtime](#07-automations-and-runtime) | [automation.md](automation.md) | [Launchd runbooks](../automation/) |

## 01 Profiles and Identity

Source: [01 · Profiles & Identity](https://www.notion.so/4010a859ed1f81fca95ac3306159a90b)

Scope: Admin identity, collaboration preferences, role boundaries, and
decision authority. SOUL.md holds identity and conduct. USER.md holds
confirmed collaboration preferences. Neither file grants access or
execution authority.

Observed in the live workspace:
- [SOUL.md](../SOUL.md) and [USER.md](../USER.md) exist and are in use.
- [Admin Architect & Planning profile](profiles/admin-architect-planning.md)
  is a draft definition. No host loads it and no configuration file
  references it.

Proposed or pending:
- Who may edit the Admin profile.
- How cross-Space handoffs are authenticated.
- Final name, host wiring, and skill set for the planning profile.

## 02 Memory and Knowledge

Source: [02 · Memory & Knowledge](https://www.notion.so/4010a859ed1f8191a3a9c7d63fdb6feb)

Scope: Continuity versus authoritative sources. Ephemeral context, native
session stores, Hindsight recall, and durable knowledge ownership. See
[memory.md](memory.md) for the policy.

Observed in the live workspace:
- Hindsight bank `admin` is the shared recall layer.
- Native app memory remains separate under `memories/`.
- [Hindsight explorer](../tools/hindsight/README.md) is the native control
  plane.

Proposed or pending:
- Which memory backend and retrieval index exists in reality.
- Which memories may be promoted between Spaces.
- Synchronization and source authority for a local MEMORY.md.

## 03 Skills and Integrations

Source: [03 · Skills & Integrations](https://www.notion.so/4010a859ed1f81bf9d68c1443c338e6f)

Scope: Capability inventory, providers, and permissions. Skills are
instructions. Integrations are connections. Neither is execution authority
by itself.

Observed in the live workspace:
- Direct local skills are inventoried in [skills/README.md](skills/README.md).
- Interactive skill groups are in [skills/skills.html](skills/skills.html).
- Plugin sources live under `plugins/`.

Proposed or pending:
- Whether the `agent-config` reference workflow is adopted. It is
  documented as planned, not installed.
- Which integrations are live and where their permission checks happen.

## 04 Tools

Source: [04 · Tools](https://www.notion.so/4010a859ed1f81378832f38705934cad)

Scope: Callable capabilities with defined inputs, outputs, side effects,
error behavior, allowed runner, required permission, and owner. See
[tools.md](tools.md) for ownership and handoff rules.

Observed in the live workspace:
- [Hindsight](../tools/hindsight/README.md) opens the native memory
  explorer for bank `admin`.
- [OpenCode Free Router](../tools/opencode-free-router/README.md) checks
  models, maintains the dated catalog, and sets the native OpenCode default.

Proposed or pending:
- Which tools are available only on local macOS versus remotely.
- How tool health is verified.

## 05 Agents and Models

Source: [05 · Agents & Models](https://www.notion.so/4010a859ed1f81238e0dca41eee46829)

Scope: Cloud and local agent profiles, model and provider choices, fallback,
cost, limits, and capability boundaries. Every Space is hybrid-capable.
See [agents-models.md](agents-models.md).

Observed in the live workspace:
- Default Hermes profile is Astra, a front-door router. It owns no
  canonical state.
- Forge profile is the software control plane. It was formerly named dev.
- Each profile has its own model and provider configuration.

Proposed or pending:
- Which providers and budgets are approved.
- How a delegated local agent returns evidence.
- Runtime configuration for the draft planning profile.

## 06 Workflows and Architecture

Source: [06 · Workflows & Architecture](https://www.notion.so/4010a859ed1f81febd84d9f5e90827b6)

Scope: Intents, handoffs, and decision gates. Universal stages: capture,
inspect context, evaluate and plan, request a human decision only if
necessary, authorized execute, verify and reconcile.

Observed in the live workspace:
- [AGENTS.md](../AGENTS.md) holds the operating instructions.
- [ARCHITECTURE.md](../ARCHITECTURE.md) holds component ownership and
  information flow.
- [admin-workflows.md](admin-workflows.md) selects methods and profiles.
- Active plans live in [superpowers/plans/README.md](superpowers/plans/README.md).

Proposed or pending:
- How versioned workflow changes are approved, dispatched, and rolled back.

## 07 Automations and Runtime

Source: [07 · Automations & Runtime](https://www.notion.so/4010a859ed1f81f4b926c83e06bbb78d)

Scope: Scheduling, actual runs, and observation. Desired configuration is
not actual runtime state. See [automation.md](automation.md).

Observed in the live workspace:
- `com.tai.model-control-sync` runs daily at 00:00 from Admin source.
- `com.tai.linear-notion-sync` runs daily at 00:00 from Development Space
  source.
- `com.tai.bridge.sync` runs per its installed plist from Admin source.

Proposed or pending:
- How launchd reads approved properties and detects drift.
- How failed jobs and run evidence are synchronized.

## Generated views

These are dated snapshots. They illustrate, but do not prove, runtime
behavior.

- [Memory relationships](memory/memory.html)
- [Skill groups](skills/skills.html)
- [Skill inventory and handoffs](skills/README.md)

## Coverage and maintenance

Snapshot date: 2026-10-22 for the generated views. Skill membership does
not represent calls or dependencies. Plugin-bundled skills and skills stored
only in other hosts are outside the inventory.

When an owning source changes, update the relevant file and check its links.
Keep source evidence separate from proposed relationships.

For identity and operating guidance, start with
[the workspace README](../README.md). For ownership and component
responsibilities, read [ARCHITECTURE.md](../ARCHITECTURE.md).
