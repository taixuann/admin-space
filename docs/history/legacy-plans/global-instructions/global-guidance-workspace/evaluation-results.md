# Global guidance batch: evaluation and execution receipt

Date: 2026-10-02

Status: **PARTIAL / NOT QUALIFIED.** Exact prompts were run in OpenCode CLI 1.18.34 using `opencode-go/deepseek-v4.1-flash`. They ran in disposable project folders with copied `AGENTS.md` files, not in live Codex/OpenCode global instruction contexts. Treat response observations below as exploratory only; actual host loading and global behavior are `NOT_ASSESSED`.

The user approved the 16 prompt texts unchanged and explicitly approved sending the candidate/baseline Codex and OpenCode instructions, Claude fallback snapshot, and relevant improve/opencode-delegate skill snapshots to OpenCode Go. The evaluation runs disabled Claude fallback and external skill loading and used `--pure`. No live instruction file, OpenCode configuration, or credential store was changed.

## 2026-10-02 isolation probe (Stage D setup, V2)

Technical isolation attempted on opencode v2.0.22 and PARTIALLY achieved:
`--standalone` + a temp `XDG_CONFIG_HOME` removes plugins (verified by log
windows keyed to run ids) and relocates the config dir; `OPENCODE_CONFIG`
or `OPENCODE_CONFIG_CONTENT` alone does NOT isolate the plugin state. Two
injection sources remain outside child-process control: (1) V2 native
compatibility discovery always scans `~/.claude/skills` and
`~/.agents/skills` (documented V2 behavior); (2) the OpenChamber desktop
context (`OPENCODE_ADDDIR_INJECT_CONTEXT=1` in `.zshrc:154`, plus the
openchamber agent-tool plugin) re-exposes `~/.agents` skills to any
`opencode run` spawned from this harness. A temporary config edit removing
`superpowers@git+…` from the live `opencode.jsonc` plugins removed the
superpowers skill set; the edit is kept removed under plan 002's quota-drop
decision (operator: "bỏ qua luôn"). `ponytail` and `openchamber-agent-tool`
remain loaded for operator tooling. `skill` permission deny rules in an
XDG temp config did NOT hide compatibility-discovered skills in the probed
build (v2.0.22).

Consequence for Stage D: variant separation is BEHAVIORAL, not sandbox
level. Each eval cwd receives exactly one governing `AGENTS.md` (baseline in
`old_skill/`, candidate in `with_skill/`); the run prompt instructs the
model to treat that file as governing; grading reads displayed behavior and
cites the governing text, not skill availability. Skill-list contamination
is recorded as a known limitation here; it cannot fabricate an approval
verdict because every expectation is judged against the governing text
content.

## Evidence

- Full relay event/result files are under `/private/tmp/global-guidance-eval/results/`; context snapshots and prompts are under `/private/tmp/global-guidance-eval/`.
- Plan 001 case 1 completed in a simplified, permission-limited baseline/candidate pair. Both corrected only the README typo. Other Plan 001 cases were not run. Earlier case-1 attempts include a local-log failure, an unrestricted baseline/candidate pair, and a two-minute permission-probing timeout; use only the simplified pair as an exploratory observation.
- Plan 002 cases 1–7 were run once per baseline/candidate in separate OpenCode worktrees. Case 2's first candidate run used the wrong workdir and is excluded; the subsequent candidate run used its own workdir. Case 5 correctly stopped at the missing parser specification, but `python -m unittest` discovered zero tests, so it is not a passing test gate. Case 6 requested calibration and exclusion records but omitted what independent work could continue. Other responses generally matched their textual expectations; none proves global instruction loading or actual Codex behavior.
- Plan 002 case 8 timed out. It is `NOT_ASSESSED` and is not usable as host-loading evidence.
- There is no skill-creator evaluation package, variance analysis, or rendered review viewer; this is not a completed skill-creator evaluation.

## Transfer boundary incident

An earlier delegated Stage D setup read the installed `skill-creator` schema/viewer files, used a broad filesystem search, and inspected OpenCode installation/configuration paths beyond the approved snapshot bundle. It was stopped before running behavior prompts.

A later Plan 002 case-8 run also crossed the approved boundary. Although its project permission file denied external directories, the event log records five completed reads of existing files in `/Users/tai/.local/share/opencode/tool-output/` (about 257,560 characters total). Those files were not among the approved instruction/skill snapshots. The model also attempted to inspect `~/.config/opencode` and other paths; those attempts were denied. A bounded pattern scan of the five returned text blocks did not find common API-key/bearer-token shapes or environment-secret assignments. That check cannot establish that the output contained no credentials or other private content. Credential exposure is therefore **UNVERIFIED**. No research-project or dataset path appears in these case-8 events.

The event log containing the returned tool-output text is preserved at `/private/tmp/global-guidance-eval/results/plan002-case08-baseline/events.jsonl` for audit. Do not reuse its session or output as evaluation evidence. No additional provider tests were started after this was found.

## Decision and remaining gates

- Candidate files remain drafts. No global instructions or installed skills were changed; no commit or publication occurred.
- Plan 001: Stage D is incomplete (only case 1 exploratory); Stage E and installation review remain pending.
- Plan 002: cases 1–7 are exploratory OpenCode responses only; case 8 and all actual global host-loading checks remain `NOT_ASSESSED`.
- The `/Users/tai/.codex` checkout remains dirty and was not modified. Its repo preflight remains a separate installation blocker for the Codex global file. At closeout, `/Users/tai/.config/opencode/opencode.jsonc` hashed to `e23193d5da7279547eb81470d4cb24b7d0844d361457861c89477a06ea9c4c81`, differing from Plan 002 baseline `61e0bd90ba93b82d6efbced46e4af4f94cb64907f548b9dbb6eca3c4bf7b468d`; the current config was not edited by this task, and its change is not yet reconciled.
- 2026-10-02 drift reconciliation (this advisor session, read-only on live files): live config hashed `e23193d…`; diff vs baseline shows only (a) comment lines stripped and (b) `"websearch": {"provider": "random"}` added — likely the opencode-quota plugin rewrite (`baseline` file mtime 2026-10-01 23:27 → live mtime 2026-10-02 14:38). No plugin/model/permission change. The current content is now snapshotted as `baseline/opencode/opencode.jsonc.e23193d-2026-10-02` (hash-verified). All ten Plan 001 sources and the other four Plan 002 sources re-verified against their baseline hashes and still match. Remaining blocker: confirm `websearch.provider: random` was user-intended (or revert it) and refresh the Plan 002 drift-table entry via review before any installation step.
- Resume provider evaluation only in an isolation boundary that prevents access to shared OpenCode tool-output, global instructions, research data, and credentials while still allowing the approved model route. Then run the required host-specific checks and independent review before considering installation.
