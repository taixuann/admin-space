# Bot management

Scope: the bot that creates and applies other bots: `harvey/`. Donna was removed on 2026-10-26. Shared rules are in [bot folders](../AGENTS.md).

## Read first

1. [bot folders](../AGENTS.md).
2. The bot's `SOUL.md`, `config.json`, and the workflow for the task.
3. [plugins.yaml](../plugins.yaml) before any plugin, MCP or memory question, and [models.yaml](../models.yaml) for aliases.

## Split of work

| Bot | Does | Never does |
| --- | --- | --- |
| [Harvey](harvey/SOUL.md) | Drafts bot files, asks Tai, applies the approved delta with `bot-ctl`, verifies. | Applies a delta Tai did not approve in chat. Decides what a bot should be. |

Donna was removed on 2026-10-26. Her profile and bot folder were backed up first (`~/.hermes/backups-admin/donna-20261026-200046/`). No workflow uses her.

Live profile changes (config, skills, model, memory) are made by Harvey with `bot-ctl apply <bot>`, only after Tai approves that exact delta in chat. Tai set this on 2026-10-26, replacing the Donna card path. It is not a permission for any other change. Plugins and MCPs are never changed by apply: Tai decides those one by one.

Each bot's runtime `SOUL.md` is a symlink to its file here. After moving a folder, retarget the link and read it back.

## Shared CLI (`scripts/bot-ctl`)

Unified CLI located at `bots/bot-management/scripts/bot-ctl`:

- `observe <bot> [-c <category>]`: Audit live profile state vs declared config (`soul`, `models`, `skills`, `plugins`, `mcp`, `memory`).
- `apply <bot> [--dry-run] [--no-smoke]`: Apply declarative config to Hermes profile with timestamped backup, SOUL symlink, skill linking & disabling, model/memory setting, and live smoke test. Covers model, SOUL, skills and memory only. Always pass the bot name: with no name it applies every bot.
- `verify [bot] [-c <category>]`: Strict assertion verification (exit 0 on match, exit 1 on drift/missing). Also checks plugins and MCPs, which apply does not change.
- `pull plugins [--write]`: Pull live plugins/MCPs catalog from Hermes and report diff with `plugins.yaml`. `--write` changes `plugins.yaml`: Tai approves first.

The code is `scripts/bot_ctl.py`, the only apply and verify code. It replaced `donna/scripts/apply.py` and `verify.py`, which were removed with the Donna folder.

