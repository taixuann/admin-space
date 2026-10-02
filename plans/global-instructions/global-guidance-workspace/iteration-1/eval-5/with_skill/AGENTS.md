# OpenCode global guidance

Follow the current task and the most specific project instructions. Keep changes within the requested scope and use the smallest applicable workflow.

## Code discovery and construction

- If a repository has a `.codegraph/` directory at its root, use the available CodeGraph MCP or CLI before grep/find or reading files to understand or locate code. If no index exists, continue with ordinary tools; do not create one unless asked.
- Before writing, modifying, or refactoring code, invoke the `aqg-code-construction` skill when available and follow it, including its audit-before-commit gate. For audit depth, use its authoritative sensitivity list: blast radius outranks size, while trivial non-sensitive changes need no audit when a direct check fully settles them. Follow other AQG skills when their triggers apply.
- If the AQG skill or its sensitivity list is unavailable, follow the owning project's engineering workflow; do not assume AQG hooks ran.
- When delegating to a fresh worker, include the applicable scope, project checks, and AQG requirements; do not assume it inherited this context.

## Scientific work

Keep raw evidence immutable and distinct from derived outputs. Preserve traceability to selected inputs, transformations, methods/settings, and relevant software versions. Do not invent missing measurements, metadata, citations, or method choices. Separate observations, interpretation, uncertainty, and scientific acceptance. Passing code tests does not establish scientific validity; follow the owning project's data, method, and acceptance gates.

## Authorized execution briefs

When given an authorized implementation brief, follow its scope and ordered steps. Use the target project's declared inputs and verification commands. Report changed paths, checks and results, deviations, missing information, and partial work. Do not broaden scope, publish, commit, or claim scientific acceptance unless both the brief and the governing project explicitly authorize that action. Do not change scientific methods, data selections, or exclusions. Stop at a named checkpoint or a material blocker. Give the parent a concrete request to relay to the user.

When user action blocks progress or a real decision boundary has arrived, end with a short **What I need from you** section. Number concrete actions, say where to act and what to return, put the most blocking item first, and state what independent work can continue. Do not add an empty or repeated footer when no action is needed.
