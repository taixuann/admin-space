---
name: plan-research
description: Build and review a question-led HTML research plan, including which analyses to use, why they fit, exact inputs, methods and validation checks. Use for research planning, analysis selection or revisions before implement-research or an existing Study action. Planning does not execute calculations.
---

# Plan Research

Write HTML plans in English. Use `simple-english` in Plain mode.
Keep source facts, identifiers and uncertainty intact.
Use the scientist's requested bold labels and lists for visual structure.
Bold only short decision, status or action labels. Keep explanations in normal text.
Use numbered lists for ordered steps and bullets for parallel choices.
These formatting preferences override Simple English's restrictions on bold.

Read [plugin context](../../references/README.md),
[consultation guide](../../references/consultation.md),
[plan records](../../references/plans.md), and
[state transitions](../../references/transitions.md).
Use [optional method examples](../../references/method-examples.md) only when
they fit the selected question; they are not defaults.
For Study INIT plans, use [Study planning coverage](../../references/study-planning.md)
to check the template against the current owning procedure.

---

## Choose support for the open decision

```text
[Selected scope] ──► [Resolve essential choices] ──► [HTML proposal]
```

### Consultation and ideation (conditional)

1. Use [`ask-einstein`](../ask-einstein/SKILL.md) when routing or selected context needs consultation.
2. Use [`brainstorming`](../brainstorming/SKILL.md) only when the direction or question remains open. For fixed descriptive work, preserve the selected scope and identify only the choices still needed to make its method executable.

### Method review (as needed)

Use a domain procedure when a concrete unresolved choice needs it. Do not run
every advisor for every plan. Keep the reason and evidence near the decision it
informs.

1. **Statistical conventions**, when inference or dependence structure is unresolved:
   - Consult [`statistical-conventions`](../../external-skills/statistical-conventions/SKILL.md) when the decision needs it.
   - Define the independent unit of analysis (avoid pseudoreplication: e.g. per-device vs per-pulse).
   - Settle test selection: paired vs unpaired, parametric vs rank-based.
   - Settle multiplicity corrections (Bonferroni, Holm, Benjamini-Hochberg FDR) when testing multiple outcomes.
   - State whether a claim is descriptive or inferential. Descriptive fitting may summarize selected observations; do not present it as inferential evidence without a suitable design.
2. **Dimensional analysis**, when formulas or unit conversions are material:
   - Consult [`dimensional-analysis`](../../external-skills/dimensional-analysis/SKILL.md) when needed to check the selected formulas.
   - Verify that all equations expand to SI base dimensions (kg, m, s, A, K, mol).
   - Carry exponents through algebraic transformations and verify dimensional homogeneity.
3. **Units and uncertainty**, when reporting or propagation choices affect the result:
   - Consult [`uncertainty-and-units`](../../external-skills/uncertainty-and-units/SKILL.md) when needed.
   - Explicitly track engineering vs SI units across ingestion, processing, and display ($\text{s} \to \mu\text{s}$, $\text{A} \to \text{mA}$, $\Omega \to \text{k}\Omega$).
   - Explicitly state what sample standard deviation $s(I)$ measures (e.g. within-window electronic noise/fluctuation) versus independent replicate uncertainty.

### Specification and checks

1. **Author Specifications in `<study-root>/spec/`**:
   - `reasoning.md`: Physical mechanism, research question, hypotheses, observation units, and replication boundaries.
   - `methods.md`: Method rationale, formulas, extraction windows, exclusion rules, and non-finite data handling.
   - `requirements.md`: Exact outputs, schemas and checks selected for this analysis.
2. **Mechanical Acceptance Checks (`acceptance-checks`)**:
   - Consult [`acceptance-checks`](../../external-skills/acceptance-checks/SKILL.md) when mechanical checks need help defining.
   - Turn every qualitative or quantitative requirement in `requirements.md` into **executable mechanical oracles**:
     - Exact paths and file existence (`figures/primary/*/*.png`, `figures/primary/*/*.pdf`, `run.lock.yaml`).
     - Exact table schemas, column names, and sorting (only if explicitly required).
     - Exact numeric formatting, tolerances, and physical ranges.
     - Style invariants only when selected for this analysis.
   - These criteria form the non-negotiable exit criterion for the implementation runner.

### Task breakdown and HTML proposal

1. **Task Breakdown**:
   Decompose only the work needed by the selected analysis into verifiable tasks.
   Name each deliverable, synthetic checks and completion condition.
