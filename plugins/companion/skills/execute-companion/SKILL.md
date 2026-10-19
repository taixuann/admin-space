---
name: execute-companion
description: Apply an exact authorized change to an existing Notion, Linear, GitHub or Google Calendar record and verify it. Use when the target and requested change are clear; refresh current state, preserve unrelated content, and stop only the affected part when identity or authorization is unresolved.
---

# Execute Companion

Read [shared operations](../../shared/references.md#shared-operations), [authorization and verification](../../shared/references.md#authorization-and-verification), and the relevant source section under [domain guidance](../../shared/references.md#domain-guidance).

Resolve the exact target by canonical ID or verified identity. Refresh its current state, required fields, relations and material effects immediately before writing. If identity, scope or authorization is unresolved, do not write; ask one focused question naming the missing target or decision rather than giving only a refusal. Confirm that the requested action is authorized and its scope is bounded. A direct, fully specified write request supplies authorization for that change; do not seek a second approval. A recommendation, idea approval or unrelated capture does not authorize additional effects.

Apply only the requested change. Preserve identity, history and all unrelated properties or content. For structural changes, inspect old and new owners, linked records and dependencies. Use native tools already available and discover their current parameters; do not invent connectors or issue types.

After each write, re-read the target and verify the requested effect and preserved fields. If interrupted or a call fails, inspect current state before retrying and repeat only missing effects. For multi-target work, report each target separately as changed, unchanged, failed or unresolved. Continue safe independent work when one target is blocked.

Do not claim that a proposed call executed. Report the source, exact verified change, readback evidence, remaining effects and any partial coverage. Do not infer completion or propagate statuses to related records.
