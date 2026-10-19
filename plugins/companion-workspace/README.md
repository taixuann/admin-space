# Companion v2 evaluation workspace

Iteration 1 compares the six candidate skills against their original source skills; Calendar is new and uses a no-skill baseline. Each case is a synthetic prompt-only response evaluation. Runs were instructed not to use live connectors or write records.

## Iteration 1 results

| Skill | Candidate | Baseline | Reading |
|---|---:|---:|---|
| Ask | 100% (6/6) | 100% (6/6) | No measured difference in these small cases. |
| Plan | 83% (5/6) | 83% (5/6) | Both missed the Calendar handoff on the near-miss case. |
| Calendar | 100% (6/6) | 100% (6/6) | The no-skill baseline also passed these constrained prompts. |
| Review | 100% (6/6) | 67% (4/6) | Candidate routed local note organization to Personal Hub. |
| Execute | 83% (5/6) | 100% (6/6) | Candidate named the ambiguity but initially omitted a focused question. |
| Capture | 67% (4/6) | 83% (5/6) | Candidate initially omitted an explicit target and Execute handoff. |

## Targeted second-pass results

These repeat the same case after a small instruction change; they are not whole-skill retests.

| Skill and case | Candidate | Original baseline | Change |
|---|---:|---:|---|
| Plan — calendar near-miss | 100% (3/3) | 67% (2/3) | Candidate now names Calendar and preserves the no-change request. |
| Execute — ambiguous issue | 100% (3/3) | 100% (3/3) | Candidate now asks for the missing repository and canonical issue. |
| Capture — explicit Linear target | 100% (3/3) | 33% (1/3) | Candidate now names L-22 and states the proposed Execute handoff. |

## Limits

- These results grade response text against three assertions per case. One run was performed for each configuration; treat pass rates as directional, not stable performance estimates.
- The collaboration runner did not expose token or duration measurements. Zero time/token fields in the generated benchmarks mean unavailable, not measured zero.
- No connector calls, live reads, writes, readbacks, or end-to-end workflows were tested.
- The approved Calendar Notion page was read, but its named attachment `calendar-companion-references.md` could not be retrieved through Notion or Google Drive. The Calendar draft is limited to the visible operational rules and does not claim connector-specific recipes.
- Human feedback is still needed before treating these drafts as accepted.

## Review pages

Iteration 1, full two-case comparisons:

- [Ask Companion](reviews/iteration-1-ask-companion.html)
- [Plan Companion](reviews/iteration-1-plan-companion.html)
- [Calendar Companion](reviews/iteration-1-calendar-companion.html)
- [Review Companion](reviews/iteration-1-review-companion.html)
- [Execute Companion](reviews/iteration-1-execute-companion.html)
- [Capture Companion](reviews/iteration-1-capture-companion.html)

Iteration 2, targeted retests:

- [Plan Companion](reviews/iteration-2-plan-companion.html)
- [Execute Companion](reviews/iteration-2-execute-companion.html)
- [Capture Companion](reviews/iteration-2-capture-companion.html)

The source snapshot is under `plugin-snapshot/plugins/companion/`. It preserves the complete pre-edit skill and shared-reference baseline.
