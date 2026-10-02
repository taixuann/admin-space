# Plan 004: Register pointer inside writing-for-agents (simple-english wiring)

> **Operator decision 2026-10-02:** "nối simple-english inline bên trong của
> writing-for-agents". Deployed live the same day, one record here.

## Status

- **Status**: DONE (live apply; skill file is the operator's dotfiles-managed install)
- **Priority**: P2
- **Effort**: S
- **Depends on**: none (complements plan 003 and GI-002's refresh pass)
- **Category**: dx
- **Planned at**: 2026-10-02, no git repo

## Change

One `## Register` section added to
`/Users/tai/.agents/skills/writing-for-agents/SKILL.md` (after the intro
pointer, before `## Context pointers`; the file went 81 → 85 lines):

- Agent-executed documents (skills, `AGENTS.md` / `CLAUDE.md`, runbooks,
  plan files) are written in the `/simple-english` Plain register: short
  imperative sentences, active voice, one instruction per sentence,
  condition before command, no contractions, no em-dashes, term defined
  before first use; tables, code, and quoted output keep their shape.
- Voice or essay documents take the writer's register (`/humanizer`'s
  domain; the two never stack on one text).
- Strict fires only when the user names STE or ASD-STE100.

Compatibility checked against the skill's own doctrine before the edit:
the register line passes the no-op test (the skill's default is structural
quality, not low register — behavior changes); it lives once as a context
pointer naming branches (the skill's own pointer discipline); the register
SPEC stays in simple-english itself, so no duplication of rules.

## Verification

- `quick_validate.py` on `~/.agents/skills/writing-for-agents` →
  `Skill is valid!`, exit 0
- New hash: `b983d87d0131aa3489bd281ea0b36774879679a6d0ba057143bfa9b65b7d54f7`
  (85 lines, was 81)

## Chain placement

This lives at the live-skill layer, outside GI-001's nine-file scope (a
separate, operator-authorized one-line-class change; GI baselines unaffected).
The chain is now: improve Phase 4 mention → GI-002 refresh-pass register
bullet → writing-for-agents Register pointer → simple-english spec. Each
consumer entrypoint names the register; the spec itself exists once.
