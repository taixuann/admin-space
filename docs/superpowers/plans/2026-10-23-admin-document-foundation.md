# Admin Document Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans after review. Steps use checkbox syntax.

**Goal:** Give each Admin document one clear responsibility and align navigation with capability management.

**Architecture:** Maintain the existing root documents. Keep short operating pointers in AGENTS.md, current ownership in ARCHITECTURE.md, and navigation in README.md. Resolve IDEA.md's existing content before adapting its role.

**Tech Stack:** Markdown and existing host instruction entrypoints.

**Spec:** [Accepted planning inputs](../specs/2026-10-23-admin-capabilities-and-documents-design-input.md).

## Global Constraints

- Preserve confirmed identity and user preferences. Add no invented preferences.
- Use writing-for-agents for persistent instructions. Write maintained files in English.
- Keep ideas, accepted policy, plans, memory, and runtime evidence distinct.
- Preserve more-specific instructions, source history, and unrelated edits.
- No deployment, scheduling, memory migration, or automatic synchronization.

## Review Focus

- Existing IDEA.md product content must survive a role change (Task 1).
- Aspirational capability must not become a claim of working runtime (Task 2).
- Root guidance must not duplicate component maintenance policy (Task 2).
- CLAUDE.md and other loading paths must retain their effective hierarchy (Task 3).
- Stale skill inventories must not be presented as current accepted state (Task 3).

### Task 1: Freeze document ownership and preserve existing ideas

**Files:** Read SOUL.md, USER.md, IDEA.md, AGENTS.md, ARCHITECTURE.md,
README.md, CLAUDE.md, docs/admin-workflows.md and stage 2's inventory.
Record the accepted content map in this plan before edits.

**Interfaces:** Produce an ownership map: identity -> SOUL; preferences -> USER;
operations -> AGENTS; components -> ARCHITECTURE; navigation -> README.
Propose IDEA as non-operative ideas; it is not accepted operational policy.

- [ ] Map overlapping or outdated passages to one owning document. Verify current
  implementation claims against their actual component sources.
- [ ] Show the existing agent-hub concept and the proposed IDEA role to the user.
  Confirm preservation in place or an exact archive destination before changing
  it. Record the accepted choice and rollback path in this task.

### Task 2: Align the root document set

**Files:** Modify SOUL.md, USER.md, IDEA.md, ARCHITECTURE.md, README.md,
AGENTS.md only where the accepted content map requires changes.

**Interfaces:** Consume Task 1's map and stage 2's accepted capability ownership.
Produce coherent documents with one owner for each durable statement.

- [ ] Use writing-for-agents. Preserve useful existing content; remove duplication
  by linking to its owner. Keep SOUL and USER limited to confirmed material.
- [ ] Apply the accepted IDEA treatment with original content preserved. Label
  unaccepted ideas clearly and link promoted work to its owning plan.
- [ ] Update architecture and navigation for global/admin management categories,
  domain handoffs, and the manual-first execution workflow. Link component
  AGENTS and README files rather than duplicating their procedures.
- [ ] Compare every changed operational claim with current evidence. Expected:
  installed, proposed, verified, and unresolved are stated separately.

### Task 3: Verify the instruction and navigation paths

**Files:** Review changed roots, CLAUDE.md, docs/README.md,
docs/admin-workflows.md, skills/AGENTS.md and plugins/AGENTS.md.
Modify pointers only when affected by Task 2.

**Interfaces:** Produce a short readback in this plan: checked links, effective
instruction chain, contradictions resolved, runtime checks performed or skipped.

- [ ] Resolve every changed relative link. Expected: existing target or explicit
  future work label; no source moved without its incoming references updated.
- [ ] Read the effective root/component hierarchy, including overrides where
  present. Confirm CLAUDE.md still imports the intended operating instructions.
- [ ] Compare root claims with stage 2's inventory. Label dated generated views
  as snapshots. Verify fresh-session loading only if loading behavior changed;
  static path checks alone do not prove runtime behavior.
- [ ] Review the scoped diff and whitespace. Commit only under the owning Git
  workflow after required checks; do not stage unrelated files or push.

## Dependencies and self-review

Drafting can start now. Final capability statements depend on stage 2's accepted
inventory. IDEA's final role and any archive path need Task 1 confirmation.
All five review cases map to checks above. No identity files were changed by
creating this plan, and no memory or automation work is implied.


## Accepted docs role and layout, 2026-10-23

The user accepted docs/ as support for root identity and operating files.
Keep specs and implementation plans in docs/superpowers/. Keep domain procedures
with the owning skill, plugin, tool, or automation. docs/ owns cross-component
and cross-Space reference material rather than copies of those procedures.

### Task 4: Complete the Admin operating reference

**Files:** Modify docs/README.md, docs/admin-workflows.md, docs/tools.md,
docs/automation.md and docs/profiles/admin-architect-planning.md. Create
docs/memory.md. Modify root AGENTS.md and ARCHITECTURE.md pointers only where
needed. Preserve existing generated views as dated snapshots until replaced.

**Interfaces:** docs/README.md maps a concrete question to its owning document.
Root files provide short pointers. Component runbooks remain the source for
component-specific commands. Task 3 verifies the additional links and hierarchy
after this task as well.

- [ ] Build a question-based index: workflow/Space routing -> admin-workflows;
  role/identity/memory bindings -> profiles; memory placement/retrieval/correction
  -> memory.md; tool ownership/handoff -> tools; job ownership/report locations
  -> automation; proposed changes -> superpowers specs/plans.
- [ ] In admin-workflows.md, define the handoff record: source intent, receiving
  Space and entrypoint, authorized scope, canonical plan, return evidence, and
  escalation owner. Preserve existing accepted tool handoff rules by reference.
- [ ] In memory.md, distinguish operating policy, task state, native session
  stores, and Hindsight recall. Describe retrieval, attribution, correction and
  ownership using current integration instructions. Keep credentials out.
- [ ] In the profile reference, name responsibilities, boundaries, supported
  methods and proposed memory/identity bindings. Separate definition, host
  configuration and tested loading. Preserve draft status for unverified wiring.
- [ ] Reconcile tools.md and automation.md with current source. Keep only
  cross-component placement and handoff rules here; link detailed runbooks.
- [ ] Check the index against five scenarios: route tool development, maintain
  a skill, inspect an automation failure, correct recalled memory, and select a
  profile. Expected: each reaches one owner without duplicate instructions.
- [ ] Follow every added link and review root/component instructions together.
  Expected: no broken references, no proposed feature reported as deployed, and
  no policy copied from a specialist skill. Run git diff --check on scoped files.

Self-review addendum: Task 4 implements the accepted docs layout. Task 3 covers
its final navigation checks. Tutorial folders, duplicated skill catalogs and a
second planning system are not needed for this deliverable.
