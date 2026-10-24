# Memory and Knowledge

Source: [02 · Memory & Knowledge](https://www.notion.so/4010a859ed1f8191a3a9c7d63fdb6feb)

Last reviewed: 2026-10-25. Status: Draft (not execution approval).

## Purpose

Keep continuity separate from authoritative sources. Ephemeral work context,
native session stores, Hindsight recall, and durable knowledge each have a
different owner. Do not promote a conversation or process log to durable
memory without a check.

## What belongs where

- Session history: conversation and tool call traces belong to the
  session or runtime owner.
- Process history: meaningful transitions and approvals remain in the
  Agents Ticket process log.
- Knowledge corpus: code, papers, datasets, and canonical documents remain
  at their owner source. Link them when needed.
- Curated continuity: durable observations, verified decisions, and useful
  lessons worth carrying into later sessions.

## Memory stores observed locally

- Hindsight bank `admin` is the shared Admin recall layer.
- Native app memory remains separate under `memories/`.
- The shared folder is not an automatic export or synchronization target
  for Hindsight.
- Hindsight is a recall layer. Current configuration and accepted
  instructions remain with their owning sources.

## Retrieval and attribution

- Check retrieved claims against the current owning source before acting.
- Record source, scope, date, owner, and correction or retention policy
  for each curated entry.
- Do not automatically turn conversations or process logs into durable
  memory.

## Correction and ownership

- Corrections happen at the owning source first.
- Recall can be stale. Live source wins when they disagree.
- Credentials and runtime stores stay outside tracked source files.

## Observed versus proposed

Observed:
- Hindsight bank `admin` is configured and the native explorer exists.
- Backend logs report authentication and model-recognition failures. See
  [diagnosis](../tools/hindsight/DIAGNOSIS.md).

Proposed or pending:
- Which memory backend and retrieval index exists in reality.
- Which memories may be promoted between Spaces.
- Synchronization and source authority for a local MEMORY.md.

## Related sources

- [Hindsight explorer](../tools/hindsight/README.md)
- [ARCHITECTURE.md memory section](../ARCHITECTURE.md)
- [AGENTS.md memory and sources](../AGENTS.md)
