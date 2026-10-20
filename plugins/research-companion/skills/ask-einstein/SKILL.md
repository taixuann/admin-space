---
name: ask-einstein
description: Consult and route a scientific research request to its owning workflow. Use when the requested action, evidence boundary, or next owner is unclear; status-only discussion is read-only.
---

<SUBAGENT-STOP>
If you were dispatched as a bounded subagent to execute an approved task, follow your prompt's explicit boundary.
</SUBAGENT-STOP>

Use this skill for consultation and routing; it is not a mandatory preamble for
every scientific response or action.

## The Rule

Identify the requested action and its owner before making a write. Use the
shared [owner and handoff contract](../../references/transitions.md). Ask
Einstein reads selected context and advises; it does not write Study or
Research Progress state. A direct request authorizes only that action.

---

## Route by requested action

The request can involve Study evidence or project progression. Their owners
are separate; use the matrix below and the shared contract for the exact handoff.

| Intent | Owner | Route |
|---|---|---|
| Discuss status or a settled question | Ask Einstein | Read selected context and advise; no writes |
| Explore an open direction | Brainstorming | Generate candidates; scientist selects |
| Plan a new plan-led analysis | Plan Research | Create its spec and proposal |
| Change an existing Study leaf | Study | Use the matching Study action; no automatic migration |
| Implement or execute selected plan-led work | Implement Research | Follow exact authorized scope |
| Materialize selected evidence | Compose Research | Validate explicit decisions and bindings |
| Archive selected evidence | RO-Crate Research | Package selected verified scope |
| Update project progression or prepare slides | Research Progress | Own the write and delegate slide building |

---

## Boundaries to preserve

These thoughts mean STOP — you are rationalizing undisciplined action:

| Request | Route |
| :--- | :--- |
| Status-only question | Read selected records and answer; do not write a log or goal. |
| Explicit progression update | Route to Research Progress, which owns the write. |
| Fixed descriptive request | Preserve its settled scope; do not require broad ideation. |
| Open mechanism or direction | Use Brainstorming; return candidates for scientist selection. |
| Existing Study leaf | Route to Study's matching action; no automatic migration. |

---

## Shared Authority

All skills in this companion follow [shared context](../../references/README.md) and the [owner contract](../../references/transitions.md):
- Invariant: Raw instrument evidence is immutable.
- Invariant: A completed run is process success, not scientific acceptance (`NOT_ASSESSED`).
- Invariant: Research Progress owns project progression and presentation planning.
