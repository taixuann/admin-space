---
name: apply-companion
description: Apply explicitly requested, concrete changes to Notion project records and verify the result. Use when the user says to write, save, or apply specified changes. A request for advice or agreement with an idea alone does not trigger execution.
---

# Apply Companion

Read [shared definitions](../../shared/README.md) and the relevant references.
Use [Working context](../../shared/references/working-context.md) to recover the concrete targets, edits and explicit write authorization. An approved proposal alone is not execution authorization. A direct, fully specified write request can proceed without a separate planning ceremony.
If a material choice remains open, use [plan-companion](../plan-companion/SKILL.md) or [ask-companion](../ask-companion/SKILL.md) before writing the dependent part.
Follow [Working context](../../shared/references/working-context.md#offer-the-next-step) to recover missing context and offer Plan when the requested change still needs design.

When applying a saved HTML plan, resolve its exact plan ID and revision under [Retrievable HTML plans](../../shared/references/plan-artifacts.md). Read the source embedded in the HTML and verify the user authorized its included edits. Update the HTML metadata and local index after verified readback; use PARTIALLY_APPLIED when any included edit remains.

Fetch the current target and schema. Compare them with the proposal. If new state changes the meaning of the edit, surface the difference before proceeding.
Follow [Coverage and effects](../../shared/references/working-context.md#coverage-and-effects) for any supported object type. Verify affected invariants and relation destinations before each dependent write. Keep unrelated effects as recommendations rather than expanding the authorized changes.
Use native connector tools. Follow their format, deletion and authorization requirements. Make the smallest complete change within the requested scope.
For Task creation or template repair, follow [Task templates and creation](../../shared/references/task.md#templates-and-creation); verify the rendered template content and all required properties after template defaults have settled.
For Resource creation or assignment, follow [Resources](../../shared/references/resources.md#templates-and-creation). Verify template content, lifecycle properties and actual Project relations, including the reciprocal side when present.
Related effects are not permission for cascading edits. Preserve unrelated records, relations and content. Scientific execution and acceptance belong to the research owner's workflow.

Read back each requested write before reporting completion. For structural and multi-part edits, also make sure that properties, relations, links and nesting match the request.
If a write partially succeeds, report the actual state. Re-read before retrying to avoid duplicate records or log entries.
If a content match fails or is ambiguous, fetch the page again. Use smaller unique text spans from the current content. Preserve nesting when replacing a paragraph with several blocks. Check each replacement against its intended section before submitting; avoid broad replacement or deletion as a workaround.
Record a progress log entry only when included in the request. Keep administrative changes distinct from research results.
Report what changed, the verification performed, and any unresolved part. Reconcile the result with all agreed items so none silently disappears. Surface relevant remaining decisions or follow-up discussion, without reopening settled choices or executing additional changes. Offer further discussion only when there is a concrete open item.
