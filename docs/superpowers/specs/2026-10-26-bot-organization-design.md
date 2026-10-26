# Bot Organization Design

Status: approved by Tai on 2026-10-26.

## Purpose

Organize Tai's OpenBot agents into departments with clear owners, and keep each bot's information in one folder, so that every new bot is set up completely before it goes live.

## Scope

In scope: the Bot Management department, the Technician department, the new-bot checklist, the bot file layout, and the write locations for specs and plans.

Out of scope: Plan Crew (Forge, Reviewer A, Reviewer B, Executor). Those agents belong to the Dev Team and are not changed by this design.

## Departments

### Bot Management, headed by Donna

Donna is the Head of Bot Management and reports directly to Tai. Three members work under her:

1. **Skills and MCP tools:** installs, revises, and checks skills and MCP tools for all bots.
2. **Workflows:** defines how work moves between bots.
3. **Profile, identity, cron, runtime, and permissions:** sets up each bot's profile, identity, scheduled jobs, runtime (cloud, local, or hybrid), and permissions.

Donna makes sure each new bot passes the checklist below before it goes live.

### Technician, headed by Bob

Bob is the Technician and belongs to its own department. Bob takes plans that Tai approves and produces skill and update work using `writing-skills`. Once Bob exists, Tai may ask Bob to create skills for routing information.

## Intake

Tai can message Donna, Bob, or the Secretary directly. Donna completes the requests that concern bot setup and reports the result to Tai.

## Bot files

All bot information lives under `~/.agents/docs/bots/`. That folder is Donna's. Donna writes it. Other agents may read it but do not write to it.

Each bot has its own folder:

```
~/.agents/docs/bots/<bot-name>/
  <bot-name>.md          # metadata and the bot's overview
  soul.md                # the bot's identity and conduct
  workflows/             # always created, even with one workflow
    workflow-1.md        # one file per workflow
    capabilities.yaml    # the skills and MCP tools the workflows use
```

- `<bot-name>.md` has these fields: `name`, `title`, `instruction`, `owner`, `soul: soul.md`, `runtime` (hybrid for now; cloud is set up later), and a short body. The body describes the bot's workflows and links to each one, with a wiki link back to `[[<bot-name>]]`.
- Each `workflows/workflow-N.md` links back to `[[<bot-name>]]`.
- `capabilities.yaml` has two lists: `skills` and `mcps`. Each entry names the item and the workflow that uses it.
- Memory is not stored in these files. Each bot uses the native OpenBot memory.

Harley is the first example, and Harley is the Secretary. Donna creates `harley/` from the Secretary's profile.

## New-bot checklist

A new bot is live only when all of these are set and checked by Donna:

- Profile: name, title, and standing instructions, recorded in `<bot-name>.md`.
- Identity: the owner is recorded in `<bot-name>.md`.
- Skills and MCP tools: listed in `capabilities.yaml`, and installed and enabled in OpenBot.
- Workflow: at least one `workflows/workflow-N.md` exists and is linked from `<bot-name>.md`.
- Scheduled jobs: none, or each one is approved by Tai.
- Runtime: `hybrid`, or cloud, local, or hybrid as chosen for this bot. Recorded in `<bot-name>.md`.
- Permissions: workspace access by default. Full access and Computer Use are set only by Tai.

## Rules

- Tai approves each new bot before Donna creates it.
- Only Tai can give Full access, turn on Computer Use, or change auto-approve.
- Nothing is deleted without Tai's approval. Agents can be deleted only in the app.
- Specs go to `~/.agents/docs/superpowers/specs/`. Plans go to `~/.agents/docs/superpowers/plans/`.

## Open items

- Donna's access is `workspace`, which does not reach `~/.agents/docs/bots/`. Tai must decide whether to set her to Full access. Until then, Donna cannot write the bot files.
- The three existing "Bot Dev" agents are to be deleted by Tai in the app. They are not part of this structure.
