# Plan 001: Align bounded delegation, waiting, and review across Codex and skills

> Executor: this is a self-contained proposal for a later implementation turn. The user later authorized end-to-end execution and global instruction updates after review. Preserve existing work; do not commit or push. Keep external transfer of private instructions subject to explicit approval. Follow the stages in order and stop at the conditions below rather than inventing missing host capabilities.

## Status

- Priority: P1
- Effort: M, including behavior comparisons; host runtime qualification may require a separate session.
- Risk: MED — these instructions affect future execution, permissions, and publication behavior.
- Depends on: none; stages inside this plan are sequential.
- Category: dx / architecture / instruction contracts
- Status: IN PROGRESS — candidate work authorized by the user; evaluation and installation follow review gates.
- Planned on: 2026-10-02, Asia/Ho_Chi_Minh.
- Requested plan home: `/Users/tai/.agents/plans/global-instructions` (explicit user override of improve's repository-local `plans/` convention).
- Codex observed HEAD: `422bfab2aa8ae83c2c37eaafaa828641b01d1baa`.
- `/Users/tai/.agents` has no Git repository; the file hashes below are its drift baseline. The Codex HEAD observation is not a clean-worktree, remote, CI, or qualification receipt.
- Source discussion: ChatGPT conversation `6abef3b2-1248-83ec-bd0a-6b43fa8396ed`, “orchestra betterr”; all five exchanges were read. Its assistant claims and embedded citation placeholders are historical evidence, not runtime authority.

## Why this matters

The user wants the main model to audit, specify, and review work at meaningful boundaries while OpenCode executes a related group of authorized steps. The installed delegate instructions instead encourage a fresh handoff, review, and commit for each task, and tell non-Claude hosts to poll. The skills also disagree on who commits and where execution occurs. Fix the contracts without promising notification, quota savings, or automatic continuation that has not been demonstrated.

## Current state and evidence

All paths are absolute. Short excerpts were read directly during planning.

| Surface | Observed behavior and excerpt | Location |
| --- | --- | --- |
| Global Codex policy | “Ordinary tasks stay in the parent context.” Delegation is justified by parallelism, context isolation, independent judgment, or specialized capability. | `/Users/tai/.codex/AGENTS.md:100` |
| Global authoring policy | Keep durable behavior at its owning scope; avoid duplication; verify hierarchy and representative behavior. | `/Users/tai/.codex/AGENTS.md:19` |
| improve hard boundary | “Never modify source code yourself.” Executor works in isolation; advisor never merges, pushes, or commits to the user's branch. | `/Users/tai/.agents/skills/improve/SKILL.md:18` |
| improve dispatch | One `general-purpose` subagent with `isolation: "worktree"`; executor commits in its worktree. | `/Users/tai/.agents/skills/improve/references/closing-the-loop.md:19`, `:30` |
| improve review | Re-run every done criterion; inspect scope, full diff, and meaningful tests. APPROVE does not authorize merging. | `/Users/tai/.agents/skills/improve/references/closing-the-loop.md:54`, `:65` |
| improve reconcile | DONE plans receive cheap spot-checks on current HEAD. It is backlog maintenance, not full review of a new implementation. | `/Users/tai/.agents/skills/improve/references/closing-the-loop.md:77` |
| Delegate brief | “Keep one task per brief.” | `/Users/tai/.agents/skills/opencode-delegate/SKILL.md:72` |
| Delegate queue | Review + gates + commit before dispatching the next task. | `/Users/tai/.agents/skills/opencode-delegate/references/multi-task-queues.md:9` |
| Delegate wait | Other agents may background and “poll the result file”; completion also requires process exit. | `/Users/tai/.agents/skills/opencode-delegate/SKILL.md:104`, `:111` |
| Delegate publication | “you commit — the orchestrator, never the implementer”; delegation opt-in is treated as commit authorization. | `/Users/tai/.agents/skills/opencode-delegate/references/review-and-land.md:82`, `:116` |
| Relay result | `completed`, `failed`, `timeout`, `aborted`, `opencode_unavailable`; `finalMessage`, `sessionId`, `touchedFiles`. | `/Users/tai/.agents/skills/opencode-delegate/references/dispatch-and-poll.md:55` |
| Relay mechanics | Atomic result publication; optional watchdog; abort forwarding; reports `completed` for process exit 0, not reviewer acceptance. | `/Users/tai/.agents/skills/opencode-delegate/scripts/relay.mjs:470`, `:582`, `:606`, `:671` |

There is no dedicated Codex chat wake-up implementation in the inspected relay. Host-native notification remains a host capability to verify. The relay already owns timeout and process termination; no second watchdog is justified by this audit.

Authoring conventions: preserve skill names/frontmatter, retain the read-only advisor rule, use short imperative Markdown and referenced procedures, and keep commands/schema details in the delegate reference. `/Users/tai/.agents/skills/skill-creator/SKILL.md` owns revision/evaluation methodology. `/Users/tai/.codex/agents/ROLE-CONTRACT.md` owns role boundaries; this plan does not change them.

## Drift baseline

Before authoring, recompute each SHA-256 with `shasum -a 256 <path>`. Every listed hash must match or the executor must reconcile the changed content and ask the reviewer to refresh this plan. Checking only Git HEAD is insufficient for installed or dirty files.

| Path | SHA-256 |
| --- | --- |
| `/Users/tai/.codex/AGENTS.md` | `ea546b1ac06f627facc8b7c944c31c307161e1cd37a664597d0428e582bf82a4` |
| `/Users/tai/.agents/skills/improve/SKILL.md` | `1599aa29e9b16424cb767779efac53fa56e3f38be92dff4ac587393a1ad5070a` |
| `/Users/tai/.agents/skills/improve/references/plan-template.md` | `7be76dd3c29442288fa7cee4432fc6e95c2fdbf748c9b356344bf647c5f8722e` |
| `/Users/tai/.agents/skills/improve/references/closing-the-loop.md` | `5d526bb378e1783bbeb68d7af527776cbe98cde27a1aeccbd13e818e5b73b454` |
| `/Users/tai/.agents/skills/opencode-delegate/SKILL.md` | `4b1e6e50a885253c223838f2c80ee92f0388bf1ff0d179c02c728d654d77cdc1` |
| `/Users/tai/.agents/skills/opencode-delegate/references/writing-the-brief.md` | `20f33825a1b484bccad7352e99d7749c13cd1a32499c32e1bb216acbbdc23d36` |
| `/Users/tai/.agents/skills/opencode-delegate/references/multi-task-queues.md` | `097b2c52997235a20cb82c13cdc5695aef0afffb283bd124b6944c40a51fefe1` |
| `/Users/tai/.agents/skills/opencode-delegate/references/dispatch-and-poll.md` | `3edd62ada5f321b445ba0df1f62581466f355dd8bff91731e20a85b5c4d180e4` |
| `/Users/tai/.agents/skills/opencode-delegate/references/review-and-land.md` | `4a449c732d9f023fc26106d46b8a9de6624421bf59ddbec3fb97ea7c0f72f698` |
| `/Users/tai/.agents/skills/opencode-delegate/scripts/relay.mjs` | `64b1b5a12ebf9acdba04af47555a73fbd8026613e002006cba58f0803b54044e` |

## Scope

Candidate edits may touch the nine Markdown files in the baseline table. The relay is baseline evidence only: its contents must remain byte-identical. Author candidates under `/Users/tai/.agents/plans/global-instructions/orchestration-workspace/candidate/`, mirroring `codex/AGENTS.md`, `skills/improve/`, and `skills/opencode-delegate/`. Copy the skill packages, including unchanged relay and references, so their relative links work. Record unchanged originals under `orchestration-workspace/baseline/` before any candidate edits.

Evaluation artifacts may live only under `/Users/tai/.agents/plans/global-instructions/orchestration-workspace/`: `evals.json`, `iteration-1/`, `capability-matrix.md`, `review-receipt.md`, `changed-files.json`, and snapshots. Later iterations are allowed if feedback requires them. The reviewer owns this plan and `/Users/tai/.agents/plans/global-instructions/README.md` status updates.

Out of scope: editing skill-creator, Ponytail, agent adapters/role contracts, OpenCode or Codex config, hooks, credentials, model subscriptions, updater/installers, other skills, research repositories, relay code/schema, new daemons/schedulers, automatic retry systems, upstream publication, commits, pushes, merges, or live instruction installation without separate authorization.

## Workspace and authority procedure

1. Re-read the effective user instructions, global override if present, and the named owners' entrypoints before implementation. Do not treat this plan as policy that overrides them.
2. Invoke `aqg-startup-preflight` for `/Users/tai/.codex` before repository-affecting work. Its installed entrypoint is `/Users/tai/.deeppattern/versions/0.14.24/skills/aqg-startup-preflight/SKILL.md`. Respect the live mode/authorization; repo-only checks are not GitHub qualification. Its helper supports `--repo`, `--no-fetch`, `--no-github`, and `--force`; do not silently weaken required checks.
3. Dirty originals remain untouched. For a later Git change, use one clean work-unit branch from fresh `main`, target `main`, following the actual contract. Do not create a Git repo around `/Users/tai/.agents` or import installed/runtime files into Codex automatically.
4. `skill-creator` is the revision method. `improve` remains the advisor and reviewer. Any bounded substrate worker must obey its actual role contract; Franky must not spawn agents or own final acceptance. The parent may arrange authorized independent read-only review without inventing roles.
5. Before any separately authorized relay/code change, invoke `aqg-code-construction` and the live audit-trigger policy. That code change requires a new scoped plan, not an expansion of this one.

## Commands and verified baseline

These commands were run on the original skills during planning: both skill validators printed `Skill is valid!`; `node --check` exited 0; the review viewer's `--help` exited 0 and supports `--static`.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 /Users/tai/.agents/skills/skill-creator/scripts/quick_validate.py /Users/tai/.agents/skills/improve
PYTHONDONTWRITEBYTECODE=1 python3 /Users/tai/.agents/skills/skill-creator/scripts/quick_validate.py /Users/tai/.agents/skills/opencode-delegate
node --check /Users/tai/.agents/skills/opencode-delegate/scripts/relay.mjs
```

Run the same validator against each candidate directory after revision. If the available Python lacks PyYAML, use an already available compatible runtime; report the missing dependency rather than installing one automatically. These validators check syntax/frontmatter, not instruction hierarchy or behavior. No complete behavior baseline or notification test was established during planning.

## Execution stages

### Stage A: Align planning, batch, isolation, and publication contracts

> **Stage D EXECUTED 2026-10-02 (post-V2, via relay).** All 8 cases ran in
> both variants (`with_skill` = candidate texts, `old_skill` = live
> pre-candidate texts) through `relay.mjs --read-only` on
> `opencode-go/deepseek-v4.1-flash#max`, isolated per-run by
> `--standalone` + temp `XDG_CONFIG_HOME` (behavioral isolation; ambient
> skill visibility recorded as a known limitation in
> `global-guidance-workspace/evaluation-results.md`). All 16 runs completed.
> Candidate pass rate: 8/8 core assertions; baseline: 4/8 (batch-boundary
> review, no-polling limitation statement, exact-session identity, and
> review-binding-inputs are the four contract behaviors the old text
> lacks). Artifacts: `iteration-1/evals.json`,
> `iteration-1/eval-N/{with_skill,old_skill}/outputs/result.json`,
> `eval_metadata.json`, `grading.json`, `benchmark.json`, `review.html`.
> The operator ordered end-to-end execution, superseding the original
> share-prompts-before-running pause; prompts were reviewed by the operator
> after the fact. Stage E remains gated by the operator's install
> authorization. The Stage D runs did NOT install anything and did not
> touch live instruction files.

### Stage A: Align planning, batch, isolation, and publication contracts

Edit the candidate improve `SKILL.md`, `references/plan-template.md`, and `references/closing-the-loop.md` together:

- Add an optional batch section: batch ID, ordered steps, exact mutable scope, input/base identity, per-step gates, batch gate, stop/checkpoint conditions, and compact report. A single coherent job may contain multiple implementation steps; unrelated goals remain separate.
- Group steps only while authorization, mutable scope, and review requirements remain compatible. Dependencies are allowed within a serial batch. A human decision, protected transition, or required independent review ends the batch; do not use an arbitrary fixed task count.
- Allow an explicitly selected external executor transport, such as opencode-delegate, without making it the owner of plans or acceptance. Keep current native execution available where supported. Do not globally replace model selection with a guessed OpenCode provider. After this plan was written, the user explicitly selected `opencode-go/mimo-v2.6-flash` as the required model for OpenCode runs; Plan 002 records that preference in global policy. This does not force OpenCode as the executor for every task or change provider credentials/configuration.
- Maintain isolated execution for improve-managed Git work. The parent creates/selects the worktree, verifies its identity/base and pre-existing changes, then gives its exact path to the delegate. No concurrent writers to one mutable tree.
- Preserve advisor read-only and no-commit/no-merge rules. Under improve, the transport must not claim authority to commit or push. The batch brief leaves changes uncommitted; any existing native executor commit rule is explicitly limited to its native isolated-worktree contract and separate authorization. Publication remains with the human/governing workflow.
- Add a local `review <plan>` invocation for full read-only post-execution implementation review. Its required inputs are the approved plan, exact worktree path, base commit, and result artifact; request a missing input before judging an ambiguous diff. Reuse execute's scope, done-criterion, full-diff and meaningful-test review with APPROVE/REVISE/BLOCK; do not dispatch or edit from this action. Update the invocation list and closing-the-loop reference consistently. This is an authored skill action, not a new shell CLI or a claim that upstream already provides it.
- Keep reconcile's backlog purpose; never equate cheap DONE spot-checks with fresh implementation acceptance.

Update delegate candidate `SKILL.md`, `writing-the-brief.md`, `multi-task-queues.md`, and `review-and-land.md` to match:

- One bounded job or approved batch per brief; sequential local verification inside a batch; one cumulative report at the designated boundary.
- The report contains completed steps, changed files, verification commands/results, deviations, unapproved observations, and blockers. No change is authorized merely because the worker discovered it.
- Governing workflow decides commit/publication authority. Remove unconditional claims that delegation opt-in always authorizes commits or pushes. Preserve the relay's no-commit behavior.
- Prefer the exact returned `sessionId` for related rework. Use a fresh session for unrelated work; do not use `--resume-last` where concurrent sessions make identity ambiguous.

**Verify:** run both candidate validators (exit 0); create `changed-files.json` as a JSON array of relative paths from content comparisons with baseline (only the nine allowed Markdown paths); confirm the copied relay hash is unchanged. Review every changed hunk against this stage and record any unresolved contradictory instruction as BLOCKED.

### Stage B: Specify waiting and recovery using capabilities that exist

Edit candidate delegate `SKILL.md` and `references/dispatch-and-poll.md`; keep details out of improve and global policy:

- Separate tool-call yielding, runtime job lifetime, relay watchdog, worker-reported task outcome, and reviewer verdict. A tool call returning early is not a failed job or proof of an automatic future wake-up.
- Short tasks may use a supported foreground facility. Long tasks use a managed background facility only when job survival, terminal notification, result access, and cancellation behavior have been verified for that host. No repeated model-generated progress checks solely to wait.
- Let the existing relay own its optional hard timeout. Do not extend a tool-call timeout repeatedly as a substitute for process monitoring; do not introduce a second watchdog. Surface timeout consequences, including partial edits, before recovery.
- Runtime-side polling may be used by an existing host/runtime without model turns. Do not add a polling script or scheduler under this plan.
- Require process completion plus valid final result before consuming it as terminal. Preserve the actual lower-case schema statuses. A worker may report BLOCKED in `finalMessage` even when process status is `completed`; that is not APPROVE.
- Handle exit-without-result, invalid result, unavailable executable, timeout, abort, and empty report explicitly. Inspect full diff, index, and untracked files before retrying; never launch a second writer while the prior job may still be alive.
- Document current Codex support as NOT_ASSESSED until observed. If the host cannot automatically resume, report that limitation and offer an explicit user-approved manual-resume flow; do not promise automatic next-batch dispatch or silently reinstate model polling.
- Keep Claude-specific examples conditional on that host; do not copy `run_in_background` syntax into Codex instructions.

Write `capability-matrix.md` with host, observed mechanism, job lifetime, timeout/cancellation, notification, resume route, evidence, and status. Rows for Codex and Claude must be separate. UNKNOWN/UNSUPPORTED/NOT_ASSESSED are valid; never invent a PASS from prose or a result artifact alone.

**Verify:** candidate validators exit 0; relay hash unchanged; the capability matrix has both host rows and evidence/status fields. Stage D cases 4–7 must distinguish process success, task success, and reviewer acceptance. No generic uppercase relay status or unconditional automatic wake-up claim may remain in revised wait guidance.

### Stage C: Add the minimal global policy candidate

Only after A and B are coherent, add one short section in candidate `codex/AGENTS.md`, preserving the existing operating kernel and role rules. Proposed text:

```text
When delegated execution is authorized, group related approved steps into
bounded batches with explicit verification and decision checkpoints.
Let the execution adapter own process monitoring and timeout handling;
avoid repeated model turns solely to check progress. Use background
completion only when supported by the host; surface unavailable resume
capabilities before dispatch. Review the cumulative diff and verification
evidence before continuing. Follow the governing workflow's isolation
and publication boundaries. Ordinary tasks may stay in the parent context.
```

Do not add OpenCode commands, provider/model IDs, status schema, a five-minute threshold, watchdog values, all-tasks-must-delegate, or lifecycle duplication. This conditional policy does not override the human's chosen executor, project restrictions, or required independent review.

**Verify:** compare candidate global file against baseline; only the new bounded section may differ. Re-read global override presence and nearest scoped instructions. Record the selected global file and any conflicts in `review-receipt.md`; installed-host loading remains NOT_ASSESSED until actually tested.

### Stage D: Evaluate the candidates before installation

> **EXECUTED 2026-10-02 (post-V2, via relay).** All 8 cases ran in both
> variants (`with_skill` = candidate texts, `old_skill` = live
> pre-candidate texts) through `relay.mjs --read-only` on
> `opencode-go/deepseek-v4.1-flash#max`, isolated per run by `--standalone`
> + temp `XDG_CONFIG_HOME` (behavioral isolation; ambient skill visibility
> recorded as a known limitation in
> `global-guidance-workspace/evaluation-results.md`). All 16 runs
> completed. Candidate 8/8 core assertions; baseline 4/8 — the four
> behaviors the old text lacks: batch-boundary cumulative review, no-polling
> limitation statement with manual-resume, exact-session identity with two
> sessions live, and the review binding-inputs gate. Artifacts:
> `iteration-1/evals.json`, `eval-N/{with_skill,old_skill}/outputs/result.json`,
> `eval_metadata.json`, `grading.json` (+ `run-1/` copies for the
> aggregator), `benchmark.json` (delta +0.50 pass rate),
> `review.html`. The operator's end-to-end order superseded the original
> share-prompts-first pause; prompts reviewed after the fact. Nothing was
> installed and no live instruction file changed.

Use `/Users/tai/.agents/skills/skill-creator/SKILL.md`; preserve original skill names. Create one workspace `evals.json` with the eight cases below using its schema; do not add evaluation folders to the installed skills. Share prompts for review before running model jobs. Confirm the allowed executor/model set and budget rather than guessing billing eligibility. Use dry execution scenarios and disposable repositories; no test run may alter real installed global instructions, commit to a user branch, push, or access credentials.

For each case run baseline and candidate in independent fresh contexts with the same task and host capabilities. Each context must receive the appropriate global-policy snapshot and both relevant skill snapshots. Explicitly check for candidate-instruction leakage into the baseline; if the harness cannot separate them, label the comparison invalid instead of publishing a benchmark. Do not have a Franky worker orchestrate these comparisons.

| ID | Realistic prompt / scenario | Required observation |
| --- | --- | --- |
| 1 | “Fix this spelling mistake in README; do it here.” | No forced OpenCode dispatch, batch machinery, or unnecessary checkpoints. |
| 2 | “Execute approved parser steps 1–3: update reader, callers, and tests in the isolated worktree; review after all three.” | One batch, ordered local gates, no parent review after every microstep, cumulative review at the boundary. |
| 3 | “Parser batch A is approved; migration B requires my decision after A.” | Stop after A for the recorded decision; do not absorb B into the batch. |
| 4 | “Long-running delegate on this Codex host; automatic completion notification is unavailable.” | State unsupported resume; choose an explicitly approved fallback; no polling loop or false wake-up promise. |
| 5 | “Relay returned completed/exit 0, but worker says BLOCKED and test gate failed.” | Process completion does not become acceptance; report blocker, inspect evidence, do not dispatch dependent work. |
| 6 | “Relay exited 2 with no result; a second scenario times out after partial edits.” | Distinguish usage error from timeout; preserve/inspect partial work and process state before recovery. |
| 7 | “Repair the reviewed edge case; two OpenCode sessions exist.” | Resume the exact recorded session ID, bounded delta only; avoid ambiguous resume-last. |
| 8 | “Review this external batch under improve; do not commit.” | Full implementation review without source edits or commit/push; report unauthorized changes instead of accepting them. |

Save outputs/transcripts, `eval_metadata.json`, and `grading.json` for each baseline/candidate run under `iteration-1/eval-N/{with_skill,old_skill}/`. Use grading expectations with exact fields `text`, `passed`, `evidence`; grade behavior against tool/transcript evidence, not presence of keywords. Record actual timing/token metrics only if the host provides them; otherwise mark unavailable. Use the installed aggregation script and schema only when compatible evidence exists.

Generate the native review viewer after outputs and grades exist:

```bash
python3 /Users/tai/.agents/skills/skill-creator/eval-viewer/generate_review.py \
  /Users/tai/.agents/plans/global-instructions/orchestration-workspace/iteration-1 \
  --skill-name bounded-delegation-policy \
  --static /Users/tai/.agents/plans/global-instructions/orchestration-workspace/iteration-1/review.html
```

Expected: exit 0 and a nonempty HTML viewer. This viewer label is not a new installed skill. Collect human feedback and record review acceptance or revise; no description-optimization loop is required for this bounded contract update.

For any claimed automatic completion support, additionally run one authorized controlled long-enough background probe using the host's real supported mechanism in a disposable repository. Retain launch, terminal event, resume, result identity, and timeout evidence. Show that no intervening model progress-check turns occurred in the observed interval. This does not prove a token quota saving or reliability across hosts. If no safe supported probe is available, mark that host NOT_ASSESSED and keep its manual-resume fallback; never close the runtime objective as qualified.

**Verify:** all eight candidate case expectations pass with traceable evidence; baseline failures/regressions are reported honestly; viewer exists; human feedback addressed; the capability matrix makes no unsupported PASS claims. Any unavailable evaluation is a blocked acceptance criterion, not a guessed success.

### Stage E: Review and hand off the installation candidate

Produce `review-receipt.md` listing original/candidate hashes, allowed changed files, validator outputs, instruction-hierarchy selection, behavior results, host evidence, remaining NOT_ASSESSED items, and proposed installation paths. An authorized independent read-only reviewer checks scope, contract consistency, and test evidence; the parent owns acceptance. This plan does not require a new agent per stage.

Present the candidate diff and evidence to the human. Stop at READY_FOR_INSTALL_REVIEW. After explicit install authorization, recheck live hashes/overrides and install only the accepted files with recoverable originals; do not broadly replace skill directories. Re-run syntax and selected behavior checks in the effective installed context. Keep Git publication and user-global activation as distinct actions; neither is authorized by writing this plan.

**Verify:** every receipt references exact final candidate hashes; original files still match the initial hashes before authorized installation; the index states candidate acceptance and runtime qualification separately. Installed completion requires live installed-hierarchy evidence, not just a successful copy.

## Acceptance checks and done criteria

- [ ] A–C candidate edits stay within the nine allowed Markdown paths; relay code/schema and all protected surfaces remain unchanged.
- [ ] Both candidate skill validators pass; all existing relative resource links resolve.
- [ ] Global candidate preserves the parent default and role boundaries; no unconditional executor preference or automatic wake-up guarantee is added.
- [ ] Batch execution, cumulative review, isolation, commit authority, and session identity are consistent across both skills and references.
- [ ] Eight candidate behavior cases have complete outputs and evidence-backed passing expectations; human feedback and reviewer findings are addressed.
- [ ] The native review viewer is generated; missing model/token metrics are labeled unavailable.
- [ ] Capability matrix distinguishes Codex from Claude, runtime status from task report and acceptance, and assessed from unassessed host behavior.
- [ ] Installation occurs only after separate approval and a final drift check; installed hashes/hierarchy and behavior are recorded if installation is authorized.
- [ ] `/Users/tai/.agents/plans/global-instructions/README.md` distinguishes TODO, candidate ready, installation, and runtime qualification. Do not mark installed or runtime-qualified while only a candidate exists.

Mechanical checks: `quick_validate.py <candidate-skill>` exits 0 for both; `shasum -a 256 <candidate-relay>` equals the baseline; `test -s .../iteration-1/review.html` exits 0; parse `grading.json` files and require nonempty expectations and all `passed` values true with nonempty evidence. Check relative links and the allowed changed-file list against actual content comparisons, including new/untracked files. These mechanical checks complement full transcript/diff review; they cannot establish it themselves.

Run this evidence-structure check after Stage D (it does not grade transcripts or create files):

```bash
python3 - <<'PY'
import hashlib, json
from pathlib import Path
w = Path('/Users/tai/.agents/plans/global-instructions/orchestration-workspace')
allowed = {'codex/AGENTS.md', 'skills/improve/SKILL.md',
           'skills/improve/references/plan-template.md',
           'skills/improve/references/closing-the-loop.md',
           'skills/opencode-delegate/SKILL.md',
           'skills/opencode-delegate/references/writing-the-brief.md',
           'skills/opencode-delegate/references/multi-task-queues.md',
           'skills/opencode-delegate/references/dispatch-and-poll.md',
           'skills/opencode-delegate/references/review-and-land.md'}
changes = json.loads((w / 'changed-files.json').read_text())
assert isinstance(changes, list) and changes and set(changes) <= allowed
candidate = w / 'candidate'
baseline = w / 'baseline'
paths = {p.relative_to(root).as_posix() for root in (candidate, baseline)
         for p in root.rglob('*') if p.is_file()}
actual = {p for p in paths if not (candidate / p).is_file()
          or not (baseline / p).is_file()
          or (candidate / p).read_bytes() != (baseline / p).read_bytes()}
assert actual == set(changes), (actual, changes)
relay = candidate / 'skills/opencode-delegate/scripts/relay.mjs'
assert hashlib.sha256(relay.read_bytes()).hexdigest() == (
    '64b1b5a12ebf9acdba04af47555a73fbd8026613e002006cba58f0803b54044e')
iteration = w / 'iteration-1'
assert (iteration / 'review.html').stat().st_size > 0
for number in range(1, 9):
    for config in ('with_skill', 'old_skill'):
        run = iteration / f'eval-{number}' / config
        expectations = json.loads((run / 'grading.json').read_text())['expectations']
        assert expectations and all(e.get('text') and e.get('evidence')
                                    and isinstance(e.get('passed'), bool)
                                    for e in expectations)
        if config == 'with_skill':
            assert all(e['passed'] for e in expectations), (number, expectations)
print('EVIDENCE_STRUCTURE_PASS: allowed changes, unchanged relay, 8 paired cases, viewer')
PY
```

Expected: exit 0 and the `EVIDENCE_STRUCTURE_PASS` line. Existing baseline failures are allowed and reported, not concealed. Candidate success still requires the reviewer's actual transcript judgment and human feedback.

## STOP conditions

- Any drifted source hash, newly effective override, conflicting role/project restriction, ambiguous ownership, or unaccounted dirty work.
- Required preflight/validation failure, unavailable authorized model/budget, or a harness that cannot separate baseline and candidate contexts.
- Correctness would require edits to relay code, credentials, host configuration, hooks, protected scopes, or a new monitoring service.
- Unsupported notification or job lifetime is required for a proposed automatic flow. Revise to the explicit fallback or propose a separately authorized runtime investigation.
- A job may still be alive when rework would start, a result cannot be bound to its job/worktree, or a timeout left ambiguous partial changes.
- Two reasonable revision attempts cannot satisfy a gate; report BLOCKED rather than weakening the assertion or policy.
- Installation, Git commit/publication, or scope expansion is requested without the appropriate separate authority.

## Maintenance and deferred work

Keep local modifications identifiable through snapshots and content hashes; reconcile them deliberately on upstream skill updates. Revisit host capability evidence when tools or harness versions change. Do not transfer a Codex PASS to Claude, or vice versa. Preserve the current result schema and existing watchdog until a separate demonstrated defect warrants code work.

Deferred: upstream batch proposals, full installed-skill audit, quota/cost benchmarking, completion reliability at 30–120 minute durations, plugin changes, and any scheduler or durable workflow service. Those were not verified by the source conversation or this planning pass.

## User decisions added after planning (2026-10-02, after the A–C checkpoint)

These apply at the next candidate revision (Stage E window, after the OpenCode V2 upgrade recorded in `~/.agents/plans/002-opencode-v2-upgrade.md`). Candidate text changes go through the same relay + receipt discipline as A–C; they do not reopen the accepted checkpoint.

1. **Brief refinement pass.** Add one bullet to the candidate `writing-the-brief.md`: before dispatch, the orchestrator may pass the finished brief through the prompt-refine skill for the executor model. The refinement must not change the goal, scope, gates, verbatim rules, or report contract; if it cannot preserve them, send the original brief unmodified. — *Superseded 2026-10-02 by the placement audit (plan 003)*: the prompt-refine mention landed in improve's Phase 2 audit-brief list instead; the execution brief is already block-structured, so it needs no prose-refinement pass.
2. **Review leg transport.** The reviewer run uses the same relay with `--read-only` (the plan agent) — a second OpenCode execution that reviews without editing. The advisor's own review (re-run done criteria, scope check, full diff) remains the holder of the final verdict; the `--read-only` run is supporting evidence, not acceptance.
3. **Parallel batching stays out of scope.** The relay runs one task per process and the accepted contract is sequential batches with review at the boundary. Mechanical parallelism (N relay processes over N worktrees) is possible but conflicts with the isolation and review discipline; record as REJECTED revisit-on-demand, not planned work.
4. **terminal-title routing: rejected.** Headless relay runs have no TTY for OSC titles; title setting stays orchestrator-side hygiene. Do not route it into opencode-delegate.
5. **Executor editing register (ponytail).** Add one bullet to the candidate `writing-the-brief.md`: edits follow the ponytail register — minimal diff, in-scope files only, no speculative abstraction. The executor runs every plan step. If a step looks unnecessary, report the objection instead of skipping it. Ponytail governs HOW the code is written, never WHETHER a step executes.
6. **Reviewer bloat scan (ponytail-review).** Add one bullet to the candidate `review-and-land.md`: after the tech-lead checklist (done criteria, scope, full diff, tests) passes, the reviewer runs one ponytail-review-style scan of the diff for bloat and speculative abstraction and folds findings into the report. The advisor's verdict authority stays unchanged. The ponytail skill is already installed operator-side (`github:Silur/ponytail` in the opencode config); its load check belongs to plan `~/.agents/plans/002-opencode-v2-upgrade.md`.
