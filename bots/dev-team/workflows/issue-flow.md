# Issue flow (GitHub issue to release, driven by kanban and Notion)

Status: approved in chat by Tai on 2026-10-27. The cron job spec and its activation are not approved yet, so nothing is scheduled.

Parents: [Forge](../forge/SOUL.md) · [Dev team](../AGENTS.md)

## Model

- One issue, one kanban card. The card is the work ticket. Its key is the issue URL, so a repeat run creates no second card. Forge spawns as many cards as there are issues.
- The review team is Athena plus opencode. Athena reviews as herself. An opencode pass is her second review. Her verdict records both.
- Athena reviews at two gates only: the plan (step 6) and the finished work before the PR (step 8). Between them Forge runs opencode freely and nothing else reviews.
- Review handoffs use `request-review` on the same card, with `athena` as reviewer. There is no second card.
- The GitHub issue holds the full verdict as a comment. The Notion ticket holds only a link to that comment and to the card. Tai reads on Notion and decides there.
- The cron job is a script, not a model. It creates cards, reads Notion, and moves cards, issues and PRs. Forge's worker makes the judgement calls.
- Forge's own chat is control only: status, approve, stop. The work runs in cards.

## Notion status (Agent Tickets, live schema checked 2026-10-26)

`Captured` → `Human review` (gate 1, then the PR) → `Approved` (cron unblocks the card) → `Done` (cron merges, releases, closes) · `Canceled` (cron closes the issue and its PR).

## Steps

1. Poll (cron script, every run). Read three sources and match them before any move: (a) kanban, `hermes kanban list`, the cards and their status, each keyed by its issue URL; (b) GitHub, `gh issue list --state open --label <agreed label>` for each repo under `tools/*/*`, with each issue's URL; (c) Notion Agent Tickets, each ticket's status and its `Issue URL` property. A card moves only when its issue URL matches the ticket and the statuses on both sides allow the move. An open issue with no card: create a card assigned to `forge`, ready, with the issue URL as idempotency key. A card blocked and its ticket Approved: unblock to ready. Ticket Done: step 11. Ticket Canceled: step 12. No match, or no issue URL: skip and log it, do not move anything. Needs the Notion `Issue URL` property (see Pending).
2. Check issue (Forge). Four parts, in this order:
   a. Read the issue with `gh`: body, comments, labels, linked PRs. A linked open PR means the issue is already in progress: skip.
   b. Read every other open issue in the same repo. If this issue duplicates a fixed one (closed, or a merged PR fixes it), comment "duplicate of #X, fixed by PR #Y", close this issue, and link. If two open issues describe the same problem, keep one, close the other, and link them. Which one to keep is proposed below, in Pending. Record each close on the card.
   c. Brainstorm and audit the issue against the current code. Verdict: solved, not solved, or unclear. Each verdict has evidence.
   d. Comment the verdict on the GitHub issue. File a `ticket-submit` ticket with status Human review. The ticket body holds only a link to that GitHub comment and the card id. Then block the card as `needs_input`.
3. Gate 1 (Tai, in Notion). Tai opens the link, reads the verdict on GitHub, and sets the ticket to Approved. The cron sees Approved and unblocks the card to ready.
4. Solved. After Gate 1, Forge comments the evidence on the issue and closes it. The card is done.
5. Not solved: plan. Forge writes the plan with `superpowers:writing-plans` into the tool repo's `docs/superpowers/plans/`, then calls `request-review` on the card with `athena` as reviewer.
6. Plan review (Athena + opencode). Athena audits the plan with `audit-writing-plans`, and opencode runs a second critique pass. Athena approves or requests changes. Changes return the card to Forge, which revises and requests review again. Limit: two review rounds, then blocked and a ticket for Tai.
7. Build (Forge, opencode). After approval, Forge runs `opencode run --auto` in a worktree, following the approved plan with `superpowers:executing-plans`, and `superpowers:subagent-driven-development` where tasks are independent. The opencode flow runs without review in between. Forge tracks the run on each dispatch until it finishes.
8. Work gate before the PR (Athena + opencode). When the build is finished, Forge runs `superpowers:requesting-code-review` to collect the base and head SHA, the plan and a description, then calls `request-review` on the card with `athena` as reviewer. Athena runs the completion review in [review](../athena/workflows/review.md): the reviewer template from that skill (`code-reviewer.md`), the checklist, then decision-engine on the whole change. Approve: step 9 opens the PR. Request changes: back to step 7. Limit: two attempts, then the card blocks and Forge sends Tai a Notion ticket to review.
9. Docs and PR (Forge). Forge updates `docs/`, `README`, `AGENTS.md` and `CLAUDE.md` where they change, with `technical-documentation`, in the same branch. It opens the PR with `Closes #N`, so the merge closes the issue. It comments the solution and the PR link on the issue, then sets the Notion ticket to Human review with a link to the PR. Gate 2 starts here.
10. Gate 2 (Tai, in Notion). Tai reviews the PR and sets the ticket to Done.
11. Merge and release (Forge, on Done). The cron sees Done. Forge first runs the repo's own release gate, if the repo has one (for development-space: `RELEASE_GATE.md`, with its secret scan, filename scan and branch-in-sync checks). A failed gate blocks the card. Then Forge checks that the PR's checks pass and that it still merges cleanly, merges it, runs `github-repo-care` to create the tag and the GitHub release, and comments the release link on the issue. If checks fail or the merge conflicts, Forge comments that on the issue and blocks the card.
12. Canceled. The cron comments on the issue that it was canceled, closes the issue, and closes its PR if one exists. The card is archived.

