# Admin tool handoff

Draft for `/Users/tai/.agents/docs/tools.md`. This document is not installed.

## Ownership

Each `/Users/tai/.agents/tools/<tool-name>/` is an independent Git repository with a stable checkout. The parent Admin repository ignores `/tools/`. Development Space hosts linked worktrees for development. Scheduled jobs call the stable checkout, not a temporary worktree.

## Prepare the handoff

For a tool request from Admin, record the following in the existing plan:

- Plan ID and absolute plan path.
- Tool name and canonical repository path.
- Exact base commit and recorded dirty state.
- Branch and worktree path.
- Requested outcome, mutable scope, and files outside scope.
- Tool AGENTS.md and required engineering skills, including CLI-developer when appropriate.
- Verification commands, expected results, and return evidence.
- Integration boundary and rollback for any runtime change.

Use writing-for-agents for every AGENTS.md creation or edit. Keep the request in the existing plan instead of creating another tracking system. A prepared handoff does not dispatch an agent, create a worktree, or authorize integration by itself.

## Branch and worktree

For work sent by Admin, use this branch in the tool repository:

`admin/<tool-name>_<plan-number>`

The plan ID is the Admin request reference, not the final implementation plan. Run the full Superpowers design, implementation planning, execution, review, and verification workflow from the request, with links back to it. This document does not bypass design approval or authorize immediate execution. Use the existing plan ID, including leading zeros. Use the tool's directory slug. Example for plan 008:

- Repository: `/Users/tai/.agents/tools/opencode-free-router`
- Branch: `admin/opencode-free-router_008`
- Worktree: `/Users/tai/development-space/worktrees/admin/opencode-free-router_008`

The branch is a Git reference. The worktree path is a directory. The shared suffix makes the handoff easy to trace. Keep worktrees ignored by Development Space Git. The branch belongs to the independent tool repository, not the Admin or Development Space repository.

Before creation, verify that the tool is an independent repository, the base exists, and the target path and branch do not conflict. Reuse an existing matching task worktree when its identity and state are verified. Preserve dirty files and unrelated branches. If the tool repository has a conflicting mandatory branch policy, report the conflict before creation.

After creation, verify the branch, HEAD, Git common directory, and worktree registration. Confirm that the intended tool instructions and engineering skills are available in the executor's context. Directory placement alone does not prove skill loading.

This convention applies to tool work requested by Admin. A tool-specific automation lives under the tool repository's `automation/<job-name>/` and uses the same tool task branch. Space-wide or multi-tool orchestration lives in the Admin repository and uses `automation/<job-name>` there. A shared reporter dependency alone does not change source ownership. Other callers follow their owning workflow.

## Return and integrate

Return the exact worktree, branch, base and final revision or uncommitted diff, changed-file summary, verification evidence, and unresolved issues. Review the cumulative change before applying it to the stable checkout. Worktree creation does not authorize commit, merge, push, restart, or publication. Keep development tests separate from live runtime stores. Verify the automation consumer after an authorized integration changes its tool.

## Automation reports

A tool-specific job keeps its runner, source plist, runbook, AGENTS.md, and Archify workflow together inside its tool repository. Write runtime reports to `~/.agents/automation/<stable-job-name>/logs/`, ignored by Admin Git. Treat an optional README there as a pointer, not another source runbook. Space-owned automation keeps source in the Admin automation directory and ignores its logs too.

Use an explicit absolute report root for the scheduled stable checkout. Worktree and fixture runs use temporary report and state roots. Include run ID, source revision, dirty state, job identity, and request reference in reports. Keep durable incident queues separate from rotating logs. Development does not update the scheduled checkout until integration is authorized and verified.
