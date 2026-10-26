# Bot models, configuration, and overview: design

Status: **draft for Tai's approval. Not built.**
Scope: the bot folders under `~/.agents/bots/`, Harvey's and Donna's roles, and one daily catalog job.
Supersedes: nothing yet. The older `2026-10-26-bot-organization-design.md` still describes Donna and Bob. Tai decides whether it is replaced.

## Intent

Each bot runs with a known model, known on/off switches and a readable overview. Tai does not pick models by hand each time. A daily job refreshes what models are available and how much quota is left, then proposes switches. Tai approves each switch. Donna applies only what Tai approved.

## Non-goals

- No automatic switch of a live profile's model. Every switch needs Tai's approval.
- No ranking by benchmark until a benchmark source and a scoring rule are approved.
- No restore of the removed OpenCode model router. It covered OpenCode only. A later integration should cover Codex, Claude, and others. Not now.
- No runtime field in bot files. Bots run locally.
- No symlinks into Hermes state (SQLite databases, lock files, sessions).

## Decisions from Tai

- Switches: the system proposes, Tai approves, Donna applies.
- The daily job refreshes the catalog on its own schedule. This design reads that as: the catalog updates daily, and a switch to a bot's model is a separate approval. **Confirm this reading.**
- `config.json` is desired state. Donna applies it, and Verify compares it with the live profile.

## Layout

```
bots/
  AGENTS.md                      shared rules
  models.yaml                    model catalog and aliases (see below)
  <bot-name>/
    SOUL.md                      frontmatter and identity
    config.json                  desired switches and model aliases
    cron/
      jobs.json                  generated snapshot of `hermes -p <bot> cron list`; read-only
    workflows/
      <workflow-name>.md         steps, and a Uses section for each skill, plugin, MCP
      workflows.html             public overview, built by Archify
      .archify/                  Archify build bundle: candidate, build script, receipts
```

## models.yaml

Two sections, with different owners so a daily refresh never overwrites a decision.

- `catalog`: written by the daily job only. For each model: provider, endpoint, model ID, reasoning effort, quota remaining, health (reachable or not), and the time it was last checked.
- `aliases`: written by Tai and by Harvey when Tai approves. Each alias maps a name, such as `coding-pro` or `free-fast`, to one catalog entry.

The alias fields follow `hermes-fleet-admin`: the provider, endpoint, model ID, and effort are a single tuple. A model name alone does not identify its transport.

## config.json (per bot)

```json
{
  "model": { "primary": "coding-pro", "fallback": ["free-fast"] },
  "skills": { "hermes-fleet-admin": true },
  "plugins": { "superpowers": true },
  "mcps": { "linear": true, "notion": false },
  "external_dirs": []
}
```

- `model`: aliases only. Donna resolves them through `models.yaml` and writes the matching Hermes keys: `model.default`, `provider`, `fallback_providers`.
- `skills`: on or off. Donna writes the disabled list (`skills.disabled`) from it. The list replaces the old one, so Donna writes the full list.
- `plugins`: on or off. **Scope to decide:** list only the plugins this bot's workflows use (small), or list every installed plugin (complete). This design proposes the small list. Unlisted plugins keep the profile default.
- `mcps`: on or off. Only MCPs Tai approved for this bot. Source: `hermes mcp list`.
- `external_dirs`: extra skill directories (`skills.external_dirs`). Empty by default.

A workflow does not choose a model at run time. Each workflow names the alias it needs in its `Uses` section. The bot's `config.json` sets the primary and fallback. A bot has one active model at a time, so a `reasoning` or `coding` role maps to a separate bot or a subagent, not a model swap inside one bot. Per-task model selection is **not verified** in Hermes.

## Daily catalog job

1. Runs once a day under the existing launchd rules (`automation/AGENTS.md`, `launchd-automation`).
2. Checks each provider in `models.yaml`: is the model listed, is it reachable, how much quota is left. It reuses the installed quota check (`quota:quota-check`) and the local quota cache. It adds no new quota source.
3. Writes the `catalog` section and a run record. It never writes `aliases`, `config.json`, or any Hermes profile.
4. For each bot whose alias is unhealthy or out of quota, writes a **proposal**: current alias, proposed alias, reason, and evidence. Proposals are files under `bots/proposals/`. Harvey shows them to Tai in chat.
5. Tai approves or rejects each proposal. Donna applies approved changes only. Verify reads the result back.

Benchmark ranking is not in the first build. It can be added later as a second source feeding the same proposals.

## Archify overview

- Each bot gets `workflows/workflows.html`, built by the Archify `workflow` type from that bot's workflow files and `config.json`. Its build bundle is `workflows/.archify/`.
- The page is a view. It is rebuilt from the sources. It is not edited by hand and it is not a dashboard.
- Each rebuild uses a fresh output folder, as the profile rules require, and the hash of the final HTML is checked.
- **Decision:** one overview of all bots. Option 1: a per-bot page only (this design). Option 2: an extra `bots/overview.html` tree of all bots, built after the per-bot pages work.

## Approval gates

Tai approves: every model switch, every permission, every MCP and plugin that adds access, every new scheduled job, every external publication, and every deletion.

## Acceptance (to check when built, not now)

- The daily job runs and writes `catalog` and a run record. A hash of every profile's `config.yaml` and of `aliases` is unchanged afterwards.
- A proposal goes to Tai. After approval, Donna applies it. Verify reads the saved value and one real request, and the result matches `config.json`.
- A change made directly in a profile shows as drift in Verify.
- `cron/jobs.json` matches `hermes -p <bot> cron list`.
- `workflows.html` passes the Archify `finalize` gates. The result is reported as automated checks only, unless someone looks at the page.

## Open items

- Confirm the daily-refresh reading under Decisions from Tai.
- Plugin scope: small list or complete list.
- One overview page for all bots, or per-bot only.
- Benchmark source and scoring rule, if ranking is wanted later.
- Whether Hermes supports per-task model selection. Until verified, bots keep one model.
- Future integration of the router for Codex and Claude. Not scheduled.
