# Working context

## Read by question

Start with the object the user names. Resolve its identity and read its current properties and body before following relevant relations. Use the actual schema rather than assuming relation names.

- Project: read purpose and current direction, then only milestones, tasks or resources relevant to the question.
- Milestone: read its Project, outcome, relevant Tasks and prerequisites. Inspect dependent work when a proposed change affects it.
- Task: read its owning Milestone and Project, deadline, priority and relevant blockers or successors. If the owner is missing, surface the gap.
- Resource or Reference: read type, status, Project/Milestone context and any explicit Area/Subarea placement. For Stable promotion, resolve the destination with the user.
- Note: read its owning context, source and date. Resolve whether it is a log entry, meeting note or separate Resource from the actual record. A note is not automatically a Task or a new database type.
- Research: follow the [research source rules](research.md). Distinguish a local Goal from a Notion Milestone and inspect their mapping rather than inferring it from names.

Stop expanding when the sources answer the question and reveal the material effects. Ask focused questions for unresolved choices, inaccessible sources or missing required inputs. Reuse information already provided. Do not ask the user to repeat facts available in inspected records.

## Coverage and effects

Use the selected workflow's scope before deciding that enough information was read:

| Workflow | Read scope | Output and write scope |
| --- | --- | --- |
| Ask | Named objects, owning context and relations that can change the advice | Advice; no persistent edits |
| Weekly review | All Milestones and Tasks in each selected Project, then week-specific records and relevant logs, notes and Resources | Review and bounded commitment; save only on request |
| Plan | Every proposed target, owning context and materially affected relations | Concrete proposal across object types; no persistent edits |
| Capture | Input, destination, owning Project and relations needed to interpret the capture | Requested entry and relevant attention pointer |
| Apply | Refresh every write target, relation destination and affected invariant | Authorized changes across object types, followed by readback |

Inspect actual schemas and resolve records by identity. For inventories, follow every result page and check truncation. A filtered view or page summary does not establish complete membership. Reconcile Project-linked Tasks with Milestone-linked Tasks; surface mismatched ownership and legacy direct-Project Tasks rather than silently omitting them. If the tools cannot enumerate the required scope, report partial coverage and the missing sources.

Before advice, proposals or writes, trace effects that can change the decision. For ownership changes, inspect the old and new parent and dependent work. For completion or archival, inspect remaining children and prerequisites. For dates or priority, inspect dependencies, weekly commitments and hard deadlines. For Resource placement, inspect Project/Milestone use and Area relations. For notes and log corrections, inspect the source entry and pointers or summaries that cite it. A wording-only edit needs less expansion than these structural changes.

Separate included changes, recommended follow-up changes and unaffected records. Reading a related object does not authorize changing it. Do not infer parent completion from child completion or propagate priority, dates or ownership automatically.

Carry a coverage receipt into the handoff: selected scope, sources read, inventory counts when claiming completeness, unresolved relations, inaccessible or truncated sources and effects considered. Report only the details that matter to the user. Keep conclusions proportional to coverage. Complete the safe independent portion while leaving unsupported decisions open.

## Owner progress and recorded state

The owner's latest clear statement is authoritative for management progress. If the owner says a named Task or Milestone is done, accept it even when Notion Status or a checklist is stale. Do not ask for the same confirmation again or demand independent proof just to reconcile management records. Attribute it as owner-confirmed; this does not claim independent scientific validation.

Clarify only material ambiguity in identity or scope. “Nearly done” keeps the object open; “basic work done” does not close advanced work. Inspect remaining children to propose their disposition, not to reject a clear owner confirmation. Never complete children or parents by cascade.

During review, propose concrete actions: target, recorded Status, desired Status, and any remaining scope or dependency effect. A progress statement supplies the fact; a request to write or Apply supplies execution authorization. Reuse authorization already given for those exact changes. If the actual completion date is unknown, record the confirmation date separately rather than inventing a completion date. Preserve historical evidence and dated corrections.

## Carry context between workflows

Keep a compact working summary in the conversation. Include only what the next decision needs:

- Intended outcome and target objects with exact URLs or local paths.
- Relevant current state, inspected sources and their version or comparison date when needed.
- User-reported updates, assumptions and source conflicts, separately attributed.
- Settled decisions, remaining questions and material related effects.
- Proposed edits and the scope of any explicit write authorization.

Update the summary when the user changes direction. Refer to the settled context across ask, plan and apply rather than interviewing the user again. If context is unavailable in a new chat, recover it from a supplied handoff and inspect the current targets.

Keep the summary in chat by default. If a durable handoff is useful, propose its destination. Save it only on request. A saved proposal remains a proposal, not current project state or permission to execute.

## Offer the next step

At a useful decision point in Ask, offer further discussion or a concrete Plan. Offer Apply only when the exact proposed edits are already clear. Do not end every answer with a workflow menu.
After presenting a Plan, invite the user to discuss it further or request Apply. If the user has already explicitly requested the same write and no material decision remains, continue to Apply without asking again.
When Apply lacks context, first recover available discussion and inspect the named objects. Ask only for missing decisions. If the scope or desired content still needs design, offer Plan; do not invent a proposal and apply it in the same step.
An offer is not a workflow selection or write authorization. Follow the user's reply, and carry the settled context into the selected workflow.

## Apply readiness

A proposal identifies targets, exact edits or draft content, relation destinations, relevant effects and unresolved decisions. For a new Task, resolve its Milestone, matching Project, concrete deadline and priority under [Task](task.md). Apply the corresponding definitions to other object types. Keep missing values open rather than inventing them.

User approval settles the proposal presented. Execution requires an explicit request to write or apply it. A direct fully specified write request supplies that authorization without a second approval ceremony. Limit execution to the authorized edits and revisit only materially changed or unresolved choices.

Before writing, refresh the target state. A new conflict can invalidate part of a proposal. Report it and settle the affected part rather than silently applying stale content or expanding scope.
