# Plan 010: Compose Admin workflows through one routing document

## Status

- Status: IN PROGRESS (docs-first) 2026-10-23. The Admin Architect & Planning profile draft and workflow docs exist. `improve` is intentionally unchanged and remains installed. The Improve rewrite in the body is superseded by the user's 2026-10-23 direction; no plugin is packaged. Evidence: [batch 7](execution-2026-10-23/batch-7-verification.md).
- Superseded in part: the profile replaces the Improve rewrite. Keep `improve` available during the transition.
- Priority: P1. Effort: M. Risk: MED for later skill activation and source migration.
- Planned at: `40e9d38238e487744ec216f5a57617e3c09cfb3e`, 2026-10-23.
- Owner: Admin at `/Users/tai/.agents`.
- Dependencies: coordinate with plan 008 for the automation contract and plan 009 for Development Space. Plan 007 remains deferred and is not revived by this proposal.

## Outcome and boundaries

Admin focuses on maintaining its environment, skills, plugins, and automations. Each tool owns an independent Git repository under the Admin-ignored `~/.agents/tools/` directory. Development Space owns engineering guidance and hosts linked development worktrees. Only Space-owned automation implementation gets the Admin-specific `automation/<job-name>` branch requirement. Admin-origin tool work uses `admin/<tool-name>_<plan-number>` in the tool repository. Other work follows its owning repository rules. Planning does not change branches.

Rewrite the local Improve candidate for the Admin advisor role: assess Admin changes, gather evidence, select the domain workflow, prepare bounded plans, and review authorized results. Preserve source read-only and approval boundaries unless a separately accepted execution design changes them. Reference domain selection through docs rather than embedding every specialist rule. Put the domain-selection table in `/Users/tai/.agents/docs/admin-workflows.md`. Keep domain rules in their owning skills. A routing document selects a workflow; it does not grant permissions or own runtime state.

## Current evidence

- `skills/improve/SKILL.md` defines a generic advisor and permits plan writes only. It already tells recon to read project instructions and design documents.
- `plans/008-skill-adaptation/candidate/improve/SKILL.md` adds two domain sections: `Agent instructions and tool plans` and `Automation plans`. These are drafts. Replace their generic framing with an Admin-focused workflow and move domain selection into the docs reference.
- `docs/README.md` states: `The operating contract stays in the root documents.` Preserve this distinction. The new routing document is a workflow reference reached from the operating entrypoint.
- `plugins/companion/plugin.json` already packages connected project workflows. Do not silently repurpose that package as Admin maintenance or revive Orchestra plan 007.
- The corrected plan 009 keeps canonical tool checkouts at `~/.agents/tools/<tool-name>` as independent repositories ignored by Admin Git. Development Space hosts linked worktrees. The earlier source-relocation proposal is superseded.

## Proposed routing table

| Work requested | Owning workflow | Supporting capability | Output |
| --- | --- | --- | --- |
| Assess or upgrade Admin | Improve for investigation and plan | Current root instructions and selected component | Bounded plan and evidence |
| Create or change a skill | Skill-creator | Writing-for-agents; source/install/runtime inspection | Evaluated skill candidate |
| Create or maintain a plugin | Host-specific plugin workflow selected after manifest inspection | Skill-creator for included skills; writing-for-agents for instructions | Validated source package, then separate host loading evidence |
| Create or change a macOS automation | Launchd-automation | Archify; Improve for plan | Process diagram, runbook, agent contract, validation |
| Build or change a CLI or script tool | Development Space's engineering workflow | Assessed CLI-developer | Callable tool and behavior checks |
| Create or edit AGENTS.md | Writing-for-agents | Agent-rules only when its inspected helper is useful | Scoped instructions and hierarchy verification |

No dedicated plugin-authoring skill has been accepted. Do not invent an installed skill name. Inspect the target host manifest and existing package conventions, then select an available capability. Discovery does not prove installation or loading.

## Proposed plugin boundary

Working name: `admin-workflows`. The final name is not selected.

Package a small Admin-facing entry skill plus Admin-specific references. Reach existing capabilities by explicit pointers or verified dependencies. Retain upstream provenance and license notices. Maintain one local Admin-focused Improve source candidate; evaluate its new description and workflow through skill-creator. Record that generic codebase auditing is no longer its default role. Do not copy every specialist skill into the package. Do not treat the plugin as a scheduler, credential store, new task database, or automatic executor.

Initially, `docs/admin-workflows.md` owns the local routing table. If plugin packaging later becomes authoritative, move that table into the package and replace the docs body with a pointer. Keep one maintained copy. Verify resolution on each intended host; local absolute paths are not a portable package dependency strategy.

