# Hindsight for Admin

Admin uses Hindsight bank `admin` as its shared experience memory.
An Admin session can run in different clients. Codex, Claude, and Antigravity are the primary intended clients.
Hermes and other clients can join when their integration explicitly selects this bank.
Only Codex and Claude wiring was verified during initial setup. Client eligibility is not proof of active integration.

## Open the native explorer

Open [Hindsight Control Plane](http://localhost:9999/banks/admin) and select bank `admin`.
The bookmark [Open Hindsight.webloc](Open%20Hindsight.webloc) opens the same address on macOS.
The UI can modify memory and configuration. Use its inspection views when reviewing state.

The existing API listens at `http://127.0.0.1:9077`.
The Control Plane uses that API. It does not create a second memory store.

## Start the UI when needed

Run the existing native CLI in a terminal:

```sh
node /Users/tai/.npm/_npx/0cc0011c1c5c749e/node_modules/@vectorize-io/hindsight-control-plane/bin/cli.js --hostname 127.0.0.1 --port 9999 --api-url http://127.0.0.1:9077
```

Keep the terminal running. Press Ctrl+C there to stop that UI process.
This path uses the installed npm cache, version 0.10.1. If the cache is removed, resolve the native package again.
No login service or automatic startup is installed by this entry.

## Memory ownership

Hindsight is the selected Admin memory service. Native app stores remain app internals and are outside the Admin memory diagram.
The existing `memories/` links and folder remain intact. They are not extra Admin backends or a Hindsight sync pipeline.
Instructions stay in the root documents. Current system state stays in its actual configuration.
The current extraction profile and errors are recorded in DIAGNOSIS.md. Local storage alone does not establish working extraction.

## Last observed state

On 2026-10-22, the native UI opened bank `admin` and reported 0 memories and 0 documents.
Knowledge page entries exist, but successful automatic ingestion is not established by this observation.

## Ingestion failure

See [DIAGNOSIS.md](DIAGNOSIS.md). The current backend reports Claude Code authentication and model-recognition errors.
An available UI does not establish working extraction.
