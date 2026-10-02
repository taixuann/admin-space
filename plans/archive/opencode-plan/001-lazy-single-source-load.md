# Plan 001: Lazy single-source loading — restore the antigravity load model

> **Executor instructions**: Follow this plan step by step. Run every
> verification command and confirm the expected result before moving to the
> next step. If anything in the "STOP conditions" section occurs, stop and
> report — do not improvise. When done, update the status row for this plan
> in the index (`/Users/tai/.opencode/plan/README.md`).
>
> **Drift check (run first)**: The baseline is the WORKING TREE of
> `/Users/tai/.codex/worktrees/rawview-sidebar/tools` at commit `9874ef32`
> (branch `codex/rawview-sidebar`).
> Run `git status --short -- scientific/raw-viewer` and compare the "Current
> state" excerpts against the live files. On a mismatch, STOP and report.

## Status

- **Priority**: P1
- **Effort**: M
- **Risk**: MED (touches the app's central load flow)
- **Depends on**: none
- **Category**: architecture / perf (folds audit findings #1, #2, #6)
- **Planned at**: commit `9874ef32`

## Why this matters

On project open, RawView inspects ALL discovered sources and then **loads every
one of them through the Python reader** with 2 concurrent workers
(`startProjectLoad`). The user's real project has 6,727 raw files, many of
them 5 MB Autolab CV files that emit ~41,000-point JSON payloads. Loading all
of them takes hours, keeps ~1.3 MB of parsed doubles per loaded file in RAM
forever (gigabytes total), and the center panel shows "Loading Source"
instead of a plot while the queue churns. The result is the observed
"constantly loading, never opens a plot" behavior.

The older, approved design (antigravity run, commit `a6be05b2` on
`origin/codex/tai-73-native-rawview-recovery`) is: **inspect everything cheaply
for sidebar metadata, but load only the source the user selects, on demand**.
This plan restores that. The UI work for a single focused figure is already
done (2026-10-02 working tree): the center panel shows one figure for
`focusedSourceID`.

## Current state

Files in the Swift package at `/Users/tai/.codex/worktrees/rawview-sidebar/tools/scientific/raw-viewer/`:

- `Sources/RawViewApp/RawViewApp.swift` — app + `RawViewModel` (state and load
  orchestration) + shell views + plot/table/inspector views.
- `Sources/RawViewApp/ProjectGalleryViews.swift` — `ProjectSourcesSidebar`
  (group-by picker + List) and `ProjectGallery` (focused single-figure pane).
- `Sources/RawViewCore/ReaderClient.swift` — `ProjectContext`, `ReaderApproval`,
  `ReaderClient.inspectMany` (batched, ≤256/batch), `ReaderClient.load(source:
  project:approval:)` (per single source URL). Per-source load already exists.
- `Sources/RawViewCore/ProjectLoadScheduler.swift` — generic 2-concurrency
  load-all scheduler. **Only used by the eager flow.**
- `Scripts/CoreSelfCheck.swift` — self-check harness; its
  `projectLoadSelfCheck()` exercises `ProjectLoadScheduler` only.
- `Scripts/check_core.sh` — compiles RawViewCore + CoreSelfCheck and runs it.
- `Scripts/package_app.sh` — release build + app bundle packaging.

Current eager flow in `RawViewModel` (excerpts as of the working tree):

```swift
func resumeOrRequestApproval() {
    guard let project, !sources.isEmpty else { return }
    guard let approval = savedApproval(for: project), approval.isCurrent(for: project) else {
        removeSavedApproval(for: project)
        hasReaderApproval = false
        requestReaderApproval()
        return
    }
    hasReaderApproval = true
    startProjectLoad(project, approval: approval)          // <-- loads ALL sources
}

private func startProjectLoad(_ context: ProjectContext, approval: ReaderApproval, sources requestedSources: [RawSource]? = nil) {
    ...
    let inventory = requestedSources ?? sources            // all 6,727
    ...
    loadingPhase = "Loading"
    await ProjectLoadScheduler.load(projectID: requestID, sources: ready, maximumConcurrentLoads: 2,
        load: { source in try await ReaderClient.load(source.url, project: context, approval: approval) },
        ...)
}
```

State surface that exists only for the eager flow:
`@Published var loadProgress/completedLoads/totalLoads/loadingPhase`,
`cancelLoad()`, `retryFailedSources()`, and `GallerySourceState.readerSHA256`
(set but never read since the inspector declutter).

The per-source primitive you will build on:

```swift
// ReaderClient.swift:296
public static func load(_ source: URL, project: ProjectContext, approval: ReaderApproval) async throws -> ReaderLoadResult
```

Sidebar grouping needs ONLY `SourceInspection` data (produced by
`inspectMany`); the measurement payloads are only needed by the focused pane.

## Commands you will need

| Purpose | Command (cwd = `/Users/tai/.codex/worktrees/rawview-sidebar/tools/scientific/raw-viewer`) | Expected on success |
|---|---|---|
| Core self-check | `sh Scripts/check_core.sh` | prints `RawView core self-check passed` |
| Build + package | `sh Scripts/package_app.sh` | prints `Packaged and verified /private/tmp/RawView-TAI73.app` |
| Launch | `pkill -f RawView; sleep 1; open /private/tmp/RawView-TAI73.app` | app opens |

Note: `swift test` cannot run in this environment (Swift Testing module
missing from the toolchain). Do not attempt to run it; `check_core.sh` is the
core gate. This is tracked in Plan 002.

## Scope

**In scope** (the only files you should modify):
- `Sources/RawViewApp/RawViewApp.swift`
- `Sources/RawViewApp/ProjectGalleryViews.swift` (dot semantics + small bits)
- `Sources/RawViewCore/ProjectLoadScheduler.swift` (DELETE)
- `Tests/RawViewCoreTests/ProjectLoadSchedulerTests.swift` (DELETE)
- `Scripts/CoreSelfCheck.swift` (remove the `projectLoadSelfCheck()` section)
- `Tests/RawViewCoreTests/MeasurementContractTests.swift` and other test files only if they reference the scheduler (check with grep; do not otherwise edit)

**Out of scope** (do NOT touch):
- `Sources/RawViewCore/ReaderClient.swift` — the trust/inspection/load layer is
  correct and battle-tested; per-source `load` already exists.
- `Sources/RawViewCore/SourceGrouping.swift`, `SourceInspection.swift`,
  `NormalizedMeasurement.swift`.
- `Scripts/package_app.sh`, `Scripts/check_core.sh` (the plan's verification
  must keep passing unmodified).
- Anything under `research-projects/` (project reader is fixed and working).

## Git workflow

- Work directly in the worktree `/Users/tai/.codex/worktrees/rawview-sidebar/tools`
  on branch `codex/rawview-sidebar`. Do NOT create new branches, push, or
  commit unless the operator says so; the operator commits per part.
- Commit style observed in `git log`: `feat(raw-viewer): ...` / `fix(raw-viewer): ...` conventional commits.

## Steps

### Step 1: Delete the load-all machinery

1. Delete `Sources/RawViewCore/ProjectLoadScheduler.swift` and
   `Tests/RawViewCoreTests/ProjectLoadSchedulerTests.swift`.
2. In `Scripts/CoreSelfCheck.swift` remove `projectLoadSelfCheck()` and its
   call site (`try await projectLoadSelfCheck()` in `main`) plus the private
   helpers that exist only for it (`ProjectLoadCheckError`,
   `ProjectLoadCheckGate`, `ProjectLoadCheckRecorder`,
   `ProjectLoadCheckEvent`).
3. `grep -rn "ProjectLoadScheduler\|projectLoadSelfCheck" Sources Tests Scripts`
   must return nothing.

**Verify**: `grep -rn "ProjectLoadScheduler" Sources Tests Scripts` → no matches.

### Step 2: Rework `RawViewModel` to inspect-all + load-on-selection

Replace the eager flow with two operations (keep all existing
approval/trust code untouched):

1. `resumeOrRequestApproval()` now: on approval-current, set
   `hasReaderApproval = true` and start **inspection only** (the first half of
   the old `startProjectLoad`: `ReaderClient.inspectMany(...)` over all
   sources with the existing progress UI: `inspectedSources`, `inspectionTotal`,
   `loadingPhase`). No load phase, no `ProjectLoadScheduler`.
2. Add `func loadFocused()`:
   ```swift
   func loadFocused() {
       guard let project, hasReaderApproval, let id = focusedSourceID,
             let source = sources.first(where: { $0.id == id }) else { return }
       guard let approval = savedApproval(for: project), approval.isCurrent(for: project) else {
           removeSavedApproval(for: project)
           hasReaderApproval = false
           requestReaderApproval()
           return
       }
       guard sourceStates[id]?.measurement == nil, sourceStates[id]?.isLoading != true else { return }
       sourceStates[id]?.isLoading = true
       sourceStates[id]?.error = nil
       let taskID = activeLoadID
       operationTask = Task { [weak self] in
           defer { if taskID == self?.activeLoadID { self?.isLoading = false } }
           do {
               let result = try await ReaderClient.load(source.url, project: project, approval: approval)
               guard taskID == self?.activeLoadID, let self else { return }
               var state = self.sourceStates[id] ?? GallerySourceState()
               state.measurement = result.measurement
               state.inspection = state.inspection
               state.isLoading = false
               state.error = nil
               self.sourceStates[id] = state
           } catch {
               guard taskID == self?.activeLoadID, let self else { return }
               var state = self.sourceStates[id] ?? GallerySourceState()
               state.isLoading = false
               state.error = error.localizedDescription
               self.sourceStates[id] = state
           }
       }
   }
   ```
   (`isLoading` on the model stays true while a focused load runs so the shell
   can show a per-source spinner — adapt the progress UI per Step 3.)
3. Trigger it: in the sidebar binding or via
   `.onChange(of: focusedSourceID)` on the model side — add to
   `ProjectGallery`/shell: whenever `focusedSourceID` changes and the source's
   state has `measurement == nil`, call `model.loadFocused()`. Also call
   `loadFocused()` once when inspection finishes for the already-focused
   source (the 2026-10-02 tree auto-selects the first loaded source at
   inspection end — change that to: set `focusedSourceID` to the first source
   and let `loadFocused()` do the loading).
4. `cancelLoad()` now simply: `operationTask?.cancel(); operationTask = nil;
   activeLoadID = UUID(); isLoading = false;` and clear `isLoading` on the
   focused state (no more "Loading cancelled." fan-out loop).
5. Remove: `retryFailedSources()` and its shell button, `loadProgress`,
   `completedLoads`, `totalLoads`, the `loadingPhase == "Loading"` branch, and
   the "Retry Failed Sources" button in `RawViewShell`. Keep
   `inspectionTotal`/`inspectedSources`/`loadingPhase` for the inspect bar.
6. `GallerySourceState`: delete the `readerSHA256` field and the assignment in
   the (former) load event handler. (`ReaderLoadResult.readerSHA256` in core
   stays — CoreSelfCheck asserts on it.)
7. Errors now live per-source: when inspection fails for a source, its error
   is already stored in `state.error`; the focused pane shows it via
   `sourceStatus`. A failed focused load stays failed until the user selects
   it again (selection change clears nothing; add a small "Load again" button
   in `sourceStatus`? No — out of scope; reselecting the row is enough
   because `loadFocused()` guards on `measurement == nil` — leave as is).

### Step 3: Adjust the shell UI to the lazy model

1. In `RawViewShell`'s sidebar column, replace the inspect/load progress block
   with: the inspecting progress bar + "Cancel Inspection" button while
   inspecting; nothing (or "Load again" handled by pane) otherwise.
2. In `ProjectGallery.focusedPane`, the loading case: while
   `state.isLoading == true`, the existing `sourceStatus` "Loading Source"
   view is fine — keep it.
3. Sidebar dot semantics (they currently signal load completion): change
   `stateColor` to `orange` when `state.error != nil`, `Color.accentColor`
   when `focusedSourceID == source.id`, otherwise `.secondary`. (Green dot is
   meaningless now — nearly everything is not loaded.)

**Verify after each of Steps 1–3**: `sh Scripts/check_core.sh` →
`RawView core self-check passed`.

### Step 4: Build, package, launch

```
sh Scripts/package_app.sh   # → Packaged and verified /private/tmp/RawView-TAI73.app
pkill -f RawView; sleep 1; open /private/tmp/RawView-TAI73.app
```

Manual acceptance with the real project
`/Users/tai/workspace/research-projects/active-projects/res_volatile-polydopamine`
(the operator performs this): open project → approval dialog if reader
changed → inspection bar fills over all sources → click a source in the
sidebar → its figure loads within seconds and fills the center panel →
switching sources loads the new one on demand. RAM stays flat.

## Test plan

- `Scripts/CoreSelfCheck.swift` still passes after scheduler removal (it is
  the regression gate for everything the lazy flow depends on:
  `ReaderClient.inspectMany` batching, cancellation, trust boundary, contract
  decode).
- Structural pattern for any new assertion: add checks to
  `Scripts/CoreSelfCheck.swift`, NOT to `Tests/RawViewCoreTests/*` (they
  cannot run in this environment).
- New self-check cases (add to `CoreSelfCheck.main`): none required for this
  plan — the change is app-orchestration, verified by build + manual
  acceptance above.

## Done criteria

- [ ] `grep -rn "ProjectLoadScheduler" Sources Tests Scripts` → no matches
- [ ] `grep -n "retryFailedSources\|loadProgress\|completedLoads\|totalLoads" Sources/RawViewApp/*.swift` → no matches
- [ ] `grep -n "readerSHA256" Sources/RawViewApp/RawViewApp.swift` → no matches
- [ ] `sh Scripts/check_core.sh` → `RawView core self-check passed`
- [ ] `sh Scripts/package_app.sh` → `Packaged and verified /private/tmp/RawView-TAI73.app`
- [ ] `git status --short -- scientific/raw-viewer` shows only the in-scope files modified/deleted
- [ ] Index status row updated

## STOP conditions

- The working tree does not contain the 2026-10-02 focused-pane UI (i.e.
  `ProjectGallery` still has a `galleryScroll` card wall) — the baseline
  differs; report instead of rewriting UI.
- `ReaderClient.inspectMany` or `ReaderClient.load` signatures changed.
- `check_core.sh` or `package_app.sh` fails twice after a reasonable fix attempt.
- You find yourself editing `ReaderClient.swift` or anything in
  `research-projects/` — out of scope; report.

## Maintenance notes

- After this lands, `RawViewModel` owns exactly two async operations
  (inspect-all, load-focused). Keep it that way; the scheduler was the only
  fan-out.
- Plan 004 (combined filtering) builds its chips on the sidebar grouping this
  plan leaves intact.
- Reviewer focus in the PR: that no code path calls `ReaderClient.load` other
  than `loadFocused()`, and that cancellation cannot leave a source stuck in
  `isLoading == true` (cancel path clears it).
