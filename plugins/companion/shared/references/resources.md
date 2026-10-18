# Resources and References

## Accepted direction

The user wants Resources DB to contain `Resource` and `Reference` only. `Skills` is slated for retirement there. This definition does not authorize deleting existing pages or changing Notion schema. Preserve their contents until a concrete migration or deletion is requested.

- Resource: material whose primary value comes from the user's authored work, synthesis, model, or judgment.
- Reference: material whose authority primarily remains with its originating external source. Summarizing or formatting a source does not change its type.

## Status and placement

Apply the same placement convention to both types:
- Draft: provisional material related to a Project; it may become Active or go directly to Archived if unnecessary.
- Active: material actually used or developed in a Project.
- Stable: durable material with at least one explicit Area or Subarea relation. Relevant Project/Milestone links may remain.
- Archived: retained Project-related history outside the current working catalogue.

Local means Project context inside Notion. Use Project-scoped wording rather than introducing filesystem storage.
Draft, Active, and Archived require Project context and have no Area/Subarea placement relations. Milestone context may refine their Project context.
Area/Subarea catalogues contain Stable objects only. Filtering a view is not a substitute for satisfying these relation rules.
Stable does not prove external facts are current or independently verified. Preserve source identity and dates for References.
Promotion may retain relevant Project/Milestone links for use or provenance. Do not detach links merely because status becomes Stable.
Before promotion to Stable, resolve at least one actual Area/Subarea target. If no target is known, leave promotion unresolved.
If a Stable object returns to a Project-scoped state, discuss its Project destination and the Area/Subarea relation changes before writing. Preserve lineage and do not remove relations automatically.
The custom `Status = Archived` value is separate from Notion's native archive action. Neither implies deletion.

## Relations and hierarchy

Project links identify the project context or use. Milestone links identify the specific work package supported. Add only materially relevant links, not every milestone in a Project.
Keep Resources/References out of Task database relations. A Task may mention the canonical page when needed for execution.
Area/Subarea identifies domain placement. Resolve the actual hierarchy and specific subarea chosen by the user; a property called `Areas` may point to a Subarea record.
Inspect record identity, parent/child relations, and available typology before classifying an Area versus Subarea. Do not infer hierarchy from titles alone or create separate databases merely because both levels exist.
Keep domain placement distinct from project use. Reuse one canonical object across relevant contexts rather than duplicating its content.
Read the live schema before writes. Missing Project/Milestone relations require a scoped structural proposal, not invented property names.
Use an actual Project relation to assign a Project-scoped Resource. A mention or Scope value alone does not establish assignment. Verify the Resource relation and the Project's reciprocal relation when one exists. Resolve property names from the live schema. Include any missing relation in the concrete proposal before changing the schema.

## Templates and creation

Inspect the database's existing templates before creating a Resource or Reference. Use the template for the selected type before filling its description and content. Keep its useful layout and fill the relevant sections. Reuse an existing page's template structure. Apply a template only once; after an interrupted call, fetch the page before retrying. Template application can append content and can take time to appear. Verify it before dependent edits.
Set type, Project relation, Scope and Status from the agreed use. Keep an ongoing log Active while it is in use. Keep a provisional snapshot Draft when its future use is unsettled. Processing an individual entry does not change the whole Resource's lifecycle status. Keep unresolved items in content under [Capture and evidence](capture.md).

## Catalogue

Treat a project catalogue as navigation into canonical Resources/References. Group by useful concerns and explain briefly when each item is used. Keep content in the owning page.
Discuss whether a candidate adds a distinct source or reusable contribution before adding it. Reuse existing material first.
Old Knowledge Object Control instructions are context to compare with this accepted direction. Surface conflicts instead of silently reapplying superseded taxonomy or placement rules.
