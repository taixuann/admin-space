# Admin tool handoff

Each tool is an independent Git repository at
`/Users/tai/.agents/tools/<tool-name>/` with a stable checkout. The Admin
repository ignores the whole `tools/` subtree. Development Space hosts linked
worktrees for development. Scheduled jobs call the stable checkout, not a
temporary worktree.

## Tool inventory

| Tool | Purpose | Repository | Branch |
| --- | --- | --- | --- |
| [Hindsight](../tools/hindsight/README.md) | Open the native memory explorer and inspect bank `admin` | `tools/hindsight/` | `main` |
| [OpenCode Free Router](../tools/opencode-free-router/README.md) | Check models, maintain the dated catalog, set the native OpenCode default | `tools/opencode-free-router/` | `main` |

The links in this table do not resolve through the Admin repository because the
subtree is ignored. Read them from the filesystem. Each tool's own `README.md` is
its runbook. Each tool's `PROVENANCE.md` records the Admin revision it was
extracted from.

## Prepare the handoff

For a tool request from Admin, record the following in the existing request or
its derived implementation plan:

- Request ID and absolute plan path.
- Tool name and canonical repository path.
- Exact base commit and recorded dirty state.
- Branch and worktree path.
- Requested outcome, mutable scope, and files outside scope.
- Tool `AGENTS.md` and required engineering skills, including `cli-developer`
  when the command-line surface changes.
- Verification commands, expected results, and return evidence.
- Integration boundary and rollback for any runtime change.

Use `writing-for-agents` for every `AGENTS.md` creation or edit. Keep the request
in the existing plan instead of creating another tracking system. A prepared
handoff does not dispatch an agent, create a worktree, or authorize integration
by itself.

## Branch and worktree

For work sent by Admin, use this branch in the tool repository:

`admin/<tool-name>_<request-id>`

The request ID is the Admin request reference, not the final implementation plan
number. Run the full design, implementation planning, execution, review, and
verification workflow from the request, with links back to it. This page does not
bypass design approval or authorize immediate execution. Keep leading zeros.

| Field | Example for request 008 |
| --- | --- |
| Repository | `/Users/tai/.agents/tools/opencode-free-router` |
| Branch | `admin/opencode-free-router_008` |
| Worktree | `/Users/tai/development-space/worktrees/admin/opencode-free-router_008` |

The branch is a Git reference. The worktree path is a directory. The shared
suffix keeps the handoff traceable. Development Space Git ignores worktrees.

Before creation, verify that the tool is an independent repository, the base
exists, and the target path and branch do not conflict. Reuse an existing
matching task worktree when its identity and state are verified. Preserve dirty
files and unrelated branches. If the tool repository has a conflicting mandatory
branch policy, report the conflict before creation.

After creation, verify the branch, HEAD, Git common directory, and worktree
registration. Confirm that the intended tool instructions and engineering skills
are available in the executor's context. Directory placement alone does not prove
skill loading.

This convention applies to tool work requested by Admin. A tool-specific
automation lives under the tool repository's `automation/<job-name>/` and uses
the same tool task branch. Space-wide or multi-tool orchestration lives in the
Admin repository on branch `automation/<job-name>`. A shared reporter dependency
alone does not change source ownership. Other callers follow their owning
workflow.

## Return and integrate

Return the exact worktree, branch, base and final revision or uncommitted diff,
changed-file summary, verification evidence, and unresolved issues. Review the
cumulative change before applying it to the stable checkout. Worktree creation
does not authorize commit, merge, push, restart, or publication. Keep development
tests separate from live runtime stores. Verify the automation consumer after an
authorized integration changes its tool.

## Automation reports

A tool-specific job keeps its runner, source plist, runbook, `AGENTS.md`, and
process diagram together inside its tool repository. Write runtime reports to
`/Users/tai/.agents/automation/<stable-job-name>/logs/`, ignored by Admin Git. An
optional README there is a pointer, not another source runbook.

`<stable-job-name>` may differ from the source folder name. A Space-owned job
uses `<source-folder>-runtime` so its report root stays outside its source. A
tool-owned job may use the job name, because its source lives in the tool
repository.

Use an explicit absolute report root for the scheduled stable checkout. Worktree
and fixture runs use temporary report and state roots. Include run ID, source
revision, dirty state, job identity, and request reference in reports. Keep
durable incident queues separate from rotating logs. Development does not update
the scheduled checkout until integration is authorized and verified.

For scheduler lifecycle rules, read [Automation](automation.md).

## Extraction record

The independent repositories were created on 2026-10-23 from Admin revision
`40e9d38238e487744ec216f5a57617e3c09cfb3e`. Files were preserved in place;
Admin removed only the index entries. Parent history was not rewritten, so every
pre-extraction file stays readable with `git show <base>:<path>`. No remote was
added and nothing was published.
