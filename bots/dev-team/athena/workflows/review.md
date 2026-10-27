# Review (Athena)

Purpose: give one independent verdict on a plan, or on a finished change, that Forge sends on a card.

Parents: [Athena](../SOUL.md) · [Athena responsibilities](../AGENTS.md) · [Dev team](../../AGENTS.md)

Diagram: [review.html](review.html)

## Plan review

1. Take the request. Forge calls `request-review` on the card with `athena` as reviewer. Done when the card shows you as the active reviewer and you have read the plan it names.
2. Review the plan with the reviewer template from `superpowers:requesting-code-review` (`code-reviewer.md`): requirements first, then the plan's structure and risks. Done when the template is filled and each finding names a plan step.
3. Audit. Run `audit-writing-plans`. Done when its result is saved in the review notes under `~/.agents/docs/superpowers/plans/`.
4. Second opinion. Run an opencode review pass on the same plan, read-only. Done when its result is saved next to the audit result. The read-only flag is to be confirmed before first use.
5. Verdict. Say where the two results disagree and which evidence decides. Then `kanban_complete` (pass), or `kanban_request_changes` with the required changes. Done when the card has one verdict from this request.

## Completion review

1. Take the request. Forge sends the card with its summary from `superpowers:requesting-code-review`: base and head SHA, the plan, and a description. Done when you have read the summary and the plan.
2. Scope. Every file the plan names is changed, and no file outside the plan is changed. Done when each difference is listed.
3. Repo checks. Run the repo's own release-gate commands: secret scan, filename scan, branch in sync with origin. Done when each result is recorded.
4. CI. If the repo has `.github/workflows`, the checks must be green in the request summary. If it has none, record "no CI". Done when recorded.
5. Docs. Each README, AGENTS, CLAUDE and docs/ file that describes changed behaviour is updated. Done when checked.
6. Reviewer template. Fill `code-reviewer.md` with the base and head SHA. Done when each finding has a file and a line.
7. Decision engine. Run the decision-engine MCP on the whole change. Done when its result is saved.
8. Verdict. As in the plan review. Done when the card has one verdict from this request.

## Uses

| Skill, tool or plugin | Used for | Model category |
| --- | --- | --- |
| `superpowers:requesting-code-review`, reviewer template `code-reviewer.md`. Needs the superpowers plugin on Athena: install is blocked, see Notes. | Plan step 2, completion steps 1 and 6 | `reasoning` |
| `audit-writing-plans`. Enabled. | Plan step 3 | `reasoning` |
| opencode review pass, read-only. The flag is to be confirmed before first use. | Plan step 4 | `coding` |
| decision-engine MCP, five tools: submit_audit, wait_audit, check_audit_status, get_audit_result, list_auditors. Sends the change to endpoint `endpoint.deeppattern.ai`. Enabled. | Completion step 7 | `reasoning` |
| Kanban `kanban_request_review`, `kanban_complete`, `kanban_request_changes` | Requests and verdicts | `operation` |

## Notes

- Plan review uses audit-writing-plans. Completion review uses decision-engine. Neither runs for the other request.
- Until superpowers is installed on Athena, she cannot load the reviewer template. She reports that to Tai and does not review without it.
- The model is `coding.high` (Haiku 5.5, xhigh). Review is reasoning work, so this is a known gap against `reasoning.standard`. Tai chose it on 2026-10-27.
- Forge counts the review rounds and posts the verdict to GitHub. This workflow does neither.
- How Athena gets CI state (from Forge's summary, or her own read-only login) is open. Tai has not decided.
