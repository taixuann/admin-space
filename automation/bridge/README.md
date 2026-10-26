# Bridge

Bridge manages multi-repository Git synchronization and Google Drive 1:1 cloud backup across local workspaces.

## Directory Layout

```
automation/bridge/
├── bin/
│   ├── bridge                    # Executable CLI entrypoint
│   └── auto-sync.sh              # Unattended runner for scheduled automation
├── config/
│   ├── github-track.yaml         # GitHub repository tracking registry
│   ├── drive-track.yaml          # Google Drive 1:1 sync profiles
│   └── com.tai.bridge.sync.plist # macOS LaunchAgent template
├── backend/
│   ├── server.py                 # Loopback REST API and frontend server (port 8768)
│   ├── scanner.py                # Git status inspector and directory tree generator
│   ├── config_manager.py         # YAML configuration reader and writer
│   ├── git_engine.py             # Git staging, commit formatting, and push engine
│   └── drive_engine.py           # Rclone mirror engine, exclude generator, and share link resolver
├── frontend/
│   ├── index.html                # Single-page dashboard interface
│   ├── app.css                   # Layout and component styles
│   └── app.js                    # UI controller and state manager
├── logs/
│   ├── github-sync.log           # GitHub sync audit trail
│   ├── drive-sync.log            # Google Drive sync audit trail
│   ├── launchd.stdout.log        # Scheduled runner standard output
│   └── launchd.stderr.log        # Scheduled runner standard error
└── tests/
    ├── test_config.py            # Unit tests for YAML configuration manager
    ├── test_git_engine.py        # Unit tests for Git automation engine
    ├── test_drive_engine.py      # Unit tests for Drive sync and auto-commit
    └── test_cli.py               # Unit tests for CLI subcommands
```

## Tracked Systems

### 1. GitHub Workspaces (`config/github-track.yaml`)

| Workspace ID | Local Path | Remote Repository | Default Branch | Tracked | Role |
| :--- | :--- | :--- | :--- | :---: | :--- |
| `research-space` | `~/academic-space/research-space` | `taixuann/research-space` | `main` | Yes | Research Space (scientific research) |
| `admin-space` | `~/.agents` | `taixuann/admin-space` | `master` | Yes | Admin Space (agent instructions, skills, automation) |
| `development-space` | `~/development-space` | `taixuann/development-space` | `master` | Yes | Development Space (engineering workshop; hosts linked worktrees only) |
| `raw-viewer` | `~/development-space/tools/research/raw-viewer` | `taixuann/raw-viewer` | `master` | Yes | Scientific data viewer tool (reached from research-space through a symlink; tracked once at its real path) |
| `personal-space` | `~/personal-space` | `taixuann/non-research-projects` | `main` | No | Personal LifeOS (local Git only) |
| `knowledge-space` | `~/academic-space/knowledge-space` | `taixuann/wiki` | `main` | No | Digital garden knowledge base (pull-only) |
| `academic-portfolio` | `~/personal-space/professional/portfolio/site` | `taixuann/academic-portfolio` | `main` | Yes | Academic and personal portfolio website |

### 2. Google Drive Cloud Profiles (`config/drive-track.yaml`)

| Profile ID | Source Directory | Remote Target | Auto-Commit | Excluded Patterns |
| :--- | :--- | :--- | :---: | :--- |
| `personal-space-sync` | `~/personal-space` | `gdrive:personal-space/` | Yes | `.git`, `.venv`, `.pytest_cache`, `.DS_Store`, `node_modules`, `.obsidian/workspace*` |
| `research-space-sync` (disabled) | `~/academic-space/research-space` | `gdrive:research/projects/` | Yes | `.git`, `.venv`, `venv`, `.build`, `.pytest_cache`, `.ruff_cache`, `.DS_Store`, `__pycache__`, `node_modules`, `worktree`, `worktrees` |
| `learn-sync` (disabled) | `~/academic-space/knowledge-space` | `gdrive:learn/` | Yes | `.git`, `.venv`, `.pytest_cache`, `.DS_Store`, `node_modules`, `.obsidian/workspace*` |

## Operational Rules

1. Only commit and push repositories where `tracked: true` in `config/github-track.yaml`.
2. Do not push un-tracked repositories (`personal-space`, `knowledge-space`) to remote GitHub origins.
3. Use the exact commit message format for automated commits:
   `automation: YYYY-MM-DD commit automatically`
4. If a local repository has uncommitted changes before Google Drive synchronization, commit changes locally before running `rclone sync`.
5. Execute Google Drive synchronization as a 1:1 mirror using `rclone sync`. Files removed locally must be removed on remote targets.
6. Share links generated for Google Drive targets must remain public read-only (`reader` role).

