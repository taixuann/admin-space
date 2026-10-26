# Create a bot

Purpose: turn Tai's request into a bot folder that Tai approves, Harvey applies with bot-ctl, and Harvey verifies. Run every phase in order. Do not skip one.

Parent: [Harvey](../SOUL.md) · Shared rules: [bot folders](../../../AGENTS.md) · Diagram: [create-bot.html](create-bot.html)

## Uses

Each phase names what it uses. `ok` means installed and enabled for Harvey, checked with `hermes -p harvey skills list` or `plugins list`. A name that is not `ok` is reported to Tai and never assumed.

| Phase | Skill, plugin, template or MCP | Status | Reason |
| --- | --- | --- | --- |
| 0 | `superpowers:brainstorming` | ok (plugin `superpowers`) | Decide whether a role is needed. Runs before Phase 1. |
| 1 | soul template (sections: Core Truths, Boundaries, Vibe, Style, Expertise, Continuity, Context) | template, no install | Shape of `SOUL.md`. |
| 1 | `writing-for-agents` | ok (external dir `~/.agents/skills`) | Wording of `SOUL.md` and `instruction`. |
| 2 | [plugins.yaml](../../../plugins.yaml), `hermes plugins list` | ok | Pick plugins and memory providers. |
| 2 | `hermes -p harvey mcp list` | ok | MCP servers seen: caveman-native, decision-engine, linear (disabled); notion (enabled, OAuth login for harvey pending). Ask Tai about each. |
| 3 | `hermes cron`, a script, or an MCP such as `notion` | notion MCP enabled, OAuth login pending | Only for a job Tai approves. |
| 4 | bot folders in `~/.agents/bots/`, `hermes profile list` | ok | Memory and knowledge. |
| Review, apply, verify | `bot-ctl` (`bot-management/scripts/bot-ctl`), `hermes-fleet-admin`, `hermes-agent` | ok | Observe, apply and verify the approved draft. |
| Any skill change | `superpowers:writing-skills` | ok (plugin) | Test before editing a skill. |
| Diagram | `archify` | ok (external dir) | Workflow HTML. |

- Model category: `reasoning.standard` for Phases 0 to 2. Harvey's primary is `operation.high`, so this is a known gap. Report it to Tai before the first design run.
- Runtime: local only. Do not ask about it.
- Worker: none. Harvey applies only the draft Tai approved in chat.

## Phase 0: Decide whether a role is needed

Completion: Tai picked one outcome, and the choice is in the chat summary.

1. Read the `description` line in each `~/.agents/bots/**/SOUL.md`. Note any bot that already covers the job.
2. Run `superpowers:brainstorming` with Tai before anything else. Ask what the job is, who it serves, and what a separate identity or permission adds.
3. Ask the anti-bloat question: could a skill, a script, or a new workflow in an existing bot do this job? Say so when it could.
4. Pick one outcome:
   - a. Extend an existing bot. Stop and write the change into that bot's workflows.
   - b. Use a skill or script with no new bot. Stop.
   - c. Create a new bot. Continue to Phase 1.

## Phase 1: Soul, model and permissions

Completion: `SOUL.md` and `config.json` exist, every field is set or `none`, and every permission and model comes from Tai's answer.

1. Ask Tai for the bot's purpose, the people it serves, and what it must never do. Ask only what the files cannot answer.
2. Write `<group>/<bot>/SOUL.md`: frontmatter (`name`, `title`, `description`, `instruction`, `enable`), then Core Truths, Boundaries, Vibe, Style, Expertise, Continuity, and `## Context` (the files the bot loads). Use `writing-for-agents` for the wording. Keep it under 200 lines. Do not add a `## Model` section: the model lives in `config.json`.
3. Ask Tai for each `dirs` path and its access level. Ask Tai for the model alias from `models.yaml`. Assume none.
4. Write the approved values into `config.json`. Mark each field `proposed`.

## Phase 2: Workflows, plugins and MCPs

Completion: each workflow file exists, and every skill, plugin and MCP it names is confirmed against the lists below.

