# Plan 007: Build Orchestra Companion around ticket intake and bounded bot requests

> Executor: Read the whole plan. Work only inside the named scope. Use Skill Creator to draft, evaluate and revise skills. Do not install, publish, dispatch external jobs or modify Notion under this plan without the separately named authorization.
>
> Drift check: `git -C /Users/tai/.agents diff --stat 5e3572e59e95d0736d9daef79b0efaa2b11c1829..HEAD -- plugins/companion plugins/marketplace.json plugins/orchestra-companion`.
> Compare the current-state excerpts below with disk. Record unrelated dirty files separately. Do not reset, stage or absorb them.

## Status

- Priority: P1
- Effort: M
- Risk: MED. The main risks are invented dispatch, duplicated tickets and excess write authority.
- Category: direction
- Status: DEFERRED, 2026-10-23, at the user's request. Implementation and installation have not started. Resume only when the user selects this work again.
- Depends on: no other local plan. Live dispatch and universal Wiki lookup have explicit gates below.
- Planned at: `5e3572e59e95d0736d9daef79b0efaa2b11c1829`, 2026-10-20.
- Repository: `/Users/tai/.agents`, branch observed as `codex/companion-v2`.
- Existing dirty state: `.skill-lock.json` modified; `skills/archify/` untracked. These are not this plan's changes.

## Why this matters

The user wants one continuing Notion ticket for each independent intent. Domain assistants capture intent. Orchestra receives it, gathers context, presents the next decision and requests bounded work from another bot. Returned work updates the same ticket. The coordinator must manage both ticket state and job requests without becoming a second project tracker or a new runtime engine.

The plugin name is `orchestra-companion`. It replaces the proposed name Astra, not the installed Companion plugin. One bot role has one plugin package as a design convention. Installing a plugin does not create an autonomous process or grant dispatch authority.

## Current state and evidence

### Local facts

- `/Users/tai/.agents/plans/README.md` declares `plans/` the single plans home. Root numbering ends at 006 before this plan.
- No root `AGENTS.md`, package build manifest or Orchestra plugin was found during scoped recon. Recheck ancestor and nested instructions before execution.
- `/Users/tai/.agents/plugins/companion/plugin.json:2-5` uses this manifest shape:

```json
"$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
"name": "companion",
"version": "0.2.0",
"description": "Discuss, plan, review, schedule, capture and execute project work across connected services."
```

- `/Users/tai/.agents/plugins/companion/README.md:1-9` describes six existing workflows, a single shared policy file and a source/cache boundary. Reuse that small package shape. Do not copy its whole policy or writing assets.
- `/Users/tai/.agents/plugins/companion/skills/execute-companion/SKILL.md:10-16` resolves identity, refreshes state, preserves unrelated fields, reads back writes and checks state before retrying. These are behavioral exemplars, not permission to modify Companion.
- `/Users/tai/.agents/plugins/companion/shared/references.md:65-85` states that capture does not authorize unrelated changes, existing authorization carries across handoffs and a request can go directly to its owner.
- `/Users/tai/.agents/plugins/companion/skills/capture-companion/evals/evals.json` provides a dry-run evaluation exemplar. Its `expectations` format differs from Skill Creator's grading `assertions`; normalize explicitly for the evaluation runner, not by silently assuming compatibility.

### Connected facts inspected on 2026-10-20

- Orchestra: https://app.notion.com/p/3fe0a859ed1f81348d1dedfed8fe526f
- Agents Ticket database: https://app.notion.com/p/3ff0a859ed1f80728ae0fdb996889173
- Data source: `collection://3ff0a859-ed1f-80c4-b3b1-000b9c10da55`.
- Development workflow: https://app.notion.com/p/3fe0a859ed1f81a5ba2cd3ff5fe930bf
- Second Brain: https://app.notion.com/p/4e60a859ed1f828f9bdf81026a1c2662

Observed ticket properties: Ticket (title), Category, Created by, Status, Created time, Last edited time. Categories: Admin, Personal, Study, Development, Research. Created by choices: Prometheus, Hugo, Atlas, Astra, Loki, Forge. Status choices: Capture, In progress, Machine review, Human review, Done, Archived. Templates: New Intent, New Plan, New Spec. These facts are snapshots, not hard-coded tool schemas.

Orchestra prose describes an older, richer schema and lifecycle. The Development document makes Atlas/Wiki optional and retains Forge planning, implementation and review gates. The user's new proposal requests Wiki context for every new or materially changed intake. Do not silently overwrite the earlier domain policy. Resolve this before activating that lane.

Second Brain navigation exposes Notes, Resources & References and Projects. Its read was partial with six unsupported Quick Capture buttons. No button behavior, exact destination schema or relation is established.

