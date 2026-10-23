# Batch 7: cumulative verification

Requests: 008, 009, 010. Executed 2026-10-23. This is the single final
validation pass over the reconciled diff. It reuses the per-batch evidence and
re-runs every check that can run without external side effects.

Scope note: this pass proves the state listed below. It is not a runtime proof
for anything that needs a schedule to fire or a Notion write to succeed. The
levels are separated at the end.

## 1. Repository and boundary state

| Check | Command | Result |
| --- | --- | --- |
| Admin HEAD | `git -C ~/.agents rev-parse HEAD` | `40e9d38238e487744ec216f5a57617e3c09cfb3e`, branch `codex/companion-v2` |
| Admin tracked files under `tools/` | `git ls-files tools \| wc -l` | `0` |
| Admin ignore rule | `grep tools .gitignore` | `/tools/` present, with the pointer comment to `docs/tools.md` |
| Tool repositories | `git -C tools/<name> remote -v \| wc -l` | `0` for all three; no remote invented |
| Tool baselines | `rev-parse --short HEAD` | `opencode-free-router` `21cb19c`, `hindsight` `ea0c7e9`, `automation-incidents` `70647f7` |
| Tool branches | `git branch --show-current` | `main` for all three |
| Tool worktree | `git -C ~/development-space/worktrees/admin/opencode-free-router_008` | branch `admin/opencode-free-router_008`, base `21cb19c`, 2 modified + 1 untracked path |
| Workshop repository | `git -C ~/development-space rev-parse HEAD` | `2fa7343800e57891947ab6683bacfcb5af350a1e` (pre-migration HEAD preserved) |
| Workshop worktrees | `git worktree list` | Main path is the new location; the Antigravity worktree resolves through `~/development-space/.git/worktrees/…` |
| Linked worktrees of other repos | `git -C ~/research-projects worktree list` | All 7 report paths under `~/development-space/…` |
| Dirty work preserved | `git status --porcelain \| wc -l` per worktree | `33, 0, 4, 2, 3, 1, 58` — identical to the pre-migration counts |

Admin working tree carries 42 staged `tools/` deletions, 22 modified tracked
paths, and 13 untracked entries (59 files reached recursively). Nothing in this
execution commits the Admin repository; commit authority was not granted.

## 2. Test suites

Each suite is stdlib `unittest` and runs under the plain `python3` on this
machine, which is 3.14. `pytest` is not installed for 3.14, so the documented
`unittest` invocation is the one that matters; the same suites also pass under
`python3.13 -m pytest`.

| Suite | Documented command | Result |
| --- | --- | --- |
| Model selection | `python3 -m unittest discover -s backend/tests -p 'test_model_sync.py'` (worktree) | `Ran 17 tests … OK` |
| Model-refresh runner | `python3 -m unittest discover -s tests` (`automation/model-refresh`) | `Ran 17 tests … OK` |
| Incident delivery | `python3 -m unittest discover -s tests -v` (`tools/automation-incidents`) | `Ran 31 tests … OK` |
| launchd skill | `python3 -m unittest discover -s tests` (`skills/launchd-automation`) | `Ran 18 tests … OK` |

Total: 83 passing. The earlier per-batch counts are unchanged, so no later
batch regressed an earlier one.

## 3. Static configuration checks

| Check | Command | Result |
| --- | --- | --- |
| Model-refresh plist | `plutil -lint automation/model-refresh/launchd.plist` | `OK` |
| Installed Linear plist | `plutil -lint ~/Library/LaunchAgents/com.tai.linear-notion-sync.plist` | `OK` (checked in batch 1) |
| Skill plist template | `plutil -lint templates/plist.template.xml` | Fails by design: the file carries `{{ }}` placeholders. The skill's verifier renders before linting, and its 18 tests cover that path. A raw `plutil` pass is not a valid check for a template. |
| Markdown links, Admin surfaces | script over `docs/`, plan files, skill docs | 74 links checked, 0 broken |
| Markdown links, tool repositories | script over all three tool repos | 15 links checked, 0 broken |
| Markdown links, job docs | script over `automation/model-refresh/**/*.md` | 2 links checked, 0 broken |
| Secret scan | regex over changed docs, skill, and tool sources | No token-shaped strings |
| Workflow diagram | structural parse, external-reference scan | `automation/model-refresh/docs/workflow.html` parses with 0 tag mismatches, has no `<script src>`, `<link>`, `fetch`, or remote font source, and names the five outcomes, the outbox, and the active label. The toolbar's Archify attribution URL is text, not a request. |

Link checks excluded `plans/global-instructions/**` evaluation fixtures, which
contain deliberately unresolvable references, and one pre-existing
`automation/track-automation/README.md` link to an absolute `personal-hub` path
that does not exist on disk. That file was not touched by this execution.

## 4. Runtime surfaces

