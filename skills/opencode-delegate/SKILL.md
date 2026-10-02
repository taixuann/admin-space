---
name: opencode-delegate
description: >-
  Delegate a coding task to the OpenCode CLI as a background implementer, then review its diff and
  land it yourself. Use this whenever the user wants to hand implementation work to OpenCode — phrasings
  like "have OpenCode do X", "delegate this to OpenCode", "run it through OpenCode", or "use OpenCode to
  implement/fix/refactor" — or wants to run a queue of coding tasks through OpenCode while staying the
  reviewer. Prefer it when the user will review the diff and commit it themselves. DO NOT USE for tasks
  small enough to do inline, or when the user wants the code written directly without delegating.
license: MIT
compatibility: Requires the `opencode` CLI installed and authenticated, Node 18+, and git. The orchestrating agent must be able to run shell commands and read files. Shell examples assume bash/zsh (macOS/Linux, or Git Bash/WSL on Windows).
metadata:
  version: 0.5.0
---

# OpenCode Delegate

You are the **orchestrator**. This skill lets you hand a bounded coding task to a separate
**implementer** — the OpenCode CLI — then review what it produced and decide what lands. You write
the brief and own the judgment and the review; OpenCode does the typing in its own session. Who
commits, pushes, or opens a PR is the **governing workflow's** call — the repo's AGENTS/CLAUDE
instructions, the plan, or an explicit user instruction — never the implementer's and never a side
effect of having delegated.

Nothing here is specific to one orchestrating agent. The loop needs only the ability to run a shell
command and read a file, so any agent with those two capabilities — Claude Code, OpenCode driving a
sibling session, or a comparable one — can drive it. (It is designed for and run on Claude Code; treat
other orchestrators as designed-for, not yet proven.)

## When NOT to use this

- The task is small enough to just do inline — delegation overhead is not worth it.
- The `opencode` CLI is not installed or not authenticated (run `opencode auth login`).
- You want to write the code yourself, or you only need a review (use the `plan` agent via `--read-only`).

## Prerequisites (check once)

1. `opencode --version` succeeds. If not, install (`npm i -g opencode-ai`, or the native installer from
   opencode.ai) and `opencode auth login`.
2. **Confirm which `opencode` is on PATH.** `command -v opencode` shows the active binary and
   `opencode --version` its version. The relay records the version it ran into `result.json`, so a stale
   binary is visible after the fact.
3. A model provider is authenticated — `opencode auth list` shows at least one credential.
4. You are in (or will point `--cd` at) the target git repository.

## Choose the implementer model

