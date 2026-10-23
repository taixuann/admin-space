# Admin Skills and Plugins Management Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans after review. Steps use checkbox syntax.

**Goal:** Establish an explicit, bounded Admin capability collection and a safe domain handoff.

**Architecture:** Keep the flat layout. Classify global and admin capabilities for management, with domain-owned capabilities recorded separately. Reconcile source, installation, and runtime evidence before changing links or packages.

**Tech Stack:** Markdown, existing filesystem links, installed host/plugin management tools.

**Spec:** [Accepted planning inputs](../specs/2026-10-23-admin-capabilities-and-documents-design-input.md).

## Global Constraints

- Global and admin are management categories, not runtime isolation.
- Preserve source targets, history, unrelated edits, and working consumers.
- Use writing-for-agents for persistent instructions. Write maintained files in English.
- No automatic installation, deletion, scheduled updater, or plugin-cache editing.
- Confirm exact domain destinations and affected consumers before migration.

## Review Focus

- A symlink removal must preserve its target and dependent consumers (Task 2).
- A plugin snapshot must not be mistaken for maintained source (Task 1).
- A domain skill with Admin consumers needs a working handoff (Task 2).
- Inventory presence must not be reported as verified runtime discovery (Task 1).
- New component instructions must preserve more-specific instructions (Task 3).

### Task 1: Establish the current inventory and proposed disposition

**Files:** Create skills/index.yaml; modify docs/skills/README.md to link to the
new canonical index. Keep plugin inventory in plugins/README.md until a separate
structured consumer is demonstrated.
Read skills/, plugins/, managed-links/, and only the relevant host registrations.

**Interfaces:** Produce the reviewed skills/index.yaml contract defined below.
Use unknown or null when provenance is not verified. Keep plugin records distinct
from independently installed skills; do not count bundled copies as independent
updater targets.

- [ ] Inventory direct entries without modifying symlink targets. Distinguish
  maintained plugins from installed copies, snapshots, and backups.
- [ ] Classify each capability from its description and consumers. Keep ambiguous
  entries unresolved. Justify global/admin retention by actual responsibilities.
- [ ] Review one symlink, one maintained skill, and one plugin against their real
  paths and host references. Expected: distinct source/install/runtime facts.
- [ ] Present the handoff rows with exact destinations and consumer effects.
  Obtain review of those concrete choices before Task 2 mutates anything.

### Task 2: Hand off research and manuscript capabilities safely

**Files:** Only the links/source entries and references accepted in Task 1.
Record the exact paths and verification commands in this task before execution.
No destination is selected merely from a Space name.

**Interfaces:** Consume the accepted handoff rows; produce preserved source,
working destination entrypoints, consumer readbacks, and a rollback map.

- [ ] Inspect the selected destination's instructions. Record source hashes,
  link targets, dependent paths, rollback, and pre-existing dirty state.
- [ ] Adapt the accepted links or source ownership. Preserve the external target
  when removing an Admin symlink. Keep Admin access where a consumer needs it.
- [ ] Read back each changed path and consumer. Compare source hashes for
  unchanged content. Expected: no broken links or lost source. Verify runtime
  discovery separately when host exposure changed; report unavailable checks.
- [ ] Update inventory dispositions and the existing docs/skills/README.md links.
  Mark older generated skill diagrams as dated snapshots until regenerated.

### Task 3: Publish the maintenance entrypoints

**Files:** Create skills/README.md, skills/AGENTS.md, plugins/README.md,
plugins/AGENTS.md. Modify docs/README.md for links.

**Interfaces:** Consume the accepted inventory. README files link to that single
inventory; AGENTS files define bounded maintenance behavior, not domain methods.

- [ ] Use writing-for-agents. Document categories, owner/source checks, provenance,
  validation, rollback, and the distinction between updates and installation.
- [ ] Keep specialized instructions in each capability. Explain that global/admin
  labels do not change discovery. Keep pending automation a proposal.
