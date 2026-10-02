# Global instruction plans

Created with `improve` on 2026-10-02. Both plans were explicitly requested for `/Users/tai/.agents/plans/global-instructions`. Planning does not edit or activate installed global instructions.

## Execution order and status

| Plan | Title | Priority | Effort | Depends on | Status |
| --- | --- | --- | --- | --- | --- |
| [001](001-bounded-delegation-policy.md) | Align bounded delegation, waiting, and review across Codex and skills | P1 | M | none | IN PROGRESS — A–C accepted; only case 1 has exploratory OpenCode responses; host qualification, remaining cases, and Stage E pending |
| [002](002-global-research-and-execution-guidance.md) | Align global scientific guidance across Codex and OpenCode | P1 | S–M | 001 candidate checkpoint and scope coordination | IN PROGRESS — cases 1–7 have exploratory OpenCode responses only; case 8 and actual host evidence NOT_ASSESSED; OpenCode config hash drift and installation pending |

Plan 002 changes overlapping Codex global instructions. Finish and review Plan 001's candidate checkpoint before drafting overlapping Codex candidate text; keep implementation candidates and installation actions serialized.

Plan 001's execution order: A align skill contracts → B specify waiting/recovery → C prepare the minimal Codex policy candidate → D approved prompt set and partial exploratory behavior comparison (see [evaluation receipt](global-guidance-workspace/evaluation-results.md)); actual host checks and remaining cases → E review candidate and handle any separately authorized installation. Codex automatic completion, Claude automatic completion, and quota savings remain NOT_ASSESSED until their specified evidence exists.

## Acceptance tracking

| Surface | Current status | Required evidence |
| --- | --- | --- |
| Plans | WRITTEN | Self-contained scopes, hash baselines, gates and stop conditions |
| Plan 001 candidate instructions | A–C CHECKPOINT ACCEPTED | Exact diff/hashes and validators verified; one exploratory OpenCode case pair only; actual Codex behavior, seven cases, and Stage E remain pending — **Stage D now executed post-V2 (8/8 candidate, 4/8 baseline, +0.50 delta); Stage E remains pending** |
| Plan 002 candidate instructions | DRAFTED | Codex/OpenCode diffs and fallback mapping recorded; prompts approved; cases 1–7 are exploratory OpenCode-only, case 8 timed out after an out-of-scope tool-output read; host evidence pending |
| OpenCode config drift | RESOLVED 2026-10-02 | Drift identified: comment-strip + websearch.provider added; snapshot `e23193d…` archived; user confirmed keep — drift gate closed |
| Installed instructions | NOT_CHANGED | User has authorized updating global guidance after review; activation still requires final drift checks and host-safe validation. Stage D executed 2026-10-02 post-V2 (candidate 8/8, baseline 4/8, delta +0.50; viewer + benchmark in `orchestration-workspace/iteration-1/`; evidence-structure check PASS). Installation remains gated by Stage E authorization. |
| Codex automatic completion | NOT_ASSESSED | Real host job lifetime, terminal event and resume evidence |
| Claude automatic completion | NOT_ASSESSED | Separate real-host evidence |
| Token/quota savings | NOT_ASSESSED | Actual measured usage; no estimates inferred from policy |

The reviewer maintains this index. Plan status values: TODO, IN PROGRESS, BLOCKED (reason), DONE, REJECTED (reason). Candidate-ready, installation, and runtime qualification are distinct states; do not mark an installed/qualified surface DONE while only a candidate exists. The partial evaluation, scope incident, and remaining gates are recorded in [evaluation-results.md](global-guidance-workspace/evaluation-results.md).

## Plan 001 findings considered and rejected

- Force every implementation through OpenCode: conflicts with the existing parent default and creates overhead for small tasks.
- Put commands, timeout values or result schemas in global AGENTS: duplicates delegate-owned procedure.
- Put background process mechanics in improve: couples planning/review to an execution transport.
- Add a second watchdog or scheduler now: the relay already has a watchdog; no demonstrated need for new infrastructure.
- Treat reconcile as complete implementation review: its current DONE path only spot-checks cheap criteria.
- Treat `completed` as accepted, or invent relay status `BLOCKED`: contradicts the observed schema and review contract.
- Promise token savings or portable automatic wake-up: neither has live evidence from the audit.

## Plan 002 findings considered and rejected

- Add lab-specific units, calibration, assay protocols, fitting or exclusion criteria globally: those belong to the owning project or study.
- Require Wiki/OpenScience, literature search, citations or a manifest for every scientific task: unnecessary for pure analysis and routine measurements.
- Disable OpenCode planning/review or globally force executor mode: overrides valid uses of the primary agent and is wider than the request.
- Fix the environment map in this change: the incorrect path is real, but mapping repair is a separate scope.
- Make the screenshot's “Nothing needed from you right now” footer mandatory: creates repeated output without unblocking work.

## Baseline and limitations

The Codex repository HEAD observed during Plan 001 was `422bfab2aa8ae83c2c37eaafaa828641b01d1baa`; Git/GitHub preflight and cleanliness were not established. `/Users/tai/.agents` is not a Git repository, so both plans use file hashes for drift checks.

Plan 002's Codex and OpenCode observations were recorded on 2026-10-02. OpenCode was `1.18.34`; official V1 documentation was used for its fallback analysis, and V2 behavior was not inferred. Host instruction injection remains unqualified. No research datasets or scientific implementation were audited.