OpenCode has **no safe default** — a bare `opencode run` errors — so a fresh run needs a model via
`--model` or a fleet `--lane` that sets one (a resumed run inherits its session's model). Naming the
model is the one decision a single-model backend like codex-delegate never had, and it has two owners:

- **The human owns which models are allowed.** `opencode models` lists hundreds of entries, most billed
  per token (OpenRouter and the like); only the human knows which are their flat-rate subscriptions, and
  the CLI can't tell them apart. So the usable set is theirs — ideally stated once in the repo's
  `AGENTS.md` or their `CLAUDE.md` (e.g. "delegate mechanical work to `opencode-go/…`, hard logic to
  `…`").
- **You, the orchestrator, pick per task — from that set.** Match the model to the brief: a cheap, fast
  model for a mechanical sweep (rename, migration, removal); a strong one for a subtle bug or a
  money/security path.
- **If no usable set is stated, ask — don't guess.** Guessing from the catalog risks a metered model and
  a surprise bill. Name the constraint to the human and let them choose.

More depth: [references/writing-the-brief.md](references/writing-the-brief.md).

## The loop

Run these five steps per task. Steps 1, 4, and 5 are your judgment; 2 and 3 are mechanical.

### 1. Write the brief

OpenCode sees **only** the text you send plus what it can read from the working tree — no chat history,
no shared context. Everything the task needs goes in the brief: the goal, the current state, what to
change, what to leave untouched, the project's **actual** gate commands (discover them from the repo's
AGENTS.md/CLAUDE.md/Makefile — do not assume), and a report contract. Tell OpenCode it will **not**
commit — the relay never commits either, and the governing workflow decides who does. Keep to one
bounded job per brief: a single task, or one *approved batch* of ordered steps when the plan or the
user authorized them together; unrelated goals never share a brief. Full guidance and a template:
[references/writing-the-brief.md](references/writing-the-brief.md).

### 2. Dispatch

Send the brief to OpenCode with the bundled helper. It wraps `opencode run`, captures the run, and
writes a structured `result.json` — so your only job is "run a command, read a file." (`<skill-dir>`
below is this skill's installed directory — the folder containing this `SKILL.md`. Claude Code prints
it as "Base directory for this skill" when the skill loads; on other orchestrators use that same
directory — if unsure where it landed, run `find ~ -name relay.mjs -path '*opencode-delegate*'` and
substitute the directory above it.)

```bash
node "<skill-dir>/scripts/relay.mjs" --brief brief.txt --model <provider/model> --cd /path/to/repo
# --model (or a --lane that sets model) is required on a fresh run
# fleet lane from delegate-setup:           add --lane <name>  (dials apply; flags still win)
# read-only (review/diagnosis, no edits):   add --read-only   (uses the plan agent)
# continue the previous OpenCode session:   add --resume-last  (delta brief only; keeps the model; only when no concurrent session makes the identity ambiguous)
# hard time limit (watchdog):               add --timeout 2h  (default: off; implementation runs routinely need 1-2h)
# see all options:                          node .../relay.mjs --help
```

The helper defaults to the write-capable `build` agent and writes its artifacts to a temp dir, so the
repo under review stays clean. It **never commits** — see step 5. Mechanics, flags, and the
`result.json` shape: [references/dispatch-and-poll.md](references/dispatch-and-poll.md).

### 3. Wait for completion

Four different things get conflated here. Keep them apart:

- **Tool-call yielding** — your shell call returning early (backgrounding, a host notification) is
  *not* the job's outcome, not a failure, and not proof the host will wake you again later.
- **Job lifetime** — the relay process runs until OpenCode exits, hits `--timeout`, or is aborted.
  The relay owns that optional hard timeout; do not re-issue a tool call in a loop to stand in for
  process monitoring, and do not add a second watchdog.
- **Worker-reported outcome** — `result.json`'s lower-case `status` (`completed` | `failed` |
  `timeout` | `aborted` | `opencode_unavailable`) plus `finalMessage`. `completed` means the process
  exited cleanly: not that the task succeeded, and not that anyone accepted it. OpenCode can report
  **BLOCKED** in `finalMessage` under status `completed` — that is a blocker to act on, never an
  APPROVE.
- **Your verdict** — step 4, after you re-verify.

A run is terminal only on **process exit plus a readable `result.json`**. Then choose the wait that
the host actually supports:

- **Short tasks:** a supported foreground facility is fine.
- **Long tasks:** background only through a host facility whose job survival, terminal notification,
  result access, and cancellation you have verified *for that host*. **Claude Code** offers
  `run_in_background: true` with completion notification; other shells (`… &` in bash/zsh including
  Git Bash/WSL, `Start-Job` in PowerShell, `start /b` in cmd) give you a process to come back to.
  Codex completion notification is **NOT_ASSESSED** — no evidence, so don't assume it.
- **No proven notification:** say so before dispatch and agree an explicit **manual-resume** step
  with the user (e.g. "when the relay exits, re-run with this command / paste `result.json` back").
  No model-generated progress checks just to wait, no promised automatic next-batch dispatch, no
  invented wake-up guarantee. A host or runtime that polls without model turns is fine — this skill
  adds no polling script or scheduler.

Whatever the path, a pre-run usage error (bad args, empty brief) exits `2` with no result file, a
missing `opencode` binary exits `127` with status `opencode_unavailable`, and a `timeout` kills the
child — so the tree may hold partial edits. Surface that before recovering: inspect `git status`,
`git diff`, `git diff --cached`, and untracked files, and **never launch a second writer while the
prior job may still be alive.** The implementer's full report is the `finalMessage` field in
`result.json` (also printed in full on stdout between the report markers); an empty `finalMessage`
means OpenCode stopped without a closing summary — judge the work from `touchedFiles` and the diff,
and fix the brief's report contract next time.

