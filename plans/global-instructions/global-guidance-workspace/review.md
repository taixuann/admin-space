# Plan 002 candidate review

Status: CANDIDATES DRAFTED; PROMPTS APPROVED; PARTIAL EXPLORATORY RESPONSES ONLY; HOST BEHAVIOR NOT ASSESSED; OPENCODE CONFIG SOURCE DRIFT DETECTED. See `evaluation-results.md`.

## Candidate paths and hashes

| Candidate | Intended live path | SHA-256 | Status |
| --- | --- | --- | --- |
| `candidate/codex/AGENTS.md` | `/Users/tai/.codex/AGENTS.md` | `b98e662f7b0152d6461d5a198a7ec2ff7d232ac4adf9ce42a27f0b3b1837594b` | Draft; based on accepted Plan 001 A-C candidate plus Plan 002. |
| `candidate/opencode/AGENTS.md` | `/Users/tai/.config/opencode/AGENTS.md` | `a31d720d74b0b40168bbb27a88a32ce942e89e67cf1b45ff32c138a0f5ef4284` | Draft; new global OpenCode guidance. |
| `candidate/claude/CLAUDE.md` | `/Users/tai/.claude/CLAUDE.md` | `fbb598e6fb15a901717e3c22d2758adf488521e91f6a3d5a93804e3dd4f879be` | Byte-identical fallback snapshot; no edit proposed. |

Only `codex/AGENTS.md` and `opencode/AGENTS.md` are candidate changes. `changed-files-002.json` records this allowlist. Other baseline snapshots remain evidence-only.

## Review findings

- Codex general guidance now starts from the active task and project, adds compact scientific evidence/uncertainty rules and the actionable blocker format, and preserves the accepted bounded-delegation section.
- Codex role and control-plane rules are grouped under a condition applying only to work in `/Users/tai/.codex` or work governed by that contract. General repository workflow now defers to the active project/task contract; this avoids imposing the workbench's Issue/PR rules on research projects.
- The user-selected `opencode-go/mimo-v2.6-flash` is explicit for fresh OpenCode runs only; resume retains the recorded model; missing route/auth means stop without substitution. No requirement routes every task through OpenCode.
- OpenCode guidance retains conditional CodeGraph discovery, AQG construction/audit behavior, shared scientific integrity, and authorized-brief execution boundaries. It omits the Claude-side `/opencode` auto-mode flag instruction because that trigger controls Claude dispatch and does not accurately set the OpenCode runner.
- Project-specific Study phases, exact inputs, methods, Git lifecycle, and acceptance remain in `/Users/tai/workspace/research-projects/AGENTS.md`; no such details were copied globally.
- Candidate wording avoids research protocols, mandatory citations/literature searches/manifests, tool permission changes, OpenCode configuration changes, and unsupported runtime claims.

## External review boundary

The automatic reviewer initially rejected the proposed transfer. The user later explicitly approved sending the specified baseline/candidate instructions, Claude fallback snapshot, and relevant improve/opencode-delegate snapshots for evaluation; the selected test route was `opencode-go/deepseek-v4.1-flash`. Cases 1–7 ran as exploratory OpenCode project-context tests. A later case-8 run crossed the approval boundary by reading five pre-existing files from `/Users/tai/.local/share/opencode/tool-output/`; this was not part of the approved transfer. The case timed out and is excluded. A bounded pattern scan found no common API-key/bearer-token shapes or environment-secret assignments, but credential inclusion cannot be ruled out. No further provider tests should use this route until a stronger isolation boundary is available. Details are in `evaluation-results.md`.

## Source drift and validation

The recorded hashes below are the Plan 002 baseline. At closeout, the live Codex AGENTS and Claude fallback still matched their recorded hashes, while the live OpenCode config differed: current `e23193d5da7279547eb81470d4cb24b7d0844d361457861c89477a06ea9c4c81` versus baseline `61e0bd90ba93b82d6efbced46e4af4f94cb64907f548b9dbb6eca3c4bf7b468d`. This task did not edit the live config. Reconcile the drift before installation; other source hashes were not rechecked at closeout.

- Codex global AGENTS: `ea546b1ac06f627facc8b7c944c31c307161e1cd37a664597d0428e582bf82a4`
- Codex environment map: `5a6669d44786dbea48da4289414baf7038e74b05679cf3f4ac93daa40cacb1ae`
- Claude global fallback: `fbb598e6fb15a901717e3c22d2758adf488521e91f6a3d5a93804e3dd4f879be`
- Research-projects AGENTS: `1e4bd50df6a3d03e25fdcddb176aa6cbc69bf880458b4070c0ef5a55d0205209`
- OpenCode config: `61e0bd90ba93b82d6efbced46e4af4f94cb64907f548b9dbb6eca3c4bf7b468d`
- Improve plan template: `7be76dd3c29442288fa7cee4432fc6e95c2fdbf748c9b356344bf647c5f8722e`
- Improve audit playbook: `587c1b927070f3c28139ad95ac34cc21a7da32618cfeb966cb774e58a865d4c8`

2026-10-02 drift reconciliation: ALL still-match values re-verified live (see evaluation-results.md). OpenCode config drifted; diff = comment-strip + `websearch.provider: "random"` added; current content snapshotted as `baseline/opencode/opencode.jsonc.e23193d-2026-10-02`. Installation gate: confirm or revert the websearch line, then update this table.

The live Claude fallback and OpenCode configuration remain unchanged; the Codex checkout remains untouched. Prompt sets remain unchanged in `behavior-cases.md`. Cases 1–7 produced exploratory paired OpenCode responses, not actual Codex/OpenCode global-host receipts. Case 8 timed out after the scope incident and remains NOT_ASSESSED. Automatic Codex/Claude wake-up remains NOT_ASSESSED per Plan 001. See `evaluation-results.md`.

## Installation and qualification

The user authorized updating both global instruction surfaces after review and approved the exact prompt set unchanged. Candidate installation remains pending because the host-specific evidence is absent, case 8 crossed the approved data boundary, the OpenCode config has source drift, and the Codex checkout is dirty. Candidate drafting is not installation; an installed file would not itself prove host loading or behavior qualification.
