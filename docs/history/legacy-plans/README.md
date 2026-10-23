# Admin request briefs and historical plans

For new designs and implementation plans, use
[Superpowers specs and plans](../../superpowers/plans/README.md).
This supersedes the 2026-10-02 single-home convention for new work. Preserve
older plans, decisions, evaluation artifacts and execution records here.
Historical Improve instructions below describe their original workflow; they do
not require Improve for new Admin work. The installed Improve skill has not
been removed by this documentation update.

## Active handoff map

| Existing request | Current treatment |
| --- | --- |
| 007 Orchestra Companion | Deferred; do not activate through migration |
| 008 model refresh | Preserve request and execution evidence; tool implementation stays in its own repository/worktree |
| 009 tool repositories / workshop | Preserve migration evidence; follow current docs/tools.md for new work |
| 010 Admin workflow composition | Superseded direction: use Superpowers plus component docs; stages 2 and 3 are linked below |
| Native execution | [Stage 1](../../superpowers/plans/2026-10-23-native-opencode-execution.md) |
| Skills and plugins | [Stage 2](../../superpowers/plans/2026-10-23-admin-skills-plugins-management.md) |
| Root documents and docs | [Stage 3](../../superpowers/plans/2026-10-23-admin-document-foundation.md) |

Adapt only remaining actionable requirements into an approved Superpowers spec
and then a task plan. Link back to these request IDs and their evidence. Do not
copy completed tasks into new unchecked tasks or rewrite historical verdicts.

## Execution order & status

| Plan | Location | Title | Priority | Status |
|------|----------|-------|----------|--------|
| 001 | `./` | Make `improve` the single core driver (Routing section) | P1 | REJECTED 2026-10-02 — operator rejected the standalone Routing-section approach; improve direction DECIDED later the same day: inline mentions (Option B, plan 003) |
| 002 | `./` | Upgrade OpenCode V1→V2; drop quota plugin; verify auth continuity | P1 | DONE 2026-10-02 — opencode v2.0.22 (brew `opencode-v2`); auth survived without re-login; ponytail plugin loads under V2; mimo + deepseek routes verified live; websearch live pending key |
| 003 | `./` | Inline skill routing mentions applied to GI-001 candidates (improve SKILL.md + closing-the-loop + delegate brief) | P1 | DONE (candidate stage; installation still gated by GI-001 Stage E) |
| 004 | `./` | `/simple-english` register pointer added inside writing-for-agents (live skill) | P2 | DONE (live; chain GI-002 refresh pass → writing-for-agents → simple-english) |
| 005 | `./` | git baseline at `~/.agents` (recovery layer) + codex candidate rewritten via writing-for-agents + simple-english | P1 | DONE (baseline commit `ac5af95`; candidate 72 lines, register-clean; Stage E install still awaits operator authorization) |
| 006 | `./` | Clean `~/.codex` repo: drop 64 dead index entries + role contract + CI; keep toml adapters; fix AGENTS.md + README pointers | P1 | DONE 2026-10-02 — 6 files tracked, status clean, AGENTS.md 72 lines, no push; WORKFLOW.md removed per operator add-on |
| 007 | `./` | Build Orchestra Companion: ticket intake and bounded bot requests | P1 | DEFERRED 2026-10-23 — user deferred this work; implementation and installation not started |
| 008 | `./` | OpenCode refresh, local logs, Notion incidents, and launchd skill rewrite | P1 | IN PROGRESS 2026-10-23 — source implemented in tool worktrees; model 17/17, runner 17/17, incident 31/31, launchd skill 18/18; not loaded, not live-tested. Activation blocked on old-runner continuity and unattended Notion auth. Evidence: `execution-2026-10-23/batch-7-verification.md` |
| 009 | `./` | Development Space, independent tool repositories, and CLI contract | P1 | IN PROGRESS 2026-10-23 — workshop renamed and 8 worktrees repaired with dirty state preserved; tool repos created for the two extracted tools plus the new incident tool; `/tools/` ignored and untracked; small-tool contract written; `bin/sync-skills` drift unrepaired. Evidence: `execution-2026-10-23/batch-7-verification.md` |
| 010 | `./` | Rewrite Improve for Admin with docs routing and later plugin packaging | P1 | IN PROGRESS (docs-first) 2026-10-23 — profile draft and routing docs exist; `improve` unchanged; Improve rewrite superseded; no plugin packaged. Evidence: `execution-2026-10-23/` |
| EXEC-2026-10-23 | `execution-2026-10-23/` | Reconciled execution record for 008/009/010 | P1 | IN PROGRESS — batches 1–7 complete; 83 tests pass; activation, Notion auth, and installer drift remain open. Evidence: `batch-7-verification.md` |
| GI-001 | `global-instructions/` | Align bounded delegation, waiting, and review across Codex and skills | P1 | **INSTALLED 2026-10-02 (Stage E, operator-authorized)** — 9 files live (5 skill files + codex AGENTS.md `5e9ca977…`); validators pass; install receipt in `orchestration-workspace/install-receipt-2026-10-02.md`; git commits `ac5af95`→`f98b9d7`; Codex host behavior checks remain NOT_ASSESSED |
| GI-002 | `global-instructions/` | Align global scientific guidance across Codex and OpenCode | P1 | **INSTALLED 2026-10-02** — Stage D executed post-V2 (candidate 8/8, baseline 0/8 with empty governance); new `~/.config/opencode/AGENTS.md` live (`45d67ebe…`, loading verified twice: harness injection + live model answer); codex-side content carried by the GI-001 rewrite; Codex host checks NOT_ASSESSED; receipt `global-guidance-workspace/install-receipt-gi002-2026-10-02.md` |
| RV-001..004 | `archive/opencode-plan/` | RawView: lazy load, verification baseline, plumbing dedupe, combined filtering | P2 | DONE (verified per their README) |
| AS-005 | `archive/opencode-plan/` | Fork AutoSci to your account and push local work | P1 | DONE |
| AS-006 | `archive/opencode-plan/` | Quartz view-only site spike | P2 | DONE (spec; local-only branch) |

