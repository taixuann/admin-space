# Closing the Loop — execute, review, reconcile, issues

The advisor's job doesn't end at the plan. This file covers the four follow-through flows: dispatching an executor and reviewing its work (`execute`), reviewing an implementation that already ran (`review`), keeping the plan backlog alive (`reconcile`), and publishing plans where work gets picked up (`--issues`).

The founding rule survives unchanged: **the advisor never edits source code.** In `execute`, a *separate executor* edits code in an isolated git worktree — the native subagent, or an explicitly selected external transport such as `opencode-delegate` given the same plan and the same exact worktree path; the advisor dispatches, reviews, and renders a verdict — like a tech lead who doesn't push commits to your branch. Selecting a transport is an execution choice: it does not transfer plan ownership, acceptance, commit, or publication authority away from the advisor and the human.

---

## `execute <plan>` — dispatch and review

### Preconditions (check all before dispatching)

- The repo is a git repository (worktree isolation requires it). If not: stop and say so.
- The plan file exists and its dependencies show DONE in `plans/README.md`. If not: stop, name the missing dependency.
- Run the plan's drift check yourself. If in-scope files changed since `Planned at`, reconcile the plan first (see below) — don't hand a stale plan to an executor.
- **The worktree is verified before anyone edits it.** Under host-native `isolation: "worktree"` the host creates it and you confirm it after spawn; with an external transport you create or select it yourself. Either way, verify before dispatch: `git -C <path> rev-parse --show-toplevel` (exact identity), the base commit the plan reviews against, and `git -C <path> status --porcelain` for pre-existing changes. Hand the executor that exact path — never let it assume which tree it is in, and never discover the base after the fact.
- **One writer per mutable tree.** If any prior job may still be alive in that worktree, do not dispatch; inspect the tree first (diff, index, untracked files) and reconcile. Two writers on one tree is an automatic STOP.
- **Pick the transport deliberately.** Native subagent by default; an external transport (e.g. `opencode-delegate`) only when the user selects it. Selecting it hands over typing only — you still own the plan, the review, the verdict, and every gate.

### Dispatch

Native path: spawn **one** `general-purpose` subagent with `isolation: "worktree"`. Executor model: default `sonnet`; use what the user named if they named one (`execute 003 haiku`).

External path (only when the user selected it): hand the same plan and your verified worktree path to the transport — for `opencode-delegate`, its relay (`scripts/relay.mjs`) runs a brief with the plan inlined, and its `--read-only` mode can run a second, review-only leg when you want an independent read of the tree. The transport runs the steps and returns a result artifact; treat that artifact as a claim, never as accepted work. When improve drives the transport, improve's report contract (item 3 below) wins; the transport's own brief-template report contract applies only to transport-owned dispatches.

Either path, the prompt must contain:

1. **The full plan file text, inlined.** The worktree contains only committed files — if `plans/` is uncommitted, the executor can't read it. Never assume; always inline.
2. The executor preamble:

> You are the executor for the implementation plan below. Follow it step by
> step. Run every verification command and confirm the expected result before
> moving on. Touch only the files listed as in scope. If any STOP condition
> occurs, stop immediately and report. Do not improvise around obstacles.
> Commit your work in the worktree following the plan's git workflow section —
> and only under that native isolated-worktree contract with separate commit
> authorization; when your dispatch says otherwise (external transport, batch
> brief, or a read-only governing workflow), leave every change uncommitted and
> say so in the report.
> One override: SKIP the plan's instruction to update `plans/README.md` —
> your reviewer maintains the index. Before reporting, audit every claim in
> your report against an actual tool result from this session — only report
> what you can point to evidence for; if a verification failed or was
> skipped, say so plainly. When finished, reply with exactly the report
> format below.

3. The report format — one cumulative report at the end of the job (or at the
   batch boundary, not after every step):

