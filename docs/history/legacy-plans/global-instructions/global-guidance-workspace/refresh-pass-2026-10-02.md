# Candidate refresh pass — applied 2026-10-02 (post-V2)

Executed per GI-002 plan section "Candidate refresh pass" (operator-approved
2026-10-02), immediately after plan 002 landed (opencode v2.0.22).

Applied:

1. `candidate/codex/AGENTS.md`: the single-model paragraph was replaced with
   the allowlist policy (four `opencode-go` models with per-model variant
   preferences, live-check-before-trust, stop on failure). File grew
   70 → 79 lines.
2. `candidate/opencode/AGENTS.md`: the authorized-briefs paragraph was split
   in the simple-english Plain register (one instruction per sentence).
   Structure otherwise unchanged (no model section — the orchestrator owns
   model choice through the brief and relay `--model`). Now 20 lines.
3. `candidate/claude/CLAUDE.md`: DROPPED from the candidate set and
   removed from disk. Rationale: V2 (migration guide) no longer reads
   `~/.claude/CLAUDE.md` as a fallback — the harm the candidate guarded
   against cannot occur on V2; CodeGraph/AQG guidance already lives in the
   OpenCode candidate itself (lines 5-10), so nothing is lost.
4. Line budget: 79 + 20 ≤ 90 per file. PASS.
5. Register: existing codex/workbench prose kept (mostly comma-joined short
   clauses; a full re-split would churn 79 lines without changing
   executability — deferred to any future content edit). No further register
   edits this pass.

Post-refresh hashes (sha-256):

- `candidate/codex/AGENTS.md` →
  `17c7f691a8ab08ec1bc93f7bca50b1c9b5c7281fec4727edf8b7a7f44898d02b`
- `candidate/opencode/AGENTS.md` →
  `45d67ebe26d78571a73b8d515ff64d75d2b9089cd6cc18bf206c606821d842dd`
- `candidate/claude/` — removed; no hash.

Behavior cases: the affected cases (per GI-002, case 8's new V2 expectation)
rerun at Stage D with host evidence; case 1-7 exploratory results from the
pre-refresh drafts remain labeled exploratory, not acceptance.

Deployment risk note: these candidates target `~/.codex/AGENTS.md` (Codex)
and a NEW `~/.config/opencode/AGENTS.md` (OpenCode V2 global). Installation
stays gated at Stage E by separate operator authorization after Stage D.