Numbering note: the GI- and RV/AS- prefixes disambiguate workstreams without
renumbering DONE records or breaking the internal cross-references and eval
artifact names inside `global-instructions/`.

## Decisions log

- 2026-10-02, plans home: `/Users/tai/.agents/plans/` is the only plans
  folder. `~/.agents/plan/` (singular) retired; its subtree moved intact to
  `global-instructions/`. `~/.opencode/plan/` is plan-mode scratch only;
  execution drains every plan into this directory.
- 2026-10-02, improve direction: the standalone `## Routing` section was
  rejected; an inline-skill-mention edit was applied and then reverted the
  same day. RESOLVED later that day: the operator picked inline mentions
  (Option B, plan 003) and they were applied to the GI-001 candidates; the
  earlier "Decision UNDECIDED / do not re-plan" wording is superseded history.
- 2026-10-02, delegation contract: the delegation plan's accepted candidate
  (in `global-instructions/orchestration-workspace/candidate/`) owns the
  improve/opencode-delegate contract changes; the live skill files still
  match their pre-candidate hashes.
- 2026-10-02, session two (V2 research turn): operator approved the
  OpenCode V1→V2 upgrade (plan 002) with the quota plugin dropped from V2
  config; auth continuity is a recorded verification step (`auth.json` lives
  in `~/.local/share/opencode/`, not the binary, so no re-login is expected).
  GI-001 gained a post-checkpoint decisions section (prompt-refine brief
  line, `--read-only` review leg, sequential-only recorded as REJECTED,
  terminal-title rejected). GI-002's single-model pin became the four-model
  allowlist policy with per-model variants (muse-spark → xhigh since it has
  no max; deepseek-v4.1-flash → max; glm-5.3-flash → max; mimo-v2.6-flash →
  no variants; live check beats displayed catalog because catalogue drift
  was observed for mimo). Operator action after upgrade: connect a free
  websearch key (Tavily first, no card; Exa optional) via TUI `/connect` or
  env var, then `websearch.provider: "random"` rotates for real.
- 2026-10-02, AGENTS.md quality turn: an audit of the instruction candidates
  against the new decisions folded four findings into the plans. GI-002
  gained a consolidated "Candidate refresh pass" section (allowlist model
  text into the codex candidate, simple-english Plain register as the
  authoring standard, claude candidate dropped after V2, V1 fallback section
  collapse, 90-line budget per global file, affected behavior cases rerun).
  GI-001 gained ponytail decisions: executor edits in the ponytail register
  (minimal diff, in-scope, every step runs, objections reported not skipped)
  and a ponytail-review-style bloat scan as a reviewer pass after the
  tech-lead checklist. The ponytail skill is already installed operator-side
  and its load check belongs to plan 002. Execution order: 002 → candidate
  refresh pass → GI Stage D.
- 2026-10-02, routing turn (plan 003, applied): the operator approved Option
  B and the deep placement audit. Five inline skill mentions applied to the
  GI-001 candidate files (prompt-refine with invariant guard, simple-english
  plan register, skill-creator toolkit line, opencode-delegate relay/
  --read-only/--resume-last wording, ponytail bloat-scan review item plus the
  smallest-diff action_safety rule in writing-the-brief). Verified-not-edited:
  review-and-land already contains the implementer sweep (ponytail-review
  substance); terminal-title rejected because OpenCode titles are native.
  Live skills unchanged; validators pass; hashes recorded in plan 003.
