# Task

## Required planning information

Each newly planned Task has one owning Milestone, the same Project as that Milestone, a concrete deadline, and an explicit Priority. These are companion's planning rules, not claims about database validation.
Inspect the live schema before writes. A relation still named `Goals` may point to Milestone DB; resolve its target instead of inventing a `Milestone` property.
Surface missing membership, deadline, or priority for the user to decide. Preserve incomplete captures without fabricated values. Distinguish external hard deadlines from user-selected completion targets and from calendar sessions.
Shared work has one owning Milestone. Reference its output from other milestones instead of duplicating the Task. Preserve legacy direct-Project tasks until reconciliation is requested.

## Templates and creation

Inspect Tasks DB templates and use the appropriate existing Task template when creating a Task. Fetch the created page until template content is ready, then fill its relevant sections with the agreed outcome and completion criteria. For an existing Task created without its template, apply it once in place and preserve existing content; never recreate the Task merely to repair its layout. After interruption, inspect actual content before retrying template application.

Template defaults may add or overwrite properties and relations. After it finishes, set and read back the agreed Project, owning Milestone, Status, Priority and concrete Due date. Verify the Project matches the Milestone and remove unintended template defaults only within the authorized Task scope. Check reciprocal relations where present. A successful template request alone does not prove completion.

## Granularity and completion

Name a concrete action and result. State what proves completion.
Use one Task for simple work. Keep a short checklist when steps belong in one execution unit.
Split work when parts need separate completion, scheduling, prerequisites, context, or review. Let meaningful boundaries determine task count.
Use intent, planning, execution, and review only where useful. Intent may be a sentence in the description; planning may happen in discussion; quick checking may finish the execution Task. Create a separate review Task when it has its own output, participant, or decision. Add audit only when justified by the actual work or requested.
Do not require every Task to follow the same phase sequence or meet a minimum duration.

## Effort and dependencies

Estimate focused effort as a range when uncertain. Separate effort from waiting time and the elapsed calendar window. Explain material uncertainty; exact scheduling remains user-owned.
Use dependency only when a Task requires another Task's output. Preferred sequence alone does not qualify. Inspect existing native dependency relations before writes and check for cycles.
Use timeline when dates and dependencies help the discussion. Keep undated work visible elsewhere. Change automatic date-shifting settings only when requested.

## Priority and selection

Use `1. Protected`, `2. Core`, `3. Opportunistic`, and `4. Deferred`. Consult the priority policy linked in [Milestone](milestone.md).
Assess Task priority independently of its Milestone and Project. Read [Weekly focus](weekly-focus.md) to select a feasible subset of work.
