# Skill Benchmark: paper-ingestion-review

**Model**: Not reported by the subagent interface  
**Date**: 2026-10-19  
**Evals**: 1–4 (1 run each per configuration)

## Summary

| Metric | With Skill | Without Skill | Delta |
|--------|------------|---------------|-------|
| Pass Rate | 100% ± 0% | 63% ± 14% | +0.38 |
| Time | unavailable | unavailable | unavailable |
| Tokens | unavailable | unavailable | unavailable |

The mean equally weights the four evaluation cases. Baselines often made sound scientific and safety judgments, but missed the exact active ledger schema and dimension-state enum.

Eval 4 uses a real paper pilot note from Notion. It correctly blocks downstream use because the approved source packet and independent review evidence are incomplete. This is not the required positive real-paper golden evaluation. That acceptance gate remains outstanding.

Timing and token counts were not available from subagent notifications. Each evaluation was run once per configuration, so these results are an initial comparison rather than a variance-tested benchmark.

## Human review

The user reviewed the iteration-1 evaluation viewer and said, “Looks good as drafted.” No changes were requested to these examples. A fresh Notion check found the task “Run real-paper golden ingestion fixture” still marked “Not Started”; the available paper page is a same-context pilot without structured Records or Findings. A complete positive real-paper packet was not available, so that acceptance gate remains open.
