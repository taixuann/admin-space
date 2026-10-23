# Batch 5: shared incident delivery tool

Request: 008. Executed 2026-10-23 in
`/Users/tai/.agents/tools/automation-incidents/`, an independent repository with
no remote.

## Repository

| Field | Value |
| --- | --- |
| Branch | `main` |
| Baseline commit | `6279388` — initial tool, 11 tracked files |
| Hardening commit | `5d8038b` — lifecycle fixes and evidence |
| Remote | None |
| Live Notion ticket | None |

## Contract

- `report --event-file` validates, persists, then attempts delivery.
- `flush` retries pending events within request and time bounds.
- `status` is read-only and reports configuration, pending state, last error, and
  each incident.
- Exit codes: `0` persisted or nothing to do, `2` invalid input/configuration,
  `3` state failure.
- Grouping is an explicit configuration field with no default:
  `job-stage-category` or `job`.
- State is durable and separate from rotating logs. Pending events never expire
  with log retention.
- Delivery is serialized by a file lock.

## Lifecycle rules verified

| Case | Observed |
| --- | --- |
| First failure | One ticket, marker `admin-incident-key: <key> episode 1` |
| Repeat unresolved | Appends an occurrence; human status preserved |
| Duplicate event ID | No second append |
| Terminal ticket | Never reopened; new episode, new marker, previous ticket referenced |
| Multiple marker matches | Delivery stops; `reconciliationRequired` records candidates |
| Create timeout after remote success | Next attempt reconciles by marker, one ticket only |
| Append timeout after remote success | `appendUncertain`; next attempt checks remote body, no duplicate append |
| Durable restart | A new process reads pending state and delivers |
| Rate limit | Batch stops after the first rate-limited result; event retained |
| Revoked auth | Event retained; non-retryable |
| Schema drift | Event retained; non-retryable |
| Recovery without auto-close | Appends recovery evidence, status unchanged |
| No recursive reporting | A delivery failure creates no new incident event |
| Concurrent reporters | One ticket, both events recorded, no lost update |

## Tests

`python3 -m unittest discover -s tests` — 31/31 pass. The suite uses only
temporary directories and the file-backed fake transport.

Notable additions after the first draft:

- `has_event` on both transports so uncertain appends can be reconciled.
- Episode-scoped markers so a closed ticket cannot capture a later episode.
- `recoversEventId` resolution for recovery events, with no silent guessing.
- Retry ordering that checks an uncertain append before deduplicating.
- Impact and previous-episode evidence in the ticket body.

## Notion transport status

Source only. It calls the installed `ntn` CLI, maps failures to stable
categories, and stays inert without configuration. No live response has been
observed. The adapter does not apply the database template and reads the first
100 blocks for reconciliation. Both limits are recorded in the README and block
activation until a supervised smoke test.

## Not done

- No live Notion ticket.
- No credential configured or extracted.
- No scheduled job references the tool.
- No push, merge, or publication.
