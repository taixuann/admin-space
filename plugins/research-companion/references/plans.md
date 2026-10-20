# Plan records

## Purpose and uses

A plan is a reviewable proposal for one owning action. It records the intended
outcome, why the action is useful, selected evidence, requirements, decisions,
steps and completion checks. Use it to continue a discussion, compare options,
review material choices or hand settled work to the action owner.

The plan's completion boundary is a concrete proposal with explicit open
questions or a scientist-approved revision. It is not a finished Study.
Ask gathers and discusses context; Plan turns it into a saved proposal when
requested; the action owner creates or changes canonical scientific artifacts.
Keep the plan in one primary HTML file with embedded source and metadata.

Write the plan in plain English. Lead with an index of planning questions.
Mark the current question, the next decision and the recommended reading order.
Link each index entry to its question section with a descriptive label.
Combine a short explanation with a diagram when relationships need one.
Keep context and source limits near the answer they support.
Use only the aspects needed for the selected question. Omit irrelevant sections.
Give one short reason when an omitted aspect needs explanation.

Each question section states its purpose, current answer and basis, open point,
recommended action, expected result and completion condition.
Develop questions from the frame instead of imposing the same questions on every study.
During brainstorming, assess the support needed for each question and explain the choice.
Keep proposed skill actions distinct from completed retrieval or analysis.
Prefer one current scientist decision over several competing calls to action.

Use short bold labels for Current step, Next action, Completion and Status.
Use lists for choices or ordered steps. Keep the explanatory sentences beside them.
Use diagrams for dependencies and branches, tables for source comparisons,
and prose for reasons and uncertainty. Choose the format by the information.
The question index provides navigation. Formatting must preserve that reading order.

Link related studies when their findings or methods answer a specific need.
State what is reused, its identity, acceptance state and transfer limits.
A related study can supply context without becoming a measurement input.
If execution consumes its artifact, declare it through the action owner.
Reused evidence does not automatically transfer scientific acceptance or sample independence.

For INIT coverage, read [Study planning](study-planning.md). For other actions,
read their current owning references and use only the relevant template sections.

## Location and identity

Save a plan beside the work it proposes. A new plan-led analysis or its result
plan belongs under `<analysis-root>/plans/`; a project-level progression plan
belongs under `progress/docs/plans/`. Use the local date and a descriptive,
filesystem-safe name. Keep consultation in chat unless a saved proposal is
requested. Do not create a competing plan under `.research-companion/`.

Keep these frontmatter fields in the renderer's embedded source:

| Field | Meaning |
| --- | --- |
| type | `study` or `research-progress`; the owning domain |
| version | `1.0.0`; this plan format, not scientific or software maturity |
| plan_id | Stable identity for this plan across revisions |
| revision | Positive integer that increases when the plan changes |
| status | `DRAFT`, `READY_FOR_REVIEW`, `APPROVED` or `SUPERSEDED` |
| created / updated | Actual local dates in `YYYY-MM-DD` form |
| target | Exact project-relative target path, existing or proposed |
| action | One explicit owning action, such as `init` or `prepare` |
| approval | `null`, or scientist identity, date, approved revision and source |
| supersedes | `null`, or the replaced plan's relative path |

Metadata describes the proposal. It does not set scientific lifecycle status.
An approved plan is not scientific acceptance or execution permission.

For a new plan-led analysis, use `action: implement`, `owner: implement-research`
and `type: study`. The specification lives in `<study-root>/spec/` (`reasoning.md`,
`methods.md`, `requirements.md`) and the implementation plan lives in
`<study-root>/plans/YYYY-MM-DD_<name>_plan.html`. Plan Research owns analysis
choice and rationale, observation units, exact inputs, parameters, exclusions,
missing-data handling, uncertainty, output checks, and task decomposition (Files,
Steps, Tests). For every window-based analysis, state each window boundary and
whether each endpoint is included; do not assume a default. Implement Research
checks that contract, writes and tests code via TDD (PREPARE phase), then
executes the authorized scope (RUN phase).

For result synthesis, use `action: compose`, `owner: compose-research` and
`type: study`. The result synthesis plan lives in
`<study-root>/plans/YYYY-MM-DD_<name>_result_plan.html`. It specifies the exact
selected run IDs, the proposed evidence dispositions (`ACCEPTED`, `REJECTED`,
`AMBIGUOUS`, `SUPERSEDED`, `MISSING`), which primary figures and views will be
promoted to `results/RESULT.md`, and any supplied interpretation. Use the
versioned Result Plan v1 fields below.
Compose Research checks that contract, verifies output checksums, stages accepted
artifacts into `results/artifacts/<run-id>/`, and writes `results/RESULT.md`.

