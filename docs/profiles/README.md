# Admin profiles

Owner: Tai.
Last reviewed: 2026-10-25.

Admin Space is the shared workspace. Profiles are participants with distinct responsibilities, not separate copies of the workspace rules.

Read [profile documentation instructions](AGENTS.md) before maintaining a profile. Open [Secretary's management workflow](secretary/secretary-workflow.html) for the shared self/other-profile process, with identity, memory and capability details in its README.

## Profiles

Open the [ecosystem map](ecosystem.html) for the existing Admin and Development role agreement. It predates the Executor draft and is not proof of operational routing or enforced isolation. The [hidden ecosystem bundle](.archify/ecosystem/README.md) holds its source and archived receipts. `ecosystem.html` is the only visible ecosystem artifact.

| Profile | Responsibility | Entry point | Capabilities |
| --- | --- | --- | --- |
| Secretary | Manage profiles, including itself; supervise scoped work, verify and report | [Secretary](secretary/README.md) | [SOUL](secretary/SOUL.md) · [Workflow](secretary/secretary-workflow.html) |
| Coordinator (Asura) | Communicate scoped handoffs with bots in other Spaces and return evidence pointers | [Coordinator](coordinator/README.md) | [HTML view](coordinator/capabilities.html) |
| Executor | Run plans sent by any authorized profile through kanban on a task branch in the owning Space; run OpenCode for code; report, then merge on Tai's approval | [Executor](executor/README.md) | [SOUL](executor/SOUL.md) · [Workflow](executor/executor-workflow.html) |
| Forge | Own Development Space: turn tool-repo issues into plans, dispatch to Executor via kanban, review, merge | [Forge](forge/README.md) | [SOUL](forge/SOUL.md) · [Workflow](forge/forge-workflow.html) |
| Supervisor (draft) | Academic Space principal investigator: ideation, literature, planning, evidence evaluation, RO-Crate packaging | [Supervisor](supervisor/README.md) | [SOUL](supervisor/SOUL.md) |
| Writer (draft) | Academic Space scientific author: manuscripts, reports, slides from sealed runs | [Writer](writer/README.md) | [SOUL](writer/SOUL.md) |

Tai retains final authority. Secretary writes plans and verifies results; Coordinator handles cross-Space communication. Executor (profile `executor`) runs plans from any authorized profile in the owning Space and reports back. Its model is runtime-managed. See [Admin Space roles and flow](../README.md) and [docs instructions](../AGENTS.md).

## Folder contract

Each profile has one entrypoint:

- `README.md`: responsibility, authority, directories, runtime and memory relationships, and navigation.
- Capabilities (skills, plugins, MCPs) are described in the README with the reason for each; the runtime configuration is the source of truth. `hermes-fleet-admin` Verify reads the runtime and reports drift from the README.
- `secretary-workflow.html`: Secretary's self-contained management workflow; the retired `profile.html` is archived in its hidden bundle. Other profiles' existing views remain unchanged.
- Secretary has four visible files and a hidden `.archify` symlink to the single root `.archify/secretary/` build bundle. Scripts, mapping, native diagrams, sources, and evidence are grouped there. See [the bundle](secretary/.archify/README.md). Other profiles are unchanged by this consolidation.
- Per-profile `capabilities.yaml` manifests were retired on 2026-10-25 (copies in `~/.agents/backups/profile-simplify-*`); they are not restored.
- `SOUL.md`: identity source or snapshot only when inspected and explicitly authorized. Explain provenance in the profile README.

These folders are documentation, not runtime homes. Keep credentials, sessions, and mutable runtime stores outside them. Do not create placeholder identity files for uninspected profiles.

## Document-first profile lifecycle

1. Define a proposed profile under `docs/profiles/<name>/` before runtime setup. Write its README, SOUL, and workflow together. Use three main README sections: identity/context (including model rationale, permissions and memory), capabilities, workflows.
2. Obtain Tai's approval of the definition, model, per-task scope, and execution boundary. A desired model or capability is not an applied setting.
3. Configure the approved profile through the supported Hermes tools. Keep runtime state separate from the maintained definition. Verify saved settings, identity loading, and a real model response.
4. For execution roles, verify the write boundary they rely on (Executor: work on the plan's task branch in the owning Space, no overwrite of uncommitted work, Tai approval for merge). Update the ecosystem and profile view from the accepted definition, with sources and evidence in hidden bundles.

Executor's runtime profile is created; see its [runtime status](executor/README.md#runtime-status). The existing `hermes-fleet-admin` skill supplies the phased lifecycle; no parallel provisioning skill is required.

## Profile maps

Use `archify` and follow [AGENTS.md](AGENTS.md). Rebuild the profile map when its role, memory targets, capabilities, or permissions change. Validate the native diagram through Archify finalize. No automatic profile-map watcher is configured.

Navigation: [Profile maintenance rules](AGENTS.md) · [Secretary workflow](secretary/secretary-workflow.html).

## Earlier inventory renderer

The legacy renderer lives in `.archify/secretary/scripts/` and is not part of the current workflow.

The watcher is a foreground process. Stop it with Ctrl-C. It does not install a scheduler or server. After a rebuild, reopen or reload the HTML file; there is no live browser push. Invalid YAML or a failed render leaves the last successful HTML unchanged.

Capability status distinguishes role selection, installation, configuration, and actual working evidence. A listed skill or plugin does not grant execution authority. Shared procedures remain with their owning skill or runbook.

## Wiki navigation

[[docs/README|Admin Space]] · [[docs/profiles/secretary/README|Secretary]] · [[docs/profiles/coordinator/README|Coordinator]]

Wiki paths assume `~/.agents` as the wiki root. Portable Markdown links above support readers without wiki-link rendering.
