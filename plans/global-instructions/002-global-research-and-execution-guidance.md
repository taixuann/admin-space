# Plan 002: Align global scientific guidance across Codex and OpenCode

> Executor: prepare a reviewable candidate update to personal global instructions. The user later authorized candidate execution and the requested global instruction update after evidence review. This does not authorize commits, pushes, scientific decisions, changes to research inputs, or external transmission of private instruction files without explicit approval. Keep raw evidence and existing instructions recoverable. Follow local/project policy wherever it is more specific.

## Status

- Priority: P1
- Effort: S–M; the text edits are small, but instruction hierarchy and behavior checks matter.
- Risk: MED — both files load broadly and can alter work across repositories.
- Depends on: Plan 001 reaches a reviewed candidate checkpoint before either candidate rewrites the shared Codex global file. Coordinate its final scope before editing overlapping candidate text; do not run candidate updates concurrently. If Plan 001 is rejected or materially changes, re-check and update this dependency before proceeding.
- Category: dx / docs / instruction policy
- Status: IN PROGRESS — user authorized candidate work and global instruction updates after review.
- Planned on: 2026-10-02, Asia/Ho_Chi_Minh.
- Requested plan home: `/Users/tai/.agents/plans/global-instructions`.
- Sequencing update 2026-10-02: an OpenCode V1→V2 upgrade (approved by the operator; plan `~/.agents/plans/002-opencode-v2-upgrade.md`) precedes any further drafting, Stage C refresh, or Stage D evaluation work. After the upgrade, the "OpenCode V1 fallback migration" section collapses to writing `~/.config/opencode/AGENTS.md` directly (V2 does not fall back to `~/.claude/CLAUDE.md`), and the recorded `opencode 1.18.34` version evidence refreshes. — *EXECUTED 2026-10-02: opencode v2.0.22 installed (plan 002 DONE); candidate refresh pass applied (see `global-guidance-workspace/refresh-pass-2026-10-02.md`); claude candidate dropped; next gate is Stage D.*
- Codex repository HEAD observed: `422bfab2aa8ae83c2c37eaafaa828641b01d1baa`. This is not a cleanliness or upstream receipt.
- `/Users/tai/.agents` is not a Git repository; use hashes below for local drift checks.
- Research checked: official Codex custom instructions documentation, official OpenCode V1/V2 instruction docs, and Nature's computational reporting guidance. Links are in “Current state”.

## Why this matters

The user wants their scientific work to inherit a small, useful set of research safeguards and wants OpenCode to act clearly as an implementation executor when given an execution brief. Today Codex has broad control-plane instructions in its global file, the OpenCode global `AGENTS.md` is absent, and OpenCode V1 falls back to an existing Claude global file with its own auto-delegation rule. Add only stable cross-project principles and a conditional execution contract; leave experiment-specific procedures and acceptance authority with their projects. The user has since explicitly selected `opencode-go/mimo-v2.6-flash` as the required model whenever OpenCode is used; a live `Say hi` call succeeded. Keep this a model-selection preference, not a mandate to use OpenCode for every task, and stop rather than silently switching models if it is unavailable.

## User decision added after planning

On 2026-10-02, the user selected `opencode-go/mimo-v2.6-flash` as the required model whenever OpenCode is used. The OpenCode CLI model catalog listed this exact route; `opencode run --model opencode-go/mimo-v2.6-flash 'Say hi'` returned `Hi!` and exit 0.

Superseded later on 2026-10-02: the single-model pin is replaced by the allowlist policy in "OpenCode model policy" below, after the operator confirmed `mimo` has no variants and the catalog display had drifted. Rework still resumes the recorded session and its model. This selection governs model choice only when OpenCode is used; native/parent execution remains available. Do not alter provider configuration or credentials, and do not silently substitute another model if a route fails.

## Current state and evidence

These are direct observations, not claims of host instruction loading qualification.

