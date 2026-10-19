---
name: plan-companion
description: Turn discussed project changes into a concrete, reviewable proposal. Use when the user asks to plan, prepare changes, reorganize project information, or define what will be written. Read sources and draft changes without applying them.
---

# Plan Companion

Read [shared definitions](../../shared/README.md) and the relevant references.
Use the settled discussion as the starting point. Inspect the actual target, schema and source context before drafting changes.
Use [Coverage and effects](../../shared/references/working-context.md#coverage-and-effects) for any Project, Milestone, Task, Resource, Reference or note proposal. Carry the coverage receipt from the owning discussion and fill material gaps. Planning can support any of these object types without a weekly review.
Use [Working context](../../shared/references/working-context.md) to reuse settled inputs and resolve required fields, identities and relation destinations.
If scope or content remains unresolved, return to [ask-companion](../ask-companion/SKILL.md) for that decision.

Render the proposal with the installed `answer-me-with-html` skill. Follow [Retrievable HTML plans](../../shared/references/plan-artifacts.md) for durable files, metadata, revision identity, lifecycle and verification. Return a short conclusion and the HTML link. Name the target records, exact edits or draft text, related effects, and remaining decisions. Distinguish recommended related changes from included changes.
For Overview layout changes, show one representative Milestone in the proposed format. State how the format applies to the other sections so the user can review it before writing.
For Evidence map changes, show the proposed groups, source links, reading purposes and material boundaries. Identify existing links or discrepancy notes to preserve or remove.
For Resource or log creation, include the existing template, actual Project relation, Scope, Status and any required schema change under [Resources](../../shared/references/resources.md). For weekly review proposals, use [Weekly focus](../../shared/references/weekly-focus.md) to show the bounded commitment and exact log and tab changes.
For a simple edit, one sentence can contain the complete proposal. Use a temporary Markdown draft as input to `answer-me-with-html`, then save only the self-contained HTML artifact under the plan artifact contract. Keep its embedded source available for future edits. This local output is part of planning; Notion records remain unchanged.

Keep planning read-only. Approval of the idea does not authorize edits that were not presented. When the user explicitly requests applying the concrete proposal, use [apply-companion](../apply-companion/SKILL.md).
An earlier explicit write request remains valid for its specified scope. Do not ask for the same authorization again unless a material decision remains unresolved.
Follow the next-step offers in [Working context](../../shared/references/working-context.md#offer-the-next-step) after presenting the proposal.
