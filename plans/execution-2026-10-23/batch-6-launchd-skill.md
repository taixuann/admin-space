# Batch 6: launchd-automation rewrite

Request: 008. Executed 2026-10-23 in `/Users/tai/.agents/skills/launchd-automation/`.
The skill is Admin-maintained source; installation is the live copy at the same
path.

## Changes

| File | Change |
| --- | --- |
| `SKILL.md` | Classify owner → fix report root → scaffold → customize → static validation → authorized deploy → live outcome |
| `references/launchd_best_practices.md` | Lifecycle reference: domains, bootstrap/bootout/print, absolute paths, sleep/wake, timezone, exit codes, rollback, dispatch vs completion |
| `scripts/scaffold_automation.py` | Required `--layout {tool,space}` and absolute `--report-root`; refuses relative or inside-source roots, existing scaffolds, wrong repository boundaries, and relative program paths; direct execution by default; opt-in `--wrapper` and `--deploy` |
| `scripts/verify_automation.py` | `--static` default (no execution, read-only `launchctl print`), opt-in `--live` with kickstart and terminal-outcome polling, installed byte comparison, duplicate-label check |
| `templates/` | Direct `ProgramArguments`, external logs, declared environment, no `WorkingDirectory`; wrapper only as an option; README and AGENTS templates |
| `templates/track_metadata.template.json` | Removed; the automation scanner never read it |
| `tests/test_skill_scripts.py` | 18 stdlib tests |

## Report root

The scaffolder refuses a report root inside the source folder. Space-owned source
at `~/.agents/automation/<job-name>/` therefore uses
`~/.agents/automation/<job-name>-runtime/logs/`. The docs and skill state this
naming rule. Admin `.gitignore` ignores `/automation/*-runtime/`.

## Verification

| Check | Result |
| --- | --- |
| Skill tests | 18/18 pass |
| `py_compile` on scripts and tests | Pass |
| `bash -n` on a rendered wrapper | Pass |
| `plutil -lint` on rendered plists | OK |
| Static run against a real folder | Returns `FAIL` for missing files, does not execute the program |
| Static no-mutation test | Fake `launchctl` records only `print` calls; marker program never runs |
| `--deploy` | Not executed; would change live launchd state |
| Live run | Not performed |

## Runtime state

- No plist was installed or removed.
- No job was booted out, bootstrapped, or kickstarted.
- `com.tai.model-control-sync` remains loaded and unchanged.
- `com.tai.linear-notion-sync` remains loaded with `runs = 0` after the path
  repair.
- `com.tai.bridge.sync` remains untouched.
- `com.tai.opencode-model-refresh` is not loaded.

## Residual risk

- `--deploy` is review-only in this execution.
- `--compare-installed` was exercised only with a temporary `HOME`.
- Absolute non-file `ProgramArguments` values need `--allow-missing-args`.
