# Bot folders

Scope: `~/.agents/bots/` and every bot folder in it. Harvey writes here. Other bots may read these files but do not write to them.

## Read first

1. This file.
2. The bot's `SOUL.md`.
3. The bot's `workflows/` file for the task.
4. `~/.agents/AGENTS.md` for shared Admin rules.

## Layout

```
bots/
  AGENTS.md                this file: shared rules for every bot folder
  models.yaml              approved models and aliases (Tai edits)
  plugins.yaml             plugin, MCP and memory-provider catalog (Tai approves)
  <group>/                 a group of related bots, with its own AGENTS.md
    <bot-name>/
      SOUL.md              frontmatter metadata and the bot's identity
      AGENTS.md            responsibility, scope, and operating rules for the bot's work
      config.json          model, dirs, skills, plugins, mcps
      workflows/           always present, even with one workflow
        <workflow-name>.md purpose, steps, uses, checks
```

Harvey is in the group `bot-management/`. Its workflows are in `bot-management/harvey/workflows/`: `create-bot.md`, `maintain-bot.md`, `delete-bot.md`. Donna was removed on 2026-10-26.

## Where each field lives

| Field | Location |
| --- | --- |
| `name`, `title`, `description`, `instruction` | `SOUL.md` frontmatter |
| `enable` | `SOUL.md` frontmatter. Only `true` or `false` |
| Identity | `SOUL.md` body |
| Responsibility, scope, operating rules | `AGENTS.md` in the bot folder |
| Context | `SOUL.md` body, section `## Context` |
| Permissions | `config.json`, `dirs`: a map of path to access (`read`, `read/write`) |
| Skills, plugins, MCPs | `config.json`: `skills.external_dirs` lists the folders Hermes reads skills from, in place, with no symlink. Apply writes that list and nothing else for skills. Which skills are on or off is Tai's choice in the live profile, not a config list. Core skills a workflow needs are named in its `Uses` section. `plugins.enable` and `mcps.enable` list what the bot must have on. A profile cloned from `default` inherits every plugin and MCP server; Tai turns each other one on or off live, and verify reports any mismatch. |
| Model | `config.json`, `model.primary` and `model.fallback` as alias names. Definitions are in `bots/models.yaml`, approved by Tai |
| Why each skill, plugin, MCP is used | The `Uses` section of each workflow file |

Do not put dirs, skills, plugins, MCPs, or workflow steps in frontmatter. Do not record a runtime. Bots run locally.

## Model category by work

Each workflow's `Uses` section names the model category its work needs. Categories are defined in `models.yaml`.

| Work type | Category | Examples |
| --- | --- | --- |
| Design, planning, judgement | `reasoning` | deciding whether a bot is needed; writing a workflow |
| Writing or changing code and skill files | `coding` | editing a `SKILL.md` or a script |
| Routine checks and approved changes | `operation` | observe, verify, apply, delete |
| Anything else | `general` | short answers, summaries |

`config.json` sets one primary alias per bot, because a bot runs one model at a time. A workflow whose category is above the primary's category is a known gap. Report it to Tai. Do not downgrade the work silently.

## Rules

- `dirs` in `config.json` is policy, not an enforced sandbox. Tai decided on 2026-10-26 to keep it that way: no Docker backend.
- Model tiers are fixed: `high`, `standard`, `light`, `free`. A model change edits an existing tier in `models.yaml`; it never adds a tier.
- Before any apply, run the pre-send check in the sending bot's `AGENTS.md`.
- Workflow diagrams: build with `archify`. Keep every component (candidate, receipts, review folders) in the hidden `.archify/` of the bot or group; only `<workflow>.html` is visible, as a symlink in `workflows/`. Regenerate the HTML whenever its `.md` changes.
- Never hardcode a variable in a workflow, script or check: models, skills, plugins, MCPs, paths and schedules are read from `config.json`, `models.yaml` and `plugins.yaml`.
- Ask Tai before any change to a plugin, MCP or memory provider, in a bot's `config.json` or in a live profile. Consult `plugins.yaml` first.
- Every bot has `SOUL.md`, `AGENTS.md`, `config.json` and `workflows/`. A field may say `none` or `inherit`. Never leave a field out.
- `SOUL.md` says who the bot is. `AGENTS.md` says what the bot is responsible for, where its work lives, and what it must not do. Each rule sits in one of the two, not both.
- Mark each field `proposed`, `approved`, `configured`, or `verified`. Keep intent apart from what was observed.
- Each workflow step ends with a completion criterion that can be checked.
- Link each workflow to `../SOUL.md`. Link `SOUL.md` to its workflow files. Use relative Markdown links.
- Before a new bot exists, run the Phase 0 decision in `harvey/workflows/create-bot.md`.
- Keep credentials, raw data, and run logs out of every bot file.

## Approval gates

Tai approves each of these:

- the draft, before anything is applied: each apply runs only the exact delta Tai approved in chat, and any change after approval needs a new approval;
- every permission path and access level;
- every plugin or MCP that adds access;
- every scheduled job;
- every publication to an outside system, such as a Notion page;
- every deletion;
- commits and Hermes configuration changes.

## Open items

- Harvey's model is `operation.high` (Sonnet 5.5, low effort). The effort setting is not verified in the runtime. Its design work is a known gap against `reasoning.standard`.
- Harvey's plugin list is unconfirmed. Superpowers is listed for Phase 0 and for skill changes. Tai confirms.
- `hermes-fleet-admin` still names Secretary, Executor, and Superpowers. Its four-phase rewrite needs a `superpowers:writing-skills` baseline before any edit. The skill is shared under `~/.hermes/skills/`, so Tai approves that edit first.
- The older design `docs/superpowers/specs/2026-10-26-bot-organization-design.md` and `docs/bots/` still describe Donna, Bob, and a different layout. Tai decides whether to supersede or delete them.
- Harvey's session loads this file only if its working directory is `~/.agents/bots/`. Not tested.
