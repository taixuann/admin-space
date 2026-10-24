# Admin architecture

Status: First working edition, 2026-10-22.

## Responsibility

Admin maintains its own agent environment and coordinates work across Spaces.
Research, Study, Development, and Personal retain their domain resources and decisions.

## Components

| Component | Responsibility | Owning location |
| --- | --- | --- |
| Identity | Mission and conduct | `SOUL.md` |
| Collaboration | Confirmed user preferences | `USER.md` |
| Operations | Task handling and verification | `AGENTS.md` |
| Capabilities | Reusable instructions and plugin sources | `skills/`, `plugins/` |
| Automation | Triggers, runners, and component assets | `automation/` |
| Memory | Recall across Admin sessions | Hindsight bank `admin` and existing native stores |
| Management | Intent, decisions, and process history | Notion Admin Home and Agents Ticket |

`README.md` is the human entrypoint. Codex discovers `AGENTS.md` in this workspace.
`CLAUDE.md` imports that same file for Claude. Its start instructions point to identity and collaboration files.
Confirm actual loading in a fresh session before claiming both runners follow the documents.

## Memory

Hindsight bank `admin` is the shared Admin memory service. Admin sessions are independent of the client app.
Codex, Claude, and Antigravity are the primary intended clients. Other clients can join through an explicit integration.
The mapping for `/Users/tai/.agents` is configured. Codex and Claude wiring is verified. Other client wiring remains unverified.
The existing local daemon hosts the backend. The current extraction profile selects `claude-code` with `gemini-3.8-flash`.
Backend logs report authentication and model-recognition failures. See [diagnosis](tools/hindsight/DIAGNOSIS.md).

Native app memory remains separate. `memories/` exposes the existing locations and shared folder.
The shared folder is not an automatic export or synchronization target for Hindsight.
Hindsight is a recall layer. Current configuration and accepted instructions remain with their owning sources.

## Tools and automation

A tool is a callable capability. An automation chooses when and how to call
capabilities. A component can provide both without requiring duplicate source
trees.

The canonical home for internal tool repositories has transitioned to **Development Space**
at `~/development-space/tools/<space>/<tool-name>/`. Development Space acts as the central
software platform and workshop: it owns tool lifecycles, ephemeral task worktrees (`worktrees/`),
engineering discipline (TDD, Superpowers, Codebase Design), and tool distribution via CLI binaries
packaged into `~/.local/bin`. Admin Space owns no product source code and consumes tools as a client.
The global ecosystem roles and boundaries are defined in `space.yaml`.

Automation source follows its owner. A job dedicated to one tool lives inside
that tool repository. A job that coordinates several tools or applies Space
policy lives under Admin `automation/<job-name>/`. Runtime reports for both kinds
go to an explicit absolute `automation/<stable-job-name>/logs/` root, outside the
source folder. [docs/automation.md](docs/automation.md) owns the placement rules.

The workspace currently contains `automation/bridge/`, `automation/model-control/`,
and `automation/track-automation/`. Read their current entrypoints before use.
Tai reports that the existing automation is running. This document does not
independently establish scheduler health.

Bridge provides synchronization capabilities. Model Control runs the existing
daily model check and selection job. The OpenCode tool, indexed in
[docs/tools.md](docs/tools.md), owns model discovery, daily state, and
default-model updates; a replacement job is implemented in that repository but
its schedule is not installed. Compatibility links preserve older spec consumers.

Skill and plugin maintenance is the next automation design area.
Define the selected component, update source, verification, and recovery before enabling new update behavior.

## Information flow

The user or an authorized trigger supplies an intent.
Admin reads the owning instructions, relevant live state, and prior memory when needed.
The owning tool or runtime executes authorized work.
Verification checks the actual effect. The result links to the canonical artifact and relevant evidence.
Significant decisions stay in the owning ticket. The configured memory integration retains eligible experience.

## Documentation and diagrams

Notion provides the design context. Local documents provide the working Admin contract.
There is no automatic bidirectional sync. Keep source links when reconciling an agreed change.

Use the installed Archify skill when a component map or workflow diagram helps explain a concrete change.
Keep diagram source and generated output together. Link the diagram here after its validation passes.
A diagram illustrates the architecture. Runtime checks establish whether the system operates as described.

## References

- [Admin Home](https://www.notion.so/4010a859ed1f81789613e07d67b7880e)
- [Profiles and Identity](https://www.notion.so/4010a859ed1f81fca95ac3306159a90b)
- [Workflows and Architecture](https://www.notion.so/4010a859ed1f81febd84d9f5e90827b6)
- [Automations and Runtime](https://www.notion.so/4010a859ed1f81f4b926c83e06bbb78d)

## Interactive views

[Admin documentation](docs/README.md) links the memory relationship map and local skill groups.
These are dated snapshots. Skill membership does not establish runtime calls.

## Memory explorer

Open [Hindsight](tools/hindsight/README.md) for the native Control Plane and bank `admin`.
