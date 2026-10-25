# Admin operating instructions

These instructions govern work inside `~/.agents`. Follow more specific component instructions for the files you change.
Use the active profile's identity and collaboration preferences. Admin Space provides shared operating rules, not a separate agent identity. Component maintenance does not assign the maintainer's identity to its users.

## Start

1. Identify the requested outcome and the component that owns it.
2. Read that component's instructions and inspect the relevant current state.
3. For roles, flow, and component placement, read [docs/README.md](docs/README.md).
4. For planning, execution, records, memory, or workflow selection, read [docs/AGENTS.md](docs/AGENTS.md). For tools or automation, read `tools/AGENTS.md` or `automation/AGENTS.md`.

Keep the root guidance in `AGENTS.md`, `CLAUDE.md`, and `README.md`. Keep identity and collaboration preferences with the active profile. Keep component explanations and runbooks under their owning directories.

## Execute

Use the installed skill or native tool that owns the task.
For each AGENTS.md, CLAUDE.md, or skill instruction change, use writing-for-agents.
Keep specialized workflow rules in their owning skill or component documentation.
Keep ordinary discussion read-only.
For authorized changes, state material assumptions and complete the bounded work.
Preserve unrelated edits, running jobs, existing links, and raw evidence.
Use the owning project's Git workflow when repository changes require it.
Keep credentials and runtime stores outside tracked source files.

For skills and plugins, distinguish maintained source, installed copy, and runtime behavior.
For automation, inspect its trigger, runner, configuration, side effects, and recovery path before changing it.
Use existing tool entrypoints before adding wrappers or moving source.

## Memory and sources

Use the configured Hindsight tools for prior Admin decisions and lessons when they affect the task.
Check retrieved claims against the current owning source before acting.
Follow the memory integration's capture rules and attribution requirements.
Keep operating policy in these documents and process history in its owning ticket.
Keep native Codex and Claude memory under their own management.

When a task belongs to another Space, inspect its entrypoint and act within the user's authorized scope.
Keep scientific methods, raw data, and acceptance decisions with the research owner.

## Verify and finish

Check every changed reference and the behavior affected by the change.
For persistent instructions, check loading paths, hierarchy, duplication, and conflicting guidance.
For installations or automation, separate configuration checks from a real runtime result.
Report what changed, what was verified, and what remains uncertain.
