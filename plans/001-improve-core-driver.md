# Plan 001: Make `improve` the single core driver that routes to leaf skills

> **Executor instructions**: Follow this plan step by step. Run every
> verification command and confirm the expected result before moving to the
> next step. If anything in the "STOP conditions" section occurs, stop and
> report — do not improvise. When done, update the status row for this plan
> in `advisor-plans/README.md`.
>
> **Drift check (run first)**: `git diff --stat 041d0456..HEAD -- advisor-plans/`
> plus `ls /Users/tai/.agents/skills/improve/SKILL.md`. The skill file lives
> outside this repo so git cannot track it — confirm its `metadata.version`
> is still `"1.0.0"` before proceeding; on a mismatch, treat it as a STOP
> condition.

## Status

- **Priority**: P1
- **Effort**: S
- **Risk**: LOW
- **Depends on**: none
- **Category**: dx
- **Planned at**: commit `041d0456`, 2026-10-02
- **Issue**: omit

## Why this matters

Twelve global skills sit flat with no stated entry point, so every agent
loads all twelve and guesses. Naming `improve` the single core driver gives
one place that says who plans, who implements, who writes, and who verifies.
Once that routing lives inside `improve` itself, later work can point each
route at local AutoSci skills without re-auditing the globals.

## Current state

The facts the executor needs, inlined:

- Target file: `/Users/tai/.agents/skills/improve/SKILL.md` — senior-advisor
  skill, read-only, produces plans for other agents. Frontmatter today:
  `name: improve`, `description: Survey any codebase as a senior advisor ...`,
  `metadata.version: "1.0.0"`. It has NO routing section — nothing names
  `opencode-delegate`, `simple-english`, `humanizer`, `playwright-cli`, or
  the remotion chain. Evidence: full read 2026-10-02, lines 1-122 end at
  "Tone of the output" with no References section.
- sibling drivers that `improve` must route to (do NOT edit these files):
  - `/Users/tai/.agents/skills/opencode-delegate/SKILL.md:18-20` — sole
    implementer gateway ("You write the brief and own the judgment").
  - `/Users/tai/.agents/skills/simple-english/SKILL.md:27-44` — technical
    writing filter, Plain default, Strict only when user names STE.
  - `/Users/tai/.agents/skills/humanizer/SKILL.md:15` — voice filter, keeps
    what it says. Rule: technical docs use simple-english, personal prose
    uses humanizer, never both blindly.
  - `/Users/tai/.agents/skills/playwright-cli/SKILL.md:4` — verifier
    (`allowed-tools: Bash(playwright-cli:*)`), snapshots over screenshots.
  - remotion chain: `remotion-create` → `remotion-markup` → `remotion-studio`
    → `remotion-render`, disposable explainers only, video last resort.
- Repo convention: work directly on `main`, small bounded commits, no
  branches by default (`AGENTS.md` — Git workflow). But the target file is
  OUTSIDE this repo, so do NOT commit it here; report the edit for the user
  to sync via their dotfiles flow.

## Commands you will need

| Purpose | Command | Expected on success |
|---|---|---|
| Confirm skill file | `ls /Users/tai/.agents/skills/improve/SKILL.md` | path printed, exit 0 |
| Check version | `grep 'version:' /Users/tai/.agents/skills/improve/SKILL.md` | `"1.0.0"` |
| Verify routing edit | `grep -c 'opencode-delegate\|simple-english\|playwright-cli\|remotion' /Users/tai/.agents/skills/improve/SKILL.md` | count ≥ 4 |
| Verify no source touched | `git status --porcelain -- advisor-plans/` | only README row change (your status update) |

## Scope

**In scope** (the only files you should modify):
- `/Users/tai/.agents/skills/improve/SKILL.md` — append one `## Routing`
  section (see Step 2), bump nothing else.
- `advisor-plans/README.md` — status row update when done.

**Out of scope** (do NOT touch, even though they look related):
- All other global skills (`opencode-delegate`, `simple-english`,
  `humanizer`, `playwright-cli`, remotion-*) — routing is declared from
  `improve` outward; editing leaves comes later as separate plans.
- All AutoSci local skills (`autosci/i18n/*/skills/`) — phase two.
- Remotion description rewrites, `openai.yaml` parity — deferred findings,
  not this plan.

