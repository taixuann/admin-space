# Plan 001 candidate checkpoint receipt

Status: **A–C REVIEWED; candidate checkpoint accepted.** This is not overall Plan 001 completion, installation approval, or host qualification.

## Binding and scope

- Plan: `/Users/tai/.agents/plans/global-instructions/001-bounded-delegation-policy.md`
- Candidate root: `/Users/tai/.agents/plans/global-instructions/orchestration-workspace/candidate`
- Baseline root: `/Users/tai/.agents/plans/global-instructions/orchestration-workspace/baseline`
- Implementation result: `opencode-stage-001/result.json` (completed, exit 0, model `opencode-go/mimo-v2.6-flash`)
- Focused correction: `opencode-stage-001-delta/result.json` (completed, exit 0, same OpenCode session)
- Changed-file evidence: `changed-files.json`; exact nine-file allowlist only.
- Copied relay script SHA-256: `64b1b5a12ebf9acdba04af47555a73fbd8026613e002006cba58f0803b54044e`, unchanged.

## Independent verification

- `quick_validate.py` on candidate `improve`: PASS (`Skill is valid!`, exit 0).
- `quick_validate.py` on candidate `opencode-delegate`: PASS (`Skill is valid!`, exit 0).
- Relative Markdown links in the nine changed docs: 22 checked, 0 missing.
- Parent review compared every allowed-file diff. It found and the same OpenCode session corrected a duplicate Batch heading and wording that could ask for authorization already recorded in the current request/contract. Re-verification confirmed the allowlist and validators still pass.
- The conditional Codex batch policy preserves the parent-context default and leaves transport, role, project, publication, and notification choices to governing instructions.
- The improve and delegate contracts agree: one cumulative review at a batch boundary, process completion is not acceptance, and commit/publication authority comes from the governing workflow.
- The dirty `/Users/tai/.codex` checkout and all active skill/config files remain untouched; installed instruction hierarchy has not been tested.

## Candidate hashes

| Candidate path | SHA-256 |
|---|---|
| `codex/AGENTS.md` | `a4519fd86d598e87152f967e84656ee8636cfc1d80d7c9eb812d569dff2f6fe3` |
| `skills/improve/SKILL.md` | `6edb6dd4aa451a38710c595f7e246d8559d2d2813871331aba5da9be1693ab62` |
| `skills/improve/references/plan-template.md` | `11863f790f7d7b1d0bacca4293c1210b6f895ffd74acf6d11bc6d6aada4337f7` |
| `skills/improve/references/closing-the-loop.md` | `ae915f515fc8d09a631e2614e491da168abe4ef98c75d56acc8a3f751667dc6b` |
| `skills/opencode-delegate/SKILL.md` | `84d46613e31bbc456e20db578c2200cb2ff4bb7d8f0f546051f2b8c1536417bc` |
| `skills/opencode-delegate/references/writing-the-brief.md` | `c53f95a1b4e216f3ce7a00ad419612d33550f38a743ac07f5d7ca483046dbccb` |
| `skills/opencode-delegate/references/multi-task-queues.md` | `8c8295b51255fcc543d561ff1dc5df39052a948a59802d0415822eb2d4738bcc` |
| `skills/opencode-delegate/references/dispatch-and-poll.md` | `96792cc3dbb9f251926600e44243d11262d5b27e8ba16ba544128ddaf54fb1fd` |
| `skills/opencode-delegate/references/review-and-land.md` | `eff2826e6bd591c984fd798d5ac84f7835de12f5c6d4e228fb3f57bafb282011` |

## Remaining Plan 001 work

- Stage D remains incomplete. The approved prompt set has one exploratory OpenCode project-context pair (case 1); this does not establish Codex-global instruction loading. The remaining seven cases, evaluator/viewer, evidenced grading, and actual host check are pending. See `/Users/tai/.agents/plans/global-instructions/global-guidance-workspace/evaluation-results.md`.
- Stage E final candidate receipt and human install review are pending.
- Native Codex notification and Claude runtime behavior remain `NOT_ASSESSED` (see `capability-matrix.md`).
- No candidate was installed; no commit, push, PR, merge, or Issue mutation occurred.

## Scope expansion recorded for Plan 002

The user explicitly selected `opencode-go/mimo-v2.6-flash` as the required model for OpenCode delegation. A live `opencode run --model opencode-go/mimo-v2.6-flash 'Say hi'` returned `Hi!` with exit 0. This user decision supersedes the earlier plan's no-model-ID default for this provider preference only; it does not force OpenCode as the executor for every task. Plan 002 must encode the model selection in the Codex global guidance and report failure without silently switching models.
