# Plan 002: Restore a working verification baseline for the Swift package

> **Executor instructions**: Follow this plan step by step. Run every
> verification command and confirm the expected result before moving to the
> next step. If anything in the "STOP conditions" section occurs, stop and
> report — do not improvise. When done, update the status row for this plan
> in the index (`/Users/tai/.opencode/plan/README.md`).
>
> **Drift check (run first)**: The baseline is the WORKING TREE of
> `/Users/tai/.codex/worktrees/rawview-sidebar/tools` at commit `9874ef32`
> (branch `codex/rawview-sidebar`).
> and compare the "Current state" excerpts against the live files. On a
> mismatch, STOP and report.

## Status

- **Priority**: P1
- **Effort**: S
- **Risk**: LOW
- **Depends on**: none (land after 001 if you want the scheduler's removal already done — `check_core.sh` edits touch `CoreSelfCheck.swift` which 001 also edits; do NOT run both concurrently)
- **Category**: tests / dx
- **Planned at**: commit `9874ef32`

## Why this matters

The repo's only core verification gate is `Scripts/check_core.sh`, which
compiles **RawViewCore only**. The app layer (`RawViewApp`, ~870 lines of
SwiftUI) is type-checked solely by the release packaging build — so a UI
logic or type error surfaces only at the very last gate. Meanwhile
`swift test` — which should run the 6 test files under
`Tests/RawViewCoreTests/` — is broken in this environment:

```
$ swift test
.../MeasurementContractTests.swift:2: error: no such module 'Testing'
```

(Toolchain: Apple Swift 6.3.1, `swift-driver 1.148.6`; `xcrun swift test`
fails identically.) Without a fix, any refactor that lands in `RawViewApp`
(Plan 001, Plan 003, Plan 004) is verified only by "did the release build
compile" — no behavioral gate.

## Current state

- `scientific/raw-viewer/Package.swift` — swift-tools-version 6.0,
  targets: `RawViewCore`, executable `RawViewApp` (deps: RawViewCore),
  test target `RawViewCoreTests`. `swiftLanguageModes: [.v5]`.
- `Tests/RawViewCoreTests/*.swift` — 6 files, all begin with
  `import Testing` / `@testable import RawViewCore`.
- `Scripts/check_core.sh` — compiles only
  `Sources/RawViewCore/*.swift` + `Scripts/CoreSelfCheck.swift` with
  `swiftc`, then runs the binary. This works today and must keep working.
- `Scripts/package_app.sh` — release `swift build` + bundle; works today.

Swift Testing is bundled with Swift 6 toolchains; `no such module 'Testing'`
with Apple Swift 6.3.1 indicates the toolchain's Swift Testing libraries are
not being linked by `swift test` in this CLT-only environment (Command Line
Tools only, no full Xcode). Verify the environment yourself:

```
xcode-select -p          # expected: /Library/Developer/CommandLineTools
xcrun --show-sdk-path
swift test 2>&1 | head   # expected: the no-such-module error
```

## Commands you will need

| Purpose | Command (cwd = `.../scientific/raw-viewer`) | Expected on success |
|---|---|---|
| Baseline gate | `sh Scripts/check_core.sh` | `RawView core self-check passed` |
| Full typecheck (new) | `sh Scripts/check_core.sh` (after Step 1 extends it) | self-check passed AND app-layer typecheck silent |
| Swift test attempt | `swift test 2>&1 | tail -3` | see Step 2 outcomes |

## Scope

**In scope**:
- `Scripts/check_core.sh` (extend)
- `Scripts/CoreSelfCheck.swift` (only if Step 1's typecheck needs a tweak — it must not)
- A new `Scripts/README.md` section is NOT created; document the new gate in the top comment of `check_core.sh` itself.

**Out of scope**:
- All `Sources/` and `Tests/` files — the audit found no compile-breaking code; if `swiftc -typecheck` reports errors in app sources, STOP and report them (do not fix here).
- `Package.swift` unless Step 2's chosen remedy requires a manifest change (see below).
- Re-blessing expected outputs — never.

## Git workflow

Same as the rest of this package's work: worktree
`/Users/tai/.codex/worktrees/rawview-sidebar/tools`, branch
`codex/rawview-sidebar`, conventional commits (`test(raw-viewer): ...`).

## Steps

### Step 1: Extend `check_core.sh` to type-check the whole package

Add, after the existing core compile+run block, a UI-layer typecheck that
catches type errors in `RawViewApp` without linking (no `@main` conflict):

```sh
echo "Type-checking app layer..."
swiftc -module-cache-path "$cache" -typecheck \
  "$repo_root/scientific/raw-viewer/Sources/RawViewCore/"*.swift \
  "$repo_root/scientific/raw-viewer/Sources/RawViewApp/"*.swift
echo "App layer type-check passed"
```

Notes: RawViewApp sources reference bundled resources via `Bundle.main` —
that type-checks fine. The `Resources/NativePlotStyle.json` decoding is
runtime-only, unaffected. Keep the module cache path shared with the core
block for speed.

**Verify**: `sh Scripts/check_core.sh` → prints BOTH
`RawView core self-check passed` AND `App layer type-check passed`, exit 0.

### Step 2: Make `swift test` work (best effort, two attempts)

1. Attempt A — full Xcode toolchain if present:
   `ls /Applications/Xcode*.app/Contents/Developer 2>/dev/null`
   If an Xcode.app exists: `sudo xcode-select -s /Applications/Xcode.app` is
   a MUTATING system command — do NOT run it. Instead run the test with an
   explicit developer dir (read-only for the repo):
   `DEVELOPER_DIR=/Applications/Xcode.app/Contents/Developer swift test 2>&1 | tail -5`
   Expected: test run completes; record pass/fail counts.
2. Attempt B — if no Xcode or still failing: `swift test` stays broken.
   Record it in the top comment of `check_core.sh`:
   `# swift test is unusable in CLT-only environments (Swift Testing missing); this script is the verification gate.`
   Do not vendored-copy Swift Testing or add dependencies. Leave
   `Package.swift` untouched.

**Verify**: either `DEVELOPER_DIR=... swift test` runs the suite (expected:
all 6 test files pass — they are all pure-logic tests) OR
`Scripts/check_core.sh` documents the limitation; report which outcome.

## Test plan

- No new tests. The plan's deliverable IS verification infrastructure.
- Sanity: after Step 1, introduce a temporary syntax error in a scratch copy
  of an app file OUTSIDE the repo (copy `ProjectGalleryViews.swift` to
  /private/tmp, add a stray `}`, run `swiftc -typecheck` on the copy plus the
  other sources manually) to confirm the typecheck rejects broken code, then
  discard the copy. The repo file itself must never be modified.

## Done criteria

- [ ] `sh Scripts/check_core.sh` runs the core self-check AND the app-layer typecheck; both pass; exit 0
- [ ] The script fails (exit ≠ 0) when a deliberately broken app file is type-checked (verified with the /private/tmp scratch copy, not by editing repo files)
- [ ] `swift test` outcome recorded: working (with command) or unusable (documented in script header)
- [ ] No files outside the in-scope list modified (`git status`)
- [ ] Index status row updated

## STOP conditions

- `swiftc -typecheck` reports errors in CURRENT app sources — report the
  errors verbatim, do not fix them in this plan (they belong to Plan 001/003).
- Step 1's extended script breaks the existing core self-check.

## Maintenance notes

- Future plans should gate on `sh Scripts/check_core.sh` (now the full
  typecheck) + `sh Scripts/package_app.sh`.
- If the team later gets a full Xcode toolchain, re-enable `swift test` and
  the `Tests/RawViewCoreTests/` files become the primary gate; keep
  `CoreSelfCheck.swift` as the integration harness either way.
