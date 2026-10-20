---
name: ro-crate-research
description: Package explicitly scoped scientific study outputs, raw inputs, and code snapshots into an RO-Crate 1.3-targeted package.
---

# RO-Crate Research (`/ro-crate-research`)

Assembles a self-contained Research Object Crate (RO-Crate 1.3-targeted) from verified study run locks, inputs, and code snapshots.

## 1. When to Use

- When a study has completed its evaluation and findings have been materialized via `compose-research`.
- When preparing an archival package for peer-reviewed publication, dataset deposit (e.g. Zenodo, OSF), or inter-laboratory replication.
- When you need a portable self-describing directory containing raw inputs, outputs, code, and `ro-crate-metadata.json`.

## 2. Mandatory Clarification Protocol

Before generating an RO-Crate package, the agent MUST NOT blindly dump all run outputs. The agent must clarify or check four specific parameters:
1. **Output Scope**: Choose exactly one: **accepted-only** (`--only-accepted`), or **all selected outputs with explicit dispositions** (`--include-all-selected-outputs`). The all-selected choice includes REJECTED, AMBIGUOUS, and SUPERSEDED outputs only when each output and run lock is bound by `results/evidence-ledger.json`; absent, stale, or unsupported dispositions fail closed. Never infer a disposition. `MISSING` is bookkeeping-only, excluded from scientific acceptance and packaging.
2. **Image Formats**: Which image formats are required?
   - Publication-quality vector (`PDF`)
   - Web raster preview (`PNG`)
   - Tabular / raw data (`CSV`, `parquet`)
   - (Specified via `--formats pdf,png`)
3. **Input Scope**: Include full raw instrument curves declared in `input.yaml`, or only derived tables?
4. **Crate Metadata**: Ask for the applicable license and require it explicitly (`--license`). Do not guess or assign a legal license. Record optional author name (`--author`) and study abstract (`--description`).

---

## 3. Invariants

- **Standard Conformance**: Uses the RO-Crate 1.3 identifiers (`https://w3id.org/ro/crate/1.3` and its `/context`). A synthetic crate passed the required 1.3 profile checks with `roc-validator` 0.12.2; each generated package still needs its own independent validation before release.
- **Checksum Verification**: Every packaged file (raw inputs, figures, tables, code) is checked against its recorded SHA-256 hash. Any mismatch fails closed immediately.
- **Atomic Assembly**: Packages are prepared in a temporary staging folder and placed at the destination atomically.
- **Fail-Closed on Overwrite**: Never silently overwrites an existing `results/package/` directory without the `--replace-package` flag.
- **Parser Dependency**: PyYAML is required for publication evidence. If it is unavailable, the command stops with an actionable dependency error; there is no permissive fallback parser.

---

## 4. Usage & CLI Command

### Dry-Run Verification (Check without Writing):
```bash
python <plugin-root>/skills/ro-crate-research/scripts/package_crate.py <study-root> \
  --project-root <project-root> --run-id <run-id-1> \
  --license "<explicit-license-identifier-or-URL>" --only-accepted --formats pdf,png --check
```

### Packaging Execution:
```bash
python <plugin-root>/skills/ro-crate-research/scripts/package_crate.py <study-root> \
  --project-root <project-root> --run-id <run-id-1> [--run-id <run-id-2>] \
  --only-accepted --formats pdf,png [--exclude-inputs] \
  --license "<explicit-license-identifier-or-URL>" [--output-dir results/package] \
  [--author "Scientist Name"] [--replace-package]
```

### Options:
- `study-root`: Path to the study directory (e.g., `studies/s-switching-analysis`).
- `--run-id`: One or more completed plan-led schema v1 run IDs. Unsupported owner/schema records are rejected.
- `--project-root`: Explicit root for resolving relative inputs recorded in the run lock.
- `--output-dir`: Target package path (defaults to `results/package`).
- Exactly one required output-scope flag: `--only-accepted` packages only ledger-bound ACCEPTED outputs; `--include-all-selected-outputs` packages selected outputs with explicit ACCEPTED, REJECTED, AMBIGUOUS, or SUPERSEDED dispositions. The latter binds every selected output hash and selected run lock to `results/evidence-ledger.json`; absent, stale, MISSING, or unsupported entries stop packaging. The selected scope and each output disposition appear in RO-Crate metadata and `README.md`.
- Use `--include-all-selected-outputs` only when the user explicitly chose all-selected scope and every package candidate has a required ledger disposition.
- `--formats`: Comma-separated list of output presentation extensions (e.g. `pdf,png,csv`); required provenance, inputs, and code are not filtered.
- `--exclude-inputs`: Explicitly omit raw inputs; the README records the package as outputs-only.
- `--check`: Dry-run mode. Previews package contents, file counts, and verifies hashes without writing.
- `--author`: Author or creator to record in the RO-Crate metadata.
- `--license` (required): Explicit license identifier or URL supplied by the responsible user; the skill never chooses one.
- `--description`: Custom description or abstract for the dataset entity.
- `--replace-package`: Overwrite existing crate directory if one already exists.

## 4. Package Structure

```text
results/package/
├── ro-crate-metadata.json        # RO-Crate JSON-LD manifest
├── README.md                     # Human-readable study overview & run manifest
├── inputs/                       # Raw input files organized by object_id
│   └── <object-id>/
├── outputs/                      # Output figures and tables from selected runs
│   └── <run-id>/
└── code/                         # Exact source code snapshots used during execution
```
