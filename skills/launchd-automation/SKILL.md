---
name: launchd-automation
description: Author, scaffold, validate, and manage production-grade macOS launchd background services, LaunchAgents, and scheduled automations with structured workspace directories (scripts/, logs/), dual-contract documentation (README.md runbook for humans, AGENTS.md contract for AI agents), safe PATH injection, launchctl lifecycle management, and dashboard tracking. Use this skill whenever the user mentions setting up a cron job on Mac, creating a launchd or launchagent service, scheduling a recurring script on macOS, running a background daemon, fixing launchctl exit codes (exit 78, exit 127), or organizing and tracking background automations across project workspaces.
compatibility: macOS (darwin)
---

# macOS launchd Automation & Tracking Skill

This skill defines the canonical, production-grade standard for creating, configuring, deploying, debugging, and tracking background automations using macOS `launchd` and `launchctl`.

It enforces **domain isolation** (organizing automations inside their owning workspace instead of dumping files into arbitrary root folders) and **dual-contract documentation** (`README.md` for human runbooks, `AGENTS.md` for AI agent boundaries).

---

## 1. Core Principles & Architecture

Every automation managed under this standard follows a strict 5-part architecture:

```text
<workspace>/automation/<job-name>/          # Or directly inside the service folder (e.g. assets/bridge/)
├── README.md                               # Human Runbook: schedule, manual execution commands, troubleshooting
├── AGENTS.md                               # AI Operating Contract: boundaries, safe commands, verification checklist
├── scripts/                                # Execution scripts
│   ├── run.sh                              # Standard environment wrapper (full PATH, tool shims, locking)
│   └── <task-script>                       # Core business logic (Python, Node, Bash, Go)
├── logs/                                   # Isolated logs directory (strictly gitignored via logs/.gitignore)
│   ├── stdout.log                          # Standard output
│   └── stderr.log                          # Standard error and tracebacks
└── <label>.plist                           # Tracked source property list (mirrored to ~/Library/LaunchAgents/)
```

### The 4 Non-Negotiable Rules
1. **Never Bare Interpreter in Plist:** `launchd` has a stripped default PATH (`/usr/bin:/bin:/usr/sbin:/sbin`). Calling `python3` or `node` directly in `ProgramArguments` will fail with **Exit 127: Command not found**. Always execute through a robust wrapper script (`scripts/run.sh`).
2. **Always Use Modern `launchctl` Syntax:** Use `bootstrap gui/<uid>` and `bootout gui/<uid>`. Never rely on legacy deprecated `load` / `unload`.
3. **Dual Contracts (`README.md` + `AGENTS.md`):** Every automation must have human runbook instructions (`README.md`) and strict agent boundaries (`AGENTS.md`).
4. **Verification Gate Before Signoff:** Never declare a service configured without triggering a test kickstart (`launchctl kickstart -k`) and asserting that the exit code is `0` with clean `logs/stderr.log`.

---

## 2. End-to-End Workflow

Follow these sequential phases when creating or migrating an automation:

### Phase 1: Determine Workspace & Naming
- Identify the owning workspace (e.g. `personal-hub/assets/bridge`, `projects/archive/automation`, `tools/<name>/`).
- Define a reverse-DNS identifier: `com.<owner>.<space>.<job-name>` (e.g., `com.tai.bridge.sync`, `com.tai.notion.export`).

### Phase 2: Scaffold Directory Structure
Use the bundled scaffolding script to generate the complete structure with one command:

```bash
python3 ~/.agents/skills/launchd-automation/scripts/scaffold_automation.py \
    --target-dir "<path/to/automation/directory>" \
    --label "com.tai.<space>.<job-name>" \
    --title "Human Readable Service Title" \
    --description "Concise explanation of what this automation does" \
    --schedule "0 4 * * *" \
    --command "python3 scripts/main.py"
```

*Schedule formats supported:*
- Standard cron: `"0 4 * * *"` (Daily at 04:00 AM)
- Interval: `"interval:3600"` (Every 3600 seconds)
- Run on load: add `--run-at-load`