```
STATUS: COMPLETE | STOPPED
STEPS: per step — done/skipped + verification command result
STOPPED BECAUSE: (only if STOPPED) which STOP condition, what was observed
FILES CHANGED: list
DEVIATIONS: plan steps you adapted, and why (empty if none)
UNAPPROVED OBSERVATIONS: things you noticed outside scope and deliberately did not touch
BLOCKERS: what must clear before dependent or follow-on work
NOTES: anything else the reviewer should know (surprises, judgment calls)
```

The report is the executor's claim, not accepted work. Unapproved observations are report material, not authorization to change more files: no change is approved because the worker discovered it.

### Batches — when the plan carries a Batch section

One coherent, user-authorized job may contain several ordered, dependent steps. Run it as a single dispatch under these rules:

- **Group only what stays compatible.** Steps belong in the same batch while authorization, mutable scope, and review requirements are the same for all of them. Dependencies between steps are expected — that is what "serial" means here.
- **The batch ends at its recorded boundary.** A human decision, a protected transition, or a required independent-review checkpoint stops the job; the executor reports and waits. The next batch is a new dispatch. There is no fixed task-count limit in either direction.
- **Gates run in order, review runs once.** Each step runs its own gate locally before the next step starts; you re-run the done criteria and read the full diff once, cumulatively, at the batch boundary — not after every microstep.
- **Scope is the batch's mutable scope**, checked against the cumulative diff plus index and untracked files, not just the last step's.
- **Unrelated goals never ride along.** A second goal is a second plan and a second dispatch, however small it looks.

### Review (the advisor's real job here)

Note on fresh worktrees: they share git history but not `node_modules` or build artifacts — the executor must install dependencies first, and check tooling that resolves from `dist/` may need one build even though the plan's command table (recon'd in the main tree) didn't mention it. Expect this; it isn't a deviation.

Review like a tech lead reviewing a PR against the spec — never fix anything yourself. Whatever produced the work, you inspect it yourself: an external transport's `result.json`, green gate claim, or completion status is a claim, not accepted work, and a process exiting cleanly is not the task succeeding and not your APPROVE.

1. **Re-run every done criterion** in the worktree. Don't trust the executor's report — verify.
2. **Scope compliance**: `git -C <worktree> diff --stat` against the plan's in-scope list (for a batch: the batch's mutable scope), including `git -C <worktree> diff --cached` for anything staged and untracked files — plain `git diff` is blind to both. Any file outside scope fails review, full stop.
3. **Read the full diff** against the base you verified at dispatch, not against whatever HEAD happens to be now. Judge it against "Why this matters" (does it solve the actual problem?) and the repo conventions named in the plan (does it look like the rest of the codebase?).
4. **Audit the new tests.** Executors game criteria — a test that asserts nothing meaningful passes `pnpm test` and proves nothing. Read what the tests assert.
5. **Bloat scan.** One pass over the diff for speculative abstraction, dead flexibility, and invented dependencies — the ponytail-review register. Fold findings into the verdict: cosmetic ones go to NOTES, contract-violating ones go to REVISE.

### Verdict

