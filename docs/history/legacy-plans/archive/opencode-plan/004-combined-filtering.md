# Plan 004: Combined multi-facet filtering in the sidebar

> **Executor instructions**: Follow this plan step by step. Run every
> verification command and confirm the expected result before moving to the
> next step. If anything in the "STOP conditions" section occurs, stop and
> report — do not improvise. When done, update the status row for this plan
> in the index (`/Users/tai/.opencode/plan/README.md`).
>
> **Drift check (run first)**: The baseline is the WORKING TREE of
> `/Users/tai/.codex/worktrees/rawview-sidebar/tools` at commit `9874ef32`
> (branch `codex/rawview-sidebar`).
> the sidebar is the navigator and `ProjectGallery` shows one focused figure.
> Compare the "Current state" excerpts against the live files; on a mismatch,
> STOP and report.

## Status

- **Priority**: P2
- **Effort**: M
- **Risk**: LOW
- **Depends on**: 001
- **Category**: direction / feature (user-approved UX upgrade)
- **Planned at**: commit `9874ef32`

## Why this matters

Today the sidebar offers one grouping facet at a time (the 2026-10-02
"Group by" picker) plus free-text search — but no way to say "show me only
Autolab CV files from 2025-11-27". The user asked for combined filtering:
**AND across facets, OR within a facet** (confirmed choice). The grouping
machinery to derive each facet's groups already exists in
`RawViewCore/SourceGrouping.swift`; this plan adds a small filter model in
core (testable via CoreSelfCheck) and wires filter toggles + removable chips
into the sidebar.

## Current state

`Sources/RawViewApp/ProjectGalleryViews.swift` — `ProjectSourcesSidebar`:

```swift
static let facets: [(String, String)] = [
    ("", "None"), ("sample", "Sample / Device"), ("instrument", "Instrument"),
    ("study", "Study"), ("mode", "Mode"), ("date", "Date / Batch"), ("status", "Status"),
]

private func groups(for key: String) -> [SourceGroup] {
    let grouping = SourceGrouping(inspections: Array(inspections.values))
    var base: [SourceGroup]
    switch key {
    case "sample": base = grouping.sampleDevice
    case "study": base = grouping.study
    case "mode": base = grouping.measurementMode
    case "date": base = grouping.dateBatch.sorted { $0.label > $1.label }
    case "status": ... (status + "Error: ..." groups)
    default: base = []
    }
    return base.compactMap { group -> SourceGroup? in
        let ids = group.sourceIDs.filter { matches($0, label: group.label) }
        return ids.isEmpty ? nil : SourceGroup(label: group.label, sourceIDs: ids)
    }
}
```

`Sources/RawViewCore/SourceGrouping.swift` exposes `sampleDevice`,
`instrument`, `study`, `measurementMode`, `dateBatch`, `status` as
`[SourceGroup]` (label + sorted sourceIDs). `SourceInspection` has
`source` (the relative path = `RawSource.id`), `instrumentName`,
`instrumentID`, `applicationMode`, `timestamp`, `deviceID`, `studyToken`,
`supportStatus`, `validationState`.

Facet membership per source is derivable by inverting the groups: for each
facet, `groups` gives label → [sourceIDs].

## Commands you will need

| Purpose | Command (cwd = `.../scientific/raw-viewer`) | Expected on success |
|---|---|---|
| Core gate | `sh Scripts/check_core.sh` | `RawView core self-check passed` (+ app typecheck per Plan 002) |
| Package build | `sh Scripts/package_app.sh` | `Packaged and verified /private/tmp/RawView-TAI73.app` |

## Scope

**In scope**:
- `Sources/RawViewCore/SourceFilter.swift` (new, ~60 lines)
- `Scripts/CoreSelfCheck.swift` (add filter assertions)
- `Sources/RawViewApp/ProjectGalleryViews.swift` (sidebar wiring + chips)
- `Sources/RawViewApp/RawViewApp.swift` (only to pass `SourceFilter` state between shell and sidebar if needed — prefer keeping state inside `ProjectSourcesSidebar`)

**Out of scope**:
- `SourceGrouping.swift` public API (extend nothing; read it).
- The focused pane, plot, inspector, reader trust machinery.
- Saved filters, filter presets, per-column tables — not requested.
- `research-projects/`.

## Git workflow

Worktree `/Users/tai/.codex/worktrees/rawview-sidebar/tools`, branch
`codex/rawview-sidebar`, conventional commits (`feat(raw-viewer): ...`).

## Steps

### Step 1: `SourceFilter` in RawViewCore

Create `Sources/RawViewCore/SourceFilter.swift`:

```swift
public struct SourceFilter: Sendable, Equatable {
    public var selections: [String: Set<String>] = [:]   // facet key -> selected labels

    public init() {}

    public mutating func toggle(facet: String, value: String)
    public mutating func remove(facet: String, value: String)
    public mutating func clear()                          // clears all facets
    public var isEmpty: Bool { selections.values.allSatisfy(\.isEmpty) }

    /// A source matches when, for EVERY facet with selections, its label set for
    /// that facet intersects the selection (AND across facets; values OR within a facet).
    public func matches(_ labelsByFacet: [String: Set<String>]) -> Bool { ... }
}
```

Matching rule (implement exactly): for each facet key with a non-empty
selection in `selections`, the source must carry at least one of the selected
labels in that facet (`!labelsByFacet[facet].isDisjoint(selected)`). Sources
lacking any label for a selected facet are EXCLUDED. Free-text search stays
in the view layer (existing `matches(_:label:)`), composed after the filter.

