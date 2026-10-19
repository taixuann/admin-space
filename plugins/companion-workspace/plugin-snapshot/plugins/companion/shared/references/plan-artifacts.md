# Retrievable HTML plans

Plan Companion owns this contract. Organization and other Companion workflows reuse it.

## Files and identity

Use the installed `answer-me-with-html` skill. Draft in Markdown and let its bundled CLI render the HTML. Read its instructions and current CLI help. Keep its styling and renderer; write no custom HTML generator. The Markdown draft is temporary input, not a saved plan artifact.
Save only the self-contained rendered HTML under the owning workspace's `.companion/plans/` when a workspace is known. Otherwise use a permitted local artifact directory and report that destination. The HTML must include the renderer's embedded `#am-source` so `am patch` can revise it later. Do not save a separate Markdown sidecar. Keep private plan artifacts out of tracked Git files. Respect local instructions and preserve existing files.
Use `YYYY-MM-DD_<project-slug>_<purpose-slug>_rNN.html`. Retain earlier revisions. Keep one stable `plan_id` across revisions and increment `revision` for substantive changes. Save an `INDEX.md` with one entry per plan: ID, title, project, current status, latest revision, updated date and one relative HTML link. Update only the entry for the current plan.

## Metadata

Put these fields in the temporary draft frontmatter. The renderer displays additional frontmatter fields in the HTML header and embeds the draft in `#am-source`. Include a readable metadata panel with the important fields too.

- `title`: readable purpose.
- `plan_id`: stable identifier, such as `companion-phd-organization-20261013`.
- `project`: exact project title.
- `project_url`: verified Notion Project URL, or unresolved when unavailable.
- `status`: DRAFT, APPROVED, PARTIALLY_APPLIED, APPLIED, SUPERSEDED or WITHDRAWN.
- `revision`: positive integer.
- `created`: ISO date or timestamp, retained across revisions.
- `updated`: ISO date or timestamp for this revision.
- `workflow`: owning Companion workflow.
- `scope`: included objects and excluded effects.
- `source_checked`: inspection timestamp; say historical when using an older snapshot.
- `coverage`: COMPLETE for the named scope only when enumeration and required content reads finish; otherwise PARTIAL with gaps.
- `supersedes`: earlier revision path, or none.

Add exact source links and material gaps in a Sources/Coverage panel. Metadata describes the plan, not live project status. Use the user's timezone for dates.

## Lifecycle

New proposals start DRAFT. Explicit approval of the exact revision can mark it APPROVED, but does not itself authorize Notion edits. An explicit request to apply a selected plan authorizes only its specified changes.
After Apply readback, mark APPLIED only if all included changes succeeded. Use PARTIALLY_APPLIED when a subset succeeded and list remaining work. Keep the report and the index consistent. Approval or application records need an attributable user instruction or verified readback; never infer them from elapsed time or unanswered choices.
When revising a plan, retain the previous files and identify the superseded revision. Refresh source targets before applying; new conflicts may reopen a dependent choice. HTML is a snapshot and does not refresh itself.

## Page and verification

Begin with Start here: the recommendation and next decision. Show a metadata panel, exact changes, one representative layout, sources/coverage and open decisions. Use 3–8 concise panels; use a linear document layout when the inventory requires more reading.
Render with `--no-open` and an explicit output path. Save only the rendered HTML in the plan directory. Inspect the page and verify its title, metadata, embedded `#am-source`, source links and content. Report renderer or visual-inspection failures without claiming a successful HTML delivery. If rendering fails, report that no final plan artifact was produced.
Return a short conclusion and the local HTML link. Keep retrieval in the local index; creating a Notion catalogue entry requires a separate write request.
