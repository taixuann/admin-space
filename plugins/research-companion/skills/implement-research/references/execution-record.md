# Plan-led execution record

Use a file-first record for one selected plan and one executed analysis.
This owner applies only to explicitly selected new plan-led analysis folders.
The schema-versioned lock is the evidence record consumed by Compose and Crate;
it does not migrate or replace records in existing Study leaves.

## Folder ownership

```text
<analysis>/
  spec/                     # reasoning.md, methods.md, requirements.md
  plans/                    # YYYY-MM-DD_<name>_plan.html
  input.yaml                # exact source declarations and hashes
  scripts/                  # entrypoint and tested support
    run.py                  # main execution entrypoint
    modules/                # shared utilities (theme.py, data.py, plot.py)
    specific/               # study-specific domain logic and fitting
    tests/                  # synthetic unit tests for TDD
  runs/<run-id>/
    run.lock.yaml           # sole execution/provenance authority
    figures/                # categorized figure bundles
      primary/              # DDMMYY-HHMMSS_<study>_<purpose>/
        <figure-id>.pdf     # primary vector export
        <figure-id>.png     # raster preview
        plot.yaml           # native FigRecipe recipe
        plot.meta.yaml      # series & palette provenance
        plot_data/          # per-series CSVs
      diagnostic/           # extraction & QC bundles
      extended/             # closeups & supplementary bundles
    tables/                 # numerical outputs (only when declared in spec/requirements.md)
```

Create directories only for actual consumers. Refuse an occupied run ID or
output path before writing. Keep every completed or failed run unchanged. New
executions get new IDs. Retain a failed allocated run with its actual error and
any partial outputs.
Do not treat copied prior outputs as newly computed evidence.

## Required record contents

Use `schema_version: 1` and `owner: implement-research`. Record:

- Run ID, COMPLETED/FAILED outcome, start and finish times with time zone.
- Exact question, selected plan path, revision, hash and actual user authorization.
- Input manifest hash and each object ID, role, source path and SHA-256.
- Method parameters, omission rules and validation outcomes.
- Entrypoint and every consumed code/helper file, with hash and recovery path.
- Interpreter path, Python/package versions, command, exit code and failure details.
- Local style/palette files consumed, with hashes and recovery copies.
- Every produced figure, recipe, data file, table and log, with path and hash.
- Input and protected-file checks before/after execution.
- Scientific acceptance `NOT_ASSESSED` unless the human study owner or PI explicitly records a decision; never infer acceptance from process success, plan approval, or output appearance.

Before execution, verify every declared input hash and exact recovered code.
Resolve relative input paths from the explicitly selected project root; do not
search by filename or infer a project root. Absolute sources are allowed only
when explicitly selected in the manifest. Reject symlinked sources, code,
snapshots, outputs and path escapes. Capture the environment actually used.
Snapshot external helpers consumed by the script or bind them to recoverable
versions; hashing an unavailable local path alone is not code recovery.

Write the final lock once after post-execution checks. A failed numerical or
output validation produces FAILED, even when the subprocess exits zero. Retain
partial evidence. If setup fails after allocation, preserve that directory and
record the actual setup error; never claim a process ran when it did not.

Use a bounded project-local invocation, not a new scheduler or persistence
service. No code snapshot proves dependency availability on another machine.
