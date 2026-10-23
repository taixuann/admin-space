# Admin capabilities and documents: accepted planning inputs

Status: Planning scope accepted on 2026-10-23. No migration or runtime change
is authorized by this record. Review concrete migration choices before execution.

## Stages

1. Native OpenCode workflow: see the existing execution plan. Prove the manual
   workflow before scheduling automation.
2. Manage skills and plugins with a bounded Admin collection.
3. Align Admin identity, collaboration, ideas, architecture, and navigation.

Stages 2 and 3 are separate deliverables. They may be planned now; they do not
require enabling stage 1 automation.

## Capability management

Use global and admin as management categories. Admin may use capabilities from
other domains. These categories do not impose runtime discovery isolation.
Keep the current flat skill layout until a demonstrated consumer needs another
layout. Add skills/README.md for people and skills/AGENTS.md for maintainers.
Use the same entrypoint distinction for plugins when their maintenance needs it.

Inventory source paths, symlinks, maintained source, installed copies, and runtime
exposure separately. Record actual owners. Research and manuscript capabilities
should leave the Admin-managed collection and belong with the relevant domain.
A destination in Study or Knowledge is a candidate, not a verified path. Inspect
its entrypoint and consumers before selecting it. Preserve original source and
history. Removing an Admin symlink is distinct from deleting its target or
uninstalling a plugin. Admin can still consume domain capabilities explicitly.

Do not pick an arbitrary maximum skill count. Keep each retained capability
justified by an Admin responsibility or cross-Space use. Automation may later
report drift or update candidates; it does not silently install, delete, or
rewrite capabilities. No updater is implemented in these stages.

## Documents

SOUL.md owns Admin identity. USER.md owns confirmed collaboration preferences.
AGENTS.md owns operational instructions and context pointers. ARCHITECTURE.md
owns current components and ownership. README.md owns human navigation.
Proposed IDEA.md role: an explicitly non-operative idea backlog. Keep accepted
plans and policy in their owning files. Confirm this role before replacing its
existing agent-hub product concept; preserve that content in history or an
agreed archive.

Use writing-for-agents for every persistent instruction change. Keep all
maintained files in English. Preserve domain ownership and native memory stores.
Future intent, installed configuration, and verified runtime must remain distinct.

## Current evidence

Read on 2026-10-23: skills/README.md and skills/AGENTS.md are absent; the older
inventory lives in docs/skills/. Many research/manuscript entries are symlinks to
~/.oleafly/skills/. plugins/ contains maintained sources and snapshots; it has no
root README.md or AGENTS.md. IDEA.md currently describes an agent-hub product.
These are observations, not a complete consumer or installation audit.


## Accepted registry and candidate installation follow-up

Plan installation and qualification of netresearch/agent-rules-skill and the
Vercel skills CLI. Keep writing-for-agents as the writing method. Validate native
install metadata and local modifications before selective updates. Do not enroll
all existing directories into an updater by assumption.

Use skills/README.md and skills/AGENTS.md as management entrypoints, with
skills/index.yaml as the curated registry. Record management category separately
from authored/imported/forked/unknown provenance. Preserve native package locks.
Generate an Archify inventory map under skills/views/ from the registry and
observed source hashes. One explicit refresh command validates before replacing
the viewer. It preserves curated metadata and the previous viewer on failure.
Archify supplies rendering, not an automatic watcher. Scheduled refresh and
updates remain later automation work after manual verification.


## Accepted supporting documentation

docs/ supports root identity and operations with question-based navigation,
cross-Space routing, profiles, memory ownership, tool handoff and automation
placement. Keep current shallow references and add docs/memory.md. Keep proposed
specs/plans under docs/superpowers/. Detailed procedures stay with components.
No extra tutorial hierarchy or duplicate catalog is required.
