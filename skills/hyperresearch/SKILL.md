---
name: hyperresearch
description: >
  Scientific literature intelligence via HyperResearch across 4 operational levels.
  Use whenever:
  (1) Looking up existing research notes, mechanisms, or indexed claims in the vault (Level 0: Instant Vault Retrieval),
  (2) Searching academic sources (OpenAlex, Crossref, CORE, PubMed) or running adversarial checks ("criticism of X", "prior art on X") for novelty/ideation (Level 1: Targeted Scholar & Adversarial),
  (3) Generating a fast, bounded landscape report or survey draft (Level 2: Light Bounded Synthesis, ~20 min),
  (4) Running an exhaustive 16-step deep literature pipeline with adversarial critics (Level 3: Full Deep Pipeline, ~2 hours — opt-in only).
  CRITICAL: Never default to Level 3 for routine lookups or novelty checks. Use Level 0 or Level 1.
---

# HyperResearch — Tiered Scientific Literature Intelligence

HyperResearch serves as the external scientific evidence and literature knowledge substrate. It operates across **4 distinct levels** to balance depth against speed and cost.

## CLI execution

Run native CLI commands from `/Users/tai/hyperresearch`. Vault discovery uses the working directory.
The global helper at `scripts/hr_bridge.py` sets this directory for you.
CLI lookup commands automatically sync the derived SQLite index and need write access to `.hyperresearch/`.
If a sandbox blocks the database, request access to the existing vault before retrying.

## The 4 Operational Levels

| Level | Name | Latency | When to use | Primary Tool / Command |
|---|---|---|---|---|
| **Level 0** | **Instant Vault Retrieval** | < 2 sec | Read existing notes, verify mechanisms, check indexed claims, answer project literature questions. | MCP tools (`search_notes`, `read_note`) or `python3 /Users/tai/.agents/skills/hyperresearch/scripts/hr_bridge.py level0-search "<query>"` |
| **Level 1** | **Targeted Scholar & Adversarial** | 10–45 sec | Verify novelty/prior-art (`$novelty`), fetch a dropped paper URL/DOI into Markdown, search counter-arguments/criticisms. | `python3 /Users/tai/.agents/skills/hyperresearch/scripts/hr_bridge.py level1-scholar "<query>"` or `level1-adversarial "<idea>"` |
| **Level 2** | **Light Bounded Synthesis** | 15–30 min | Fast landscape scoping before starting a new direction, drafting a survey/related work section from scratch. | `/Users/tai/hyperresearch/.venv/bin/hyperresearch run init <tag> --profile light` (5 steps: decompose -> sweep -> single draft -> polish -> readability) |
| **Level 3** | **Full Deep Pipeline** | 1.5–2.5 hr | Flagship literature reviews, comprehensive thesis background, major contested domains with severe contradictions. **Opt-in only.** | `/hyperresearch <query>` (Full 16-step pipeline with triple draft ensemble and 4 adversarial critics) |

---

## Non-Negotiable Rules

1. **NEVER default to Level 3.** Routine tasks (ideating, novelty screening, drafting sections, looking up numbers) must use Level 0 or Level 1. Launching a Level 3 run for a routine check is a process violation.
2. **Read before claiming.** Attribute facts to specific note IDs or DOI records returned by Level 0 or Level 1 queries.
3. **Markdown vault is canonical.** Saved notes reside under `research/notes/*.md` with raw PDFs in `research/raw/*.pdf`.

---

## Workflows by Task

### 1. Novelty Verification (AutoSci `$novelty`)
When evaluating an idea's novelty:
```bash
python3 /Users/tai/.agents/skills/hyperresearch/scripts/hr_bridge.py level1-adversarial "<idea description>"
```
This queries OpenAlex, Crossref, and CORE for prior art, criticisms, and boundary conditions across 3 targeted queries in under 30 seconds.

### 2. Ideation Landscape Scan (AutoSci `$ideate` Phase 1)
First, check the local vault for existing coverage (Level 0):
```bash
python3 /Users/tai/.agents/skills/hyperresearch/scripts/hr_bridge.py level0-search "<topic or mechanism>"
```
If no notes exist, run a fast scholar search (Level 1) to identify 5–10 canonical papers:
```bash
python3 /Users/tai/.agents/skills/hyperresearch/scripts/hr_bridge.py level1-scholar "<topic or mechanism>" --limit 10
```

### 3. Fetching a Paper into the Vault
When you have a DOI or paper URL (arXiv, Nature, Science, etc.):
```bash
python3 /Users/tai/.agents/skills/hyperresearch/scripts/hr_bridge.py level1-fetch "<url_or_doi>"
```
Extracts full text via `pymupdf`, resolves open-access copies via Unpaywall/Europe PMC if paywalled, and writes a clean Markdown note to `research/notes/`.

### 4. Survey / Related Work (AutoSci `$survey`)
- **If a final report exists**: Read `research/notes/final_report_<tag>.md` and synthesize directly into LaTeX.
- **If starting from zero**: Run Level 2 (Light synthesis, ~20 min) to produce a single synthesized draft, then format into LaTeX.

### 5. Deep Literature Report (Standalone `$hyperresearch`)
Only run when the user explicitly requests an exhaustive, multi-hour deep dive:
- Follow the router at `/Users/tai/hyperresearch/.agents/skills/hyperresearch/SKILL.md`.
