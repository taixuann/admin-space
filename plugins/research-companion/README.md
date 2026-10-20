# Research Companion Plugin

A global Research Companion plugin for scientific research workflows. Research data and scientific writes remain under the selected project’s owners and gates.
It provides consultation, intent capture, planning, execution, evidence materialization and archival packaging.

1. **Study evidence**: Existing Study leaves remain owned by Study. Plan Research → Implement Research applies to explicitly selected new plan-led analysis folders.
2. **Project progression**: Research Progress owns project goals, logs, stories and presentation planning; it delegates slide construction to `consulting-pptx`.

---

## Packaged script paths

When a skill invokes a script bundled here, resolve the absolute script path from that skill’s loaded `SKILL.md` location. The plugin root is two directories above the skill folder. Do not assume the current project contains this plugin or use a path under the selected project to locate bundled scripts.

## Global use

research-capture captures explicit scientific research intent only. It uses the Agents Ticket database current New Intent template, sets new tickets to Research and Capture, keeps planning tabs empty, checks for duplicates, preserves supplied wording and sources, and reads the result back. Tools, skills, agents, bots, plugins and their coordination belong to Admin. Capture does not authorize scientific planning, execution or acceptance.

## Architecture & Directory Structure

```text
research-companion/
├── plugin.json               # Manifest
├── README.md                 # User guide & component index
├── rules/
│   └── AGENTS.md             # Owner-routing rules & evidence invariants
├── references/               # Shared single source of truth
│   ├── README.md             # Concepts and ontology
│   ├── consultation.md       # Consultation rules
│   ├── plans.md              # Research plan schemas
│   ├── study-planning.md     # Study method boundaries
│   ├── transitions.md        # Shared owner and handoff contract
│   ├── method-examples.md    # Optional, non-universal analysis and style examples
│   └── progress-synthesis.md # Research Progress-owned evidence and presentation actions
├── skills/                   # Primary lifecycle skills
│   ├── ask-einstein/         # Meta-routing dispatcher (using-superpowers style)
│   ├── brainstorming/        # Scientific ideation across 9 named moves
│   ├── plan-research/        # Question-led HTML planning (spec/ & plans/)
│   ├── implement-research/   # TDD code & FigRecipe execution (scripts/ & runs/)
│   ├── compose-research/     # Result synthesis into RESULT.md & evidence ledger
│   └── ro-crate-research/    # Archival packaging into RO-Crate 1.3
└── external-skills/          # Bundled domain advisor & utility skills
    ├── statistical-conventions/
    ├── dimensional-analysis/
    ├── uncertainty-and-units/
    ├── acceptance-checks/
    ├── hypotheses/
    ├── experimental-design/
    ├── consulting-pptx/
    ├── literature-review/
    └── research-lookup/
```

---

## Owner and handoff contract

Use [references/transitions.md](references/transitions.md) as the single routing authority. Brainstorming is conditional on an open direction; fixed descriptive work can proceed within its selected scope. A completed run grants no implicit next action, and process completion is separate from artifact disposition and scientific acceptance.

### 1. Study Level
- **Brainstorming (`/brainstorming`)**: Explore mechanisms, anomalies, and parameter boundaries.
- **Plan Research (`/plan-research`)**: Author `<analysis>/spec/` and `<analysis>/plans/YYYY-MM-DD_<name>_plan.html` for a selected new plan-led analysis.
- **Implement Research (`/implement-research`)**: TDD test suites, `scripts/run.py`, FigRecipe hierarchical bundles (`figures/primary/`, `diagnostic/`, `extended/`), and `runs/<run-id>/run.lock.yaml`.
- **Compose Research (`/compose-research`)**: Materialize findings from sealed run locks into `results/RESULT.md` and staged artifacts in `results/artifacts/`.
- **RO-Crate Packaging (`/ro-crate-research`)**: Create a self-contained, standardized RO-Crate 1.3 package at `results/package/`.

### 2. Progress Level
- **Progress Documentation (`progress/docs/`)**:
  - `progress/docs/goals/`: Long-form goal documents linking to accepted study findings.
  - `progress/docs/plans/`: Presentation plans (`YYYY-MM-DD_weekly_plan.html`).
  - `progress/docs/log.md`: Research Progress-owned provenance entries for explicitly selected evidence and goals.
- **Presentation Execution (`consulting-pptx`)**: Render deck into self-contained dated folder `progress/presentation/weekly/<date>/`:
  - Interactive HTML deck (`<purpose>.html`)
  - PowerPoint presentation (`<purpose>.pptx`)
  - Vector PDF slide export (`<purpose>.pdf`)
  - Embedded figures and styling assets.

---

## Ask Einstein: The Meta-Router

`/ask-einstein` reads selected context and advises or routes an unclear action. It does not own Study or Research Progress records, and status-only discussion does not authorize a write.
