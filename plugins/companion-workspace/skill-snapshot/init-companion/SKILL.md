---
name: init-companion
description: Orient Companion in a local workspace or selected folder before choosing a workflow. Use when the user asks to initialize Companion, understand folder rules, or resolve which instructions and workflow apply. Read applicable AGENTS.md files and folder entrances, then carry the selected scope into the owning workflow.
---

# Init Companion

Establish the working context. Initialization reads guidance and selects the next workflow. It creates no files or management records.

## Resolve the target

Use the workspace and path named by the user. Otherwise, use the current workspace and the stated task. Ask only when different possible targets would change the applicable rules.

For work across connected workspaces, read `$CODEX_HOME/ENVIRONMENT.md` when present. Treat its paths as discovery hints. Confirm the selected workspace and its owner before following a link or symlink outside the current workspace.

Finish this step with one resolved workspace, target path, and requested action. Keep explicit exclusions, such as assets, in scope throughout the handoff.

## Read the applicable guidance

Follow the host's instruction discovery and precedence rules. Reuse instructions already loaded in the conversation when they are current. Read applicable ancestor instructions and the workspace entrypoint. Then check each directory along the selected path for scoped `AGENTS.md` and host-supported overrides. Before descending into a child, read its applicable instructions. Read sibling instructions only if the task expands into that sibling.

Read the workspace README and storage schema when present. Read the selected collection's entrance according to its own guidance. For local document work, follow [Document Companion](../document-companion/SKILL.md) for README scope. Inspect immediate entry names when an entrance is missing. Report the gap without creating a replacement or inferring that the folder is empty.

Finish this step when the instruction chain for the selected path is accounted for. Distinguish accepted rules, proposed arrangements, current files, and unresolved conflicts. If a conflict prevents the requested action, explain the affected part and ask only for the decision needed to continue.

## Hand off the task

Choose the workflow that owns the requested action:

| Request | Workflow |
| --- | --- |
| Local document placement, naming, collection guidance, or file maintenance | [Document Companion](../document-companion/SKILL.md) |
| Project decisions, workload, or information placement in Notion | [Ask Companion](../ask-companion/SKILL.md) |
| Project-wide Notion Notes and Resources organization | [Organize Companion](../organize-companion/SKILL.md) |
| Concrete Notion change proposal | [Plan Companion](../plan-companion/SKILL.md) |
| Explicitly requested Notion changes | [Apply Companion](../apply-companion/SKILL.md) |
| Requested project update or evidence capture | [Capture Companion](../capture-companion/SKILL.md) |
| Weekly outcomes and next week's selection | [Weekly Review Companion](../weekly-review-companion/SKILL.md) |

Read the selected workflow and continue in the same conversation. Carry forward the target, sources read, applicable rules, exclusions, existing authorization, and material gaps. For mixed requests, give each action its owning workflow. Local-only work needs no Notion connection.

Keep the handoff short. State the target, the rules that change how the task proceeds, and the next action. If the user asked only for orientation, stop there. If the user already requested a concrete action, preserve that authorization and continue under the owning workflow. Initialization alone supplies no permission to move files, rewrite instructions, or change Notion.
