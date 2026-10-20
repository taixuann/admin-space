# Owners and handoffs

Use the owner of the requested action. A folder name, completed run, or prior
approval does not grant authority to perform a different action. The shared
matrix below is the routing authority for this plugin; skills link here rather
than repeat a competing lifecycle.

| Intent | Owner | Allowed action |
|---|---|---|
| Discuss status or a settled question | Ask Einstein | Read selected context and advise; no writes |
| Explore an open direction | Brainstorming | Generate candidates; the scientist selects a direction |
| Plan a new plan-led analysis | Plan Research | Write the selected analysis spec and HTML proposal |
| Change an existing Study leaf | Study | Use the matching Study action; no automatic migration |
| Implement or execute selected plan-led work | Implement Research | Follow the exact authorized scope and record one run |
| Materialize selected evidence | Compose Research | Validate explicit dispositions and create RESULT artifacts |
| Archive selected evidence | RO-Crate Research | Package the explicitly selected evidence and provenance |
| Update project progression or prepare slides | Research Progress | Own the progression action and delegate slide building |

Brainstorming is conditional. Use it when direction, mechanism, or candidate
questions remain open. For fixed descriptive work, preserve the selected scope
and review only methods that remain unsettled. Do not manufacture statistical
inference requirements, and distinguish descriptive fitting from inferential
claims. Domain procedures are selected when a concrete unresolved decision
needs them; they are not mandatory steps for every plan.

The scientist's words and choices remain distinguishable from proposals.
Label generated interpretations as model-authored proposals. Never present
draft text as verbatim scientist wording. A direct request authorizes only the
requested action; do not ask again for the same settled scope. Essential open
method choices still block execution.

## Plan locations

- New plan-led analysis and result plans live under the selected analysis
  folder's `plans/`: `YYYY-MM-DD_<name>_plan.html` and
  `YYYY-MM-DD_<name>_result_plan.html`.
- Research Progress action plans live under
  `progress/docs/plans/YYYY-MM-DD_<action>_<target>.html`.
- Keep consultation and review notes in the conversation unless the user asks
  for a saved proposal. Do not create a second active plan under
  `.research-companion/plans/`.
- Each plan has a stable `plan_id` and a positive, increasing `revision`.
  Preserve prior revisions; link replacements with `supersedes`. The active
  revision is the exact file selected for the requested action.

## Evidence handoffs

Implement Research records process status separately from scientific
acceptance. A completed run remains `NOT_ASSESSED` until the human study owner
or PI explicitly records a decision; never infer acceptance from process status,
plan approval, or output appearance.
Result plans bind the selected run IDs to lock hashes, explicit artifact
dispositions, question sections, evidence views and any supplied observations.
Compose copies supplied values as text; it does not calculate or reinterpret
scientific metrics. `MISSING` is bookkeeping-only and is excluded from scientific
acceptance and packaging. Crate packages only the selected, verified scope.

For Research Progress, use the owning skill for status, logs, goals and slides.
A status question is read-only. A request to update a log is routed to Research
Progress; Compose does not append progression records.