## Scope

This planning pass writes only `plans/`. Implementation scope after selection: a local routing document, its docs index and minimal root discovery pointer, an Admin-focused Improve rewrite with a concise docs reference, then a separate candidate plugin package if still useful. Use writing-for-agents for every changed AGENTS.md and skill. Do not bulk-rewrite unrelated instructions.

Out of scope: deployment, global plugin installation, live service changes, credentials, automatic updates, changing native memory, and actual tool-repository extraction. Plan 009 owns that migration and its consumer checks.

## Steps and completion gates

1. Inventory effective instructions and installed skill entrypoints for each table row. Record maintained source, installed copy, host support, and missing capability separately. Gate: every route points to an inspected owner or explicitly records an unresolved selection.
2. Draft `docs/admin-workflows.md` and a separate `docs/tools.md` under the plan before installation. The workflow table points tool requests to tools.md. That file owns Admin tool handoff fields, branch naming, worktree placement, return evidence, and integration boundaries. Add a separate docs/automation.md for scheduler ownership, tool-owned versus Space-owned source, centralized reports, and a pointer to launchd-automation for lifecycle rules. A reviewable draft is at `plans/010-admin-workflow-draft/docs/tools.md`. Use condition-based pointers and the proposed table. Keep task rules in the named owner. Gate: each request selects one main workflow with support skills as needed; no duplicated automation or skill-authoring rules.
3. Rewrite the local Improve candidate around the Admin advisor workflow: identify requested change and owning component; read Admin docs routing; inspect current state; plan the selected bounded work; hand off only when requested; review evidence. Use skill-creator and writing-for-agents. Update the description to reflect Admin upgrades, skills, plugins, and automation. Keep domain rules behind the docs reference. Gate: no stale claims that this is the unchanged generic advisor; no duplicated domain policy; source read-only boundaries remain explicit. An unrelated repository request routes to its owning engineering workflow instead of imposing Admin rules.
4. Evaluate fixtures through skill-creator: Admin upgrade, automation failure, skill update, plugin change, CLI request, and an unrelated repository audit. Add one mixed request where an automation needs a tool change. Gate: separate ownership and plans; tool implementation uses a Development Space worktree of the independent tool repository; only Space-owned automation receives the Admin automation branch rule; tool-specific jobs share the tool task branch; all AGENTS edits use writing-for-agents; advisor performs no installation or restart.
5. Install the accepted Admin-focused skill and docs integration only after behavior review. Recheck effective hierarchy, pointers, and package loading. Then assess whether a plugin provides a concrete convenience beyond the working local map. Gate: local workflow is usable without plugin packaging.
6. If packaging is selected, inspect target host packaging requirements, create a candidate package with skill-creator, validate references and dependencies, and test in a fresh host session. Gate: source validation and host loading are reported separately; unavailable dependencies remain explicit; no hidden global activation.

## Verification and stop conditions

Structural checks: `git diff --check -- plans`, verify referenced plan files exist, inspect every changed instruction for duplicated authority. Behavior checks use the six fixtures and the mixed request above; text checks do not replace them. Discover host/package validators from actual manifests before recording executable commands. No plugin runtime validator has been selected in this pass.

Stop on conflicting source ownership, missing host capability, unowned dirty changes, duplicate routing authorities, or a migration requiring an unreviewed live service change. Preserve existing jobs and links. Report outstanding decisions without claiming installation.

## Maintenance

Update routing when the owning workflow changes. Update domain behavior in the owning skill. Keep accepted state, plan history, and runtime evidence separate. Plugin packaging must preserve these boundaries.

## Tool handoff draft

[Review tools.md](010-admin-workflow-draft/docs/tools.md). Install it at `docs/tools.md` only during implementation. Plan 009 references this contract rather than defining another tool-handoff authority. Validate plan 008 example mapping to branch `admin/opencode-free-router_008` and worktree `~/development-space/worktrees/admin/opencode-free-router_008`. No worktree is created in this planning pass.

## Request-to-execution boundary

Admin request numbers identify intent, accepted boundaries, and success criteria. The Admin-focused Improve rewrite prepares these briefs and routes them through the full Superpowers design, implementation planning, execution, review, and verification workflow. Preserve design approval and integration boundaries. Do not present an Improve request brief as a completed Superpowers implementation plan. Store design and implementation artifacts in their owning repository and link them back to the request; record exact paths and revisions in the handoff.

The docs routing table points tool engineering to tools.md and automation placement to automation.md. Domain lifecycle rules remain in launchd-automation. This avoids copying the same ownership table into Improve.
