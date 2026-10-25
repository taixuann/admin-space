# Profile documentation instructions

Scope: `docs/profiles/` and its profile subdirectories. Follow the repository's root AGENTS.md and the user's authorized scope.

## Read first

Read `README.md` here, then the selected profile's `README.md` and `capabilities.yaml`. Read `../README.md` for roles and flow and `../AGENTS.md` before changing execution guidance. Use `writing-for-agents` for instruction changes and `archify` for profile maps.

## Profile documents

Create a proposed profile definition in `docs/profiles/<name>/` before runtime setup. Use three main README sections: profile identity and context, capabilities, workflows. Under identity and context, include model selection and rationale, path-based working permissions, and memory setup. Keep intended model/reasoning choices and memory targets separate from saved settings and tested behavior. Keep links within the relevant section and use standard Markdown. Apply this contract when a profile is revised; do not rewrite unrelated profiles during a Secretary-only task.

For a documentation-first review, write only the agreed definition files and mark them as a draft. Do not create a runtime, configure its model or memory, or claim sandbox enforcement before the definition and deployment scope are approved. A new proposed SOUL is a draft identity, not a snapshot of an existing runtime.

Keep one entrypoint in `<profile>/README.md`. Put the approved target capability set in `<profile>/capabilities.yaml`. Keep identity provenance beside a requested SOUL.md copy. Documentation folders are not runtime homes.

The README explains role, authority, working directories, memory, and collaboration. The YAML lists skills, plugins, MCPs, external tools, and automation. It describes desired capabilities, not proof that a connection or plugin works. Refer to the native runtime configuration for actual loading.

## Archify profile map

For a full profile map, produce `<profile>/profile.html` as a native Archify diagram unless the profile has an approved workflow-led package below. Start with the profile as the focal node. Branch into:

- Memory: provider, intended bank, information retained, and retrieval limits.
- Capabilities: skills, plugins, MCPs, external tools, and automation from the YAML.
- Work and execution: how the profile uses its capabilities and workers to complete its responsibilities.
- Workspace access and permissions: allowed work, read-only boundaries, approval gates, and human authority.

Show why a capability is used, not only its name. Show Secretary and OpenCode as Admin-local workers. Show Coordinator as the cross-Space communication role. Keep each receiving Space's domain authority intact.

Use Architecture for interactions and boundaries. Use Tree for a profile-centered decomposition; state that branches are responsibilities, not runtime calls. Use other native modes only when the requested behavior requires them. A table-only explainer is not the profile map.

Read the selected Archify schema, example, and authoring defaults. Keep candidate source and validation receipts together under an explicit `.archify/` directory. Run the full native `finalize` command and check its actual result. Distinguish automated browser checks from perceptual visual review.

Use the profile README, current user decisions, capability YAML, and owning instructions together. YAML alone cannot establish memory health, permissions, or work flow. Mark targets, observed configuration, and verified behavior separately. For an uninspected profile, show agreed responsibilities and label runtime details unknown.

The earlier `capabilities.html` files are inventory views, not the requested profile architecture. Preserve them and their evidence unless removal is authorized. The existing inventory renderer is not the default profile-map workflow. Do not start a watcher, server, or scheduled rebuild merely to author a map.

## Secretary workflow-led package

Keep four visible Secretary files: `README.md`, `SOUL.md`, `capabilities.yaml`, and `secretary-workflow.html`. Keep the hidden `.archify` relative symlink to root `.archify/secretary/`. The public workflow may be a relative symlink to its self-contained HTML in that bundle. Keep its candidate, build instructions and receipts under `workflow/`. It must render as one native diagram without frames or adjacent HTML dependencies.

Show one profile-management flow for Secretary itself or another profile, with create, update, maintain and delete as operations. Separate receiving/supervision, methods/policy, Executor preparation, authorized application and verification. Coordinator is optional information support. Executor remains proposed until deployed and isolation-tested. Planning and skill writing support the flow rather than create more work types. Model choices remain task/runtime-driven.

Preserve the retired explorer at `.archify/secretary/native/profile-legacy.html`. Its old builder and mapping under `scripts/` are legacy support, not the current workflow generator. Legacy rebuilds must stay in the hidden archive and must not recreate public `profile.html`. Keep compatibility links and historical receipts intact. Rebuilding the current workflow must leave only the four visible profile files and the hidden bundle link.

`capabilities.yaml` owns approved capability targets. Future automated discovery must record observations separately; it must not silently overwrite approved choices or enable capabilities. Do not install a refresh job or watcher from a future automation preference.

Run native Archify finalize after moving or rebuilding a workflow at a new canonical path. Preserve prior artifact evidence as history; old receipts do not certify new bytes or paths. Keep self-adaptation bounded by evidence and authorization, not self-granted permissions or silent configuration changes.

## Links and verification

Keep `ecosystem.html` as the single visible ecosystem artifact in this directory. Group its candidate sources, build support, and receipts under `.archify/ecosystem/`. Preserve historical evidence and distinguish the existing diagram from proposed roles that have not been drawn or deployed yet.

Link the native profile map from its README and the profile index. Keep portable Markdown links and requested wiki links. Wiki paths assume `~/.agents` as the root; include file extensions for YAML and HTML.

After edits, check changed link targets, map checks, and requested contents. Preserve unrelated edits, historical evidence, and exact identity copies. Do not change a runtime home, permissions, memory wiring, plugins, or another bot's identity through a documentation edit.

This file governs documentation maintenance. Its presence is not proof that every runtime automatically loads nested AGENTS.md files. Ensure a task or parent instruction points workers here before relying on it.