- [ ] Follow all new local links. Read root and component instructions together.
  Expected: one inventory authority, no contradictory maintenance rules, no
  claims of installation or runtime success without evidence.
- [ ] Review only this deliverable's diff. Commit scoped files only under the
  owning repository's workflow; preserve unrelated work and do not push.

## Readiness and handoff

Task 1 is the discovery deliverable. Task 2 remains gated on exact destination
and consumer evidence; refine its file list before executing it. No skill moves,
plugin uninstalls, or runtime isolation are performed by writing this plan.

Self-review: requirements map to Tasks 1–5. Task 4 checks install scope and local
modifications. Task 5 checks generated-view freshness and preservation of curated
metadata. Concrete migration/install scope remains gated on inspected evidence.


## User clarification and scoped cleanup, 2026-10-23

The user explicitly allowed removal of research/manuscript symlinks because
domain workspaces already provide those capabilities. Removed 36 Admin symlinks
whose targets were under ~/.oleafly/skills/. Verified all target directories
remain. [Recovery manifest](evidence/2026-10-23-removed-research-symlinks.json)
records exact paths. This completes only that cleanup, not the full inventory
or plugin migration. Real directories and plugin-bundled skills were preserved.

The Admin bundle must cover document maintenance, skills/plugins lifecycle,
launchd support, cross-Space routing, and profile design including identity and
memory policy. Profile definition and runtime configuration remain distinct.
Evaluate installed capabilities first, then candidate additions. Do not treat
a new general skill as a replacement for each host's native plugin manager.

The Notion profile definition remains a draft. Use it as design evidence:
https://app.notion.com/p/4020a859ed1f813d8d5acc6d1676a247 .


## Accepted registry and viewer direction, 2026-10-23

skills/README.md is the human management entrypoint. skills/AGENTS.md owns the
maintenance procedure. skills/index.yaml is the single curated skill registry.
Do not create a second manually maintained management-inventory.md. The older
docs/skills/ inventory and diagrams become historical views or redirect to the
new entrypoint after their consumers are reconciled.

### Registry contract

Use schema_version: 1 and a skills list. Each entry has a unique stable id,
name, path relative to skills/, category (global, admin, domain, unresolved),
origin (authored, imported, forked, unknown), owner (string or null), source_url
(string or null), source_revision (string or null), installed_version (string or
null), local_changes (true, false, or null), update_manager (vercel-skills,
manual, host-plugin, none), and notes (string). Authorship must come from evidence,
not folder location. Forked denotes an imported source with maintained changes.
A version string alone is not a pinned source revision.

The index records curation and provenance. Scan output records observed paths,
hashes, symlink targets, and observation time. Keep these in separate generated
fields/artifacts so refresh cannot silently rewrite authorship, source or owner.
Unknown entries produce a review suggestion rather than guessed provenance.

### Task 4: Install and qualify the two selected candidates

**Files:** Create skills/installations.md for pinned install records and rollback.
The installed agent-rules package must occupy skills/agent-rules/ only after
confirming no existing owner. Vercel CLI installation and its lock state follow
the chosen package manager's native layout; record absolute paths in this file
before running install commands. Do not add a second custom installer.

**Interfaces:** agent-rules supplements writing-for-agents with repository checks.
Vercel skills CLI manages only entries with verified native install/lock metadata.
The Admin index does not replace or fabricate its native lockfile.

- [ ] Inspect current upstream packages and pin exact versions/revisions from
  https://github.com/netresearch/agent-rules-skill and
  https://github.com/vercel-labs/skills . Record licenses, required runtime versions,
  install scope, affected paths, package hooks, and rollback. Use the smallest
  supported local installation; no unrelated global config edits.
- [ ] Stage agent-rules and the CLI in a disposable scope. Inspect agent-rules'
  generator and default compatibility-link behavior before running it. Test on
  a fixture, preserving existing AGENTS.md and CLAUDE.md. It must not overwrite
  this workspace's curated instructions or create live hooks automatically.