### 4. Review — do not trust the self-report

OpenCode's `result.json` includes its own final message and any gate claims — and its `status` only
describes the *process*. A task result is not accepted work until your review says so. **Re-verify,
don't accept:**

- **Re-run the project's gates yourself** (the test/lint/build commands from step 1). Never take
  "gates passed" on faith.
- **Read the diff** against the brief: did OpenCode do what was asked, nothing more (scope creep) and
  nothing less? `touchedFiles` in the result is your starting point.
- **Run the relevant guard skills** on the diff if you have them installed (clean-code-guard,
  test-guard, etc. from `guard-skills`) — this skill produces the work; those skills judge it.
- For schema/migration changes, round-trip them; for removals, grep for dangling references.

Full checklist: [references/review-and-land.md](references/review-and-land.md).

### 5. Land it

The implementer edits the working tree and never commits; the relay never commits either. **Who
commits is the governing workflow's decision** — the repo's instructions, the plan, or an explicit
user instruction. Where that workflow gives you commit authority, commit as the party that verified
the work, and only after the gates pass and the diff holds:

- Commit the verified work yourself, with a clear message.
- If it needs changes, send a delta brief on the **same session** — prefer the exact `sessionId`
  from the result; use `--resume-last` only when no concurrent session makes the identity ambiguous —
  then review again.

Where the governing workflow does not grant that authority (a read-only advisor such as `improve`,
or a brief that says "leave it uncommitted"), hand the tree back instead: report the diff, the gate
results, and where the work sits. Pushes, PRs, and merges are separate authority; opting into
delegation is not opting into publication.

## Autonomy model

OpenCode's autonomy is governed by the **agent**, not a sandbox enum:

- **`build`** (the relay default) — write-capable; edits files in the working dir headlessly. The
  equivalent of "let it implement."
- **`plan`** (via `--read-only`) — read-only; reviews and diagnoses without touching the tree. The
  equivalent of "let it look but not edit."

Permissions **auto-approve by default**: the relay passes `--auto` so a headless run never blocks on a
prompt no one can answer. That is the point of unattended delegation — the orchestrator's diff review
and the implementer sweep (step 4) are the safety net, not a per-action prompt. Pass `--no-auto` to
honor the agent's own permission config instead (allow/ask/deny per action); pair it with an agent whose
in-workspace permissions are set to *allow*, or a headless run can hang waiting on an `ask`.
**Read-only (`plan`) runs never get `--auto`** — auto-approving would let the plan agent's ask-gated
edit/bash permissions through and defeat "read-only," so a review can't be tricked into touching the tree.

## Authorization model

Delegation is something the human opts into, and opting in authorizes **the run** — not publication.
Commit, push, PR, and merge authority come from the governing workflow, not from the act of
delegating; when it is silent on who lands the work, ask rather than assume. Two standing limits on
the mandate: **surface, don't absorb** (report OpenCode's design decisions, defensible-but-unasked
turns, and non-blocking nitpicks rather than silently keeping them) and **stop for scope changes**
(if correct completion needs going beyond the brief, ask — don't expand the mandate yourself). The
full treatment is in [references/review-and-land.md](references/review-and-land.md).

## References

- [references/writing-the-brief.md](references/writing-the-brief.md) — how to write a brief OpenCode can
  execute blind: structure, XML blocks, the report contract, embedding the real gate commands.
- [references/dispatch-and-poll.md](references/dispatch-and-poll.md) — `relay.mjs` flags, the
  `result.json` contract, backgrounding per orchestrator, and recovery when a run misbehaves.
- [references/review-and-land.md](references/review-and-land.md) — the review checklist, the landing
  boundary the governing workflow sets, and the rework cycle on a resumed session.
- [references/multi-task-queues.md](references/multi-task-queues.md) — running a sequential queue:
  carrying constraints forward, progress tracking, and the end-of-run coherence check.