1. Write the job: its trigger and its success criteria.
2. Check `<group>/<bot>/workflows/` and other bots' workflows for a match. Extend a match instead of duplicating it.
3. Count the actions. Map each to a skill, script, plugin, MCP or agent. Use a script for fixed steps. Use an agent only where judgment is needed.
4. Consult [plugins.yaml](../../../plugins.yaml) and `hermes plugins list`. Propose plugins and a memory provider. Ask Tai before enabling any.
5. Run `hermes -p harvey mcp list`. Ask Tai, for each server: does this bot use it? Record yes or no. Enable nothing without a yes.
6. Write `workflows/<name>.md` with phases, explicit handoffs between bots or people, error recovery per step, which steps run in parallel or in sequence, a `Uses` table in the form above, and a link to `../SOUL.md`.
7. Validate every named skill, plugin and MCP against the lists. If one is missing, do not write the file. Report the gap to Tai.

## Phase 3: Automation

Completion: every job has the seven items below, and every outside destination has Tai's approval.

1. For each job, decide on schedule or on demand, and agent or script.
2. Record: trigger, timeout, retries, failure handling, output destination, notification, recovery.
3. A job that publishes to an outside system, such as a Notion page, needs Tai's approval naming the destination. The `notion` MCP is enabled for harvey, but its OAuth login is pending, so it also needs Tai's yes in Phase 2.
4. No job is added unless Tai asks for one.

## Phase 4: Memory and knowledge

Completion: Tai confirms the context list and the memory choice.

1. Memory: the bot folders hold what each bot does. Harvey reads `~/.agents/bots/` to know every bot. Build no separate wiki or index.
2. Knowledge: the live profiles. Read them with `hermes profile list` and `bot-ctl observe <bot>`.
3. Each bot uses its own native Hermes memory unless Tai picks an external provider from `plugins.yaml`. Create a shared memory bank only when Tai asks.
4. Check that `## Context` lists every file the bot needs. Store no credentials, raw data or full run logs in any bot file.

## Review, apply and verify

Completion: Harvey sent Tai a verify report with the result of each check.

1. Run the pre-send check in [AGENTS.md](../AGENTS.md). Any failure or suspicious item stops here and goes to Tai.
2. Summarize the draft: the soul, workflows, permissions, plugins, MCPs, jobs, and every field still `proposed`. Run `python3 ~/.agents/bots/bot-management/scripts/bot-ctl apply <bot> --dry-run` and show Tai its output.
3. Wait for explicit approval of that exact delta. A question about the draft is not approval. Any change after approval needs a new approval.
4. Apply: `python3 ~/.agents/bots/bot-management/scripts/bot-ctl apply <bot>`. Always pass the bot's name. The tool backs up the profile to `~/.hermes/profiles/<bot>/backups/<timestamp>/` first, leaving out `.env`, then sets the SOUL symlink, model, skills and memory, then runs a smoke test ("say hi").
   Completion: exit 0 and the backup path is in the output. Exit non-zero: stop, report the output to Tai, and do not retry with a different change.
5. Sync: check `config.json`, skills, `SOUL.md` and workflows together. Regenerate each workflow's HTML with `archify` into `.archify/`, link it, and pass the browser check.
6. Verify: `python3 ~/.agents/bots/bot-management/scripts/bot-ctl verify <bot>`. Exit 0 means every check matches. Exit 1 lists each drift or missing row: report them to Tai. A plugin or MCP drift is not fixed by Harvey; Tai decides.
7. Read back with `hermes -p <name> config get`, check identity loads in a fresh session, and run one real request. Mark each field `configured` or `verified`. Report pass, blocked or untested per check.

## Error recovery

- Phase 0 ends in outcome a or b: stop. Create no bot.
- A required skill, plugin or MCP is missing: stop at Phase 2 step 7 and report it.
- Tai does not approve: keep the draft. Apply nothing.
- Apply exits non-zero: report the output. Do not retry without Tai's decision.
- Verify shows drift or missing: report the rows. Return to the draft only if Tai asks.
- A plugin or MCP in `config.json` is not live: `apply` does not change it. Report it; Tai decides whether to enable it or change `config.json`.
