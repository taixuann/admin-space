# Manifest-backed documentation views

Use when a structured capability manifest must drive an Archify HTML view that changes with the source.

## Build in order

1. Inspect the profile README, capability manifest, owning automation rules, and installed renderer. Establish whether the reader needs an inventory, a profile/workflow explanation, or both. Use the inventory recipe below only for an inventory; use `archify` and its interactive-profile-explorers reference for an operational profile view. A capability list alone cannot supply permissions, identity, memory health, or workflow dependencies.
2. Keep one authored `capabilities.yaml`. Use `skills`, `plugins`, `mcps`, `external_tools`, and `automation` lists. Keep desired targets compact; use structured entries such as `name` and `detail` when a capability needs qualification. Keep secrets and copied runtime configuration out of the manifest.
3. Replace the old Markdown inventory rather than preserving two editable sources. Update README tables of contents, ordinary links, and wiki links. Include `.yaml` or `.html` in wiki targets after changing file type; extensionless links may still resolve only Markdown.
4. Generate an Archify explainer draft from every manifest section, including empty sections. Label the view as desired targets rather than live runtime state. Treat all manifest values as untrusted display data: validate types and duplicate keys, reject unsupported fields, and escape values before inserting them into Markdown tables or directives.
5. Reuse an existing documentation build entrypoint. If none fits, use one small owner-local renderer script and focused tests, not a new service or generic plugin framework. Use installed parsing dependencies and the native Archify CLI; inspect command help rather than guessing flags.
6. Finalize the generated explainer through Archify. Preserve its delivery metadata and verify the receipt against the actual HTML bytes. Keep candidates and build evidence separate from authored profile files. Do not hand-edit generated HTML after delivery; that disconnects the artifact from its source and provenance.
7. Provide a one-shot rebuild command. Add foreground change watching only when the agreed interaction requires automatic file regeneration. If watching is selected, watch content changes so atomic saves work. Preserve the last good HTML on malformed input and rebuild after corrected input. Require a finite positive polling interval to avoid a crash or busy loop.
8. Explain the dynamic contract precisely: an on-demand watcher rebuilds the file while running; a standalone HTML reader needs reload or reopening. State whether the watcher is running. File regeneration is not live browser push, and neither implies an installed scheduler. Add persistent jobs or browser-serving infrastructure only when explicitly requested.
9. Verify the path before reporting completion. Keep runtime application of targets out of a documentation build.

## Focused proof

Run the owning test command and `git diff --check`. Include these cases:

- Valid schema, wrong field types, missing sections, unknown fields, and duplicate YAML keys.
- All five sections appear, including empty lists.
- Delimiters, code fences, HTML-like text, and directive-like values cannot become executable markup or unintended renderer structure.
- A real manifest change changes both generated source and HTML through the actual Archify renderer.
- Malformed YAML preserves the last good artifact; corrected YAML rebuilds successfully.
- Renderer failure returns failure without claiming a fresh artifact.
- Watch iterations detect edits and recovery; invalid polling intervals are rejected before watching starts.
- Ordinary links, wiki targets, and table-of-contents entries point to the new files.

Put test fixtures under the configured managed scratch directory, derived from the environment or owning runtime convention. Never hardcode a machine-specific temporary-directory path; that makes a passing local test fail on the next machine or runtime.

Inspect the generated receipts and compare their artifact hashes with the delivered HTML. Distinguish static artifact checks, automated browser checks, and perceptual review. Explainer finalization alone may not run a browser.

## Handoff

Report the manifest path, HTML view, rebuild/watch command, actual test results, whether watching is active, and material limits. State that desired plugin, MCP, automation, or memory targets have not been applied unless a separately authorized runtime operation was actually verified.
