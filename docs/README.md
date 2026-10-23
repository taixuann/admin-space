# Admin documentation

Use these views to explore Admin. The operating contract stays in the root documents.

| View | Question | Scope |
| --- | --- | --- |
| [Memory relationships](memory/memory.html) | How do shared and native memories relate? | Conceptual configuration view |
| [Skill groups](skills/skills.html) | Which local skills serve each purpose? | 61 direct local skills, grouped for navigation |
| [Skill inventory and handoffs](skills/README.md) | Where is each source, and how can skills work together? | Source links and proposed combinations |

Open the HTML views in a browser. Expand skill groups to inspect their members. Use the viewer controls to explore the diagram.

## Operating reference

For Admin maintenance and workflow selection, read [Admin workflows](admin-workflows.md). This reference complements the root instructions; the interactive views above remain snapshots.

| Reference | Question |
| --- | --- |
| [Admin workflows](admin-workflows.md) | Which method owns this request, and which profile is in effect? |
| [Admin Architect & Planning profile](profiles/admin-architect-planning.md) | What does the draft planning profile cover, and what is still open? |
| [Admin tool handoff](tools.md) | Where does tool source live, and how is a tool task handed off? |
| [Automation](automation.md) | Does this job belong to a tool or to Admin, and where do reports go? |

## Coverage and maintenance

Snapshot date: 2026-10-22. Skill grouping is editorial. Membership edges do not represent calls or dependencies.
Plugin-bundled skills and skills stored only in other hosts are outside this inventory.
Memory arrows describe configured relationships, not a recorded cross-host execution test.

Each view keeps its candidate JSON beside the generated HTML. Skill inventory.json records the inspected file hashes.
When the owning source changes, update the relevant candidate and run Archify finalize again.
Generated pages are snapshots. There is no automatic refresh or scheduler in this documentation change.

For identity and operating guidance, start with [the workspace README](../README.md).
For ownership and component responsibilities, read [ARCHITECTURE.md](../ARCHITECTURE.md).

## Next views

Add a skill interaction diagram when a concrete workflow establishes the actual handoffs.
Add automation and plugin views after tracing their current entrypoints and runtime references.
Keep source evidence separate from proposed relationships.

## Live memory

Open [the native Hindsight explorer](../tools/hindsight/README.md) to inspect current bank state.
The memory diagram describes the model and client integration boundary.
