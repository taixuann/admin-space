# {{SERVICE_TITLE}} (`{{LABEL}}`)

{{SERVICE_DESCRIPTION}}

---

## 1. Quick Info & Schedule

| Property | Value |
| :--- | :--- |
| **Service Label** | `{{LABEL}}` |
| **Schedule** | `{{SCHEDULE_HUMAN_READABLE}}` |
| **Root Directory** | `{{WORKING_DIR}}` |
| **Runner Script** | `{{RUNNER_RELATIVE_PATH}}` |
| **Standard Output Log** | `logs/stdout.log` |
| **Standard Error Log** | `logs/stderr.log` |
| **macOS LaunchAgent** | `~/Library/LaunchAgents/{{LABEL}}.plist` |

---

## 2. Directory Layout

```text
{{DIR_NAME}}/
├── README.md                           # This operational runbook
├── AGENTS.md                           # Operating instructions and safety contracts for AI agents
├── scripts/
│   ├── run.sh                          # Main wrapper script (sets up PATH and handles locks)
│   └── {{MAIN_TASK_FILE}}              # Core logic implementation
├── logs/
│   ├── stdout.log                      # Standard execution output
│   └── stderr.log                      # Error outputs and stack traces
└── {{LABEL}}.plist                     # Original plist version (mirrored to ~/Library/LaunchAgents)
```

---

## 3. Operational Runbook

### Run Manually (Test)
To run the job immediately in the foreground without waiting for the scheduled time:
```bash
cd "{{WORKING_DIR}}"
bash scripts/run.sh
```

### Check Service Status in launchd
Check if the service is loaded and see its PID / last exit status:
```bash
launchctl list | grep "{{LABEL}}"
```

### Inspect Detailed launchd Properties
Inspect state, scheduling, environment, and error conditions:
```bash
launchctl print gui/$(id -u)/{{LABEL}}
```

### Trigger Immediate Execution via launchctl
Force `launchd` to kick off the service right now:
```bash
launchctl kickstart -k gui/$(id -u)/{{LABEL}}
```

### View Live Logs
Stream execution logs and errors:
```bash
# Follow both output and errors
tail -f logs/stdout.log logs/stderr.log
```

### Reload / Apply Changes
After editing the `.plist` file:
```bash
# Unload existing job
launchctl bootout gui/$(id -u)/{{LABEL}} 2>/dev/null || true

# Copy latest plist to LaunchAgents
cp "{{LABEL}}.plist" ~/Library/LaunchAgents/

# Bootstrap the updated job
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/{{LABEL}}.plist
```

### Uninstall / Disable Service
To stop and permanently remove the scheduled service:
```bash
launchctl bootout gui/$(id -u)/{{LABEL}} 2>/dev/null || true
rm -f ~/Library/LaunchAgents/{{LABEL}}.plist
```

---

## 4. Troubleshooting & Exit Codes

| Exit Code | Meaning | Remediation |
| :--- | :--- | :--- |
| `0` | Success | Normal operation. |
| `78` | Configuration / Permission Error | `launchd` could not read the plist or execute the runner. Check file permissions (`chmod +x scripts/run.sh`). |
| `127` | Command Not Found | A required binary is not in PATH. Check `PATH` in `scripts/run.sh` and plist `EnvironmentVariables`. |
| `1` | Task Execution Failure | Check `logs/stderr.log` for Python/Node/Shell tracebacks. |