**Documented deviations are judged on merit, not reflex-blocked.** "Do not improvise" exists to stop silent drift; an executor that hits a real obstacle (e.g. the plan's approach breaks existing test mocks), adapts minimally, and explains it in NOTES has done the right thing. Approve it if the adaptation serves the plan's intent and stays in scope; treat *undocumented* deviations as review failures.

| Verdict | When | Action |
|---|---|---|
| **APPROVE** | Criteria pass, scope clean, quality holds | Update index status to DONE. Present to the user: diff summary, worktree path and branch, anything from NOTES. **Merging is the user's decision — never merge, push, or commit to their branch.** |
| **REVISE** | Fixable gaps | Send the same executor a delta brief with specific, actionable feedback ("criterion 3 fails: X; the error handling in `api.ts:90` swallows the error — use the Result pattern per the plan"); for `opencode-delegate` continue its recorded session using the exact `sessionId` from the result, falling back to `--resume-last` only when no concurrent session makes the identity ambiguous. **Max 2 revision rounds**, then BLOCK. |
| **BLOCK** | STOP condition hit, scope violated unrecoverably, or revisions exhausted | Mark BLOCKED in the index with the reason. Refine or rewrite the plan with what was learned. Tell the user what happened and what changed in the plan. |

Running verification commands inside the executor's worktree is fine — it's isolated and disposable. The no-mutating-commands rule protects the user's working tree, not the worktree.

---

## `review <plan>` — read-only review of an implementation that already ran

Full post-execution review for work you did not watch happen: an external batch, a resumed session, a tree another agent says is done. It is read-only end to end — never dispatch, never edit, never commit, never push.

**Required inputs — all four, before you judge anything:**

1. The approved plan (file path or index entry).
2. The exact worktree path holding the implementation.
3. The base commit the work started from.
4. The executor's result artifact — report text, `result.json`, or transcript, whatever the transport produced.

If any input is missing, ask for it first. An ambiguous diff reviewed against the wrong base is worse than no review. Record the binding — plan, worktree path, base commit, head commit — because your verdict applies to exactly that diff and nothing else; a later change invalidates it.

**Then run execute's review unchanged**, in the bound worktree:

1. Re-run every done criterion.
2. Scope compliance against the plan's in-scope list (or the batch's mutable scope): `git -C <worktree> diff --stat <base>..HEAD`, plus `--cached` and untracked files.
3. Read the full diff against "Why this matters" and the repo's conventions.
4. Audit the tests the change adds or touches.
5. Bloat scan as in execute's item 5.

**Verdict:** APPROVE / REVISE / BLOCK as in `execute`, with read-only actions:

| Verdict | Action |
|---|---|
| **APPROVE** | This diff meets this plan at this binding. Present the summary, worktree path, base and head. **APPROVE is not merge, push, or commit authority.** |
| **REVISE** | Return specific, actionable feedback to whoever owns the executor and stop — `review` does not dispatch. Max 2 rounds against the same binding, then BLOCK. |
| **BLOCK** | STOP condition, scope violated, or revisions exhausted. Report; do not repair anything yourself. |

Report unauthorized or out-of-scope changes instead of absorbing them, and say plainly when the result artifact and the tree disagree — the tree is the evidence.

---

## `reconcile` — keep `plans/` alive

Process what happened since the last session. Read `plans/README.md` and every plan file, then per status:

- **DONE** — spot-check that the done criteria still hold on the current HEAD (cheap ones only). Mark verified in the index. Don't delete plan files — they're the record. This is backlog maintenance: a cheap DONE spot-check is never acceptance of a fresh implementation. That is `review <plan>`.
- **BLOCKED** — read the reason. Investigate the underlying obstacle in the codebase. Either rewrite the plan around it (new number if the approach changed fundamentally, in-place refresh otherwise) or mark REJECTED with one line of rationale.
- **IN PROGRESS** (stale) — flag it to the user; an executor probably died mid-run. Check the worktree if one exists.
- **TODO** — run the drift check. If drifted: re-verify the finding still exists (it may have been fixed in passing), then refresh the "Current state" excerpts and `Planned at` SHA. If the finding is gone, mark REJECTED ("fixed independently").

Finish with a short report: what's verified done, what was refreshed, what's rejected, and what's executable right now.

---

## `--issues` — publish plans as GitHub issues

Modifier on any planning invocation (`/improve --issues`, `/improve security --issues`). The flag is the user's authorization to create issues — never create them without it.

1. Preflight: `gh auth status` succeeds and the repo has a GitHub remote. If either fails, write the plan files as normal and say why issues were skipped.
2. Visibility check: `gh repo view --json visibility`. If the repo is **public**, warn the user that issues are publicly visible and get explicit confirmation before publishing any plan that describes a security vulnerability, credential location, or other sensitive finding.
3. Show the list of titles about to become issues; confirm once if interactive.
4. Per plan: `gh issue create --title "<plan title>" --body-file <plan file>`. Labels: `improve` plus the category — apply only if the labels exist or can be created without erroring; skip labels rather than fail.
5. Record each issue URL in the plan's Status block (`- **Issue**: <url>`) and the index.

The plan file remains the source of truth; the issue is distribution. The self-containment rule pays off here — the issue body needs no edits to make sense to whoever (or whatever) picks it up.