| Surface | Observation | Reading |
| --- | --- | --- |
| `com.tai.model-control-sync` | Loaded, exit `0`, untouched | Legacy schedule still owns model refresh |
| `com.tai.linear-notion-sync` | Loaded, `state = not running`, `runs = 0`, stdout/stderr under `~/development-space/…` | Repaired and reloaded, never executed |
| `com.tai.bridge.sync` | Loaded, exit `0` | Untouched |
| `com.tai.opencode-model-refresh` | Not loaded | Replacement schedule never activated |
| Report root `~/.agents/automation/opencode-model-refresh/` | Absent | No live run has written evidence |
| Incident state directory | Absent | No live ticket, no persisted episode |
| OpenCode default model | `opencode/deepseek-v4.1-flash-free` in `~/.config/opencode/opencode.jsonc` | Unchanged |
| Legacy runner `automation/model-control/run-sync.sh` | Byte-identical to the pre-execution version; still calls `model_sync.py` then `model-control/index-if-needed.sh` | Unrelated indexing behavior preserved |
| `automation/model-control/*` symlinks | `app.css`, `index.html`, `model-control-spec.json` all resolve into `tools/opencode-free-router/model-control/` | Display assets survive the Git extraction because the tool directory still exists on disk |

## 5. Skill installation state

`~/.agents/skills` is the canonical source for OpenCode, Codex, Goose, and Pi;
Claude Code and Gemini need symlinks, produced by `bin/sync-skills`.

| Check | Result |
| --- | --- |
| Skill source present | `skills/launchd-automation/` with `SKILL.md`, reference, scaffold, verifier, templates, 18 tests |
| OpenCode discovery | The `launchd-automation` entry offered to this session carries the rewritten description verbatim, so the loader parsed the new frontmatter |
| Claude Code discovery | `~/.claude/skills/launchd-automation` does not exist — the skill is not visible to Claude Code |
| Installer drift, Claude Code | `bin/sync-skills --check` | 8 skills to add, 39 links to retarget from absolute `~/.oleafly/skills/…` paths to relative ones |
| Installer drift, Gemini | same run | 47 skills to add, 4 links to retarget |

The drift predates this execution and is wider than the deliverable. The
installer was not run: it would mutate 102 unrelated links across two hosts.
Adding the single `launchd-automation` link would make the rewritten skill
visible in Claude Code; that is a one-line decision left to the owner.

## 6. Evidence levels

The distinction below is the honest status of each deliverable.

| Level | What is proven | What is not |
| --- | --- | --- |
| Source implementation | Code, docs, skill, and repositories exist with passing tests and lints | — |
| Skill installation | Skill source is in the canonical directory and OpenCode discovers the new version | Claude Code and Gemini do not see it until the installer runs |
| Behavior evaluation | Unit tests cover failure paths, locking, recovery evidence, exit codes, and the two layouts | No representative end-to-end task was run against the new profile, because the profile is still a draft |
| Service configuration | Plists lint, installed label is loaded, report roots are declared | The replacement job is not loaded; no schedule has fired |
| Live runtime | Legacy job still loaded and untouched | No new job has executed; no run evidence exists under the live report root |
| Notion delivery | Fake-transport end-to-end run produced create, recovery, and status-unchanged behavior | No live API call; unattended authentication, template application, and pagination remain unverified |

## 7. Open gates

1. `com.tai.opencode-model-refresh` cannot replace the legacy schedule until
   `model-control/index-if-needed.sh` has its own job. The model-refresh runner
   covers model selection only. Its plist also calls the stable checkout
   `~/.agents/tools/opencode-free-router/automation/model-refresh/runner.py`,
   which does not exist there yet: the work is uncommitted on the tool branch.
   Activation therefore needs the branch committed to the tool repository and
   the stable checkout updated, not just a `launchctl bootstrap`.
2. Incident grouping policy is a required config field with no default. Until a
   value is chosen the job would fail at configuration, not silently guess.
3. Unattended Notion authentication is unresolved, so the transport stays inert
   in any scheduled context.
4. The profile's final name, runtime format, attached skill set, ticket trigger,
   and review threshold are still open; `docs/profiles/admin-architect-planning.md`
   is a draft.
5. `cli-developer`, `agent-rules`, and the `agent-skills` phase skills are
   referenced by the profile work but are not installed on this machine.
6. `bin/sync-skills` drift (section 5) is unrepaired.

## 8. Late additions

The process diagram landed after the main pass and was checked separately
(section 3). It states the same caveat as section 7: the label is not installed,
the tree it describes is untracked, and the diagram is descriptive rather than
executable.

Reading the runner against its own runbook surfaced one wording defect.
`README.md` said delivery failure "never counts as a successful refresh", which
implies delivery can change the outcome. In `runner.py` the outcome and exit
code are decided before delivery, so a successful refresh with a failed report
still records `success` and exits `0`, leaves the event in `incident-outbox/`,
and records the failure in `latest-delivery.json`. The runbook now says that.
Failure events are emitted only for a failed refresh; a success after a failed
`latest-result.json` emits one recovery event.