2. **Author Standalone HTML Plan**:
   - File path: `<study-root>/plans/YYYY-MM-DD_<name>_plan.html`.
   - Render with the installed `answer-me-with-html` skill, following its current command and resolving the renderer from that skill bundle rather than assuming a machine-specific install path:
     ```bash
     node <answer-me-with-html-skill>/scripts/am.mjs render - -o <path> --no-open
     ```
   - **Single source of truth**: Do NOT create or maintain separate `.md` plan files. The single HTML file serves human inspection (rich cards, flowcharts, callouts) and machine execution (YAML frontmatter and task definitions embedded inside `<textarea id="am-source">`).

### Index maintenance (`README.md`)

Maintain `<study-root>/README.md` adapting index standards:
- **Execution Order & Status Table**: `Plan`, `Title`, `Priority`, `Effort`, `Depends on`, `Status` (`TODO` | `IN PROGRESS` | `DONE` | `BLOCKED` | `REJECTED`), `Target Run`.
- **Plan Naming Convention**: `YYYY-MM-DD_<name>_plan.html`; retain the stable plan identity and revision in its metadata.
- **Specification Pointers**: Direct links to `spec/reasoning.md`, `methods.md`, `requirements.md`.
- **Dependency & Execution Notes**: Exact constraints and historical run records.

---

## Two Planning Modes

`plan-research` operates in two distinct modes depending on lifecycle stage:

### Mode 1: Analysis Implementation Planning (`action: implement`)
Use before code execution when a research question needs an empirical run:
- **Spec Authoring**: `spec/reasoning.md`, `methods.md`, `requirements.md`.
- **Method review**: Use relevant domain procedures only for concrete unresolved choices; state descriptive versus inferential claims. For every window-based analysis, define each window boundary and explicitly state whether each endpoint is included.
- **Task Decomposition**: TDD steps (Reader, Analysis, Visualization, Runner).
- **Output Artifact**: `<study-root>/plans/YYYY-MM-DD_<name>_plan.html` with a stable `plan_id` and positive, increasing `revision`.
- **Handoff Target**: Hand off to [`implement-research`](../implement-research/SKILL.md).

### Mode 2: Result Synthesis Planning (`action: compose`)
Use after a run completes and seals `runs/<run-id>/run.lock.yaml`, BEFORE materializing results into `results/RESULT.md`:
- **Run Selection**: Explicitly pick the target `run-id`(s) to evaluate.
- **Evidence Disposition Proposal**: Record an explicit disposition for each selected output:
  - `ACCEPTED`: Meets all acceptance criteria, clear physical signal, suitable for publication.
  - `REJECTED`: Experimental artifact, instrument compliance limit hit, or corrupt sweep.
  - `AMBIGUOUS`: Inconclusive signal requiring further investigation or replication.
  - `SUPERSEDED`: Replaced by a more recent run or corrected methodology.
- **Question, view and observation bindings**: Follow the Result Plan v1 contract in [plan records](../../references/plans.md). Bind questions to exact `spec/reasoning.md` headings and evidence IDs. Views and supplied observations must reference that evidence; Compose copies values as strings and does not calculate or reinterpret them.
- **Interpretation**: Distinguish scientist-supplied text from model-authored proposals. Never label drafted text as verbatim scientist wording.
- **Output Artifact**: `<study-root>/plans/YYYY-MM-DD_<name>_result_plan.html`.
- **Handoff Target**: Hand off to [`compose-research`](../compose-research/SKILL.md).

---

## Handoff & Execution

1. **For Implementation Plans (`action: implement`)**:
   - `implement-research` audits the selected plan and `<study-root>/spec/`.
   - **PREPARE**: Scaffolds `scripts/` via `python <plugin-root>/skills/implement-research/scripts/scaffold.py <study-root>` and executes tasks sequentially via TDD on synthetic fixtures without reading real measurements.
   - **RUN**: Executes only with explicit scope authorization, preserves any allocated run, checks required outputs, and seals a `COMPLETED` or `FAILED` lock.
   - Keep process status `COMPLETED` separate from scientific acceptance (`NOT_ASSESSED` by default). The human study owner or PI records acceptance explicitly; never infer it from execution status.

2. **For Result Plans (`action: compose`)**:
   - When the scientist approves the Result Plan, invoke `compose-research`:
     ```bash
     python <plugin-root>/skills/compose-research/scripts/compose.py <study-root> \
       --project-root <project-root> --plan <path-to-result-plan.html> \
       --authorization "<human authorization>"
     ```
   - `compose-research` verifies output hashes against the run lock, stages accepted artifacts into `results/artifacts/<run-id>/`, and materializes `results/RESULT.md` and `results/evidence-ledger.json`.