- [ ] Verify CLI help/version and native list/check behavior against one fixture
  imported skill. Record the actual commands and output in installations.md.
  Test a locally edited import: preserve it and report the difference before any
  update. Unknown, authored and plugin-managed entries are not bulk-update targets.
- [ ] Install at the reviewed scope and read back paths, versions and discovery.
  Verify agent-rules in a fresh intended-host session. CLI availability does not
  prove skill discovery. Keep writing-for-agents as the instruction-writing method.
- [ ] Register the accepted installations in index.yaml. Document the manual
  check -> inspect diff -> update selected entry -> verify -> refresh procedure.
  No scheduled update or unattended bulk update is enabled by this task.

### Task 5: Generate a current skill map from the registry

**Files:** Create skills/scripts/refresh-index.mjs,
skills/tests/refresh-index.test.mjs, skills/views/observed.json,
skills/views/candidate.json, skills/views/skills.html. Modify skills/README.md
and skills/AGENTS.md with the single refresh procedure.

**Interfaces:** Manual command:
`node /Users/tai/.agents/skills/scripts/refresh-index.mjs --check` (read-only), or
`node /Users/tai/.agents/skills/scripts/refresh-index.mjs --write` (generate).
Inputs: index.yaml and direct skill entrypoints. Outputs: observed.json and an
Archify tree candidate grouped by management category and marked by origin.
The viewer depicts inventory and ownership, not runtime calls or a dashboard.

- [ ] Inspect existing inventory helpers and installed YAML parsers before adding
  logic. Reuse a supported parser; never hand-parse YAML. Record the selected
  parser dependency and exact invocation before implementing this task.
- [ ] Write fixture tests with Node's test runner. Assert duplicate ids and invalid
  paths fail; scan does not traverse symlink targets recursively; unknown origin
  remains unknown; authored/imported/forked metadata survives refresh; changed
  SKILL.md bytes make --check exit 1; identical inputs yield identical candidate
  bytes. Expected first run: failures for the unimplemented entrypoint.
- [ ] Implement the two explicit modes. --check writes nothing and exits 0 only
  when recorded input hashes and generated artifacts match; malformed input or
  drift exits nonzero with a specific reason. --write generates to staging,
  validates, and replaces outputs only after successful checks. Retain the prior
  delivered viewer on failure and report it as stale. Never edit index curation
  or skill source as a side effect of rendering.
- [ ] Run `node --test skills/tests/refresh-index.test.mjs`. Expected: all fixture
  assertions pass. Test malformed YAML and missing/broken entrypoints too.
- [ ] Use archify's tree authoring references and native finalize pipeline. Feed
  candidate.json to the installed Archify CLI with absolute paths and working
  directory fixed to /Users/tai/.agents. Validate and browser-check the delivered
  viewer. Record index/source hashes and generated-at time in observed.json.
  A registry group edge means membership, not an execution dependency.
- [ ] Make --write invoke generation and Archify finalization as one refresh
  operation. Treat any failed gate as refresh failure, never publish it as current.
  Run --write followed by --check. Expected: exit 0 and a matching viewer receipt.
- [ ] Require refresh after accepted add/remove/update/reclassification in
  skills/AGENTS.md. Link skills/views/skills.html from skills/README.md. Read back
  representative authored, imported, forked/unknown entries against their sources.

Archify does not watch index.yaml or regenerate automatically by itself. This
stage provides a manual refresh command and a maintenance rule. Future automation
can call the same proven command after the workflow is stable. It may check for
updates separately; rendering must not fetch or install packages.

### Added review findings

Resolved competing inventory locations by choosing skills/index.yaml. Separated
curated provenance from observed hashes and Vercel's own lock metadata. Kept
locally modified imports outside blind update flows. The exact package pins,
install scope and YAML parser require discovery before Tasks 4–5 execute.
No packages, registry script, or viewer are installed/generated by this plan edit.