Record explicit user implementation/execution authorization separately from
review status. If the scientist requests execution of settled choices, do not
invent approval of a new revision or ask for that scope again. Essential open
method choices still block execution. Keep an updated unapproved plan
READY_FOR_REVIEW with the actual authorization source rather than falsely
marking its exact content APPROVED.

## Review and revision

- Use `DRAFT` while essential choices remain unresolved.
- Use `READY_FOR_REVIEW` after self-review when the plan is concrete and feasible.
  State inspection gaps and nonessential limitations explicitly.
- Use `APPROVED` only after the scientist explicitly approves that exact revision.
  Record the approval source; never infer it from a filled template or self-review.
- If approved content changes materially, preserve the approved file and create
  a new revision file, for example `_r2.html`. Link it with `supersedes`, set its
  status to `DRAFT`, and leave its approval empty. Do not overwrite prior approval.
- Mark a prior plan `SUPERSEDED` only when replacement is explicitly settled.
  Preserve its approval and history. A new draft does not silently retire it.
- For unapproved edits, increment revision and refresh updated. Re-review the
  affected requirements. Keep a short change note instead of a full transcript.

## Content and handoff

The template holds requirements, evidence, decisions and steps in one place.
For each step, state its deliverable, check and completion condition. Scale
detail to the action. Keep scientific calculations in RUN, not in planning.
Use Study INIT's framing dimensions for init plans. For prepare plans, map the
accepted specifications to readers, dependencies, code, outputs and preflight.
For run plans, name readiness checks, exact inputs, outputs and stop conditions.
For result plans, name selected locks, evidence dispositions and output scope.
Read Research Progress's matching action for project-level plans.

Borrow explicit files, constraints and verification steps from software planning.
Use Superpowers for authorized software implementation when it applies.
Its coding execution workflow cannot choose methods, clear scientific gates,
or automatically execute a research plan.

Before execution, refresh the plan's target and cited sources. If a material
source or decision changed, return the affected part for review. Respect the
exact authorized action; a completed action grants no next action by itself.

HTML is the primary plan. Use the installed renderer and retain its embedded
`am-source` so an agent can recover the exact draft and metadata.
Edit the source and regenerate with the same renderer. Do not edit generated HTML.
Keep prior Markdown plans as historical records, not a second active authority.
Identify the active HTML and revision in the historical record when switching.
Temporary source drafts are rendering inputs, not separately maintained plans.
An HTML plan does not grant execution permission or scientific acceptance.

## Result Plan v1

A machine-readable result plan uses `schema_version: 1`. This contract applies
to new plan-led result plans; it does not describe historical records.

```yaml
schema_version: 1
plan_id: result-plan-id
revision: 1
decision_source: Explicit human review source
run_bindings:
  - run_id: selected-run-id
    lock_sha256: <lowercase SHA-256 of selected run lock>
assessments:
  'selected-run-id/object-id': ACCEPTED
questions:
  - question_id: Q1
    text: User-authored question text
    source_heading: Exact heading in spec/reasoning.md
    evidence_ids: [selected-run-id/object-id]
views:
  - view_id: V1
    evidence_id: selected-run-id/object-id
    label: User-supplied view label
observations:
  - observation_id: O1
    question_id: Q1
    evidence_ids: [selected-run-id/object-id]
    label: User-supplied observation label
    value: '0.125'
    unit: V
    method: User-supplied method
    limits: User-supplied limits
interpretation: Optional supplied interpretation
interpretation_source: human
```

`plan_id`, `decision_source`, question and evidence IDs are non-empty; revision
is a positive integer. Each selected run has exactly one lock-hash binding.

Artifact assessments are recorded by the human study owner or PI; they are
never inferred from process success, plan approval, or generated output. `MISSING`
is bookkeeping-only. It is not a scientific assessment and is excluded from
acceptance and all packaging scopes. It must not be used as an accepted RESULT
artifact or included in an RO-Crate.
Questions bind to an exact Markdown heading in `spec/reasoning.md`; their text
must occur in that heading's section after normalization (case and whitespace
folding, Markdown emphasis/code markers and blockquote prefixes removed). Each
question cites one or more unique selected output IDs. Views cite one selected,
explicitly `ACCEPTED` output linked to a question. Observations cite a declared
question and only evidence linked to that question. Their `value`, `unit`,
`method` and `limits` are supplied strings. Compose records them without
computing or interpreting them. Use empty `views` or `observations` lists when
none are selected. A non-empty interpretation declares `human` or `model` as
its source; generated text is not labeled as verbatim scientist wording.