## Known Limits

- Only `personal-space-sync` is enabled for Google Drive. `research-space-sync` and `learn-sync` stay disabled in config (re-enable with `bridge track drive <id> --enable`).
- The daily job auto-commits and pushes every `tracked: true` repository. Review pending changes in those repositories before the run.
- The installed LaunchAgent must be loaded for any scheduled run; a manual run does not replace it.

## CLI Reference

Run the executable CLI wrapper:

```bash
./automation/bridge/bin/bridge <command> [options]
```

### Inspect Status

```bash
# Human-readable table
./automation/bridge/bin/bridge status

# Machine-readable JSON output for agents
./automation/bridge/bin/bridge status --json
```

### Synchronize GitHub Repositories

```bash
# Preview changes without modifying repositories
./automation/bridge/bin/bridge sync github --dry-run

# Execute commit and push for all tracked repositories
./automation/bridge/bin/bridge sync github

# Synchronize one specific repository
./automation/bridge/bin/bridge sync github --repo admin-space

# Output execution result as JSON
./automation/bridge/bin/bridge sync github --json
```

### Safe Fast-Forward Pull (`--ff-only`)

Safely pull updates from remote GitHub repositories without creating merge commits or overwriting uncommitted work:

```bash
# Preview what would be pulled across pull-enabled and tracked repositories
./automation/bridge/bin/bridge sync github --pull --dry-run

# Safe fast-forward pull for all eligible repositories
./automation/bridge/bin/bridge sync github --pull

# Safe pull for one specific repository (e.g. knowledge-space)
./automation/bridge/bin/bridge sync github --pull --repo knowledge-space

# Direct command alias
./automation/bridge/bin/bridge pull --repo knowledge-space
```

Safety rules applied during pull:
- **Clean working tree**: Required. If uncommitted changes exist, pull is blocked.
- **Fast-forward only (`--ff-only`)**: Prevents unwanted merge commits.
- **Diverged branches**: Stops immediately and reports conflict for manual review.
- **No auto-commit**: Local commits are never made prior to pull.

### Synchronize Google Drive Profiles

```bash
# Preview changes without modifying remote targets
./automation/bridge/bin/bridge sync drive --dry-run

# Execute local auto-commit and 1:1 mirror sync
./automation/bridge/bin/bridge sync drive

# Synchronize one specific profile
./automation/bridge/bin/bridge sync drive --profile personal-space-sync

# Check file differences without uploading or deleting
./automation/bridge/bin/bridge sync drive --diff

# Output execution result as JSON
./automation/bridge/bin/bridge sync drive --json
```

### Manage Tracking

```bash
# Enable or disable tracking for a GitHub workspace
./automation/bridge/bin/bridge track github <workspace-id> --enable
./automation/bridge/bin/bridge track github <workspace-id> --disable

# Enable or disable a Google Drive sync profile
./automation/bridge/bin/bridge track drive <profile-id> --enable
./automation/bridge/bin/bridge track drive <profile-id> --disable
```

### Retrieve Public Read-Only Share Link

```bash
./automation/bridge/bin/bridge share drive <profile-id>
```

## Scheduled Automation (macOS LaunchAgent)

The daily runner executes automatically at 04:00 AM local time via macOS `launchd`.

### LaunchAgent Configuration

File location:
`~/Library/LaunchAgents/com.tai.bridge.sync.plist`

Schedule:
`Hour: 1, Minute: 0` daily.

### Manual Service Management

```bash
# Check service registration
launchctl list | grep com.tai.bridge.sync

# Reload service
launchctl unload ~/Library/LaunchAgents/com.tai.bridge.sync.plist
launchctl load ~/Library/LaunchAgents/com.tai.bridge.sync.plist

# Execute runner script manually
./automation/bridge/bin/auto-sync.sh
```

## Web Dashboard

Start the loopback server:

```bash
python3 automation/bridge/backend/server.py 8768
```

Open `http://127.0.0.1:8768/` in the browser.

Features:
- Tabs for `GitHub`, `Drive`, and `Untracked` workspaces.
- Synchronized dual tree view for local directories and remote Google Drive folders (280px height).
- Interactive folder inclusion and exclusion toggles (`Select All • Clear`).
- Real-time Git status inspection and branch switching.

## Verification

Run the test suite before submitting changes:

```bash
cd automation/bridge && PYTHONPATH=bin:backend python3 -m unittest discover -s tests
```

All 23 test cases must exit with code 0 (`OK`).
