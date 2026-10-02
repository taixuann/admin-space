# Research-projects guidance

This repository hosts reproducible scientific research projects, empirical
studies, and project-level progression.

## Canonical skill surface and routing

Use the reference-routed domain skills under `.agents/skills/`:

- `study`: `/study init`, `/study prepare`, `/study run`, `/study result`,
  and `/study audit`.
- `research-program`: `/research-program init`, `/research-program create`,
  `/research-program update`, `/research-program capture`,
  `/research-program prepare`, and `/research-program run`.
- `consulting-pptx`: executive and presentation slide deck production.

Generic scientific capabilities are external:

- **OpenScience**: scientific reasoning, targeted scholarly lookup, formal literature review,
  scientific writing, citation management, peer review, statistics/method critique.
- **HyperResearch**: deep exploratory research, broad literature landscape discovery,
  citation-chain traversal, persistent research corpus/vault, adversarial synthesis.
- **Superpowers**: software-engineering execution only.

## Workflow and Tool Ownership Boundaries

- **Research Projects**: Owns canonical project state, empirical Study leaves
  (`STUDY.md`, `input.yaml`, `runs/`, `results/`), project progression (`progress/`),
  and data parsing contracts.
- **OpenScience**: Bounded scientific reasoning, hypotheses, literature search,
  method critique, peer review, and manuscript section drafting. Returns bounded
  findings only; does not mutate Research Projects state directly.
- **HyperResearch**: Deep exploratory research and persistent research vault. The vault
  is external research memory, not canonical Research Projects state.
- **Superpowers**: Used strictly for software-engineering execution discipline
  (planning, TDD, systematic debugging, verification). Not the scientific research workflow.
- **consulting-pptx**: Slide deck layout, styling, and rendering; consumes accepted
  evidence without recalculation.

High-value routing invariants:

| Requested target/state | Required owner | Boundary |
| --- | --- | --- |
| Study intent and exact input selection | `/study init` | creates or updates only `STUDY.md` and `input.yaml` |
| prepared scientific implementation | `/study prepare` | prepares code and records its fingerprint; does not execute |
| scientific execution | `/study run` | validates preparation, then records one immutable run lock |
| evidence summary or portable package | `/study result` | follows explicitly selected run locks; no recomputation |
| Study structure and provenance audit | `/study audit` | read-only; no scientific acceptance |
| cross-project scientific memory | AutoSci | separate future scientist-reviewed synthesis/ingestion; Study RESULT never mutates AutoSci |
| project progression, goals, and stories | `/research-program` (init/create/update/capture) | progression is project-level; Study owns execution evidence |
| presentation planning and slide production | `/research-program prepare` then `/research-program run` | PREPARE authors the plan; RUN delegates slide construction to `consulting-pptx` |
| targeted lookup & scientific reasoning | OpenScience | bounded findings; no direct state mutation |
| deep landscape exploration | HyperResearch | exploratory notes and vault; external research memory |
| manuscript writing and review | OpenScience | consumes accepted RE-* evidence and Research Program context |


## Boundaries

- Do not move, rename, delete, or overwrite raw research evidence without an
  approved manifest and a post-change hash/reference check.
- Keep scientific interpretation, protocol changes, and publication selection
  behind the owning project's human gates.
- Treat `/Users/tai/workspace/tools` as the owner of reusable executable
  capabilities. Do not copy a shared tool into a project or skill.
- Active research projects reside under `active-projects/`. Raw evidence
  remains immutable and owned by the project.

## Git workflow

This is a personal scientific research repository.

Default:
- work directly on `main`;
- make small bounded commits;
- validate relevant behavior before commit/push;
- use Git for history, provenance, and rollback.

Do not create a branch, worktree, or pull request by default.

Use a temporary branch/worktree only when:
- a large/high-risk migration has significant blast radius;
- isolated experimentation is genuinely safer;
- external collaboration/review specifically requires a PR.

Do not create Git ceremony merely because a Linear issue exists.

### Operating model
- **Normal research / tooling change**: `main` → inspect → edit → run relevant validation → inspect diff → bounded commit → push.
- **Larger work**: `main` → several bounded commits → verify each useful boundary → push.
- **Exception**: large/high-risk migration → temporary branch/worktree if isolation materially helps → merge back → remove temporary branch. PR is optional, not mandatory.
- **Linear role**: roadmap, backlog, milestones, and decision/obligation tracking; not a Git execution engine requiring mandatory branch/worktree/PR per issue.
- **Superpowers role**: used for planning, TDD, debugging, and verification discipline; does not require branching or PRs for every task.

## Execution sessions and lifecycle freeze

- The scientific lifecycle is frozen. New agents, routers, workflow engines,
  DAG runtimes, persistence services, or artifact databases require observed
  failure evidence and OBSERVE → PROPOSE → REVIEW → ACCEPT → UPDATE.
