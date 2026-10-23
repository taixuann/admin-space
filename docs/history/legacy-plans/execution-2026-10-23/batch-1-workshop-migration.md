# Batch 1: workshop path migration and consumer repair

Request: 009. Executed 2026-10-23. Pre-state in `evidence/pre-migration.txt`.

## Inventory result

| Surface | Finding | Action |
| --- | --- | --- |
| Workshop repository | Clean, `master` at `2fa7343…`, 306 tracked files | Moved, unmodified state preserved |
| Workshop linked worktree | One Antigravity worktree outside the workshop | `.git` file repaired |
| Linked worktrees of other repositories inside the workshop | 7: 6 of `research-projects`, 1 of `research-projects/tools/raw-viewer` | Registration repaired, dirty work preserved |
| Active processes | None with the old path in `ps` | No process stopped |
| Symlinks into the old path | None found in `~/.claude`, `~/.codex`, `~/.config/opencode`, `~/.agents`, `~/.gemini` | Nothing to rewrite |
| `com.tai.linear-notion-sync` | Loaded, daily 00:00, runner and both log paths under the old workspace path; no tracked source plist existed | Installed plist edited, reloaded |
| `com.tai.bridge.sync` | Tracks the workshop by id and path | Config path and description updated |
| `com.tai.model-control-sync` | Points at `~/.agents`, unaffected | Untouched |
| `automation/track-automation` snapshot | Three old-path strings for the Linear job | Path strings corrected in the snapshot |
| `automation/linear-notion-tracking` (`projects.json`, `forge_driver.py`, `README.md`) | Live `workshop_path`/`worktrees_dir` values and defaults | Updated |
| `~/.codex/config.toml` | Project trust entry, two hook-state keys, `git-worktree-root` | Updated, TOML re-parsed |
| `~/.gemini/config/projects/…json` | Antigravity project registry pointed at the old path | `folderUri` and display name updated |
| `dossiers/tai-78_dossier.json` | Historical run evidence | Preserved unchanged |
| Worktree plan receipts under `worktrees/` | Historical evidence containing old absolute paths | Preserved unchanged |

## Migration sequence performed

1. Confirmed the target path was absent and the workshop tree was clean.
2. `mv /Users/tai/agent-development /Users/tai/development-space`.
3. `git -C /Users/tai/development-space worktree repair <antigravity worktree>`.
4. `git -C /Users/tai/research-projects worktree repair` for 6 worktrees;
   `git -C /Users/tai/research-projects/tools/raw-viewer worktree repair` for 1.
5. Edited the installed `com.tai.linear-notion-sync.plist`, ran `plutil -lint`,
   then `bootout` and `bootstrap` for that label only.
6. Updated the bridge config, the track-automation snapshot, the Linear job
   configuration, `~/.codex/config.toml`, and the Antigravity project registry.
7. Rewrote `AGENTS.md` and `README.md`; added `docs/small-tool-contract.md`.

## Verification

| Check | Command | Result |
| --- | --- | --- |
| Workshop HEAD preserved | `git -C ~/development-space rev-parse HEAD` | `2fa7343800e57891947ab6683bacfcb5af350a1e` |
| Workshop tree state | `git status --short` | Only the files this batch edited; no deletions |
| Workshop worktree list | `worktree list --porcelain` | Main path is `/Users/tai/development-space`; Antigravity worktree present |
| `research-projects` worktree list | `worktree list --porcelain` | All 7 worktrees report new paths |
| Dirty work preserved | `git status --porcelain` in each worktree | Counts unchanged from pre-state (33, 0, 4, 2, 3, 1, 58) |
| Plist syntax | `plutil -lint` | OK |
| Service reload | `launchctl print gui/$(id -u)/com.tai.linear-notion-sync` | `state = not running`, `runs = 0`, new stdout/stderr paths |
| Codex config | `tomllib.loads(...)` | Parses; zero occurrences of the old path |
| Broken symlinks | `find … -type l ! -exec test -e` | None |
| Stale live references | `grep` over tracked live files | None; only preserved historical evidence remains |

## Limits

- The Linear job was reloaded but not executed. A real run would perform a
  Linear-to-Notion sync with external side effects, which this batch did not
  authorize. `runs = 0` is configuration evidence, not a runtime result.
- No tracked source plist exists for `com.tai.linear-notion-sync`. The installed
  plist is the only copy. Rollback copy:
  `evidence/linear-notion-sync.plist.pre-migration`.
- The workshop repository changes are uncommitted. Its automation commits on its
  own schedule; this execution does not add commit authority.
