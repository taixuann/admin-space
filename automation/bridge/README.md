# Bridge

Bridge manages multi-repository Git synchronization and Google Drive 1:1 cloud backup across local workspaces.

## Directory Layout

```
assets/bridge/
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
| `research-projects` | `~/research-projects` | `taixuann/research-projects` | `main` | Yes | Scientific research projects |
| `agent-skills` | `~/.agents` | `taixuann/agent-skills` | `master` | Yes | Agent skills library |
| `agent-development` | `~/agent-development` | `taixuann/agent-development` | `master` | Yes | Agent development sandbox |
| `raw-viewer` | `~/research-projects/tools/raw-viewer` | `taixuann/raw-viewer` | `master` | Yes | Scientific data viewer tool |
| `academic-portfolio` | `~/personal-hub/professional/portfolio/site` | `taixuann/academic-portfolio` | `main` | Yes | Academic and personal portfolio website |
| `personal-hub` | `~/personal-hub` | `taixuann/non-research-projects` | `main` | No | No | Personal LifeOS (local Git only) |
| `learn-wiki` | `~/learn` | `taixuann/wiki` | `main` | No | Yes | Digital garden knowledge base (pull-only) |

### 2. Google Drive Cloud Profiles (`config/drive-track.yaml`)

| Profile ID | Source Directory | Remote Target | Auto-Commit | Excluded Patterns |
| :--- | :--- | :--- | :---: | :--- |
| `personal-hub-sync` | `~/personal-hub` | `gdrive:personal-hub/` | Yes | `.git`, `.venv`, `.pytest_cache`, `.DS_Store`, `node_modules`, `.obsidian/workspace*` |
| `research-projects-sync` | `~/research-projects` | `gdrive:research/projects/` | Yes | `.git`, `.venv`, `venv`, `.build`, `.pytest_cache`, `.ruff_cache`, `.DS_Store`, `__pycache__`, `node_modules`, `worktree`, `worktrees` |
| `learn-sync` | `~/learn` | `gdrive:learn/` | Yes | `.git`, `.venv`, `.pytest_cache`, `.DS_Store`, `node_modules`, `.obsidian/workspace*` |
| `knowledge-base-sync` | `~/knowledge-base` | `gdrive:knowledge-base/` | No | `.git`, `.venv`, `.pytest_cache`, `.DS_Store`, `node_modules`, `.obsidian/workspace*` |

## Operational Rules

1. Only commit and push repositories where `tracked: true` in `config/github-track.yaml`.
2. Do not push un-tracked repositories (`personal-hub`, `learn-wiki`) to remote GitHub origins.
3. Use the exact commit message format for automated commits:
   `automation: YYYY-MM-DD commit automatically`
4. If a local repository has uncommitted changes before Google Drive synchronization, commit changes locally before running `rclone sync`.
5. Execute Google Drive synchronization as a 1:1 mirror using `rclone sync`. Files removed locally must be removed on remote targets.
6. Share links generated for Google Drive targets must remain public read-only (`reader` role).

## CLI Reference

Run the executable CLI wrapper:

```bash
./assets/bridge/bin/bridge <command> [options]
```

### Inspect Status

```bash
# Human-readable table
./assets/bridge/bin/bridge status

# Machine-readable JSON output for agents
./assets/bridge/bin/bridge status --json
```

### Synchronize GitHub Repositories

```bash
# Preview changes without modifying repositories
./assets/bridge/bin/bridge sync github --dry-run

# Execute commit and push for all tracked repositories
./assets/bridge/bin/bridge sync github

# Synchronize one specific repository
./assets/bridge/bin/bridge sync github --repo agent-skills

# Output execution result as JSON
./assets/bridge/bin/bridge sync github --json
```

### Safe Fast-Forward Pull (`--ff-only`)

Safely pull updates from remote GitHub repositories without creating merge commits or overwriting uncommitted work:

```bash
# Preview what would be pulled across pull-enabled and tracked repositories
./assets/bridge/bin/bridge sync github --pull --dry-run

# Safe fast-forward pull for all eligible repositories
./assets/bridge/bin/bridge sync github --pull

# Safe pull for one specific repository (e.g. learn-wiki)
./assets/bridge/bin/bridge sync github --pull --repo learn-wiki

# Direct command alias
./assets/bridge/bin/bridge pull --repo learn-wiki
```

Safety rules applied during pull:
- **Clean working tree**: Required. If uncommitted changes exist, pull is blocked.
- **Fast-forward only (`--ff-only`)**: Prevents unwanted merge commits.
- **Diverged branches**: Stops immediately and reports conflict for manual review.
- **No auto-commit**: Local commits are never made prior to pull.

### Synchronize Google Drive Profiles

```bash
# Preview changes without modifying remote targets
./assets/bridge/bin/bridge sync drive --dry-run

# Execute local auto-commit and 1:1 mirror sync
./assets/bridge/bin/bridge sync drive

# Synchronize one specific profile
./assets/bridge/bin/bridge sync drive --profile personal-hub-sync

# Check file differences without uploading or deleting
./assets/bridge/bin/bridge sync drive --diff

# Output execution result as JSON
./assets/bridge/bin/bridge sync drive --json
```

### Manage Tracking

```bash
# Enable or disable tracking for a GitHub workspace
./assets/bridge/bin/bridge track github <workspace-id> --enable
./assets/bridge/bin/bridge track github <workspace-id> --disable

# Enable or disable a Google Drive sync profile
./assets/bridge/bin/bridge track drive <profile-id> --enable
./assets/bridge/bin/bridge track drive <profile-id> --disable
```

### Retrieve Public Read-Only Share Link

```bash
./assets/bridge/bin/bridge share drive <profile-id>
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
./assets/bridge/bin/auto-sync.sh
```

## Web Dashboard

Start the loopback server:

```bash
python3 assets/bridge/backend/server.py 8768
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
python3 -m unittest discover -s assets/bridge/tests
```

All 20 test cases must exit with code 0 (`OK`).
