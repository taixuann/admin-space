---
name: receiving-ticket
description: Receive and assess an existing Agents Ticket before any work is routed. Use when the user asks Orchestra Companion to receive, inspect, qualify, or prepare a ticket for human review; verify the ticket, category, context and source coverage, then update the ticket with an attributed review packet and stop for the user's decision.
---

# Receiving Ticket

Use this action to prepare one selected Agents Ticket for the user's decision. A ticket is the continuing record for its intent, any later plans, execution evidence and reviews. Receiving authorizes intake and context-gathering updates to that ticket; it does not authorize downstream work.

## 1. Resolve the ticket

Use the ticket URL or page ID supplied by the user. If they identify it only by title, search the Agents Ticket database and confirm the matching page using its title and context. If several pages remain plausible, ask which one they mean.

Fetch the selected page and the current data-source schema. Read the whole available ticket body, properties, relevant linked context and last-edited time. Check for truncation. Do not treat a matching title as proof of identity.

## 2. Classify and check continuity

Use the database's current Category options and the user's stated intent. Apply these distinctions:

- Scientific questions, research milestones and research knowledge work: Research.
- Bounded scientific study work: Study.
- Workspace tools, skills, agents, bots, plugins and their coordination: Admin.
- Personal goals: Personal.
- Development work outside the tools/skills/agents/bots administration scope: Development.

Keep the category the user already chose when it still fits. If category and intent conflict, explain the conflict and ask before changing it. Do not create a second ticket for a follow-up to the same continuing intent; preserve its source and history.

## 3. Check context and sources

Identify what is already known, what the user supplied, and what remains unresolved. Preserve the user's wording as intent; label any assistant-written interpretation. Do not invent facts, decisions, deadlines, acceptance criteria, or source coverage.

For each new or materially changed intake, request a scoped context check from /wiki-companion before completing the review packet, when that skill is available. Give it the ticket's question, exact relevant scope and source locations already named or clearly linked. Do not ask it to scan unrelated Drive, GitHub, Linear, Notion or ~/learn content. This bounded Wiki check is part of intake, not approval to route or execute work. If the skill or a source is unavailable, record the specific gap and do not imply that the lookup happened.

## 4. Record the intake packet

Add an attributed, dated intake entry to the existing ticket using its current template. Put sourced findings and links in Context & Sources; put the intake event and any unresolved lookup in the Status log. Keep user wording, source findings, assistant interpretation and open questions distinct.

Use targeted content edits. Preserve the original intent, current schema, plan tabs and unrelated history. Do not create plan content in Spec & Plan during intake. Do not add a “Requested next step” section; record the decision the user needs to make in the review packet.

After saving the packet, set Status to Human review when that value exists in the live schema. This means the packet is ready for the user to assess; it does not mean the user has accepted a route. A documented source gap may remain visible for the user's decision.

Read the ticket back. Confirm identity, category, status, body changes and links. If an edit fails or readback is incomplete, report what succeeded and leave unresolved effects explicit.

## 5. Stop for the human decision

Present the review packet with the ticket link, category, context gathered, remaining gaps and decision needed. Do not route to another plugin, start a brainstorm or plan, execute work, or claim a bot accepted an assignment until the user chooses the action and target. If the user approves a route, pass only the exact ticket, revision, action, target, scope and authority they selected.

Keep proposed, sent, accepted and completed distinct. A tool or skill merely being present does not prove it ran or accepted the handoff.
