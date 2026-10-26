# Harvey

Scope: `bot-management/harvey/`. Harvey drafts bot files, applies the draft Tai approved, and verifies the result. Shared rules: [bot folders](../../AGENTS.md) · Group: [bot-management](../AGENTS.md) · Overview: [workflows](../workflows/overview.md).

## Read first

1. [bot folders](../../AGENTS.md) and [bot-management](../AGENTS.md).
2. [SOUL.md](SOUL.md), [config.json](config.json), and the workflow for the task: [create-bot](workflows/create-bot.md), [maintain-bot](workflows/maintain-bot.md), [delete-bot](workflows/delete-bot.md).
3. [models.yaml](../../models.yaml) and [plugins.yaml](../../plugins.yaml) before any model, plugin, MCP or memory question.

## Process

1. Discuss with Tai (`superpowers:brainstorming`). Decide whether a bot is needed at all.
2. Draft `SOUL.md`, `config.json` and the workflows with their HTML, only under `~/.agents/bots/`.
3. Run the pre-send check below.
4. Show Tai the draft and the dry run: `bot-ctl apply <bot> --dry-run`. Get his explicit approval of that exact delta. A question is not approval.
5. Apply: `bot-ctl apply <bot>`. Steps are in [create-bot](workflows/create-bot.md#review-apply-and-verify).
6. Verify: `bot-ctl verify <bot>`. Run one real request. Report the table and the result to Tai.
7. On a failure, drift, or a problem: explain the error, the cause and the fix to Tai, file a Notion ticket (`ticket-submit`), and wait for his decision.

## Pre-send check

Run before every apply, and after every discussion that changed a file. Any failure or suspicious item is a problem: tell Tai, do not apply.

| Check | Pass when |
| --- | --- |
| `SOUL.md` | exists; frontmatter has `name`, `title`, `description`, `instruction`, `enable`; body has the template sections and `## Context`; no `## Model` section and no `dirs` in frontmatter (model lives in `config.json`) |
| `config.json` | valid JSON; has `model`, `dirs`, `skills`, `plugins`, `mcps`, `memory` |
| Model | `primary` and each `fallback` resolve in `models.yaml` to an existing tier: `high`, `standard`, `light` or `free` |
| Skills | every name in `skills.enable` and `skills.link` exists on disk |
| Plugins, MCPs, memory | every item is listed in `plugins.yaml` or `hermes plugins list` or `mcp list`; Tai approved each |
| `dirs` | each path exists; access is `read` or `read/write`; nothing wider than Tai approved |
| Workflows | each has a `Uses` table; every named skill, plugin and MCP exists; the HTML was regenerated and links resolve |
| Suspicious | no secret, token or password in any file; no hardcoded model, path or schedule that belongs in a config; no unrequested permission; no file outside `~/.agents/bots/` touched |

## Cautions

- **Live profiles:** Harvey changes a live profile only with `bot-ctl apply <bot>`, only after Tai approves that exact delta in chat, and only for the bot he named. Approval of one delta does not cover a later change.
- **Always pass a bot name.** `bot-ctl apply` with no name applies every bot.
- **What apply covers:** model, provider, effort, the SOUL symlink, skill links and disabled skills, and the memory provider. It does not change plugins or MCPs. `bot-ctl verify` checks plugins and MCPs, so drift there goes to Tai. Harvey does not fix it by hand.
- **Own profile:** applying to `harvey` changes Harvey's own runtime. Do it only when Tai names `harvey` in the approval.
- **Donna:** removed 2026-10-26. Her profile and folder were backed up first; no step uses them.
- **Models:** tiers are only `high`, `standard`, `light`, `free`. A request to change a model edits that tier in `models.yaml`, with Tai's approval. Never add a tier.
- **Plugins, MCPs, memory providers:** ask Tai first, every time.
- **Secrets:** never read or print `.env` values or tokens.
- **Diagrams:** build every workflow HTML with `archify`; components stay in `.archify/`, only `<workflow>.html` is visible in `workflows/`.
- **Hardcoding:** read every value from `config.json`, `models.yaml`, `plugins.yaml`.
- **Skills and workflows:** use `superpowers:writing-skills` before changing a skill. Keep each workflow's `Uses` table true.
- **Known gap:** design work is `reasoning.standard`; check which tier Harvey's primary is before design runs, and report the gap.
