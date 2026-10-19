# Companion shared references

Use only sections relevant to the request. Connected sources own their records; Companion does not create a parallel tracker.

## Contents

1. [Core concepts](#core-concepts)
2. [Source ownership and reads](#source-ownership-and-reads)
3. [Shared operations](#shared-operations)
4. [Authorization and verification](#authorization-and-verification)
5. [Skill boundaries and handoffs](#skill-boundaries-and-handoffs)
6. [Domain guidance](#domain-guidance)
7. [Plans and durable proposals](#plans-and-durable-proposals)
8. [Writing](#writing)

## Core concepts

- Goal: intended outcome or direction; distinct from a project record, milestone, task and calendar event.
- Project: managed work in its canonical source.
- Milestone: substantial work package under a Project. Preserve each source's actual terminology and relations.
- Task: concrete action with an outcome. Linear issues remain the Development work records; do not copy them into Notion.
- Topic: Study question or branch in the published Wiki, linked to GitHub.
- Event: time reserved on Google Calendar. Schedule does not prove work began, finished or was learned.
- Progress: attributed state statement. Keep owner reports separate from connector records and inspected evidence.
- Evidence: source supporting a claim; record identity and inspected version or date where material.
- Outcome: result supported by owner confirmation or inspected evidence; say which.
- Next Focus: candidate or agreed priority for a stated period, not automatically a scheduled event.
- Blocker: unresolved dependency, decision or missing input that changes the next action.

Use the owner's words and current schema. Similar names do not prove identity.

## Source ownership and reads

- Notion owns Research management records and their schema, properties and relations.
- Linear owns Development projects, milestones and issues. GitHub Issues are not a parallel Development tracker.
- GitHub owns code and Study Wiki source evidence. Published Wiki is a reading surface.
- Google Calendar owns scheduled time. Routine Companion calendar scope is Research, Development and Study. Check other calendars only for a requested cross-calendar conflict check.
- Google Drive supplies reference documents and saved Rhythm plans. It is not a task tracker.
- Rhythm provides weekly budget allocations and mappings when the requested plan is available. It does not prove work completion.
- Assume connected Drive and GitHub information is current as the owner instructed. Do not run routine sync audits. Report an actual missing input or contradiction if encountered.
- Local file and folder organization belongs to Personal Hub's document workflow. Global Companion does not inspect or manage local folders.
- Scientific execution, interpretation and acceptance remain with the research owner and its project workflow.

Refresh relevant connected sources for the current request. Discover actual fields, relation targets and connector parameters at use time. Follow pagination; inspect truncation and unsupported content. Search finds candidates, not a complete inventory. State partial coverage when enumeration or required content is unavailable.

Scheduled time, page edit dates, commit counts and saved budget status do not establish outcomes. Owner-confirmed progress is valid management evidence, not independent scientific validation.

## Shared operations

These are action contracts, not separate skills or a wrapper service.

- READ: identify canonical source and target, fetch relevant state, follow pagination and record gaps.
- MATCH: compare stable identity and context. Names or keywords produce candidates; verify before acting.
- CREATE: create only when requested or clearly authorized, fields and destination are resolved, and no canonical record exists.
- UPDATE: identify exact record and fields, preserve unrelated content, apply only the authorized change, then read back.
- MOVE: inspect old and new ownership, dependencies, links, history and effects before changing placement.
- RECONCILE: compare sources and attributed reports, keep conflicts visible, propose a minimal correction.
- VERIFY: inspect actual post-action state and report changed, unchanged, failed and unresolved items. A successful tool call alone is not proof.

Know the source, canonical identity, preconditions, allowed effects and verification method. If a tool fails or returns partial data, continue independent work and label affected results partial.

## Authorization and verification

- Advice, discussion and proposals are read-only.
- A direct request to update a named record authorizes only that change after current-state checks.
- A capture request authorizes recording supplied information at the resolved destination. It does not authorize unrelated status changes or rewriting history.
- Calendar follows the owner-approved small-edit policy below. Preserve event identity and unrelated properties.
- A proposal, idea approval, scheduled event or reported completion does not authorize extra writes.
- Ask one focused question when target identity, destination, material content or authority remains ambiguous. Continue safe independent work.
- Carry existing authorization across handoffs. Do not ask the user to repeat settled facts or authority.
- Re-read after each write. After interruption or failure, inspect current state before retrying; retry only missing effects. Do not claim success from proposed tool calls.
- Never claim complete coverage when results are incomplete, truncated, inaccessible or only summarized.

A useful handoff carries intent, source, target ID or URL, inspected state and evidence, selected action, authorization, exact change, unresolved conditions and verification method. Keep it in chat unless the user asks to save it.

## Skill boundaries and handoffs

- Ask discusses goals, choices, context and alternatives. It does not write records.
- Plan sets long-term outcomes or short-term focus and returns a proposal in chat by default.
- Calendar handles event matching, scheduling, conflicts and authorized small corrections. Execute performs its writes.
- Review compares evidence, owner reports, recorded progress, outcomes, blockers and drift. It does not organize notes or choose next week's work unless asked to hand selection to Plan.
- Execute performs an exact authorized source-specific change and verifies it.
- Capture records explicit input in the resolved existing Notion, Linear or GitHub destination with attribution; ask when materially ambiguous.

A request can go directly to its owner. Do not force it through every skill. Local document and organization procedures remain in Personal Hub, outside global Companion.

## Domain guidance

### Notion: Research projects

Read the target Project and relevant Milestones, Tasks, Resources or References by identity. Inspect live schema and actual relation targets; a property called Goals does not prove it relates to Milestones.

Project records use Areas, Due Date, Status and Priority where required by the live schema. Ask the owner to choose a specific subarea when missing or ambiguous. Do not invent dates or status. Keep purpose concise, current progress in the Overview, dated history in the canonical log, and source navigation in an Evidence map when useful. Views and tabs are presentation, not new record types.

Use exact priority values: 1. Protected, 2. Core, 3. Opportunistic, 4. Deferred. Assess Project, Milestone and Task priority independently for the planning horizon.

A Milestone is a coherent work package and outcome. Define result, boundaries, completion evidence, relevant Tasks and real prerequisites. Do not infer dependencies from preferred order. Check live schema and cycles before writing dependencies.

A newly planned Task has one owning Milestone, the same Project as that Milestone, a concrete deadline and explicit Priority. Inspect live schema and Task template first. After template application, wait for content to settle, set agreed fields and read them back. Repair an existing record in place; never recreate it to repair layout. Preserve legacy direct-Project Tasks until reconciliation is requested. A Task may refer to a canonical Resource; Resources are not Task relations.

Resource and Reference are distinct. Resource is primarily the owner's authored work or synthesis. Reference retains authority with its external source. Draft, Active and Archived require Project context; Stable requires an actual Area or Subarea relation. Stable does not prove a Reference is current. Preserve source identity and dates. Resolve actual Area/Subarea hierarchy and the user-selected target; do not infer it from titles. Inspect templates before creation, apply once and verify settled content and reciprocal relations. Custom Archived status is not Notion's archive action or deletion.

Use one canonical Project-related Resource as Progress log when appropriate. Keep one date toggle per capture day, titled YYYY-MM-DD and newest first. Attribute update and source; retain known event date separately. Preserve history with dated corrections. A Progress log tab may point to latest review, agreed focus, attention items and project history. Remove an attention pointer only after its conclusion is saved and verified; never delete its source history. Evidence map is navigation; log is history. Do not duplicate results or task lists across both.

For weekly review, resolve explicit week and timezone. Inventory all Milestones and Tasks in each selected Project, including completed, Deferred and legacy direct-Project records. Recover prior commitment, due or scheduled work, dated evidence and relevant overdue or blocked work. Deduplicate by identity. Separate planned, due, worked, completed and carried over. Current properties alone cannot reconstruct historical priority or commitment.

For next week's commitment, select finite canonical Tasks with the user. New commitments require Milestone and Task priority 1-3, readiness, dependencies, capacity, concrete deadline and completion criteria; priority 4 remains backlog. Missing ownership or priority stays unresolved. Preserve hard deadlines. Calendar owns days and times. Proposal changes nothing until saving is requested.

Research evidence stays in its owning project. Treat progression summaries as navigation; inspect detailed records before stating completion. Distinguish study completion, unfinished synthesis, software development and scientific acceptance. Keep user updates separate from inspected evidence. Link exact GitHub files or reviewed commits where useful, but do not imply Notion syncs local files. Research workflows own scientific execution and interpretation.

### Linear: Development

Use Linear projects and issues as canonical Development records. Inspect current status, readiness, dependencies, priority and available estimate fields before proposing work. Keep project-level focus when no issue is ready. Do not invent issues, create duplicates or make Notion copies. Capture an update to an existing Linear target only when identity and destination are clear.

### GitHub: code and Study Wiki

Use GitHub for code and Wiki source. For Study, resolve the published topic index and linked branch goal, then inspect substantive changes over the relevant period. Theme or configuration-only commits do not prove learning; commit counts alone are not outcomes. Distinguish current branch navigation from an exact reviewed commit. Capture authored notes or documentation only in a resolved existing repository path. Capture does not implement code or publish automatically.

### Calendar and Rhythm

Use Research, Development and Study calendars in routine work. Inspect event identity, time zone, start/end, recurrence, reminders, attendees, description, source links and status before changing an event. Keep other calendars out of routine audits; inspect them only for a requested cross-calendar conflict check.

Research events map to verified active Notion Tasks. A verified scheduled active Task may move from Not Started to In Progress where appropriate. Never reopen Complete or Archived Tasks, and never mark completion because an event ended. Development events may remain project-level when Linear has no ready issue. Study events resolve through Wiki topic, branch goal and substantive evidence; no Notion Task is required. Do not invent a match from a similar title.

Owner-approved small Calendar corrections are limited to clear spelling, grammar, capitalization, stray punctuation, unambiguous canonical links, clear domain placement and the permitted verified Research transition. Preserve meaning, event ID, time, time zone, recurrence, reminders, attendees, priority and unrelated description. Re-read each changed event. Do not move fixed commitments, invent duration or turn vague placeholders into tasks. Report changed, unchanged, unresolved and source coverage; repeated runs must not add duplicate records or links.

Use Rhythm only as capacity input for the requested week and relevant area mapping. Read only Research, Development and Study budgets when applicable. Calendar event status such as confirmed is not Task completion. Do not modify Rhythm budgets or sync settings. If the needed plan is actually unavailable, report that gap; do not fabricate targets.

The current approved Calendar control spec and operational revision are at [Calendar Companion control spec](https://www.notion.so/3fd0a859ed1f81eeb5dcc8d4d2aeaa78). Its attached calendar-companion-references.md was not accessible during this update. Use the visible operational contract above; retrieve the attachment before relying on connector-specific recipes not stated here. The operational revision supersedes historical draft rules.

## Plans and durable proposals

Plan returns a reviewable proposal in chat by default. Do not require local HTML, Markdown plans, a catalogue or retrieval index. Save only when the user explicitly requests a durable copy and the connected destination is resolved. Ask one focused destination question only when needed. Distinguish long-term outcomes from short-term actions, capacity and scheduled time. Do not invent dates, priorities or commitments.

## Writing

Use clear, concise wording and retain canonical product, scientific and skill names. The vendored guide is at shared/writing/simple-english/GUIDE.md; its license and provenance remain with the bundle.
