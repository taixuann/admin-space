# Bot Organization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking. This plan changes OpenBot agents and documentation files only. It has no code, so there are no test commits; each task is checked by reading back its result.

**Goal:** Set up the Bot Management department (Donna as head, three members), the Technician department (Bob), and the per-bot folders under `~/.agents/docs/bots/`, with a checklist that every new bot must pass.

**Architecture:** Donna and her three members manage bot setup and own `~/.agents/docs/bots/`. Bob is a separate department that carries out approved skill work. Each bot has one folder with its metadata, soul, workflows, and `capabilities.yaml`. All agents are OpenBot agents, created and configured through the OpenBot tools.

**Tech Stack:** OpenBot agent tools (`create_agent`, `install_local_skill`, `update_profile`, `read_agent`, `list_agents`), the local skill library, Markdown and YAML files.

**Spec:** `/Users/tai/.agents/docs/superpowers/specs/2026-10-26-bot-organization-design.md`

## Global Constraints

- New agents use workspace access and Computer Use off. Only Tai can change either.
- Tai approves each new bot, its name, and its description before it is created.
- Nothing is deleted by an agent. Tai deletes agents in the app.
- Plan Crew (Forge, Reviewers A and B, Executor) is not changed.
- `~/.agents/docs/bots/` is written only by Donna. Secretary and Bob read it and do not write to it.
- Memory is native OpenBot memory. No memory file is created for any bot.
- Donna has Full access, set by Tai on 2026-10-26. Tasks 5 and 6 depend on it.

## Review Focus

- A bot is created with a checklist item missing (profile, identity, skills, workflow, scheduled jobs, runtime, permissions). Test: Task 7 Step 2 checks all seven for each bot.
- An agent has Full access or Computer Use on that Tai did not set. Test: Task 7 Step 3 reads each agent's access and Computer Use.
- Two agents share a name in the roster. Test: Task 7 Step 4 checks names in `list_agents` are unique.
- A bot folder lacks `workflows/` or `capabilities.yaml`, or a workflow file is not linked from `<bot-name>.md`. Test: Task 7 Step 5 checks the file layout and links.
- `capabilities.yaml` names a skill that is not installed on that bot, or an MCP that is not connected. Test: Task 7 Step 6 compares it with `read_agent`.

---

### Task 1: Tai deletes the three Bot Dev agents

**Files:** none. This is a user action in the OpenBot app.

- [ ] **Step 1: Tai deletes** Bot Dev · Lead, Bot Dev · Skills & Automation, and Bot Dev · Memory & Profiles in the app.
- [ ] **Step 2: Confirm.** Run `openbot.list_agents`. Expected: none of the three names appear.

### Task 2: Create Bob, the Technician (on hold)

**Status:** on hold. Tai may drop the Technician department. Do not run this task until Tai confirms.

**Files:** none (OpenBot agent).

**Interfaces:**
- Consumes: the Technician section of the spec.
- Produces: an agent named `Bob`, title "Technician: skill and update work from approved plans".

- [ ] **Step 1: Tai approves** the name `Bob` and the description below.
- [ ] **Step 2: Create Bob** with `openbot.create_agent`. Description: Bob is the Technician in Tai's OpenBot team, a separate department from Bot Management. Bob takes plans Tai has approved and produces skill and update work using `writing-skills`. Bob does not change bot setup, which belongs to Donna. Bob does not commit, delete, publish, or send without Tai's approval. Bob reads `~/.agents/docs/bots/` but does not write there. Use absolute paths.
- [ ] **Step 3: Install `writing-skills`** on Bob with `openbot.install_local_skill`, using its library id and revision.
- [ ] **Step 4: Set access.** Set access with `openbot.update_profile`, then confirm with `openbot.read_agent` that access is `workspace` and Computer Use is off.

### Task 3: Update Donna to Head of Bot Management

**Files:** none (OpenBot agent profile).

**Interfaces:**
- Consumes: the Bot Management section and the checklist in the spec.
- Produces: Donna's description names her as Head of Bot Management, lists the three members, and states the checklist.

- [ ] **Step 1: Read Donna** with `openbot.read_agent`. Note the current description and installed skills.
- [ ] **Step 2: Update Donna's description** with `openbot.update_profile`. Replace "HR department" with "Head of Bot Management". List the three members and the checklist from the spec. Keep the rules: no Hermes configuration changes, no deletions, and no publishing without Tai's approval.

