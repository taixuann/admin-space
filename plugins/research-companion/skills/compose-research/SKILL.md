---
name: compose-research
description: Synthesize verified findings from completed study runs into results/RESULT.md and staged evidence artifacts. Strictly read-only on calculations.
---

# Compose Research (`/compose-research`)

Extract, assess, and synthesize scientific evidence from completed study runs into a permanent `results/` folder without rerunning calculations or modifying raw experimental data.

## 1. When to Use

- When an empirical study run has finished and sealed its outputs into `runs/<run-id>/run.lock.yaml`.
- When you want to materialize findings into `results/RESULT.md` and stage primary figure bundles into `results/artifacts/<run-id>/`.
- When the human study owner or PI records explicit scientific assessments (`ACCEPTED`, `REJECTED`, `AMBIGUOUS`, `SUPERSEDED`) against specific outputs. `MISSING` is bookkeeping-only and cannot be accepted or packaged.
- Before archiving a study via `ro-crate-research` or logging progress into `progress/docs/log.md`.

## 2. Invariants

- **Strict Read-Only on Computation**: Never reruns simulations, fits models, or alters raw input files.
- **Fail-Closed Verification**: Accepts only completed `implement-research` schema v1 locks, and verifies their required snapshots, inputs, code, outputs, identities, paths, and recorded SHA-256 hashes. Unsupported owners or schemas are reported as unsupported, not migrated. Scientific acceptance is recorded only by the human study owner or PI and is never inferred from process success.
- **Transactional Atomic Staging**: Results are staged in a temporary directory and moved into `results/` atomically; prior results are restored if any failure occurs.
- **Relative Path Governance**: Respects shared contracts defined in [../../references/progress-synthesis.md](../../references/progress-synthesis.md) and [../../references/transitions.md](../../references/transitions.md).
- **Parser Dependency**: PyYAML is required for publication evidence. If it is unavailable, the command stops with an actionable dependency error; there is no permissive fallback parser.

## 3. Usage & CLI Command

### Plan-Led Execution (Recommended):
```bash
python <plugin-root>/skills/compose-research/scripts/compose.py <study-root> \
  --project-root <project-root> \
  --plan <study-root>/plans/YYYY-MM-DD_<name>_result_plan.html \
  --authorization "<human authorization>" [--replace-result]
```

### Dry-Run Verification (Check without Writing):
```bash
python <plugin-root>/skills/compose-research/scripts/compose.py <study-root> \
  --project-root <project-root> \
  --plan <study-root>/plans/YYYY-MM-DD_<name>_result_plan.html \
  --authorization "<human authorization>" --check
```

### Manual CLI Overrides:
```bash
python <plugin-root>/skills/compose-research/scripts/compose.py <study-root> \
  --project-root <project-root> --run-id <run-id-1> [--run-id <run-id-2>] \
  --assess <run-id>/<output-id>=ACCEPTED|REJECTED|AMBIGUOUS|SUPERSEDED \
  --authorization "<human authorization>" [--replace-result] \
  [--interpret "Verbatim scientist interpretation note"]
```

### Options:
- `study-root`: Path to the study directory (e.g., `studies/s-switching-analysis`).
- `--plan`: Path to a structured Result Synthesis Plan (`.html` or `.yaml`) with `schema_version: 1`, `plan_id`, `revision`, `decision_source`, `run_bindings` (run ID plus lock SHA-256), scoped `assessments`, `questions`, `views`, `observations`, and optional interpretation. Heuristic plan parsing is not supported. Evidence references use `run-id/object-id`; each question must match content under its exact `spec/reasoning.md` heading, views must select accepted evidence linked to a question, and observation values/units/method/limits are copied from the plan without calculation.
- `questions`: Each item has `question_id`, `text`, `source_heading`, and non-empty `evidence_ids`.
- `views`: Each item has `view_id`, `evidence_id`, and `label`. Use an empty list when no presentation views are selected.
- `observations`: Each item has `observation_id`, `question_id`, `evidence_ids`, `label`, `value`, `unit`, `method`, and `limits`. `value` is a quoted string so its supplied representation is preserved. Use an empty list when the plan supplies no observations.
- `--check`: Dry-run mode. Previews the planned evidence mapping, staged paths, and verifies all SHA-256 hashes without modifying files on disk.
- `--run-id`: One or more completed run IDs to include (overrides or supplements plan).
- `--assess`: Assign disposition to a run-scoped output ID (e.g. `run-1/fig:vt_shift=ACCEPTED`).
- `--authorization`: Record the human authorization for explicit decisions. Missing decisions are never inferred.
- `--project-root`: Explicit root for resolving relative input manifest paths.
- `--replace-result`: Overwrite existing `RESULT.md` and `evidence-ledger.json` (required if updating).
- `--interpret`: Provide verbatim scientist notes to append to `RESULT.md`.

## 4. Generated Artifacts

1. `results/RESULT.md`:
   - Answers the primary question from `spec/reasoning.md`.
   - Cites selected run IDs and verification statuses.
   - Summarizes evaluated outputs in a table with stable `RE-xx` evidence IDs and links to staged artifacts.
   - Includes limits, dispositions count, and scientist interpretation.
2. `results/evidence-ledger.json`:
   - Machine-readable ledger tracking all outputs, SHA-256 checksums, and disposition decisions.
3. `results/artifacts/<run-id>/`:
   - Copies of all `ACCEPTED` output figures and tables, verifying hash integrity.