| Surface | Live state | Evidence |
| --- | --- | --- |
| Codex global instructions | `/Users/tai/.codex/AGENTS.md` exists. It has personal task-first, skill, simplicity, environment and memory guidance, then extensive AI Labs role/control-plane policy and a default branch/PR process. | The control-plane block begins at `:35`; global repository workflow at `:136`. |
| Codex override | `/Users/tai/.codex/AGENTS.override.md` is absent. | Checked directly on 2026-10-02. Recheck before activation. |
| Codex scope | Official docs say global `AGENTS.override.md` or else `AGENTS.md` is loaded, then applicable project instructions are concatenated root to leaf. | [Codex custom instructions](https://learn.chatgpt.com/docs/agent-configuration/agents-md), sections “How Codex discovers guidance” and “Create global guidance”. |
| OpenCode global instruction | `/Users/tai/.config/opencode/AGENTS.md` is absent; config overrides and environment flags inspected have no custom instruction path or Claude-fallback disable flag. | `/Users/tai/.config/opencode/opencode.jsonc:1-8` contains its header and plugins; `XDG_CONFIG_HOME`, `OPENCODE_CONFIG`, `OPENCODE_CONFIG_DIR`, `OPENCODE_DISABLE_CLAUDE_CODE`, and `OPENCODE_DISABLE_CLAUDE_CODE_PROMPT` were unset. |
| OpenCode version and fallback | `opencode --version` returned `1.18.34`. V1 docs describe `~/.claude/CLAUDE.md` as the global fallback if the OpenCode global AGENTS file is absent, with the OpenCode AGENTS file taking precedence. | [OpenCode V1 rules](https://opencode.ai/docs/rules/), “Claude Code Compatibility” and “Precedence”. |
| Fallback content | `/Users/tai/.claude/CLAUDE.md` exists. It contains CodeGraph discovery guidance, AQG code-construction discipline, and a conditional `/opencode` auto-delegation rule. The current auto flag was absent. | Lines `1-43`; specifically `:15-34` and `:37-43`. |
| OpenCode V2 caveat | V2 has different documentation: it combines sources and currently documents only `AGENTS.md` discovery, not the V1 Claude fallback behavior. Do not infer V2 semantics for this installed V1 binary. | [OpenCode V2 instructions](https://opencode.ai/v2/docs/instructions/). |
| Research owner | `/Users/tai/workspace/research-projects/AGENTS.md` contains study/program routing, raw-evidence handling, input ownership, scientific acceptance gates and a direct-on-`main` default. | Lines `6-23`, `25-54`, `57-90`. |
| Environment map | `/Users/tai/.codex/ENVIRONMENT.md` names `/Users/tai/workspace/projects` as research root, but that path is absent. `/Users/tai/workspace/research-projects` exists. | Environment map `:55-64`; checked both paths on 2026-10-02. The currently mapped active leaf is absent. |
| Reproducibility guidance | Nature recommends appropriate validation, input-file availability, software/version information, preprocessing and bias reporting. These support compact general principles; they do not prescribe a single lab workflow. | [Computational tools reporting guidelines](https://www.nature.com/documents/Computational_tools_reporting_guidelines.pdf), pages 1–2. |
| Instruction design | OpenAI recommends task-relevant, concise AGENTS guidance and workflow-specific skills, and warns against forcing full documentation reads for every edit. | [Rethinking skills and prompts for GPT-6 Astra](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra). |

Plan 001 also targets the Codex global file, and the installed OpenCode fallback is material to Plan 001's waiting policy. Respect their dependency; keep one coordinated candidate so the same global text is not edited by two workstreams.

## Drift baseline

Before writing a candidate, recompute these hashes with `shasum -a 256 <path>`. A mismatch requires inspecting current content, refreshing excerpts and hashes, and reconciling Plan 001. Never overwrite a changed original from an old candidate.

| Path | SHA-256 |
| --- | --- |
| `/Users/tai/.codex/AGENTS.md` | `ea546b1ac06f627facc8b7c944c31c307161e1cd37a664597d0428e582bf82a4` |
| `/Users/tai/.codex/ENVIRONMENT.md` | `5a6669d44786dbea48da4289414baf7038e74b05679cf3f4ac93daa40cacb1ae` |
| `/Users/tai/.claude/CLAUDE.md` | `fbb598e6fb15a901717e3c22d2758adf488521e91f6a3d5a93804e3dd4f879be` |
| `/Users/tai/workspace/research-projects/AGENTS.md` | `1e4bd50df6a3d03e25fdcddb176aa6cbc69bf880458b4070c0ef5a55d0205209` |
| `/Users/tai/.config/opencode/opencode.jsonc` | `61e0bd90ba93b82d6efbced46e4af4f94cb64907f548b9dbb6eca3c4bf7b468d` |
| `/Users/tai/.agents/skills/improve/references/plan-template.md` | `7be76dd3c29442288fa7cee4432fc6e95c2fdbf748c9b356344bf647c5f8722e` |
| `/Users/tai/.agents/skills/improve/references/audit-playbook.md` | `587c1b927070f3c28139ad95ac34cc21a7da32618cfeb966cb774e58a865d4c8` |

## Scope

After the Plan 001 coordination gate, prepare candidates in `/Users/tai/.agents/plans/global-instructions/global-guidance-workspace/candidate/` and byte-preserving baselines in its sibling `baseline/`, using this layout:

- `candidate/codex/AGENTS.md` — candidate for `/Users/tai/.codex/AGENTS.md`.
- `candidate/opencode/AGENTS.md` — new global OpenCode instructions intended for `/Users/tai/.config/opencode/AGENTS.md`.
- `candidate/claude/CLAUDE.md` — only a fallback-compatibility candidate if host tests show a needed behavior would be lost when OpenCode stops using the Claude fallback. Preserve Claude's existing instructions and scope the change to compatibility; do not edit the live file during candidate work.
- `baseline/` — exact snapshots of every file in the drift table. Include the research project file for comparison, never as an edit target.
- `behavior-cases.md`, `load-receipts.md`, and `review.md` — prompt cases and observed results; no real scientific datasets are needed.

Only the three candidate instruction files above may differ from their matching baselines. Configuration, project instruction files, skills, the environment map, plugins, auto-mode flag, source data and research code are out of scope. The environment-map mismatch may be reported as a separate follow-up; do not silently edit it as part of this instruction plan.

Keep any finalized plan artifacts in `/Users/tai/.agents/plans/global-instructions`. Candidate originals in the home paths remain unchanged until a future, separate instruction-install action is explicitly authorized.

## Execution preflight

Before repository or instruction edits, invoke `aqg-startup-preflight` for `/Users/tai/.codex` according to `/Users/tai/.deeppattern/versions/0.14.24/skills/aqg-startup-preflight/SKILL.md`. GitHub/Git status for the current session is UNKNOWN; do not infer clean state from the HEAD recorded here. The global-policy candidate itself is read-only planning output; no preflight receipt is claimed by this plan.

Re-read the live Codex override, OpenCode version, relevant environment flags, target paths, project rules and hashes immediately before activation. For activation of the Codex control-plane repository, follow that repository's current lifecycle and validation contract. OpenCode global activation is a distinct local-runtime action.

## Candidate policy

### Codex global file

Preserve the current task-first principles, user-global override precedence, durable-memory boundary, and project-first routing. Keep global content broadly useful across scientific, writing and software work.

Move or rewrite Codex repository role/AI Labs policy as explicitly conditional guidance that applies only when the task edits `/Users/tai/.codex` or is governed by its control-plane contract. Keep the substantive role boundaries intact there; do not make Prometheus/Franky/Athena semantics universal scientific-project policy.

Make the global Git lifecycle conditional on repository instructions and task contract. Its current “ordinary repository changes use the Issue/PR/CI surface” rule must not silently override a repository such as research-projects whose owner explicitly uses direct bounded work on `main`. Preserve explicit publication gates when the active project requires them.

Add a short shared scientific baseline, not a lab protocol:

```text
For scientific work, keep raw evidence immutable and distinguish it from
derived outputs. Preserve traceability to selected inputs, transformations,
methods/settings, and relevant software versions. Do not invent missing
measurements, metadata, citations, or method choices. Separate observations,
interpretation, uncertainty, and scientific acceptance. Passing code tests
does not by itself establish scientific validity. Follow the owning project's
data, method, and acceptance gates.
```

Add an actionable blocker convention modeled on the screenshot, only when user action blocks progress or a real decision boundary has arrived:

```text
End a blocked turn with a short “What I need from you” section. Number each
concrete action and name where to do it and what to send back. Put the most
blocking request first; say what independent work will continue. Do not add
a repeated footer when no user action is needed.
```

Keep this concise. Do not require Wiki/OpenScience, a literature search, a research skill, citations, a manifest, or a particular artifact on every scientific task. Route through the project's own domain instructions when present. Do not treat memory or session content as canonical scientific evidence.

### OpenCode model policy (user decision updated 2026-10-02)

OpenCode runs use only the user-approved allowlist, all from the flat-rate `opencode-go` provider. Fresh runs pick by task character; rework resumes the recorded session and therefore its original model. If a selected model is unavailable or cannot authenticate, stop and report the failure; do not substitute a model outside the allowlist. Before trusting any route after an upgrade, verify it live with a one-word call (`Say hi`, exit 0); catalog display can drift.

| Model | Preferred variant | Default for |
| --- | --- | --- |
| `opencode-go/muse-spark-1.3-contributor` | `xhigh` (its highest; no `max` variant exists) | mechanical sweeps, bulk edits, cheap fast loops |
| `opencode-go/deepseek-v4.1-flash` | `max` | routine implementation with moderate depth |
| `opencode-go/glm-5.3-flash` | `max` | subtle logic, review passes |
| `opencode-go/mimo-v2.6-flash` | none (the model has no variants) | explicit pinning only; keep working as fallback |

Catalog drift is a known hazard: on 2026-10-02 `mimo-v2.6-flash` was absent from the displayed catalog while a live call (`Say hi`, exit 0) succeeded. Trust a live check over the displayed catalog. A failed live check is a STOP-and-report condition, never an automatic substitution.

### OpenCode global file

Scope this file to OpenCode behavior across projects. Reuse the same shared scientific baseline and blocker rule, avoiding contradictory wording. Add an execution section that applies **only when OpenCode receives an authorized implementation brief**:

```text
For an authorized execution brief, follow the supplied scope and ordered
steps, use the target project's declared inputs and verification commands,
and report changed paths, checks/results, deviations, missing information,
and partial work. Do not broaden scope, alter scientific methods/data
selection/exclusions, publish, commit, or claim scientific acceptance unless
the brief and governing project explicitly authorize that action. Stop at a
named checkpoint or a material blocker and give the parent a specific request
to relay to the user.
```

Treat this as an execution contract, not an assertion that OpenCode may only execute. Do not globally disable its plan/review agents or change tool permissions, auto-mode, model/provider settings, or background-wait mechanism in this plan.

### OpenCode V1 fallback migration

Adding the OpenCode global file changes its documented V1 precedence and shadows the current `~/.claude/CLAUDE.md` as OpenCode's global fallback. Before installation, compare all current fallback guidance with the candidate. Carry into the OpenCode candidate any CodeGraph/AQG behavior that OpenCode currently needs; retain host-specific syntax and triggers only where they remain accurate. Keep the live Claude file intact so Claude users retain its intended behavior. If preserving an OpenCode behavior requires editing the fallback, stop: revise the candidate and this scope before proceeding, rather than silently changing a file shared by Claude. Verify the real host behavior on the installed version; do not use V2 docs as a substitute.

The OpenCode project `/Users/tai/workspace/research-projects/AGENTS.md` remains the owner for Study/Research Program phases, actual inputs, raw file handling, domain methods, project Git workflow, output contracts and scientific acceptance. Do not duplicate or weaken it in the global candidates.

### Candidate refresh pass (operator decision 2026-10-02)

One grouped revision of the instruction candidates happens after the OpenCode V2 upgrade lands (`~/.agents/plans/002-opencode-v2-upgrade.md`), folding in every item below, then rerunning validators and receipt checks. Do not edit candidates piecemeal before then.

- `candidate/codex/AGENTS.md` line 64: replace the single-model paragraph with the allowlist policy from "OpenCode model policy" (four models, per-model variant preferences, live check before trust, stop on failure instead of substitution).
- `candidate/opencode/AGENTS.md`: structure stays; it carries no model selection (the orchestrator owns that through the brief and relay `--model`).
- Authoring register for all candidate text: simple-english Plain. Short imperative sentences, one instruction per sentence, define a term before its first use, never Strict mode. Existing candidate text already sits close to this register; the refresh pass splits remaining long compound sentences. The writing-for-agents skill (available operator-side) is the named reference for editing these AGENTS.md candidates.
- `candidate/claude/CLAUDE.md`: drop from the candidate set after V2 unless host evidence shows a required OpenCode behavior would be lost; record the drop rationale in `review.md`.
- V1 fallback wording above collapses to plain creation of `~/.config/opencode/AGENTS.md` (V2 discovers only AGENTS.md). The CodeGraph and AQG guidance still travels into that file.
- Line budget: each global instruction candidate stays at or under 90 lines (current: codex 70, opencode 21). Guidance longer than that belongs in project-level files.
- Behavior cases after the refresh: rerun the affected cases; case 8's V1-fallback expectation becomes "a V2 session discovers only AGENTS.md global guidance and CodeGraph/AQG behavior remains present".

## Validation steps

### Step 1: Resolve source drift and candidate ownership

Recompute all listed source hashes; confirm Plan 001 is not actively authoring an overlapping Codex global candidate. Snapshot the originals into `baseline/` without changing them. Record original/candidate paths explicitly in `review.md`.

**Verify:** `shasum -a 256` matches every table value and the Plan 001 coordination note is recorded. Otherwise STOP for a refreshed baseline or wait for the overlapping candidate to finish.

### Step 2: Draft the two candidates and fallback mapping

Draft concise candidate files using the policy above. Compare each sentence with its intended audience and with the existing project guidance. Mark each existing Codex control-plane clause as either retained globally, made conditional on the Codex repository, or removed as duplicate/stale, with evidence and rationale in `review.md`. For OpenCode, account for every instruction in the current Claude fallback that its precedence change would hide. If the candidate cannot preserve required OpenCode behavior without scope expansion, STOP.

**Verify:** a complete line-by-line mapping is recorded; no raw-data method/parameter or absolute project checkout path has been generalized into global instructions; only candidate files differ from baselines.

### Step 3: Exercise representative cases in both hosts

Use the actual installed Codex and OpenCode contexts if available. Begin each case in a fresh session so initial instruction loading is observable. Do not edit source or access experimental data in these checks. Record the exact prompt, host/version, loaded-instruction evidence, response, and assessment in `behavior-cases.md`.

1. **Trivial unrelated edit request** — the response stays proportionate and does not require scientific rituals or an audit for a typo.
2. **Routine scientific data question with incomplete metadata** — distinguishes observed facts from assumptions, asks for data only if material, and does not invent units or provenance.
3. **Authorized local exploratory fit with declared inputs/method** — uses the owning project instructions, preserves raw inputs and labels exploratory output as exploratory; does not demand publication review automatically.
4. **A model result that passes software tests but has no domain validation** — does not claim scientific acceptance.
5. **Long OpenCode implementation brief with clear scope/gates** — reports completed batch evidence and returns at the named checkpoint; no invented permissions or commit authorization.
6. **Executor discovers missing instrument calibration or ambiguous exclusions** — provides one prioritized, concrete user request with location and requested evidence; records safe independent work that can continue.
7. **Unrelated document/writing request** — no forced scientific tools, Git branching, or OpenCode dispatch.
8. **OpenCode V1 session after adding the global candidate** — verify that required CodeGraph/AQG guidance remains available and that only the expected instructions are loaded; confirm the Claude fallback shadowing behavior from actual host evidence.

If the host cannot expose loaded instruction context safely, mark that result NOT_ASSESSED; a plausible response is not proof that a particular file loaded. Do not install the candidate merely to run these checks. Use an isolated config/home or a disposable OpenCode context where the host supports it; if safe isolation is unavailable, retain the candidate-only result and request a separate activation/evidence step.

**Verify:** each case is PASS/FAIL/NOT_ASSESSED with evidence and rationale; no failure is papered over by prompt wording. Both hosts are reported separately.

### Step 4: Independent review and candidate handoff

Have an authorized read-only reviewer inspect the two diffs, the Codex clause mapping, the V1 fallback comparison, the project-vs-global scope, and all behavior receipts. The parent owns final acceptance. Revise only within scope and repeat affected cases.

Write `review.md` with candidate hashes, file allowlist, mapping, all case results, unresolved uncertainties, and distinct statuses for candidate accepted, installed, and host-loaded. Present the candidate for human decision. Do not activate or commit it in this plan.

**Verify:** reviewer finds no contradictory absolute global rule, lost required V1 fallback guidance, raw-data mutation instruction, false scientific acceptance shortcut, or claim of runtime loading without evidence. Candidate status may become READY_FOR_INSTALL_REVIEW; installation and qualification remain separate.

## Commands and acceptance criteria

During candidate-only drafting, confirm original hashes remain unchanged:

```bash
shasum -a 256 /Users/tai/.codex/AGENTS.md \
  /Users/tai/.codex/ENVIRONMENT.md \
  /Users/tai/.claude/CLAUDE.md \
  /Users/tai/workspace/research-projects/AGENTS.md \
  /Users/tai/.config/opencode/opencode.jsonc
```

Expected: each original matches the drift baseline. For the Codex candidate, use the repository's current AGENTS validator and run `codex debug prompt-input` only in a disposable/isolated context if supported. For OpenCode, use current v1's supported instruction inspection path if available; do not invoke V2-only flags. If a load receipt is unavailable, report it as NOT_ASSESSED.

- [ ] Codex global candidate separates personal general defaults from Codex-workbench-only role/PR rules.
- [ ] Codex global candidate allows the owning project to govern its own branch, evidence, and scientific workflow.
- [ ] Both global candidates carry concise shared principles: preserve raw evidence; trace derived results to relevant inputs and method/software details; distinguish observation, interpretation, uncertainty, and acceptance; software tests alone are not scientific validation.
- [ ] Both candidates require concrete blocker requests only when user action is needed; the request says where to act and what evidence to return, prioritizes blocking items, and does not force a no-action footer.
- [ ] OpenCode execution guidance is conditional on an authorized brief and describes execution/report boundaries without disabling planning, review, tools, or host-specific workflow.
- [ ] The V1 fallback's OpenCode-relevant behavior is mapped and retained in the candidate; the live Claude file remains unchanged.
- [ ] Research project rules remain the detailed authority for exact inputs, methods, raw data, analyses, Git workflow, and scientific acceptance.
- [ ] All eight behavior cases have evidence and separate Codex/OpenCode outcomes; unknown loading is NOT_ASSESSED.
- [ ] Independent review and candidate hashes are captured; originals are unchanged until any separately authorized installation.
- [ ] Update `/Users/tai/.agents/plans/global-instructions/README.md` without changing Plan 001's status.

## STOP conditions

- Any source hash differs, Plan 001 has an uncoordinated overlapping candidate, or a newly effective override changes the intended target.
- Actual OpenCode V1 behavior conflicts with documented precedence or candidate mapping; do not rely on V2 documentation to resolve it.
- Introducing the OpenCode global file would silently discard OpenCode-relevant AQG/CodeGraph guidance and the candidate cannot retain it without changing protected files.
- A proposed rule requires fixed assay conditions, units, calibration, model choice, exclusion criteria, or publication gates that belong to a specific project/study.
- A test case asks the executor to touch real raw data, make a scientific decision, or activate global policy.
- Behavior evidence is unavailable but someone proposes marking host loading or scientific acceptance PASS.
- Candidate requires a change to role definitions, plugin configuration, tool permissions, environment-map paths, research project files, or external service to work.
- Installation/activation or repository publication is proposed without a distinct authorization and fresh state check.

## Maintenance notes

The `~/.codex/AGENTS.md` is both user-global guidance and a tracked Codex control-plane repository file. Preserve that dual role with explicit conditional wording; verify its actual Codex instruction injection before claiming the intended split works. OpenCode `~/.config/opencode/AGENTS.md` is local user configuration and globally affects OpenCode. Recheck V1/V2 fallback behavior when upgrading OpenCode. Keep stable principles global, experiment procedures in project instructions/skills, and per-run details in the brief.

This plan audits instruction placement and representative behavior only. It does not audit scientific code or datasets, validate a measurement, fix the environment map, qualify OpenCode plugins, or prove long-run executor reliability.
