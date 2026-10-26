# Maintain a bot

Purpose: keep a bot's files and live profile in agreement after Tai asks for a change, or after a verify run shows drift. A change to a bot always checks four things together: `config.json`, skills, `SOUL.md`, and workflows (with their HTML). Harvey runs it on demand. No scheduled check exists.

Parent: [Harvey](../SOUL.md) · Shared rules: [bot folders](../../../AGENTS.md) · Diagram: [maintain-bot.html](maintain-bot.html)

## Uses

| Step | Skill, tool or script | Status | Reason |
| --- | --- | --- | --- |
| Observe, verify | `bot-ctl observe <bot>`, `bot-ctl verify <bot>` (`bot-management/scripts/bot-ctl`) | ok | Read-only. Compares `config.json` with the live profile. |
| Decide | `hermes-fleet-admin`, `superpowers:brainstorming` | ok | Harvey drafts the delta and asks Tai. |
| Apply | `bot-ctl apply <bot>` | ok | Applies only the approved delta. |
| Skill change | `superpowers:writing-skills` | ok | Test before editing a skill. |
| Report | Notion MCP, `ticket-submit` (skill), `notion-cli` (`ntn`, second path) | MCP needs Tai's login | Harvey files an error and its fix into the Notion Agent Tickets database. |
| Diagram | `archify` | ok | Regenerate the workflow HTML. |

Model category: `operation.standard` for observe, verify and apply. `reasoning.standard` for deciding what a change should be (known gap).

## Steps

1. **Trigger.** Tai asks for a change, or a verify run shows drift.
   Completion: the reason is stated in the chat.
2. **Observe.** Run `bot-ctl verify <bot>`. Use `bot-ctl observe <bot> -c <category>` for detail.
   Completion: a table of rows, each `match`, `drift`, `missing` or `untested`.
3. **Draft.** Harvey drafts the change to the four items in step 4. Mark each changed field `proposed`. Tai picks which side wins when the record and the live profile differ.
   Completion: the draft and the dry run are shown to Tai.
4. **Update together.** Before apply, Harvey updates and checks all four:
   - `config.json`: model, dirs, skills, plugins, mcps, memory.
   - Skills: enabled list matches what is installed.
   - `SOUL.md`: identity and `## Context` still true.
   - Workflows: `.md` updated, `Uses` table correct, HTML regenerated into `.archify/` and linked, then browser check passes.
   Completion: each of the four is `match` or listed as a gap.
5. **Approve.** Tai approves the exact delta in chat.
   Completion: explicit approval in chat. A question is not approval.
6. **Apply and verify.** Follow [create-bot, Review, apply and verify](create-bot.md#review-apply-and-verify), steps 1 and 4 to 7. Harvey runs the pre-send check first; a failure goes to Tai.
   Completion: `bot-ctl apply` exited 0, and `bot-ctl verify` shows no drift or missing row, or each remaining row is reported to Tai.
7. **Report.** Harvey sends Tai the table with pass, blocked or untested per check.
   Completion: report sent.

## Error recovery

- Observe or verify errors: report the command and the error. Do not change the profile to fix it.
- A mismatch Tai does not decide: leave both sides unchanged and report it.
- Apply exits non-zero: report the output and wait. No retry without Tai.
- Verify shows drift after apply: report the rows. Plugin and MCP drift is Tai's decision.
- A scheduled check needs Tai's approval before it is set up. None exists today.
