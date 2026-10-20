---
name: research-capture
description: Capture an explicitly requested scientific research intent as one Agents Ticket in Notion. Use only for Research-category intent, milestones, or scientific research goals and milestones; preserve the user's wording and uncertainty, apply the New Intent template, check for duplicates, keep the ticket at Capture, and verify the saved record.
---

# Research Capture

Use this skill only when the user explicitly asks to record a scientific research intent. Discussion, questions, and proposals alone do not authorize a Notion write.

This skill is for Research tickets only. Workspace tools, skills, agents, bots, plugins and their coordination belong to Admin; do not capture those through Research Capture. If the request is outside scientific research, explain that it is outside this skill's scope and leave Notion unchanged.

## Capture one research intent

1. Read the user's current request and relevant conversation context. Keep one continuing objective in one ticket. Preserve the user's wording as the intent; label any summary or interpretation as assistant-written.
2. Collect only context and source links already supplied or needed to identify the research work. Do not search broadly or invent a project, measurement, decision, milestone, or deadline.
3. Fetch the Agents Ticket data source and current schema. Search likely title and key terms for a duplicate. Reuse the matching ticket when the user is continuing that same intent; do not create a second ticket.
4. For a new ticket, use the database's current default New Intent template and set Category to Research, Status to Capture, and Created by to Loki when that option exists. Do not add a separate Requested next step section. Do not change properties on an existing ticket unless the user asks.
5. Wait for the template content to finish applying, then fill only the relevant Init fields: original intent, desired outcome, why it matters, constraints, open questions, context, and supplied sources. Keep the Spec & Plan tabs empty; capture does not write a plan. Add a dated status-log entry identifying that the intent was captured and any material unresolved question.
6. Read the page back. Confirm title, category, creator and status, and verify the intent, context and sources. Return the Notion link and say exactly what was captured. If creation or readback fails, report that plainly and do not claim success.

## Boundaries

- Capture records research intent. It does not approve a plan, assign a bot, route work, create a scientific Study, run analysis, or establish scientific acceptance.
- Do not classify workspace tools, skills, agents, bots, plugins or their coordination as Research; use Admin.
- Do not change an existing ticket's status just because its context was updated.
- Keep raw scientific evidence immutable and outside ticket bodies; link to its project-owned location instead.
- Do not send private or unrelated source material into the ticket.
