# Plan 009: Establish Development Space and a small-tool contract

## Status

- Status: IN PROGRESS 2026-10-23. Workshop renamed and 8 worktrees repaired with dirty state preserved; `tools/opencode-free-router` and `tools/hindsight` are independent repositories; Admin Git ignores `/tools/` and has no tracked tool paths. Small-tool contract written. OpenCode discovers the rewritten `launchd-automation` skill; the Claude Code and Gemini mirrors still need `bin/sync-skills`. Evidence: [batch 7](execution-2026-10-23/batch-7-verification.md).
- Priority: P1
- Effort: M
- Risk: MED. Moving the main checkout can break linked worktrees and scheduled jobs.
- Category: migration and developer tooling
- Planned at: Admin commit `40e9d38238e487744ec216f5a57617e3c09cfb3e`, 2026-10-23.
- Development base: `2fa7343800e57891947ab6683bacfcb5af350a1e`, branch `master`.
- Depends on: no implementation dependency on plan 007, which remains deferred. Coordinate with plan 008 for the automation consumer contract.

## Intent and ownership

Rename `/Users/tai/agent-development` to `/Users/tai/development-space`. Keep it a software-development workshop with reusable engineering skills and isolated worktrees. Each tool remains a separate Git repository at `/Users/tai/.agents/tools/<tool-name>/`. The parent Admin repository ignores the entire `/tools/` subtree. Development Space hosts linked worktrees of those repositories, not their canonical checkouts. This corrects the earlier proposal to move tool source into Development Space.

```text
~/.agents/                         # Admin repository
  .gitignore                      # /tools/
  automation/                     # Tracked Admin orchestration
  tools/                          # Ignored by the Admin repository
    <tool-name>/                  # Independent repository and stable checkout
      .git/
      backend/
      tests/
~/development-space/              # Engineering workshop
  .agents/skills/                 # CLI development and engineering skills
  worktrees/
    admin/<tool-name>_<plan-number>/ # Linked worktree for an Admin request
```

Keep worktrees ignored by the workshop repository. A tool's own ignore rules exclude its secrets, runtime stores, logs, and local dependencies. Do not add tools as Admin submodules or gitlinks. Admin automation calls the stable tool checkout. Development worktrees use isolated test state and do not mutate the live checkout or its runtime store. Review and verify a tool change before applying it to the stable checkout under the user's authorized integration scope.

Development Space owns reusable engineering guidance. Each tool owns its callable behavior and results. Automation source follows its owner: tool-specific jobs live inside tool repositories; Space orchestration lives in Admin. Runtime reports are centralized under Admin automation job folders. Improve owns investigation, plans, and review. Launchd-automation owns macOS automation rules. Writing-for-agents guides every AGENTS.md creation or edit in this work, including any nested file. Apply it to each changed file; do not bulk-generate instructions across unrelated repositories.

## Current state and evidence

- `/Users/tai/agent-development/AGENTS.md` states: `This workspace is a temporary software-development workshop. It owns reusable procedures and isolated worktrees. It owns no product source code.` Preserve this boundary.
- Its Worktrees section still names `~/agent-development/worktrees/`.
- Its README lists `.agents/skills/` as the local specialist home.
- Read-only Git inspection found a clean workshop checkout on `master` and a linked Antigravity worktree outside the workshop. Reinspect both before mutation.
- `/Users/tai/Library/LaunchAgents/com.tai.linear-notion-sync.plist` contains the old workspace path. Inspect its exact runner, source plist, loaded state, and side effects before migration. Do not print private configuration.
- `/Users/tai/development-space` did not exist during inspection.
- Admin plan 008 has draft skills under `/Users/tai/.agents/plans/008-skill-adaptation/`. They are not installed.

## Suggested executor toolkit

- Improve: plan and read-only review.
- Writing-for-agents: every AGENTS.md or skill instruction edit; verify hierarchy, scope, pointers, and duplication.
- Skill-creator: inspect, draft adaptations only where required, compare baseline and candidate behavior, collect feedback, then install accepted skills.
- Launchd-automation: inspect and migrate the existing path-dependent service.
- CLI-developer: command design, implementation, help, error handling, and relevant language references.

## Candidate assessment

### CLI Developer

Source: https://github.com/jeffallan/claude-skills/tree/main/skills/cli-developer

The inspected entrypoint covers commands, flags, configuration, non-interactive operation, signal handling, testing, and Python, Node, and Go references. It also imposes universal completion, three-platform testing, and a 50 ms startup target. Evaluate these against internal scripts rather than adopting the whole document blindly. Its wording about piped stdout needs clarification: structured result data belongs on stdout; diagnostics belong on stderr.

