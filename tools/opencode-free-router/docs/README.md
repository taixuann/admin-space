# Shared OpenCode model tool

[Open the interactive daily-selection map](routing.html).

## Active workflow

The existing daily automation calls the tool. The tool reuses today's successful catalog or refreshes stale data.
It ranks provider candidates from the public Arena agent, webdev, and text leaderboards, probes in configured group order through native OpenCode, saves `../model-list.json`, and changes only OpenCode's default model.
The backend is a CLI tool. There is no HTTP gateway.

Provider group order and model membership are in [selection.json](../selection.json). Per-group ordered scores, source matches, route health, and the selected model are recorded in the generated model list.

## Current validation

On 2026-10-22, benchmark ordering selected `opencode/deepseek-v4.1-flash-free` at score `0.8081`; the source boards were fetched on 2026-10-20, within the seven-day freshness window. Its native probe and a normal unpinned OpenCode call both returned the expected OK response. Other candidates remain unchecked today.

## Historical route probes

- [Direct API probes](verification.json)
- [Complete native Zen checks](zen-cli-verification.json)
- [Targeted rechecks](rechecks.json)

These older probes establish individual responses at their recorded times. They are not the daily cache.
Eight of nine Zen candidates returned OK in the complete native check. `jev-1.13-free` failed.
Go free and Muse subscription availability differ. Google previously returned OK, followed by HTTP 503 responses.

Read the [tool runbook](../README.md) for freshness, backups, quota, and compatibility limits.
