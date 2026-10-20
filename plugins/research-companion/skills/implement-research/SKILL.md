---
name: implement-research
description: Implement and execute an explicitly selected new plan-led analysis. Use when asked to turn its selected plan into tested scripts or an authorized run. Existing Study leaves stay with Study; planning selects the scientific method and implementation follows it.
---

# Implement Research

Turn a study-local plan into validated code and one traceable analysis run.
Use this owner for explicitly selected plan-led analysis folders. Keep
existing Study leaves under their current owner unless migration is authorized.
Read the project's instructions, [plan records](../../references/plans.md),
[state transitions](../../references/transitions.md), and the [execution record](references/execution-record.md).

## 1. Audit the study spec and plan

Read the study's self-contained documentation from:
- `<study-root>/spec/` (`reasoning.md`, `methods.md`, `requirements.md`)
- `<study-root>/plans/` (`YYYY-MM-DD_<name>_plan.html`)

Check the selected plan revision, authorization, analysis contract and task breakdown:
- Question, exact inputs, observation units, parameters, missing/non-finite data handling.
- Verify tasks are decomposed into bite-sized units with explicit files and tests.
- Compare these decisions with the scientist's instructions and source file headers.
- Return unresolved scientific choices to `ask-einstein` or `plan-research`;
  do not invent a fit, threshold, window, or error bar while coding.
- An explicit request to implement and run authorizes only that selected scope. Essential unresolved method choices return to planning.

## 2. PREPARE: Task-by-task implementation with TDD

Adapt the canonical Study script layout (`scripts/modules/`, `scripts/specific/`, `scripts/run.py`), retaining `scripts/tests/` for synthetic unit testing.
Initialize standard scaffold via:
`python <plugin-root>/skills/implement-research/scripts/scaffold.py <study-root>`
(renders templates from `assets/templates/scripts/` directly into the study leaf).

1. **Input reader & validation**:
   - Read only the exact entries in `input.yaml` (`schema_version: 1`, `owner: implement-research`, and nested `inputs[].files[]` with `path` and SHA-256).
   - Resolve relative paths from the explicitly selected project root. Reject symlinks, absent or malformed hashes, changed files, malformed nested records and filename-search fallbacks.
   - Test supported formats and edge cases with synthetic data.
2. **Task 2: Numerical extraction & summary metrics**:
   - Write tests in `scripts/tests/test_analysis.py` (window boundaries, sample means, ratios, SD).
   - Implement metrics in `scripts/specific/analysis.py`.
   - Verify tests pass without reading real empirical data.
3. **Visualization**, when selected by the plan:
   - Follow the selected output and styling requirements. Do not impose a global plot style or choose a case-specific preset without authorization.
   - Save declared outputs through `modules/plot.py`.
4. **Task 4: Entrypoint & composition**:
   - Keep `scripts/run.py` as the execution owner. It imports `specific.analysis.run_study_analysis(data, params)`; select another `specific.<NAME>` module with `--specific` only when the plan requires it.
   - Pass `--study-root`, `--project-root`, `--plan`, and `--authorization` explicitly. Use `--run-id` or `--out` to select the unique run allocation; declare parameter overrides with `--param`, `--params-json`, or the `STUDY_PARAMS` JSON environment variable.
   - Never generate ad-hoc outer `execute.py` or `helper-source.yaml` scripts.
   - Run tests: `.venv/bin/python -m unittest discover -s scripts/tests -p "test_*.py"`.

Completion of PREPARE: relevant synthetic tests pass, syntax compiles, module
boundaries hold, and selected code and input records can be recovered. No
empirical calculations occur during prepare.

## 3. RUN: Real execution and immutable provenance

Execute the validated code once against the declared raw inputs:
1. **Pre-flight inventory & scope gate**:
   - Verify SHA-256 hashes of inputs declared in `input.yaml`.
   - Inventory protected assets: `spec/`, `plans/`, `scripts/`, `color-code.yaml`.
   - Gate `tables/`: Only generate tabular files if their exact schema and names are declared in `spec/requirements.md`. Do not spawn unapproved tables.
2. **Run allocation & clean environment**:
   - Allocate a unique run directory. Reject an occupied path before writing; preserve an allocated directory and record setup or execution errors as `FAILED`.
   - Prohibit polluting the run folder with runtime cache directories (e.g. `runtime/`, `matplotlib/`, `scitex/`). Configure `MPLCONFIGDIR` and temporary directories in system temp (`/tmp`).
   - Snapshot the selected plan, `input.yaml`, executed code and consumed local style dependencies into the run folder with hashes.
   - Record environment: interpreter, package versions, command, parameters, timestamps.
3. **Execute entrypoint & Figure bundle hierarchy**:
   - Run `scripts/run.py` within isolated environment.
   - Group generated figures into 3 functional subdirectories under `figures/`:
     - `figures/primary/`: Core deliverables answering the research question.
     - `figures/diagnostic/`: Quality control, extraction interval verification, transient checks.
     - `figures/extended/`: Zoomed closeups, supplementary, or exploratory comparisons.
   - Package each figure in its own self-contained bundle directory named `DDMMYY-HHMMSS_<study>_<purpose>/`, preserving the entire native FigRecipe ecosystem:
     - Primary vector export: `<figure_id>.pdf`
     - Raster visual preview: `<figure_id>.png`
     - Native FigRecipe recipe: `plot.yaml` (or `<figure_id>.yaml`)
     - Raw data series: `plot_data/*.csv` (or `<figure_id>_data/*.csv`)
     - Provenance metadata: `<figure_id>.meta.yaml`
4. **Post-flight verification & seal execution lock**:
   - Verify that all declared figures and tables exist and are non-empty.
   - Disallow symlinked outputs.
   - Write `runs/<run-id>/run.lock.yaml` indexing all outputs with SHA-256 digests.
   - Set status to `COMPLETED` only after execution and required-output checks pass; otherwise record `FAILED` and preserve partial outputs.
   - Default scientific acceptance to `NOT_ASSESSED`. Compose and Crate consume this record under the plan-led v1 contract. Never overwrite or silently retry.

## 4. Review, update index, and report

1. Inspect delivered tables and figures. Confirm provenance and preservation.
2. Update the status row in `<study-root>/README.md` to `DONE` (recording the target run ID).
3. Separate process success from scientific interpretation and acceptance.
4. Report the run path, key observations, and material limitations.
