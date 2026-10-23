# Install receipt — GI-001 Stage E — 2026-10-02

Operator authorized install ("install." after reviewing the surfaces list).

## Pre-install drift check

All 9 live files matched their plan-recorded baselines:
`~/.codex/AGENTS.md` `ea546b1a…`; improve `SKILL.md` `1599aa29…`,
`plan-template.md` `7be76dd3…`, `closing-the-loop.md` `5d526bb3…`;
opencode-delegate `SKILL.md` `4b1e6e50…`, `writing-the-brief.md`
`20f33825…`, `multi-task-queues.md` `097b2c52…`,
`dispatch-and-poll.md` `3edd62ad…`, `review-and-land.md` `4a449c73…`.
PASS — proceed.

## Installed (candidate → live)

| Live file | Installed hash |
| --- | --- |
| `~/.codex/AGENTS.md` | `5e9ca9776f3965d13282551a18f8d7d92d68977ff8407bd8ca43ae193f96ccb2` (72 lines; the writing-for-agents/simple-english rewrite) |
| `~/.agents/skills/improve/SKILL.md` | `e6b0f2f5…` |
| `~/.agents/skills/improve/references/plan-template.md` | `11863f79…` |
| `~/.agents/skills/improve/references/closing-the-loop.md` | `8449fcd7…` |
| `~/.agents/skills/opencode-delegate/SKILL.md` | `84d46613…` |
| `~/.agents/skills/opencode-delegate/references/writing-the-brief.md` | `33551cb0…` |
| `~/.agents/skills/opencode-delegate/references/multi-task-queues.md` | `8c8295b5…` |
| `~/.agents/skills/opencode-delegate/references/dispatch-and-poll.md` | `96792cc3…` |
| `~/.agents/skills/opencode-delegate/references/review-and-land.md` | `eff2826e…` (unchanged from A–C) |

Relay `relay.mjs` untouched (hash `64b1b5a1…` verified by the
evidence-structure check after Stage D).

## Incident during install (caught + fixed)

The first copy pass pulled `codex/AGENTS.md` from
`orchestration-workspace/candidate/` (the STALE GI-001 Stage-A version,
`a4519fd8…`, 151 lines) instead of the rewritten candidate in
`global-guidance-workspace/candidate/` (`5e9ca977…`, 72 lines). Detected by
the post-install hash check (151 ≠ 72; a4519fd8 ≠ 5e9ca977), re-copied from
the correct source, re-verified. The 8 skill files were correct on the
first pass (orchestration-workspace IS their canonical candidate source).

## Post-install verification

- `quick_validate.py` on live `~/.agents/skills/improve` → `Skill is valid!`, exit 0
- `quick_validate.py` on live `~/.agents/skills/opencode-delegate` → `Skill is valid!`, exit 0
- Mentions present in live improve: `/prompt-refine` ×1, `/simple-english`
  + `/skill-creator` ×2, `review <plan>` variant ×3 matches, `Bloat scan`
  review item ×2 (execute + review lists), `resume-last` wording present.
- Delegate governing-workflow wording present; smallest-diff rule present.
- `~/.agents` git: install committed as `f98b9d7` (baseline `ac5af95`
  precedes it); tree clean.

## Notes

- `~/.codex` repo left UNCOMMITTED (its own lifecycle): the working tree
  now carries the installed candidate text; the pre-install content stays
  recoverable at `orchestration-workspace/baseline/codex/AGENTS.md`
  (`ea546b1a…`). Any commit inside `~/.codex` remains the operator's act.
- Codex host behavior checks (its control-plane cases) remain
  NOT_ASSESSED — they need a real Codex host run, separate from this
  install.
- Recovery: `git -C ~/.agents checkout <file>` for the five skill files;
  copy `baseline/codex/AGENTS.md` back for the Codex global file.

## GI-002 follow-ups (separate authorization, after its Stage D)

- New file `~/.config/opencode/AGENTS.md` (the OpenCode global candidate,
  20 lines, `45d67ebe…`).
- Codex global file reconcile on top of the installed GI-001 text (the two
  plans coordinate on this file; GI-002's changes are a subset now mostly
  covered by the rewrite: conditional role framing, scientific baseline,
  blocker convention, allowlist).
