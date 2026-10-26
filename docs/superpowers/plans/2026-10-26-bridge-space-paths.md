```yaml
requester: secretary
space: ~/.agents
base: master
branch: executor/bridge-space-paths
scope: [automation/bridge/config/github-track.yaml, automation/bridge/config/drive-track.yaml, automation/bridge/README.md, automation/bridge/tests/]
checks:
  - /opt/miniconda3/envs/core/bin/python3 -m unittest discover -s automation/bridge/tests -v
  - python3 -c "import yaml;[yaml.safe_load(open(f'automation/bridge/config/{n}.yaml')) for n in ('github-track','drive-track')]"
  - every workspace `path` and Drive `source_path` in both YAML files exists on disk (print a PASS/FAIL line per path)
  - each tracked github workspace's `remote_repo` and `default_branch` equal `git -C <path> remote get-url origin` and `git -C <path> branch --show-current` (print the pairs)
  - rg -n "research-projects|personal-hub|agent-skills|agent-development|assets/bridge|~/learn|~/knowledge-base" automation/bridge --glob '!logs/**' --glob '!.pytest_cache/**' returns nothing
  - git diff --name-only shows only in-scope files
engine: self
report: kanban card comment + kanban_complete summary to Secretary
```

# Bridge: align config and runbook with the three Space repos

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans.

**Goal:** The Bridge sync job (`automation/bridge`) tracks the current Space layout: Admin `~/.agents`, Development `~/development-space`, Research `~/academic-space/research-space`, and its Drive profile for personal files writes to the Drive folder `personal-space`.

**Architecture:** Config and docs only. `config/github-track.yaml` and `config/drive-track.yaml` are the source of truth; `README.md` mirrors them. No backend code, no launchd change.

**Spec:** Tai, 2026-10-26: the three Space repos are `admin-space`, `development-space`, `research-space`; Drive runs into the `personal-space` folder for now.

## Global Constraints

- Preflight exception granted by the requester: the tree has unrelated pre-existing modifications under `skills/` and `.skill-lock.json` (written by the daily skills job). They are not yours: do not stage, revert, or touch them, and do not block on them. Check scope with `git diff --name-only` against your own files only.
- Do not run `bridge sync ...` (any mode), `rclone`, or launchctl. Config edits and read-only checks only. Secretary runs the live dry-runs.
- Do not edit `bin/`, `backend/`, `frontend/`, `scripts/`, or the plist.
- Keep each workspace's `tracked` / `pull_enabled` value exactly as it is now.

## Verified facts (2026-10-26)

| Space | Local path | origin | Branch |
| --- | --- | --- | --- |
| Admin | `/Users/tai/.agents` | `taixuann/admin-space` | `master` |
| Development | `/Users/tai/development-space` | `taixuann/development-space` | `master` |
| Research | `/Users/tai/academic-space/research-space` | `taixuann/research-space` | `main` |
| Raw Viewer | `/Users/tai/development-space/tools/research/raw-viewer` | `taixuann/raw-viewer` | `master` (the path under research-space is a symlink to it) |
| Personal | `/Users/tai/personal-space` | `taixuann/non-research-projects` | `main` |
| Knowledge | `/Users/tai/academic-space/knowledge-space` | `taixuann/wiki` | `main` |
| Portfolio | `/Users/tai/personal-space/professional/portfolio/site` | `taixuann/academic-portfolio` | `main` |

Drive folders that exist: `research`, `learn`, `knowledge-base`, `personal-space`, `archive`, `inbox`.

## Review Focus

- Wrong `remote_repo` pushes to a nonexistent repo: the origin comparison check catches it.
- Renaming an id breaks a CLI/test reference (`--repo agent-skills`, `--profile personal-hub-sync`): update tests and README examples together.
- Two workspaces resolving to one git repo (raw-viewer symlink): use the real path only, once.
- `learn-sync` and `knowledge-base-sync` overlap (knowledge-base is inside knowledge-space). Do NOT merge or remove them; list it in the report.

### Task 1: Update both YAML files

**Files:** Modify `automation/bridge/config/github-track.yaml`, `automation/bridge/config/drive-track.yaml`; Test `automation/bridge/tests/` (fix any id the tests reference).

**Interfaces:** Produces the ids the README uses: github ids `admin-space`, `development-space`, `research-space`, `raw-viewer`, `personal-space`, `knowledge-space`, `academic-portfolio`; Drive ids `personal-space-sync`, `research-space-sync`, `learn-sync`, `knowledge-base-sync`.

- [ ] **Step 1:** In `github-track.yaml` set id, name, path, `remote_repo`, `default_branch` from the table above (Research: id `research-space`; Admin: id `admin-space`; Development: id `development-space`; raw-viewer path is the real development-space path; Personal: id `personal-space`; Knowledge: id `knowledge-space`).
- [ ] **Step 2:** In `drive-track.yaml` set `personal-space-sync` `remote_target` to `gdrive:personal-space/`; rename `research-projects-sync` to `research-space-sync` (keep `gdrive:research/projects/`); keep the other two targets unchanged.
- [ ] **Step 3:** Run the unit tests; fix references to renamed ids in `tests/`; rerun → PASS.
- [ ] **Step 4:** Run the YAML, path-exists, and origin-match checks from the header; paste the output.

### Task 2: Update the README

**Files:** Modify `automation/bridge/README.md`.

- [ ] **Step 1:** Replace `assets/bridge/` with `automation/bridge/` everywhere (layout tree, CLI examples, test command).
- [ ] **Step 2:** Regenerate both tracking tables from the two YAML files (ids, paths, remotes, branches, tracked flags, Drive targets) and fix example ids in CLI snippets and rule 2 (`personal-space`, `knowledge-space`).
- [ ] **Step 3:** Add a "Known limits" note: `learn-sync` and `knowledge-base-sync` overlap; the job auto-commits and pushes tracked repos daily; the installed LaunchAgent must be loaded for any run.
- [ ] **Step 4:** Run the `rg` stale-term check → no output; run all checks; commit on `executor/bridge-space-paths`; stop for Tai's review. Do not merge, push, or deploy.