**Verify**: `sh Scripts/check_core.sh` → passed (Step 2 adds the assertions).

### Step 2: Self-check assertions

Append to `Scripts/CoreSelfCheck.swift` `main` (after the existing grouping
checks, which build a `SourceGrouping` over 2 fixture inspections — reuse
those fixtures):

```swift
let filter = SourceFilter()   // plus fixture-derived facet maps:
// fixture a.csv: instrument=Fixture, mode=sweep, date=2026-09-30, device=D1, study=S1
// fixture c.csv has an error row, not an inspection — excluded from label maps.
precondition(filter.isEmpty)
precondition(filter.matches(["instrument": ["Fixture"], "study": ["S1"]]))
var f = SourceFilter(); f.toggle(facet: "instrument", value: "Fixture")
precondition(f.matches(["instrument": ["Fixture"], "study": ["Other"]]))   // OR within facet
var g = SourceFilter(); g.toggle(facet: "instrument", value: "Fixture"); g.toggle(facet: "study", value: "Missing")
precondition(!g.matches(["instrument": ["Fixture"], "study": ["S1"]]))     // AND across facets excludes
f.remove(facet: "instrument", value: "Fixture"); f.clear()
precondition(f.isEmpty && f.matches([:]))
```

(Adjust variable names to the real fixture data — the file's existing
grouping section builds `inspections` from the `inspectionJSON` literal; use
the same values.)

**Verify**: `sh Scripts/check_core.sh` → `RawView core self-check passed`.

### Step 3: Sidebar wiring

1. `ProjectSourcesSidebar` gains `@State private var filter = SourceFilter()`
   and a `labelsByFacet(for: RawSource) -> [String: Set<String>]` built from
   the source's `SourceInspection` (map facet keys: `sample`→deviceID,
   `instrument`→instrumentName ?? instrumentID, `study`→studyToken,
   `mode`→applicationMode, `date`→the `SourceGrouping.date(from:)` result —
   note that helper is private; either reuse by making it internal
   `public/internal` in SourceGrouping.swift (acceptable minimal change) or
   replicate the 10-char ISO date check in SourceFilter construction —
   prefer making `SourceGrouping.date(from:)` internal).
2. Group headers (in `groupSection`) get a trailing filter toggle that is
   visible only when a facet is active: a small text button showing `●`
   when that group's label is selected, `○` otherwise. Tap toggles
   `filter.toggle(facet: facet, value: group.label)`.
3. Sources shown under "All files" and inside groups =
   `filteredSources.filter { filter.matches(labelsByFacet(for: $0)) }`.
   Update `filteredSources` and `groups(for:)` to compose:
   search (existing) ∩ filter (new). Keep the picker's facet choice as the
   grouping; filtering works across facets regardless of which facet is
   displayed.
4. Above the List, render active filter chips:
   `HStack` of `Button("Instrument: Autolab USTH ✕") { filter.remove(facet:value:) }`
   wrapped so they wrap into rows (use a simple `VStack` of `HStack`s or a
   LazyVGrid; no new dependency). Add a "Clear filters" text button when
   non-empty. `filter.clear()` on project change is automatic because
   `ProjectSourcesSidebar` state resets when `sources` is reinstalled — verify
   that claim in the real app; if identity persists, add
   `.onChange(of: sources.count) { filter.clear() }`.
5. Show an empty-state label when the combined filter yields zero sources:
   `ContentUnavailableView("No Matching Sources", ...)` inside the List
   instead of nothing.

**Verify**: `sh Scripts/check_core.sh` → passed.

### Step 4: Build, package, launch

```
sh Scripts/package_app.sh
pkill -f RawView; sleep 1; open /private/tmp/RawView-TAI73.app
```

Manual acceptance (operator): select Instrument=Autolab, then Study=X →
sources narrow to the intersection; chips removable; clearing restores all;
search composes with filters.

## Test plan

- New assertions in `Scripts/CoreSelfCheck.swift` (Step 2) — this is the
  regression gate (Swift Testing files cannot run in this environment).
- Cases covered: empty filter matches all; single-facet single value; OR
  within facet (two values, one matches); AND across facets (conflict
  excludes); facet with no label on the source excludes; remove/clear.

## Done criteria

- [ ] `Sources/RawViewCore/SourceFilter.swift` exists and is compiled by the package (no Package.swift change needed)
- [ ] `sh Scripts/check_core.sh` → self-check passed, including the new filter preconditions
- [ ] `sh Scripts/package_app.sh` → packaged and verified
- [ ] `grep -n "filter" Sources/RawViewApp/ProjectGalleryViews.swift` shows the chips row and toggle wiring
- [ ] No out-of-scope files modified (`git status`)
- [ ] Index status row updated

## STOP conditions

- `SourceGrouping` semantics change under you (e.g. status groups include
  errors) — status facet filtering includes the `Error: ...` groups; that is
  intended; anything else unexpected, report.
- Plan 001 has not landed (scheduler still present / gallery cards exist).
- The 6,727-source list regresses in responsiveness after wiring (measure by
  scrolling with filters empty).

## Maintenance notes

- When a new grouping facet is added to `SourceGrouping`, the sidebar
  `facets` list and `labelsByFacet` must be extended together — the
  precondition suite in CoreSelfCheck guards the matching rule only.
- Reviewer focus: that the `date` facet label used for filtering is identical
  to the displayed group label (both derive from `SourceGrouping.date(from:)`).
