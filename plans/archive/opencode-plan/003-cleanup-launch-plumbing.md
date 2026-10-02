# Plan 003: Deduplicate the reader-process launch plumbing and drop dead state

> **Executor instructions**: Follow this plan step by step. Run every
> verification command and confirm the expected result before moving to the
> next step. If anything in the "STOP conditions" section occurs, stop and
> report — do not improvise. When done, update the status row for this plan
> in the index (`/Users/tai/.opencode/plan/README.md`).
>
> **Drift check (run first)**: The baseline is the WORKING TREE of
> `/Users/tai/.codex/worktrees/rawview-sidebar/tools` at commit `9874ef32`
> (branch `codex/rawview-sidebar`).
> live files; on a mismatch, STOP and report.

## Status

- **Priority**: P2
- **Effort**: S
- **Risk**: LOW
- **Depends on**: 001 (its Step 2 removes `GallerySourceState.readerSHA256`; doing 003 first would conflict — land 001 first, then verify the remaining grep)
- **Category**: tech-debt
- **Planned at**: commit `9874ef32`

## Why this matters

`ReaderClient.swift` contains two near-identical ~24-line blocks that build
the Python `Process` (candidate list, env scrubbing, user-site-packages
injection) — one in `runInspection` (lines ~241–263), one in `load` (lines
~312–336). Any future change (adding a Python path, changing env policy) must
be made twice; if only one gets it, inspection and load silently use
different runtimes. Separately, the 2026-10-02 inspector declutter left
`GallerySourceState.readerSHA256` written but never read — dead state that
misleads readers into thinking the field is consumed.

## Current state

`Sources/RawViewCore/ReaderClient.swift`:

- `runInspection(...)` — `private static func` at line 234. Inside its
  `Task.detached` closure, lines ~241–263:
  ```swift
  let process = Process()
  let output = Pipe(), diagnostics = Pipe(), input = Pipe()
  let pythonCandidates = [
      "/Library/Frameworks/Python.framework/Versions/3.13/bin/python3",
      "/opt/homebrew/bin/python3", "/usr/local/bin/python3", "/usr/bin/python3"
  ]
  if let python = pythonCandidates.first(where: { FileManager.default.isExecutableFile(atPath: $0) }) {
      process.executableURL = URL(fileURLWithPath: python)
      process.arguments = [reader.path, "inspect-many", "--paths-json"]
  } else {
      process.executableURL = URL(fileURLWithPath: "/usr/bin/env")
      process.arguments = ["python3", reader.path, "inspect-many", "--paths-json"]
  }
  process.currentDirectoryURL = project.root
  ... (pipes, env copy, env-key removal loop, pythonVersion + user-site PYTHONPATH injection)
  ```
- `load(...)` — `public static func` at line 296. Lines ~312–336 repeat the
  same `pythonCandidates` / env-scrub / `pythonVersion` + user-site block with
  `["load", <path>]` arguments and no stdin pipe.

Also duplicated downstream: both have the same `readOutput` 32 MiB limit,
timeout scheduling (300 s), and post-exit hash re-verification pattern —
those are similar but NOT identical (inspection closes stdin, load does not;
error fallback differs). Consolidate ONLY the Python/env selection, not the
process lifecycle.

`Sources/RawViewApp/RawViewApp.swift`:
```swift
struct GallerySourceState {
    var inspection: SourceInspection?
    var measurement: NormalizedMeasurement?
    var readerSHA256: String?      // written at every load event, read nowhere
    var error: String?
    var isLoading = false
}
```
After Plan 001 lands, `grep -n readerSHA256 Sources/RawViewApp/RawViewApp.swift`
should already show no matches; if it still shows matches, remove them here.

## Commands you will need

| Purpose | Command (cwd = `.../scientific/raw-viewer`) | Expected on success |
|---|---|---|
| Core gate | `sh Scripts/check_core.sh` | `RawView core self-check passed` (and app typecheck if Plan 002 landed) |
| Package build | `sh Scripts/package_app.sh` | `Packaged and verified /private/tmp/RawView-TAI73.app` |

## Scope