## Limits and failures

- Two review rounds at the plan gate and two attempts at the work gate. Round counts come from the `request-changes` events on the card. The bots' comments on the card record each round for humans. After the limit, the card blocks as `needs_input` and Forge sends Tai a ticket. It does not retry.
- A dirty worktree or a failed `git pull --ff-only` is a blocker: comment on the card, then stop.
- Dispatch needs the gateway running. If it is down, cards wait in ready.

## Gates and invariants

- Gate 1: Approved in Notion starts planning. Gate 2: Done in Notion starts merge and release. Forge does not merge before Done.
- Duplicates: close one, keep one, link them. Closing on GitHub can be undone by reopening.
- The issue closes on merge (`Closes #N`), or at Canceled. Opening a PR does not close the issue.
- Idempotency: the card key is the issue URL. Each `ticket-submit` call appends a recurrence log to the open ticket, not a new ticket.
- Changes to `AGENTS.md`, `CLAUDE.md` or `SOUL.md` can hit an approval prompt in an unattended run. The run then stops and reports it.
- `opencode run --auto` grants every permission inside its worktree. Forge pushes only the branch it created.

## Uses

| Skill, tool or plugin | Used for | Model category |
| --- | --- | --- |
| `gh` (`github` skill) | Read issues, duplicates, PRs, comments, close, merge | `operation` |
| `superpowers:brainstorming` | Verdict (step 2c) | `reasoning` |
| `audit-brainstorming` (`~/.hermes/skills`, external hub). Not enabled for Forge yet. | Stress-test of the verdict | `reasoning` |
| `superpowers:writing-plans` | Plan (step 5) | `reasoning` |
| `audit-writing-plans` (external hub). Not enabled for Athena yet. | Plan audit (step 6) | `reasoning` |
| `/opencode` (`opencode run --auto`) | Build (step 7), second review pass (steps 6, 8) | `coding` |
| `superpowers:executing-plans`, `superpowers:subagent-driven-development` | Build (step 7) | `coding` |
| Kanban (`kanban_*` tools) and the `kanban-handoffs` skill | Cards, review requests, blocks, unblocks | `operation` |
| `ticket-submit` with `ntn` | Notion ticket and status reads (steps 1, 2d, 3, 9, 10, 11) | `operation` |
| `technical-documentation` | Docs (step 9) | `general` |
| `github-repo-care` | Tag and release (step 11) | `operation` |
| Hermes cron | The cron script every run. Not approved. | `operation` |
| decision-engine MCP (sends the whole change out to an external service) | Completion review, step 8 | `reasoning` |
| `superpowers:requesting-code-review` (Forge: SHAs and summary. Athena: reviewer template `code-reviewer.md`) | Step 8 | `coding` |
| `superpowers:verification-before-completion` | Forge, before it reports a card done | `operation` |
| `superpowers` plugin | Skills above. On Athena: install blocked, see Pending | none |

## Pending

Open items, recorded here until each is decided. Tai approves each one that changes config, a schema or a live profile.

- Cron job spec: interval, the script, and its location (`harvey/cron/<job>/`). Tai approves the exact spec before activation.
- Cron behaviour when `gh` or Notion cannot be read. Tai deferred this; it must be written before activation.
- The existing Hermes job `dev-space-issue-pr` in Forge's profile overlaps this. It must be replaced, not run alongside.
- Which duplicate to keep. Proposed: the one with a linked PR, then the fuller description, then more comments. Tai to confirm.
- Notion Agent Tickets property `Issue URL` (URL) is required: step 1 matches tickets to cards and issues by it. `Card` (text) is optional. Schema change: Tai approves.
- Ticket title for dedup. `ticket-submit` dedups by title, so the title must contain the repo and the issue number, or unrelated issues merge.
- Enabling `audit-brainstorming` for Forge and `audit-writing-plans` for Athena changes profile config. Tai approves the exact delta.
- Athena's `superpowers` plugin: the Hermes scanner blocked the install from `obra/superpowers` (170 findings after removing the duplicated report; several HIGH, mostly `rm -rf` examples in install docs and one `printenv` example in a systematic-debugging skill). Tai decides: review and force the install, copy the already-installed commit `8ca22db` from forge, or drop superpowers from Athena. Until then Athena cannot load the reviewer template.
- Athena's profile is created and verified; the draft in `athena/` is still `enable: false`. Athena needs no GitHub login: she reviews the local worktree, and Forge posts to GitHub. How she gets CI state is open.
- Forge's runtime SOUL links to `~/.agents/bots/dev-team/forge/SOUL.md`. Applied 2026-10-27 with `bot-ctl apply forge --only soul,memory`.
- The label that marks an issue for Forge.
- The diagram does not draw the return arrows of the review loops. Archify's layout did not allow them. The cards carry the loops.