- 2026-10-02, review round: a fresh-context cold read of the deployed files
  found six real issues (README direction contradiction, commit-actor line in
  writing-the-brief, `--resume-last` vs exact sessionId, rival report
  contracts, the `review <plan>` list falling out of sync with execute's five
  items, an ambiguous prompt-refine guard referent); all fixed in the
  candidates and records, validators re-pass, new hashes in plan 003.
  Deferred: improve's pre-existing text issues logged in 003. New to the
  notes: the writing-for-agents skill is the named reference for the AGENTS.md
  candidate refresh pass.
- 2026-10-02, worktree closeout: the `scientific-skills-plans` WIP audited
  as fully landed — repo relocated `workspace/research-projects` →
  `~/research-projects`, tree clean, skill upgrades committed
  (`ac1446b7`, plans 001-006) plus follow-up test growth. Stale marker dir
  removed; `~/.codex/worktrees/` empty. No action left.
- 2026-10-02, Stage E prep (plan 005): operator replaced the folder-baseline
  workflow with a git repo at `~/.agents` (baseline commit `ac5af95` taken
  before any live change; recovery = `git checkout`; baseline/ folders stay
  as historical A-C evidence only). Codex candidate AGENTS.md rewritten
  through /writing-for-agents + /simple-english: 79 → 72 lines, role
  definitions moved to a ROLE-CONTRACT.md pointer, register-clean. Also
  removed the `superpowers@…` plugin entry from live opencode config during
  the isolation probe (operator declined it earlier: "bỏ qua luôn" — kept
  removed; ponytail + openchamber-agent-tool remain).
- 2026-10-02, Stage E INSTALL (operator: "install."): all 9 GI-001 files
  installed live after pre-install drift check PASS. Incident caught and
  fixed: codex AGENTS.md first copied from the stale Stage-A candidate
  (a4519fd8, 151 lines), re-copied from the rewritten one (5e9ca977, 72
  lines). Post-install validators pass on both live skills; install
  receipt written; ~/.agents git committed `ac5af95` → `f98b9d7`; tree
  clean. ~/.codex committed by operator (`51d5820` cleanup).
- 2026-10-02, codex-chatpgt repo end-of-life (operator: push then delete):
  pushed `2f4ca10..51d5820` (3 commits incl. pre-existing `422bfab`;
  secret scan clean), operator deleted the GitHub repo (verified
  `ls-remote` → "Repository not found"), local `.git` removed.
  `~/.codex` is now a plain working folder (AGENTS.md + README +
  agents/*.toml + runtime). Install history preserved in receipts +
  `~/.agents` git.
- 2026-10-02, GI-002 Stage D + INSTALL (end-to-end chain close): 16 runs
  via relay (`deepseek-v4.1-flash#max`, behavioral isolation) all completed;
  candidate 8/8, baseline 0/8 (empty governance — the true pre-install
  state). New `~/.config/opencode/AGENTS.md` live (`45d67ebe…`, 20 lines),
  loading verified TWICE: the harness injected it as session instructions,
  and a fresh run answered the scientific-baseline question verbatim.
  Rollback = `rm` that one file. GI-002's codex draft file superseded by
  the GI-001 rewrite (its asks covered there). End-to-end chain fully
  installed: plan 002 (V2) + refresh pass + GI-001 (9 files) + GI-002
  (OpenCode global). Operator-side leftovers: Tavily `/connect`, real
  Codex host checks, `~/.codex` commit.

## Open gates (block the marked plans until resolved)

- Plan 002 (OpenCode V2 upgrade) — DONE; auth + plugin gates passed (see
  `002-opencode-v2-upgrade-workspace/post-state.txt`).
- GI-002 Stage D — EXECUTED post-V2 via relay under behavioral isolation
  (limitation recorded in `evaluation-results.md`); the case-8 credential
  question from the OLD incident remains recorded there (UNVERIFIED);
  resuming further eval rounds requires the full-sandbox envelope if the
  operator wants stricter separation.
- Operator follow-up after V2: connect a free Tavily key (no card) via TUI
  `/connect` or `TAVILY_API_KEY`; `websearch.provider: "random"` is now
  live and rotates for real.
- The `/Users/tai/.codex` checkout is dirty and now carries the INSTALLED
  GI-001 candidate text; committing inside `~/.codex` remains the
  operator's lifecycle act; pre-install content recoverable at
  `orchestration-workspace/baseline/codex/AGENTS.md`.

## Findings considered and rejected

- Rewriting DONE records or renumbering plans during consolidation: breaks
  internal cross-references and eval artifact names; DONE files are records.
- Deleting either workspace (evidence preservation): the receipts, baselines,
  and candidate hashes are the only proof of what was evaluated and accepted.

## Native execution follow-up

- [011: Native OpenCode execution](../../superpowers/plans/2026-10-23-native-opencode-execution.md): DRAFT. Final Decision Engine review, one repair cycle and one re-review. Mechanism research and design approval precede executable configuration steps.
