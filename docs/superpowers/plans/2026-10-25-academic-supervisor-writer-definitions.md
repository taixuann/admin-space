```yaml
requester: secretary
space: ~/.agents
scope: [docs/profiles/supervisor/, docs/profiles/writer/, docs/profiles/README.md]
checks:
  - test -f docs/profiles/supervisor/README.md -a -f docs/profiles/supervisor/SOUL.md -a -f docs/profiles/supervisor/capabilities.yaml
  - test -f docs/profiles/writer/README.md -a -f docs/profiles/writer/SOUL.md -a -f docs/profiles/writer/capabilities.yaml
  - python3 -c "import yaml,sys;[yaml.safe_load(open(f'docs/profiles/{p}/capabilities.yaml')) for p in ('supervisor','writer')]"
  - every relative Markdown link in the changed files resolves to an existing file
  - hermes profile list shows no new profile (definition-only)
  - git status shows no changes outside scope
report: kanban card comment + kanban_complete summary to Secretary
```

# Academic Supervisor and Writer profile definitions (draft)

Requested by Tai 2026-10-25. Definition-only: no runtime profile, model, memory, plugin or identity changes.

## Goal

Create draft Admin-owned profile definitions for two Academic Space bots, **supervisor** and **writer**, following the `hermes-fleet-admin` skill (profile lifecycle, Define phase) and `docs/profiles/AGENTS.md`.

## Settled decisions

- The research-space "OpenCode worker" / experimenter role is the existing shared **executor**; do not define a separate experimenter profile. Supervisor hands execution plans to executor.
- Definitions live in `~/.agents/docs/profiles/<name>/` (Admin convention), not in research-space.
- Status: draft definition. Model = preference only, runtime-managed.

## Inputs (read-only)

- `~/academic-space/research-space/AGENTS.md`, `docs/README.md`, `docs/workflows.md`
- Existing drafts: `~/academic-space/research-space/docs/profiles/{supervisor,writer}/{README.md,SOUL.md,capabilities.yaml}`
- `~/academic-space/knowledge-space/AGENTS.md` (writer/supervisor read knowledge; knowledge-space is not their write area)
- `~/academic-space/academic-architecture.html` (roles and flows)
- Pattern to match: `docs/profiles/executor/`, `docs/profiles/forge/`, `docs/profiles/AGENTS.md`

Never edit anything under `~/academic-space`.

## Steps

1. Load `hermes-fleet-admin`, `documentation-writer`, `writing-for-agents`, `superpowers:executing-plans`.
2. For each of supervisor and writer, write `README.md` with the three sections required by `docs/profiles/AGENTS.md` (identity and context incl. model preference, path-based working permissions, memory; capabilities; workflow). Base content on the research-space drafts; fix references: experimenter → executor, working Space = `~/academic-space/research-space`.
3. Write `SOUL.md` as a draft identity (adapted from the research-space draft; mark provenance).
4. Write `capabilities.yaml` as approved-target list (skills, plugins, MCPs, tools). Only list skills/tools that exist on this machine or mark them `status: proposed`.
5. Add both to `docs/profiles/README.md` index as draft.
6. Run every check; report results, deviations, and open questions (e.g. where supervisor's plans live, memory bank choice).

No Archify HTML, no runtime creation, no commits.