### Approved direction from the discussion

1. Keep Orchestra Companion separate from Companion and domain plugins.
2. Keep one ticket through intent, context, plan/spec, decisions, execution and review.
3. Start ticket control with `receiving-ticket` and `routing-ticket`.
4. Expose request-brainstorm, request-plan, request-execute, request-review, request-audit, request-reconcile and request-handoff as thin action skills sharing one contract.
5. Domain capture supplies intent and enough known context. Preserve originating actor, such as Loki, across later handoffs.
6. Request Wiki context before human route review for new or materially changed intake, subject to the domain-policy conflict above.
7. A bot returns a result. Orchestra records it and chooses the next action with the user. Do not force every request through all seven action kinds.
8. No scheduler, DAG engine, queue service, automatic watcher or new task database.

Latest diagram: `/Users/tai/research-projects/.archify/workflow-orchestra-control-20261020-152123/orchestra-control.html`. It is optional visual context. This plan remains self-contained without that file.

## Suggested executor toolkit

- `/Users/tai/.agents/skills/skill-creator/SKILL.md`: draft, dry-run evaluation, human feedback and revision.
- `/Users/tai/.agents/skills/writing-for-agents/SKILL.md`: focused persistent instructions and reference ownership.
- `/Users/tai/.agents/skills/simple-english/SKILL.md`: Plain register.
- Native Notion tools: read schema and record identity; later write/readback only with explicit pilot authorization.
- Existing host delegation tools: discover actual capabilities. A plugin name alone is not callable transport.

## Scope

Future implementation may create only:

```text
plugins/orchestra-companion/
  plugin.json
  README.md
  shared/references.md
  shared/examples.md
  skills/receiving-ticket/SKILL.md
  skills/routing-ticket/SKILL.md
  skills/request-{brainstorm,plan,execute,review,audit,reconcile,handoff}/SKILL.md
  evals/evals.json
  evals/fixtures.json
plugins/orchestra-companion-workspace/   # evaluation outputs and qualification records
```

Each brace expression above expands to seven real skill directories. Do not generate empty directories or unnecessary scripts. Add a deterministic check only for a responsibility that cannot be verified with existing tools.

Keep out of scope:

- Companion renaming/refocusing; Wiki, Research, Admin or Study plugin implementation.
- Adding capture skills to existing plugins or global always-capture rules.
- `skills/`, `.skill-lock.json`, `plugins/marketplace.json`, installed caches and global agent instructions.
- Notion schema/template migrations, live ticket creation and source document edits.
- Credentials, sync settings, external messaging, automatic workers and runtime services.
- Scientific data, analysis, experiment execution, GitHub merge or publication.

Domain capture adapters and Wiki Companion are integration dependencies. Use fixtures or an explicitly labelled manual context handoff until their real capabilities exist. Never pretend these proposed plugins executed.

## Commands and verification baseline

Run from `/Users/tai/.agents` unless stated otherwise.

| Purpose | Command | Expected result |
|---|---|---|
| Observe baseline | `git status --short` | Record all pre-existing paths without editing them |
| Validate JSON | `python3 -m json.tool plugins/orchestra-companion/plugin.json` | Exit 0 |
| Validate one skill | `python3 /Users/tai/.agents/skills/skill-creator/scripts/quick_validate.py plugins/orchestra-companion/skills/receiving-ticket` | Exit 0; valid skill |
| Validate evaluation input | `python3 -m json.tool plugins/orchestra-companion/evals/evals.json` | Exit 0 |
| Inspect patch hygiene | `git diff --check -- plugins/orchestra-companion plans/007-orchestra-companion.md plans/README.md` | Exit 0; separately inspect newly created files |
| Evaluation viewer | `python3 /Users/tai/.agents/skills/skill-creator/eval-viewer/generate_review.py --help` | Exit 0; use supported static output arguments |

Validator and viewer paths were located during recon. Their execution was not tested in the planning turn. If Python dependencies or runner support are missing, report the gap. Do not install dependencies without scope approval. No repository-wide build/test command was established; this is a skill package, not an application build.

## Target contracts

### Ticket control

`receiving-ticket` accepts a canonical ticket reference or an authorized capture packet. Read current schema and body, verify identity and duplicates, classify domain/input kind, identify missing information and preserve history. New authorized tickets start at Capture. Existing follow-ups reuse the ticket and retain origin. Input kind stays in content unless a field migration is approved.

For new or materially revised input, request scoped Wiki context. Sources may include relevant `~/learn` entrypoints, named GitHub paths, specific Drive folders and related Notion records. A request does not mean scanning all systems. Missing capability/access is an explicit gap. Do not claim no evidence exists from an inaccessible source. Reuse valid context for unchanged result returns.

