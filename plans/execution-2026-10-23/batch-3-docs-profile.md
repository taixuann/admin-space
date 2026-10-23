# Batch 3: documentation and planning profile

Request: 010 (with the 008/009 boundaries). Executed 2026-10-23.

## Result

| Artifact | Purpose | State |
| --- | --- | --- |
| `docs/tools.md` | Tool index, independent-repository rule, worktree and branch contract, return fields, report root | Written; replaces `tools/README.md` |
| `docs/automation.md` | Owner classification, source placement, report root, current jobs, runtime limits | Rewritten |
| `docs/admin-workflows.md` | Routing table, profile separation, known capability gaps, plan-version warning | Written |
| `docs/profiles/admin-architect-planning.md` | Draft profile: responsibilities, operating sequence, method selection, handoff, open decisions | Draft only |
| `docs/README.md` | Documentation index updated | Updated |
| `ARCHITECTURE.md` | Tools and automation boundary section | Updated |

## Supersession recorded

The user's 2026-10-23 direction supersedes the Improve rewrite in request 010:

- `improve` is unchanged and remains installed.
- No replacement Admin skill was written.
- The profile is a draft definition, not a runtime configuration.
- `plans/010-admin-workflow-draft/` remains a design input.
- `plans/008-skill-adaptation/candidate/improve/` remains a record and is not
  installed.

## Report-root convention

`docs/automation.md` and `docs/tools.md` now state that `<stable-job-name>` is a
runtime name, not always the source folder name. A Space-owned job uses
`<source-folder>-runtime` so the report root stays outside its source. A
tool-owned job may use the job name. Admin `.gitignore` gained
`/automation/*-runtime/` in addition to the model-refresh entry.

## Capability gaps inspected

Resolved against the host skill catalog:

- `cli-developer` is not installed.
- `agent-rules` is not installed.
- The `agent-skills` phase skills named in earlier routing text are not
  installed.

The profile names `cli-developer` as a method and marks it unavailable. No
installation was attempted.

## Checks

- Every new document is in English.
- Links added from `docs/README.md` and `ARCHITECTURE.md` point at files that
  exist.
- `improve` was not edited: `git diff --exit-code skills/improve` at the time of
  this batch returned no change.
- No plugin was created.

## Not done

- No host loads the profile.
- No skill was installed from the profile's method list.
- The final profile name, runtime format, ticket trigger, and review threshold
  remain open.
