# Track Automation (`assets/track-automation`)

A lightweight, zero-dependency visual inventory and health monitor for all automated services, LaunchAgents, and Crontab schedules running on macOS.

## Architecture & Components

```
assets/track-automation/
├── index.html            # Standalone visual dashboard (offline-ready, zero CDN dependencies)
├── app.css               # Clean Zen theme with responsive grid, status badges, and modals
├── app.js                # Search, live filters (by category and status), and log inspect drawer
├── scan_automations.py   # Python 3 stdlib auto-discovery scanner
├── automations.json      # Structured registry of all discovered automations
├── automations_data.js   # Offline JS bundle enabling direct file:// double-click opening
├── bin/
│   └── track-automation # Executable CLI wrapper
└── tests/
    └── test_scanner.py   # Comprehensive unit test suite
```

## Discovered Automation Sources

1. **macOS LaunchAgents (`~/Library/LaunchAgents/*.plist`)**:
   - Parses plist XML definitions using standard `plistlib`.
   - Cross-references live runtime state from `launchctl list` (PID, loaded status, last exit codes).
   - Humanizes schedules (`StartCalendarInterval`, `StartInterval`, `RunAtLoad`, `KeepAlive`).
   - Inspects `StandardOutPath` and `StandardErrorPath` logs with file sizes and live tail snippets.

2. **Crontab (`crontab -l`)**:
   - Parses active cron expressions (e.g. `0 9 * * 1`) into human-readable phrases ("Every Mon at 09:00").

3. **Bridge Sync & Workspaces (`assets/bridge`)**:
   - Extracts rich metadata for `com.tai.bridge.sync`: tracked GitHub repositories, safe pull Wiki, Google Drive 1:1 mirror profiles, and last unattended run timestamp.

## Categories

- **Sync & Backup**: Bridge Multi-Repo & Drive Sync, Zotero OakReader Sync, Notion Local Markdown Export, AI Labs Git.
- **LifeOS & Productivity**: Notion Pulse, Tasknotes / Taskwarrior GCal Sync, Daily Briefing.
- **AI & Background Daemons**: Hermes Gateway, Ollama Local Runner, Codex Router, OpenCode News Scrapers, Paperflow GUI.
- **System & Maintenance**: Google Updater, Keystone, Engineering System Maintenance, MySQL.
- **Cron / Custom**: Custom cron jobs and user scripts.

## Usage

### 1. Re-scan Automations via CLI

```bash
# Run scanner and refresh automations.json + automations_data.js
./assets/track-automation/bin/track-automation

# Output formatted JSON directly to stdout
./assets/track-automation/bin/track-automation --json

# Re-scan and immediately open the visual dashboard in your browser
./assets/track-automation/bin/track-automation --open
```

### 2. Open Dashboard in Browser

You can view the dashboard in any browser using either method:
- **Direct Double-Click**: Open [`assets/track-automation/index.html`](file:///Users/tai/personal-hub/assets/track-automation/index.html) directly in Safari / Chrome / Arc (`file://` scheme works completely offline).
- **CLI**: Run `open assets/track-automation/index.html`.

### 3. Run Unit Tests

```bash
python3 -m unittest assets/track-automation/tests/test_scanner.py
```