### Phase 3: Customize Business Logic & Scripts
1. Place business logic inside `scripts/` (e.g., `scripts/main.py` or `scripts/sync.sh`).
2. Ensure `scripts/run.sh` invokes this logic. The wrapper template automatically handles:
   - Exporting `/opt/homebrew/bin`, `/usr/local/bin`, and `~/.local/bin`.
   - Loading `mise`, `pyenv`, or `nvm` if installed.
   - Sourcing local `.env` if present.
   - Preventing overlapping runs via `/tmp/<label>.lock`.
   - Trapping errors and logging ISO-8601 timestamps.
3. Make all scripts executable: `chmod +x scripts/run.sh`.

### Phase 4: Lint Plist Syntax
Always lint the property list before touching launchd:
```bash
plutil -lint "<label>.plist"
```
Must return: `<label>.plist: OK`.

### Phase 5: Deploy & Bootstrap
Copy the plist to the macOS user agents directory and bootstrap into the current GUI user session:
```bash
# 1. Bootout existing instance if currently loaded
launchctl bootout gui/$(id -u)/<label> 2>/dev/null || true

# 2. Copy plist to user LaunchAgents directory
cp "<label>.plist" ~/Library/LaunchAgents/

# 3. Bootstrap into launchd
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/<label>.plist
```

### Phase 6: Automated Verification (Zero Silent Failures)
Run the bundled verification tool to validate files, permissions, launchd status, and trigger a live test:
```bash
python3 ~/.agents/skills/launchd-automation/scripts/verify_automation.py \
    "<path/to/automation/directory>" \
    --kickstart
```

*What the verification checks:*
- [x] All directories (`scripts/`, `logs/`) exist and `logs/.gitignore` is active.
- [x] `README.md` and `AGENTS.md` are present.
- [x] `scripts/run.sh` has executable permissions (`+x`).
- [x] `plutil -lint` passes with zero syntax errors.
- [x] `launchctl list | grep <label>` confirms service registration.
- [x] Kickstart run returns Exit Code `0`.
- [x] `logs/stderr.log` has zero fatal exceptions.

### Phase 7: Register with Automation Tracking Dashboard
If the system uses `assets/track-automation` (or similar dashboard):
1. Verify that `metadata.json` exists in the automation root (generated by scaffolding).
2. Run tracking rescan or update `automations.json` so the job appears in the unified monitoring UI.

---

## 3. Quick Reference Commands

| Action | Command |
| :--- | :--- |
| **Run manually once** | `cd <target-dir> && bash scripts/run.sh` |
| **Check service list** | `launchctl list \| grep "<label>"` |
| **Inspect service detail** | `launchctl print gui/$(id -u)/<label>` |
| **Force kickstart** | `launchctl kickstart -k gui/$(id -u)/<label>` |
| **View live logs** | `tail -f logs/stdout.log logs/stderr.log` |
| **Unload/Stop service** | `launchctl bootout gui/$(id -u)/<label>` |
| **Verify setup** | `python3 ~/.agents/skills/launchd-automation/scripts/verify_automation.py <target-dir>` |

---

## 4. Troubleshooting & Exit Code Matrix

| Exit Code | POSIX Name | Root Cause & Resolution |
| :---: | :--- | :--- |
| `0` | `EX_OK` | Success. Everything operating normally. |
| `78` | `EX_CONFIG` | **Launchd configuration error.** Plist syntax is corrupted, target binary in `ProgramArguments` does not exist, or WorkingDirectory path is invalid. Run `plutil -lint` and inspect paths. |
| `126` | `Permission Denied` | Script is not executable. Run `chmod +x scripts/run.sh`. |
| `127` | `Command Not Found` | A tool called in script is missing from PATH. Check `PATH` in `scripts/run.sh` and ensure Homebrew (`/opt/homebrew/bin`) is included. |
| `1` | `General Failure` | Script logic threw an error. Read `logs/stderr.log` for Python/Node/Shell tracebacks. |