`routing-ticket` reads the concrete human decision or already-granted authority. Bind target bot, action, scope, destination and proposal revision. It can propose a route while unresolved, but cannot claim dispatch. Rejected or deferred proposals remain preserved without executing.

### Bot request control

All seven request skills read the same shared contract. Each states its action-specific input, expected return and boundary. Keep specialized brainstorming, planning, execution and auditing procedures with their owners.

Request fields: ticket ID, request ID, input/proposal revision, target bot/plugin/skill, action, objective, input/source links, exact scope, permitted effects, authority evidence, acceptance criteria and return destination.

Return fields: matching IDs and revision, outcome, findings, output links, actual actions, verification, limitations and next needed decision. Outcomes: completed, partial, needs-input, failed, declined. These are job outcomes in content, not new Notion Status values.

- brainstorm: alternatives and unresolved choices, not implementation.
- plan: bounded plan/spec and acceptance evidence, not execution permission.
- execute: exact approved effects within domain gates.
- review: machine assessment of a named packet/version. Asking the human for a decision is a separate interaction, not a machine review job.
- audit: named audit scope; external processing only when explicitly authorized.
- reconcile: compare actual state with the approved effects; fixes require their own existing authority.
- handoff: transfer a bounded job to an available receiver. If specifically preparing a next-session handoff, invoke the host's owning handoff skill rather than inventing a format.

Sent, accepted, completed and user-accepted are distinct. An unavailable host transport produces a proposed handoff only. Never start another chat or send another chat a message without direct user authorization under that host's rules.

### State and human review

Use existing observed status choices, with phase/purpose in content. Propose this mapping for owner review before live use:

- Capture: raw intent registered and not ready for a route decision.
- Machine review: requested context or assessment being evaluated; does not assert a deployed background job.
- Human review: a concrete versioned route/plan/result packet awaits the user.
- In progress: a confirmed authorized assignment is active.
- Done: approved required effects are verified and no required work remains.
- Archived: explicit management archival only; not deletion or automatic rejection.

Track needs-input, failed, declined, deferred and stale in content without inventing new status options. Preserve actual decisions; a status cell is not authenticated approval. Apply no related status propagation. Material revisions invalidate only the affected proposal/approval; retain prior history.

## Steps and gates

### 1. Confirm baseline and write the shared contract

Re-read the cited Notion pages, current schema and local exemplars. Record access/coverage and conflicts in the workspace. Read applicable instructions and isolate source work from unrelated changes before implementing. Do not treat the current dirty branch as a clean implementation baseline.

Draft `shared/references.md` with the contracts above, source ownership and ticket body sections. Draft synthetic examples in `shared/examples.md`, including Volatile PDA and a non-Research intake. Keep deployment configuration and private facts outside the distributable package.

Verify: `git status --short` and inspect the two new files. Gate: every request/return field and state boundary above is present; no out-of-scope file changed. Save this checklist and results in `orchestra-companion-workspace/contract-review.md`. Stop for the universal-Wiki/Development policy decision before live activation; fixture-based authoring can continue.

### 2. Draft the plugin and two ticket skills

Follow the existing manifest's format with name `orchestra-companion` and an initial development version. Use `receiving-ticket` and `routing-ticket` as skill names. Keep descriptions specific to their triggers. README must state manual invocation, source/cache distinction, proposed dependencies and explicit write/readback boundaries.

Verify: run JSON validation and quick_validate for both skill directories. Exit 0 is required. Check all relative Markdown links resolve. Do not add package-specific discovery fields without verifying the current host convention.

### 3. Add the seven thin request skills

Create exactly the seven request directories listed in Scope. Each loads the shared contract and describes only its distinct purpose. Do not implement seven copies of routing, transport or retry logic. Read real target skills before claiming compatibility; unresolved target names stay explicit in examples.

Verify: run quick_validate once per directory, nine skills total including ticket skills. Record command/exit for each. Read the cumulative diff to confirm no specialist workflow was duplicated. Stop if exposing commands requires edits to protected marketplace/cache/global files.

### 4. Evaluate with synthetic fixtures

Create `evals/evals.json` and `evals/fixtures.json`. Run Skill Creator's with-skill and baseline comparison on the same fixtures with no live writes. Use supported executor/runner mechanisms only. If isolated runs are unavailable, report that limitation and use labelled inline walkthroughs, not fabricated scores.

Required cases: (1) new Volatile PDA capture with origin Loki; (2) duplicate and same-ticket follow-up; (3) missing Wiki/access with no fabricated context; (4) Development conflict with mandatory lookup; (5) no human approval; (6) exact approved request-plan without implementation; (7) unavailable target/transport; (8) stale return; (9) partial write followed by retry; (10) machine review versus human acceptance; (11) unrelated status/Second Brain filing rejected; (12) external audit without processing authority; (13) concurrent unresolved request does not create duplicate job; (14) terminal job refinement gets a new request ID within the same ticket.