Prefer upstream unchanged when its actual behavior meets the fixture contract. If it creates unnecessary UX or packaging requirements, prepare a small attributed adaptation with provenance and tests. Do not fork solely to rename the skill.

### Agent Rules

Source: https://github.com/netresearch/agent-rules-skill
Entry: https://github.com/netresearch/agent-rules-skill/blob/main/skills/agent-rules/SKILL.md

The inspected entrypoint offers project/scope detection, command extraction, generation, freshness checks, and content/command verification. It declares Bash 4.3+, jq 1.7+, MIT and CC-BY-SA-4.0 licensing. Inspect the complete pinned package and licenses before redistribution. Check dependency availability on macOS.

Use it as a discovery and verification assistant if fixtures prove useful. Writing-for-agents remains the writing guidance. Review its automatic CLAUDE/GEMINI symlink behavior, generated markers, line caps, allowed-tools declarations, and command execution before enabling any generator. An upstream tool declaration grants no local authority. Preserve curated instructions. Do not run extracted commands until their side effects are reviewed.

## Scope

Implementation scope, after the migration inventory is complete:

- Workshop directory move and its own README, AGENTS, skill packages, and install metadata.
- Exact old-path references proven to be live consumers, including the identified service, with source and installed configuration reconciled.
- Per-tool independent repository extraction, Admin `/tools/` ignore boundary, and Development Space worktree registration.
- Admin Improve candidate and plan references required to express the ownership boundary.

Out of scope: bulk AGENTS rewrites, relocation of unrelated product repositories, native app memory, credentials, global plugin installation, Notion records, unrelated automations, and new publishing or CI requirements.

## Implementation steps and gates

1. Reorient from the workshop instructions. Record Git bases, dirty state, linked worktree identities, relevant symlinks, source and installed service configuration, active processes, and external old-path consumers. Read the current owning policies before execution. Gate: a bounded inventory names every known live consumer and its migration action. If the target exists or ownership is ambiguous, stop.
2. Prepare rollback and service continuity. Record prior paths and configuration hashes without secrets. Determine whether a running process needs a controlled stop and restart. Gate: the migration sequence preserves unrelated work and has an explicit runtime check. Do not infer that a directory move authorizes terminating active work.
3. Move the workshop to `/Users/tai/development-space` during the agreed execution step. Repair Git worktree metadata with native Git facilities. Update only inventoried references. Use launchd-automation for any service changes. Gate: `git -C /Users/tai/development-space status --short` preserves the recorded state; `git -C /Users/tai/development-space worktree list --porcelain` lists the new main path and existing linked worktree; Git operations in each linked checkout succeed. Inspect symlinks and relevant service paths separately. Verify a fresh service result if the service was changed.
4. Fetch candidate skills into a staging area within Development Space. Pin exact revisions. Inspect scripts, references, licenses, dependencies, and install behavior before activation. Keep candidate packages staged and inactive during inspection. Keep source provenance separate from the future installed copy. Gate: entrypoints, references, licenses, dependencies, and activation scope are known; no global or workspace activation occurs yet.
5. Evaluate three fixtures: a tiny Python CLI, a multi-command tool with state-changing behavior, and an existing curated AGENTS.md with scoped instructions. Compare baseline and candidate behavior through skill-creator. Gate: non-interactive operation, valid JSON, documented exits, stderr diagnostics, preserved curated policy, no unsolicited symlinks or live command execution. Record results and user feedback before accepting adaptations. After acceptance, install only selected packages under the workshop's `.agents/skills/` convention and verify loading in a fresh workspace session. Gate: the intended workspace discovers the accepted package; no accidental global activation occurs.
6. Establish the small-tool contract below at the owning Development Space documentation scope. Update the Improve candidate with a conditional pointer to that contract. Use writing-for-agents for all changed instruction files. Gate: automation plans still reach launchd-automation; tool plans reach the engineering contract; unrelated plans gain no automation or CLI obligations. Validate installed hierarchy after activation.

## Small-tool contract to establish

Default layout:

```text
tools/<tool-name>/
  README.md
  AGENTS.md
  backend/              # CLI entrypoint and implementation
  tests/                # Meaningful behavior checks
  docs/                 # Supporting docs when needed
  pyproject.toml        # Or language-native manifest when needed
```

A one-file tool may keep one entrypoint in backend/. Add modules only when responsibility requires them. Existing package conventions can take precedence when a new backend wrapper would add indirection. Do not create an empty folder merely to satisfy the tree.

Document the stable invocation, configuration, inputs, outputs, exit codes, timeout, interruption, rerun semantics, and state location. Provide --help and a non-interactive path. Offer stable JSON results for automation; put diagnostics on stderr. Preserve prior valid state when an update fails. For mutations, document whether repeated calls are safe and how partial failure is recovered. Keep credentials and mutable runtime state out of tracked source. Test success, invalid input, and the main failure path. Do not impose new dependencies, package publishing, shell completions, or cross-platform support without a consumer.

