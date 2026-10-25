```yaml
requester: secretary
space: ~/.agents
base: master
branch: executor/supervisor-profile
scope: [docs/profiles/supervisor/README.md, docs/profiles/supervisor/supervisor-workflow.html, docs/profiles/supervisor/capabilities.yaml, docs/profiles/README.md]
checks:
  - test -f docs/profiles/supervisor/README.md -a -f docs/profiles/supervisor/supervisor-workflow.html
  - test ! -e docs/profiles/supervisor/capabilities.yaml
  - every relative Markdown link in the changed files resolves to an existing file
  - git status shows no changes outside scope
  - nothing under ~/academic-space or ~/.hermes was modified
engine: self
report: kanban card comment + kanban_complete summary to Secretary
```

# Supervisor profile (Academic Space): reconcile definition, then create runtime

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans. Task 1 is for Executor (kanban). SOUL edit and Task 2 is attended: Secretary runs it only after Tai approves, never an unattended card.

**Goal:** `supervisor` becomes a Hermes profile whose working directory is `~/academic-space/research-space`, with skills loaded from `openscience-adapter`, and a definition in Admin that matches the research-space content.

**Architecture:** Hermes profile (direction A) that owns research-space. The research-space definition is the content source of truth (Tai, 2026-10-25). Admin keeps the profile folder shape (README, SOUL, one workflow HTML; no capabilities.yaml). Runtime is configured only through `hermes` CLI.

**Tech Stack:** Hermes CLI (`profile`, `config`, `skills`), Archify (workflow HTML, copied not rebuilt), Markdown.

**Spec:** Tai's decisions in session 2026-10-25: A, skills from `openscience-adapter`, research-space version is canonical. Supersedes the supervisor half of [2026-10-25-academic-supervisor-writer-definitions.md](2026-10-25-academic-supervisor-writer-definitions.md). The writer half is untouched.

## Global Constraints

- Never write under `~/academic-space`; it is read-only input. Raw data stays immutable.
- No commit to `master`, no push, no merge without Tai's approval.
- Runtime changes (Task 2) need Tai's explicit go-ahead, a backup, and a rollback line first.
- Do not clone from another profile with `--clone-channels`. No Discord token for supervisor yet.
- Model is not chosen here; Tai sets it in the runtime.

## Review Focus

- **Experimenter (settled by Tai).** In research-space, `experimenter` is the run step: Supervisor runs it itself with `/opencode` in `research-space`. No Executor card for study runs, no separate experimenter profile. Replace every 'delegate to executor' statement in README accordingly; SOUL is updated by Secretary (see below).
- **Skill gap (settled by Tai).** `compose-research`, `ro-crate-research`, `figrecipe-run` live in `research-space/.openscience/skills`; load that directory as a second external dir next to the adapter.
- **Protected file.** Executor does not edit `SOUL.md` on an unattended card. Secretary edits `docs/profiles/supervisor/SOUL.md` attended after Task 1 (experimenter wording: Supervisor runs studies itself with `/opencode`, no Executor hand-off).
- **Unrelated skills.** The adapter exposes document, poster, and image skills. A broad skill set may crowd the Supervisor's prompt; trim with `skills.disabled` after observing.
- **Executor reach.** Supervisor sends Executor into research-space; this needs the Executor README to allow an owner-bot requester outside Admin. It already does ("scope = requester's own authority").

## Task 1: Reconcile the Admin definition to the research-space content

**Files:**
- Modify: `docs/profiles/supervisor/README.md`, `docs/profiles/README.md` (SOUL.md is out of scope)
- Create: `docs/profiles/supervisor/supervisor-workflow.html` (copy of `~/academic-space/research-space/docs/profiles/supervisor/supervisor-workflow.html`)
- Delete: `docs/profiles/supervisor/capabilities.yaml` if it exists (tracked, recoverable)

**Interfaces:**
- Consumes: research-space `docs/profiles/supervisor/{README.md,SOUL.md,supervisor-workflow.html}`, `docs/profiles/AGENTS.md`.
- Produces: a README with the three required sections whose content follows research-space (responsibilities 1–5, gates, contract wording), with the settled experimenter wording (Supervisor runs studies itself via `/opencode`). SOUL keeps the Admin provenance note updated to "reconciled to research-space".

- [ ] **Step 1: Diff.** Run `diff` of both README and SOUL pairs; list content that exists only in research-space.
- [ ] **Step 2: Rewrite README.** Keep the Admin three-section layout and permissions table; replace the narrative of responsibilities and workflow with research-space content; capabilities section names skills from `openscience-adapter` and lists `.openscience/skills` (`compose-research`, `ro-crate-research`, `figrecipe-run`) as a second external skills dir. Status line: draft reconciled, runtime pending.
- [ ] **Step 3: Do not touch SOUL.md.** Report any SOUL differences found in Step 1 for Secretary.
- [ ] **Step 4: Copy the workflow HTML** with `cp`; keep it as-is. Do not rebuild or copy receipts. Link it from the README workflow section.
- [ ] **Step 5: Run checks** from the header; report output.
- [ ] **Step 6: Commit on `executor/supervisor-profile`**, then stop for Tai's review.

## Task 2: Create the runtime profile (attended, gated)

**Files:** `~/.hermes/profiles/supervisor/` (new; Hermes-managed). Nothing else.

**Interfaces:**
- Consumes: Task 1 merged or approved; Tai's go-ahead in chat.
- Produces: profile `supervisor` with `terminal.cwd`, `skills.external_dirs`, memory enabled, SOUL symlink.

- [ ] **Step 1: Backup and rollback.** Record `hermes profile list` output. Rollback: `hermes profile delete supervisor` after checking its dependent jobs; no other profile is touched.
- [ ] **Step 2: Create.** `hermes profile create supervisor --clone-from executor --description "Academic Space PI: research-space ideation, plans, evidence review"` (executor is the closest seed: no channels, built-in memory). Then read back `config get memory`, `plugins list`, and list inherited plugins to Tai.
- [ ] **Step 3: Identity.** Back up the runtime `SOUL.md` to the profile's `backups/`, then replace it by symlink to `docs/profiles/supervisor/SOUL.md` per the canonical-identity procedure in `hermes-fleet-admin`.
- [ ] **Step 4: Directory and skills.**
  `hermes -p supervisor config set terminal.cwd ~/academic-space/research-space`
  `hermes -p supervisor config set skills.external_dirs '["~/.agents/skills","~/academic-space/research-space/.agents/plugins/openscience-adapter/skills","~/academic-space/research-space/.openscience/skills"]'`
  Read back both. Keep `~/.agents/skills` only if the executor seed already had it.
- [ ] **Step 5: Verify.** `COLUMNS=250 hermes -p supervisor skills list --enabled-only` shows the 46 adapter skills plus the 3 OpenScience skills. Fresh session: `hermes -p supervisor chat -q "Read-only check, change nothing: 1) name and role 2) run pwd 3) load skill acceptance-checks and quote its first heading 4) load skill compose-research and quote its first heading"`. Expected: role Supervisor, pwd research-space, both headings quoted.
- [ ] **Step 6: Report** saved vs observed separately. Update the README runtime-status table. Gateway/Discord and Bot Chat registration stay untested.