**In scope**:
- `Sources/RawViewCore/ReaderClient.swift` — extract ONE private helper; do not change behavior.
- `Sources/RawViewApp/RawViewApp.swift` — only if `readerSHA256` plumbing still exists after 001.

**Out of scope**:
- Any change to process timeouts, output limits, env key list, Python candidate ORDER (first executable wins: `/Library/Frameworks/Python.framework/Versions/3.13/bin/python3` first — this is load-bearing, tested against the live project).
- `Scripts/*`, `Tests/*` (unless a test file references a removed symbol — check, don't edit otherwise).
- Everything under `research-projects/`.

## Git workflow

Worktree `/Users/tai/.codex/worktrees/rawview-sidebar/tools`, branch
`codex/rawview-sidebar`, conventional commits (`refactor(raw-viewer): ...`).

## Steps

### Step 1: Extract the shared Python-launch configuration

In `ReaderClient.swift`, add a private helper near `RunningProcess`:

```swift
private struct ReaderPythonLaunch {
    let executableURL: URL?
    let baseArguments: [String]   // WITHOUT the reader path and mode args
}

// ponytail: linear scan of fixed candidates, first executable wins — replace with
// a settings file only if a second site with a different Python layout appears.
private static func readerPythonLaunch() -> ReaderPythonLaunch { ... }
```

And a `private static func configureEnvironment(_ environment: inout [String: String], pythonPath: String?)` for the env-copy, key-removal, and user-site injection (exact same key list `["PYTHONPATH", "PYTHONHOME", "PYTHONSTARTUP", "PYTHONINSPECT"]`, exact same user-site path construction from `pythonVersion(at:)`).

Then in both `runInspection` and `load`, replace the duplicated blocks with
calls to these helpers. The behavior difference between the two sites is only
the trailing arguments — keep each call site's own
`process.arguments = [reader, mode, ...]` line intact.

**Verify**: `sh Scripts/check_core.sh` → self-check passed (the trust
boundary section launches the real stub reader via `ReaderClient.load`, so a
broken launch path fails loudly here).

### Step 2: Remove dead `readerSHA256` app state (if present after 001)

`grep -n "readerSHA256" Sources/RawViewApp/RawViewApp.swift` — remove any
remaining declaration/assignment. Core's `ReaderLoadResult.readerSHA256` and
the CoreSelfCheck assertion `loaded.readerSHA256.count == 64` stay untouched.

**Verify**: `grep -rn "readerSHA256" Sources/RawViewApp/` → no matches; core
matches remain only in `Sources/RawViewCore/ReaderClient.swift` +
`Scripts/CoreSelfCheck.swift`.

### Step 3: Build and package

**Verify**: `sh Scripts/package_app.sh` → `Packaged and verified /private/tmp/RawView-TAI73.app`.

## Test plan

- The existing `Scripts/CoreSelfCheck.swift` trust-boundary section is the
  behavioral test for this refactor: it launches a real stub `reader.py`
  through `ReaderClient.load` (including the changed-file rejection and
  oversized-output cases). It must keep passing unchanged.
- `Tests/ReaderTrustTests.swift` contains a parallel Swift Testing version of
  the trust checks that cannot run in this environment — do not edit it; if
  `swift test` becomes usable (Plan 002), it must also pass.

## Done criteria

- [ ] `grep -c "pythonCandidates" Sources/RawViewCore/ReaderClient.swift` → exactly 1 occurrence (the helper)
- [ ] `sh Scripts/check_core.sh` → self-check passed (full trust-boundary run)
- [ ] `sh Scripts/package_app.sh` → packaged and verified
- [ ] `grep -rn "readerSHA256" Sources/RawViewApp/` → no matches
- [ ] No files outside the in-scope list modified (`git status`)
- [ ] Index status row updated

## STOP conditions

- Any behavioral difference appears in the self-check run (different python
  chosen, env differences) — restore and report.
- The extraction would need to touch the `RunningProcess` cancellation logic
  or the post-exit hash re-verification — out of scope, report.

## Maintenance notes

- Future: if a third reader invocation mode is added, it must use the shared
  helper — reviewer checklist item.
- Plan 002's app-layer typecheck makes this diff's safety much cheaper;
  land 002 before this plan if it exists.