For tool work sent by Admin, use branch `admin/<tool-name>_<plan-number>` in the independent tool repository and worktree `/Users/tai/development-space/worktrees/admin/<tool-name>_<plan-number>`. Plan 010 owns the handoff contract in `docs/tools.md`. Only Space-owned automation implementation uses `automation/<job-name>` in Admin. A tool-owned job uses the tool task branch. Planning itself does not switch branches.

## Verification and completion

No build, test, or install command for the candidate packages was established during this planning pass. Discover exact commands from the pinned manifests; record them before execution rather than inventing them. For the rename, verify Git metadata, every inventoried consumer, relevant symlinks, and the changed service's fresh runtime result. A clean Git status alone is insufficient.

Done means the new workspace path works, consumers are repaired, selected skills load only at the intended scope, fixture evaluations pass, instruction loading is checked, and the cumulative diff stays within scope. Separate source installation, skill discovery, behavior checks, and service runtime evidence in the result.

## Stop conditions and maintenance

Stop on unowned dirty work, target collision, missing worktree metadata, unknown live consumer, unavailable migration permission, incompatible skill dependencies, or behavior that overwrites curated rules. Preserve evidence and report the exact blocked action. Keep rollback available until consumers pass. Recheck contracts when CLI signatures, schemas, install scope, or automation consumers change.

## Independent tool repositories and migration gates

Current evidence: `git -C /Users/tai/.agents ls-files tools` reported 42 tracked paths on 2026-10-23. Adding `/tools/` to `.gitignore` alone will not stop tracking them. This plan has not changed the ignore file or index.

1. Inventory each tool's existing Git root, remotes, history, dirty changes, tracked source, runtime files, secrets, and live consumers. Use `git -C <tool> rev-parse --show-toplevel` to distinguish a real tool repository from inherited Admin repository membership. Do not initialize over an existing repository or linked worktree.
2. For tool source currently owned by Admin Git, prepare a reviewed extraction with provenance to the parent base and path. Preserve recoverable history or an agreed source snapshot. Create an independent local source baseline after excluding credentials and runtime files. An independent repository does not require a new remote or publication.
3. Verify each tool can recover its maintained source independently. Then add `/tools/` to Admin's root ignore file and remove only the inventoried tool paths from the parent index while preserving all working files. Do not delete files or rewrite parent history. Coordinate these changes as one reviewed migration boundary. Previously committed secrets require a separate explicit remediation decision; ignore rules do not erase history.
4. Verify `git -C /Users/tai/.agents ls-files tools` is empty; `git -C /Users/tai/.agents check-ignore --no-index tools/<tool-name>/backend/<source-file>` matches the intended rule; and `git -C /Users/tai/.agents/tools/<tool-name> rev-parse --show-toplevel` resolves to that tool. Verify nested source is not lost, replaced by a gitlink, or exposed by an unintended remote.
5. Create a linked worktree at `/Users/tai/development-space/worktrees/admin/<tool-name>_<plan-number>/` from that tool repository on branch `admin/<tool-name>_<plan-number>` for an Admin-origin request. Gate: `git -C <tool-repository> worktree list --porcelain` lists both checkouts; workshop Git does not track the worktree. Use CLI-developer in the engineering workspace while following the tool's own AGENTS.md. Carry the engineering skill explicitly into the task because physical worktree placement alone does not prove host skill discovery or instruction loading.
6. Run isolated CLI and failure-path tests in the worktree. Keep the stable checkout unchanged during development. Define the reviewed integration and rollback step before updating the stable checkout; verify actual automation consumers after integration. Never point scheduled jobs at temporary worktrees by default.

Update workshop instructions with writing-for-agents while preserving their no-product-source ownership rule: the workshop holds worktrees; each independent tool repository owns source. Plan 010 owns the Admin-specific Improve rewrite and docs composition. Only Space-owned automation implementation receives the Admin `automation/<job-name>` branch convention. Admin-origin tool branches use `admin/<tool-name>_<plan-number>`. Resolve a conflicting mandatory repository policy before creation.

## Tool-owned automation and Superpowers pipeline

A tool-specific job keeps automation source inside the independent tool repository. Its reports go to `~/.agents/automation/<job-name>/logs/`; tests use a temporary report root. A shared incident reporter dependency alone does not make the job Space-owned. Request IDs such as 008 identify intent and goals. Development derives the design and executable implementation plan through the full Superpowers pipeline and links them back to the request. Keep tool automation on `admin/<tool-name>_<request-id>`; no second automation branch is required for the same tool task. Space orchestration alone uses an Admin automation branch.