For each case assert correct target/IDs/revision, allowed effects, preserved origin/history, accurate partial state and no false dispatch/success. Fixtures must contain no private source text or secrets. New request names must not imply installed bot discovery.

Verify: JSON parses; each case has actual recorded output, grading evidence and timing when the runner supplies it. Aggregate using Skill Creator's documented schema. Generate its review viewer and collect human feedback before claiming behavioral readiness. Require all authorization, identity, duplicate and false-success assertions to pass. Explain failures rather than averaging them away.

### 5. Review the cumulative candidate and stop at qualification

Check package structure, relative links, no unsupported commands and exact scope. Run all nine validators, both JSON checks and scoped diff hygiene again after any repair. Review the complete candidate and evaluation evidence against this plan. Report residual limitations, including untested fresh-chat discovery and connector writes.

Verify: save `orchestra-companion-workspace/qualification.md` with actual command results, evaluation findings, changed-file list and the verdict READY FOR INSTALL REVIEW or REVISE. Update Plan 007's index row to describe candidate completion, not installed completion.

Installation or a live pilot is a separate authorized step. It must verify source/cache identity, fresh-chat routing, exact sandbox ticket schema, real connector readback and actual host dispatch. A live pilot must not edit the real Volatile PDA records by default.

## Execution batches

- Batch A: steps 1-3, candidate authoring only. Human review of the shared contract ends the batch if unresolved choices affect behavior. Keep fixtures unconnected to live sources.
- Batch B: steps 4-5, synthetic evaluation and cumulative review. Human feedback ends the batch. No automatic evaluation-to-install transition.
- Installation, Notion migration, domain adapters, Wiki implementation and live dispatch are excluded follow-ups. Record their dependencies without implementing them.

## Reuse references

Borrow concepts, not a new engine:

- https://a2a-protocol.org/latest/topics/life-of-a-task/ : continuing context versus individual immutable terminal jobs. Ticket maps conceptually to context; request ID maps to a job. Do not claim A2A conformance.
- https://docs.langchain.com/oss/python/langchain/multi-agent/subagents : supervisor selects a specialist and integrates its return; shared dispatch is an available pattern.
- https://docs.langchain.com/oss/python/langchain/human-in-the-loop : distinguish proposed effects from human decisions. Runtime adoption would require checkpoint/persistence design and is outside scope.
- https://github.com/Algorant/tandem : concrete task-contract/delegation example. Repository lists MIT; inspect exact files and license before copying. Do not introduce its task store as a second authority.

These sources were retrieved through Exa in the design discussion. No implementation was installed, benchmarked or audited. Check current versions and license before any reuse.

## Done criteria

- [ ] New plugin contains two ticket skills and seven thin request skills, all nine passing quick_validate.
- [ ] Manifest and evaluation JSON parse; local links resolve.
- [ ] Shared contract has one authority for IDs, revisions, effects, outcomes, decisions and retry/readback.
- [ ] Synthetic cases have actual outputs and assertion evidence; critical assertions pass.
- [ ] Human evaluation feedback has been incorporated or left as an explicit unresolved gate.
- [ ] Cumulative review confirms no out-of-scope changes or secret/private source reproduction.
- [ ] Qualification distinguishes structural validation, behavioral evaluation, installation and live integration.
- [ ] Candidate is not installed, published or represented as a functioning runtime.

## STOP conditions

Stop the affected step and report if baseline/source contracts materially drift, the target plugin already exists with overlapping ownership, an instruction conflict cannot be resolved, a required validation fails twice, or implementation needs a protected path. Also stop live integration if the Wiki/Development policy remains contradictory, connectors cannot prove identity/readback, or no real dispatch mechanism exists. Continue independent plan-authorized fixture work where safe. Never substitute a different executor/provider silently.

## Maintenance notes

Keep actor identity, plugin identity and host transport separate. Keep current records in their owning sources and link them from the ticket. New actions must reuse the request contract and add specific evaluation cases. A schema or host-command change requires refreshed qualification. Do not turn a successful candidate evaluation into claims of installed behavior, completed work or scientific acceptance.

## Planning validation record

This planning turn read the Improve template, existing plans index, Companion manifest, Execute skill, shared policy and capture evaluation exemplar. It ran target-repository preflight with no fetch or GitHub queries. Preflight observed the unrelated dirty paths stated above. No source implementation, tests, installation, Git commit, push or external write was performed. Commands listed for future implementation are gates, not claims that those checks passed now.
