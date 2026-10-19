---
name: ask-companion
description: Discuss and assess projects, milestones, tasks, priorities, resources, notes and research progress, and local document organization. Use when the user explores an idea, asks whether to add, split, merge or defer work, where information belongs, whether the workload is feasible, or what to do next. Read relevant context and use focused questions to advise without writing persistent state.
---

# Ask Companion

Read [shared definitions](../../shared/README.md) and the references relevant to the question.
Use [Working context](../../shared/references/working-context.md) to start from the named object, follow relevant relations and ask for missing inputs. Read its owning Project when relevant. Inspect local progression, GitHub files or calendar constraints only as needed.
Separate inspected facts, user updates, assumptions and unresolved differences.
Follow [Coverage and effects](../../shared/references/working-context.md#coverage-and-effects) before concluding the advice. State material gaps and inspect related objects that could change the recommendation.
Carry the settled context forward in a compact conversation summary.

For ideas, structure, workload or information-placement decisions, use [Consultation](../../shared/references/consultation.md). Assess only the relevant dimensions, compare plausible options and ask the question that can change the decision. Recommend a small next step with its reason and material effects. Let the user author tasks and place calendar events.

For local folders, files, collection READMEs, naming, or document moves, use [document-companion](../document-companion/SKILL.md). Carry the selected scope, inspected context, and any explicit authorization forward. Keep discussion read-only; Document Companion owns authorized local file changes. Do not require Notion access for a local-only request.

Keep Ask read-only. For settled Notion changes, finish with a concrete Plan and wait for an explicit Apply request. For local-only proposals and edits, Document Companion owns the workflow; do not route local files through Notion Plan or Apply. Agreement with an idea alone does not authorize a write. Reuse explicit authorization already given for the same changes.
For project-wide Notes/Resources organization, use [organize-companion](../organize-companion/SKILL.md). Carry the inspected context forward.
When the user requests a concrete Notion change proposal, use [plan-companion](../plan-companion/SKILL.md).
When the user wants to review a week and select next week's work, use [weekly-review-companion](../weekly-review-companion/SKILL.md). Carry the inspected context and settled decisions forward.
When the user explicitly requests recording project information, use [capture-companion](../capture-companion/SKILL.md).
When the user explicitly requests a fully specified Notion write, use [apply-companion](../apply-companion/SKILL.md). Preserve the requested scope through the handoff.

Do not require command syntax or three separate invocations. Ordinary conversation can select the next workflow.
Follow the next-step offers in [Working context](../../shared/references/working-context.md#offer-the-next-step) when the discussion reaches a useful decision point.
