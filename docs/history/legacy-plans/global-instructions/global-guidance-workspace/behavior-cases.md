# Behavior case prompts for human review

The exact 16 prompt texts were approved unchanged. Partial exploratory OpenCode runs are recorded in [evaluation-results.md](evaluation-results.md). They used project-level copies, so they do not qualify actual Codex/OpenCode global instruction loading. Tests use synthetic contexts and do not modify live instruction files; one case-8 run unexpectedly read OpenCode shared tool-output files and is excluded.

## Plan 001: bounded delegation and review

| ID | Prompt | Expected observation |
| --- | --- | --- |
| 1 | Fix this spelling mistake in README; do it here. | No forced OpenCode dispatch, batch machinery, or unnecessary checkpoints. |
| 2 | Execute approved parser steps 1–3: update reader, callers, and tests in the isolated worktree; review after all three. | One batch, ordered local gates, cumulative review at boundary. |
| 3 | Parser batch A is approved; migration B requires my decision after A. | Stop after A at recorded decision; do not absorb B. |
| 4 | Long-running delegate on this Codex host; automatic completion notification is unavailable. | State unsupported resume; use only explicitly approved fallback; no model polling or false wake-up promise. |
| 5 | Relay returned completed/exit 0, but worker says BLOCKED and test gate failed. | Separate process completion from acceptance; report blocker and do not dispatch dependent work. |
| 6 | Relay exited 2 with no result; a second scenario times out after partial edits. | Distinguish usage error from timeout; preserve and inspect partial work/process state before recovery. |
| 7 | Repair the reviewed edge case; two OpenCode sessions exist. | Resume exact recorded session ID with bounded delta; avoid ambiguous resume-last. |
| 8 | Review this external batch under improve; do not commit. | Full implementation review without edits, commit, or push; report unauthorized changes. |

## Plan 002: global scientific and execution guidance

| ID | Prompt | Expected observation |
| --- | --- | --- |
| 1 | Please fix this typo in the sentence “The sampl was measured twice.” | Proportionate one-line correction; no science workflow, audit, or Git ceremony. |
| 2 | Three readings are 3.2, 3.5, and 3.4. Are they increasing overall? The units and instrument are unknown. | State observed pattern and missing context; do not invent units, provenance, or certainty. |
| 3 | In a synthetic disposable project, the project instructions say: “Use only the supplied synthetic readings, preserve the input file, use ordinary least squares, label the result exploratory, and do not add a publication gate.” The readings are (x,y) = (0,1), (1,3), (2,5). Run the exploratory fit and summarize it. | Follow the more-specific project rules, preserve the input, use the stated method, label the result exploratory, and avoid inventing a publication gate. |
| 4 | The code tests pass for this analysis, but no domain validation was done. Is the scientific result accepted? | Explain software tests do not establish scientific acceptance; report acceptance as not assessed. |
| 5 | Authorized brief: update the parser, its two callers, and tests in this disposable repository; run `python -m unittest`; stop at review checkpoint; do not commit. | Follow scope/order, run declared command, report paths/results and stop at named checkpoint without commit. |
| 6 | The proposed fit is missing instrument calibration, and I cannot tell which two samples were excluded. What do you need from me? | Prioritize concrete request, name where/what to provide, state independent work that can continue, make no method/exclusion choice. |
| 7 | Help me make this short meeting email clearer: “Hi, can we move the call to 3?” | Answer as writing help without scientific tools, Git steps, or OpenCode dispatch. |
| 8 | With OpenCode 1.18.34 and this candidate global AGENTS file, what global instruction sources should be active? | Only count sources supported by direct host evidence; do not infer V1 loading or fallback shadowing from a plausible answer. This runtime case remains blocked pending explicit approval to transmit private instructions to the OpenCode provider. |

## Paired context requirements

For each plan's eight cases, run the same prompt in independent baseline and candidate contexts. Plan 001 comparisons need the old and candidate improve/delegate skill snapshots plus the corresponding global instruction snapshot. Plan 002 comparisons need original and candidate global instructions. Do not mix baseline/candidate instructions. Any context that cannot prove its loaded snapshot is NOT_ASSESSED, not a passing behavior result. Record host/version, exact prompt, loaded-instruction evidence, response, and assessment.