## Steps

### Step 1: Confirm the target matches Current state

Open `/Users/tai/.agents/skills/improve/SKILL.md`, check frontmatter
`name: improve` and `metadata.version: "1.0.0"`, and confirm no `## Routing`
heading exists yet (`grep '^## Routing'` returns nothing).

**Verify**: `grep '^## Routing' /Users/tai/.agents/skills/improve/SKILL.md` → exit 1 (no match). If it matches, STOP — someone already did this.

### Step 2: Append the Routing section

Append exactly one section at the end of `SKILL.md`, before nothing
(it becomes the last section):

```markdown
## Routing

Single core driver: this skill plans, others execute.

- Implement: delegate via `opencode-delegate` (write the brief, review the
  diff, land it yourself). Never implement inside this skill.
- Write: `simple-english` for technical docs and plans (Plain default;
  Strict only when the user names STE/ASD-STE100/compliance), `humanizer`
  for personal voice prose. Never stack both on one text.
- Verify: `playwright-cli` for browser checks (prefer snapshot over
  screenshot); re-run project gates, never trust self-reports.
- Explain: `remotion-create` → `remotion-markup` → `remotion-studio` →
  `remotion-render` for disposable explainers; interactive HTML and diagrams
  beat video for daily science work.
- Grow: `skill-creator` owns skill lifecycle (draft → eval → iterate).
- Local projects (e.g. AutoSci): route through the same drivers —
  `improve` audits the local skill, `skill-creator` shapes it,
  `opencode-delegate` implements, `simple-english` polishes its docs.
```

Keep the existing tone (plain advisory prose). Change no other line.

**Verify**: `grep -c 'opencode-delegate\|simple-english\|playwright-cli\|remotion' /Users/tai/.agents/skills/improve/SKILL.md` → ≥ 4, and `grep '^## ' ` shows `Routing` as the last heading.

### Step 3: Self-check the edited skill

Re-read the appended section. Confirm: no secret values added, no
instructions to ignore previous instructions, frontmatter untouched,
line count grew by ~20 lines only.

**Verify**: `grep 'version:' /Users/tai/.agents/skills/improve/SKILL.md` → still `"1.0.0"`.

## Test plan

No automated tests exist for skills. Manual checks, following the
`skill-creator` qualitative-review pattern (run the skill, read output):
- Trigger test: ask "audit this repo for quick wins" — `improve` should
  fire and its output should reference the routing (delegate, not implement).
- Negative test: ask "write a sad commit message" — `improve` must NOT
  fire (that belongs to `humanizer`/writer path).
- Record both results in your final report; no files needed.

## Done criteria

Machine-checkable. ALL must hold:

- [ ] `grep '^## Routing' /Users/tai/.agents/skills/improve/SKILL.md` exits 0
- [ ] `grep -c 'opencode-delegate\|simple-english\|playwright-cli\|remotion' /Users/tai/.agents/skills/improve/SKILL.md` returns ≥ 4
- [ ] `grep 'version:' /Users/tai/.agents/skills/improve/SKILL.md` still shows `"1.0.0"`
- [ ] No file under `/Users/tai/.agents/skills/` other than `improve/SKILL.md` modified
- [ ] `advisor-plans/README.md` status row updated to DONE

## STOP conditions

Stop and report back (do not improvise) if:

- The file at `/Users/tai/.agents/skills/improve/SKILL.md` does not match
  Current state (different version, Routing already present, frontmatter
  changed).
- Any verification fails twice after a reasonable fix attempt.
- The routing appears to require editing a second skill file to make sense.
- You discover the assumption "improve is the agreed single driver" is
  false (user wants multiple drivers).

## Maintenance notes

For the human/agent who owns this after the change lands:

- When a new global skill is installed, add one bullet here — not a new
  driver. Drivers stay few; leaves grow.
- Reviewer should scrutinize wording drift: if the Routing section starts
  prescribing implementation details, it violates improve's read-only rule.
- Deferred follow-ups (not this plan): remotion description rewrites,
  `openai.yaml` parity decision, `simple-english`/`humanizer` router detail,
  phase-two AutoSci local audit through these same drivers.