### Task 4: Create the three Bot Management members

**Files:** none (OpenBot agents).

**Interfaces:**
- Consumes: the three member roles in the spec.
- Produces: three agents, each reporting to Donna.

- [ ] **Step 1: Tai approves** the three names and descriptions.
- [ ] **Step 2: Create "banana" (Skills and MCP)** with `openbot.create_agent`. Description covers skills and MCP tools for all bots, reporting to Donna. Install `writing-skills` with `openbot.install_local_skill`.
- [ ] **Step 3: Create "apple" (Workflows)** with `openbot.create_agent`. Description covers how work moves between bots, reporting to Donna. Install `writing-plans`.
- [ ] **Step 4: Create "pearl" (Profiles and Runtime)** with `openbot.create_agent`. Description covers profile, identity, scheduled jobs, runtime, and permissions for each bot, reporting to Donna. Do not install `hermes-fleet-admin` unless Tai asks; it is written for Hermes.
- [ ] **Step 5: Set access.** For each of the three, set access with `openbot.update_profile`, then confirm with `openbot.read_agent` that access is `workspace` and Computer Use is off.

### Task 5: Donna creates the bot folder structure

**Files (created by Donna):**
- Create: `~/.agents/docs/bots/<bot-name>/<bot-name>.md`
- Create: `~/.agents/docs/bots/<bot-name>/soul.md`
- Create: `~/.agents/docs/bots/<bot-name>/workflows/` (always present)

**Interfaces:**
- Consumes: the Bot files section of the spec.
- Produces: one folder per bot, and the metadata fields `name`, `title`, `instruction`, `soul`, `runtime`.

- [ ] **Step 1: Confirm Donna's access** with `openbot.read_agent`. Expected: access is `full` for Donna.
- [ ] **Step 2: Create `~/.agents/docs/bots/` if missing.** Donna creates the folder only.
- [ ] **Step 3: Create Harley's folder.** Donna writes `harley/harley.md` with the fields from the spec. Harley is the Secretary. `soul.md` is a copy of `~/.agents/docs/profiles/secretary/SOUL.md`. The body describes Harley's workflows and links `[[harley]]`.
- [ ] **Step 4: Add a `workflows/` folder for every bot,** even if it has one workflow.

### Task 6: Donna writes each bot's capabilities

**Files (created by Donna):**
- Create: `~/.agents/docs/bots/<bot-name>/workflows/capabilities.yaml`
- Create: `~/.agents/docs/bots/<bot-name>/workflows/workflow-N.md`

**Interfaces:**
- Consumes: the skills installed on each bot, read with `openbot.read_agent`.
- Produces: `capabilities.yaml` with `skills:` and `mcps:` lists. Each entry names the item and the workflow that uses it.

- [ ] **Step 1: Write `capabilities.yaml` for each bot** with a `skills:` list and an `mcps:` list. Use only skills that are installed on that bot.
- [ ] **Step 2: Write each `workflows/workflow-N.md`** and link it back to `[[<bot-name>]]`.

### Task 7: Verify the structure

**Files:** none.

- [ ] **Step 1: Read every agent** in the two departments and Donna with `openbot.read_agent`.
- [ ] **Step 2: Check the checklist.** For each new bot, confirm the seven items: profile, identity, skills, workflow, scheduled jobs, runtime, permissions. Expected: every item is set, or marked as needing Tai's decision.
- [ ] **Step 3: Check access.** Expected: all new agents show access `workspace` and Computer Use off, except Donna's Full access that Tai set.
- [ ] **Step 4: Check names.** Run `openbot.list_agents`. Expected: no duplicate names.
- [ ] **Step 5: Check the file layout.** Each bot folder has `<bot-name>.md`, `soul.md`, and `workflows/`. Each workflow file is linked from `<bot-name>.md`.
- [ ] **Step 6: Check capabilities.** Each skill in `capabilities.yaml` appears in `read_agent` for that bot. Each MCP is connected, or marked as not connected.
- [ ] **Step 7: Report to Tai** with the roster table and any item that is not set.

## Approval gate

Approved by Tai on 2026-10-26, with these changes: the three members are named banana (Skills and MCP), apple (Workflows), and pearl (Profiles and Runtime). Technician (Bob) is on hold until Tai confirms whether to keep it. Donna must not create Bob until then.
