# Admin Integration Readiness

Status: consolidation authorized 2026-10-23. The user selected all current Admin repository work and one remaining local branch, master. Independent tool repositories remain separate. No remote push requested.

## Verified Git state

The base branch is master, at b149275; there is no local main branch.
The working branch codex/companion-v2 is at 40e9d38, three commits ahead of master.
Those commits change 804 files, including 326 plugin files, 356 skill files,
42 automation files and 42 tool files. A whole-branch merge includes this history.
New Superpowers plans and several docs are untracked. They are not in any commit.
Other changes include staged tool untracking, skill-link removals, launchd code,
and changing runtime logs. Preserve all unrelated edits and existing index state.

## Proposed bounded integration

- Include reviewed Admin root instructions, docs, planning artifacts, diagrams,
  the authorized research-link cleanup and its recovery manifest.
- Review independent-tool untracking with its ignore rule as one operation.
  Verify tool directories and repositories remain before committing parent deletions.
- Qualify the launchd skill source and tests before including its pending changes.
- Keep OpenCode Free Router implementation changes in its independent worktree.
  No tool commit, merge, activation or model configuration update is included.
- Keep changing logs, generated runtime state and unrelated plugin changes outside
  a newly selected Admin change set. Do not bulk-stage the shared worktree.

Before integration, decide whether the three existing broad commits belong in
master. If yes, qualify that whole branch plus a scoped Admin follow-up commit.
If not, construct a reviewed selective change set in an isolated checkout from
master. Test the resulting tree, not only the current dirty checkout.
No branch deletion, force update or remote push is authorized by this record.

## Plans transition

plans/README.md now routes new planning to docs/superpowers/. Keep old request
briefs and execution evidence intact. Stages 1–3 are current draft plans, not
proof of implementation readiness. Convert only outstanding accepted requirements;
retain source IDs, dependencies and unresolved gates. Improve is not uninstalled.

## Consolidation decision

The user resolved the earlier scope question: include the three existing commits
and the current Admin working changes. Preserve checkpoints and independent tool
working trees. Commit before fast-forwarding master; remove only the fully merged
local feature branch. launchd skill tests passed 18/18 before consolidation.
This is source-history consolidation, not runtime activation or acceptance of
every draft plan. No new automation is started.
