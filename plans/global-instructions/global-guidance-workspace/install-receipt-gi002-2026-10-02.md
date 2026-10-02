# Install receipt — GI-002 (OpenCode global guidance) — 2026-10-02

Authorization: the operator's standing end-to-end order ("chạy end-to-end
toàn bộ") covers the whole chain; this install is one new file, reversible
by `rm`.

## Stage D outcome (executed this turn, post-V2, via relay)

16 runs (8 cases × baseline/candidate), all `completed`, transport =
`relay.mjs --read-only`, model `opencode-go/deepseek-v4.1-flash#max`,
per-run isolation by `--standalone` + temp `XDG_CONFIG_HOME` (behavioral
isolation; ambient skill visibility = known limitation, recorded in
`evaluation-results.md`). Candidate behavior 8/8 scenarios matched the
governing text (proportionate trivial handling, no invented significance,
declared-inputs exploratory labeling, tests ≠ scientific acceptance,
brief-contract boundaries, concrete blocker request WITH independent-work
line, no rituals on writing, guidance content verified). Baseline
(old_skill dirs carry no governing text — the true live OpenCode state
before this install): 0/8 with generic honest holds.

Codex host outcomes for GI-002's cases: NOT_ASSESSED (needs real Codex
runs; the codex global file content already landed via the GI-001 install
rewrite — GI-002's codex-side asks are covered there).

Artifacts: `iteration-1/evals.json`, `eval-N/{with_skill,old_skill}/outputs/result.json`,
`eval_metadata.json`, `grading.json`, `run-1/` copies, `benchmark.json`,
`review.html`.

## Install

- NEW FILE `~/.config/opencode/AGENTS.md` ←
  `global-guidance-workspace/candidate/opencode/AGENTS.md`
  hash `45d67ebe26d78571a73b8d515ff64d75d2b9089cd6cc18bf206c606821d842dd`,
  20 lines.
- Verification (two independent):
  1. The harness injected the file as session instructions immediately
     after install (system-level evidence of loading).
  2. A fresh `opencode run` in `/Users/tai` answered the scientific-baseline
     question with the governing rule verbatim: "Keep raw evidence immutable
     and distinct from derived outputs, preserving traceability…".
- Rollback: `rm ~/.config/opencode/AGENTS.md` (no other file touched).

## Chain state after this install

- GI-001: INSTALLED (9 files, receipt `orchestration-workspace/install-receipt-2026-10-02.md`).
- GI-002: INSTALLED (OpenCode global guidance live; codex-side content
  carried by the GI-001 rewrite; its own codex draft file superseded).
- Open loops (operator-side): Tavily key via `/connect` (websearch for
  real); Codex host behavior checks (real Codex runs); `~/.codex` commit
  (operator's own lifecycle act).
