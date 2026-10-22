# macOS launchd Best Practices & Reference Manual

A comprehensive engineering guide for authoring, debugging, and maintaining background daemons and user agents on macOS.

---

## 1. Domains: Where Services Run

macOS `launchd` manages services across distinct domains:

| Domain Target | Typical Path | Context & Permissions | Use Case |
| :--- | :--- | :--- | :--- |
| **User Agent** (`gui/<uid>`) | `~/Library/LaunchAgents/` | Runs as logged-in GUI user. Has access to user files, keychain, display server. | **Default for 99% of user automations** (sync, scripts, backups). |
| **System Agent** | `/Library/LaunchAgents/` | Runs per user on login, configured globally by admin. | Multi-user workstation software. |
| **System Daemon** (`system`) | `/Library/LaunchDaemons/` | Runs as `root` even when no user is logged in. No GUI access. | Hardware monitors, network proxies, low-level servers. |

> **Always use User Agents (`gui/$(id -u)`)** for personal tasks, repositories, and data sync. Never install user automation into `LaunchDaemons`.

---

## 2. Modern `launchctl` vs Legacy Commands

Apple deprecated `load` / `unload` in macOS 10.11+. Modern tooling uses domain targets:

### The Modern Way (Recommended):
```bash
# Bootstrap (load and enable service in user GUI session):
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.example.service.plist

# Bootout (unload and stop service):
launchctl bootout gui/$(id -u)/com.example.service

# Kickstart (force immediate execution / restart):
launchctl kickstart -k gui/$(id -u)/com.example.service

# Inspect live status, environment, and error states:
launchctl print gui/$(id -u)/com.example.service
```

### The Legacy Fallback:
```bash
launchctl load -w ~/Library/LaunchAgents/com.example.service.plist
launchctl unload -w ~/Library/LaunchAgents/com.example.service.plist
launchctl list | grep com.example
```

---

## 3. The 3 Deadly Traps of macOS `launchd`

### Trap 1: Minimal Default PATH (Exit 127)
`launchd` runs in a stripped sandbox where `PATH` is only `/usr/bin:/bin:/usr/sbin:/sbin`.
- Tools installed via Homebrew (`/opt/homebrew/bin` on Apple Silicon, `/usr/local/bin` on Intel) or managers (`pyenv`, `mise`, `nvm`, `cargo`) will **fail with Exit 127: Command not found**.
- **Fix:** 
  1. Define `<key>EnvironmentVariables</key>` with explicit `PATH` in the `.plist`.
  2. Use a wrapper script (`scripts/run.sh`) that explicitly exports the full PATH and sources tool shims.

### Trap 2: Working Directory Pitfall
If `WorkingDirectory` is omitted, the process runs in `/`. Any relative file access (e.g., `open('data.json')` or `./scripts/task.sh`) will fail or attempt to write to the read-only root volume.
- **Fix:** Always set `<key>WorkingDirectory</key>` to the absolute path of the automation directory.

### Trap 3: Silent Failure & Stale Exit Codes
`launchctl list` only reports the last exit code, and launchd will not log to the system console by default. If `StandardOutPath` and `StandardErrorPath` are not specified, stderr disappears into `/dev/null`.
- **Fix:** Always specify explicit log paths in a `logs/` subdirectory and inspect them after bootstrapping.

---

## 4. Exit Code Diagnostics

| Code | POSIX Name | Root Cause & Diagnostic |
| :--- | :--- | :--- |
| `0` | `EX_OK` | Successful termination. |
| `1` | General Error | Script or application threw an uncaught error. Check `logs/stderr.log`. |
| `78` | `EX_CONFIG` | Launchd configuration failure. Usually: plist syntax invalid, permissions issue, or `ProgramArguments` target does not exist. |
| `126` | Permission Denied | Runner script is not marked executable. Fix with `chmod +x scripts/run.sh`. |
| `127` | Command Not Found | A binary called inside the script is missing from PATH. |

---

## 5. Scheduling Primitives

### Option A: Calendar-based (`StartCalendarInterval`)
Run at specific times of day, day of week, or day of month:
```xml
<!-- Daily at 04:00 AM -->
<key>StartCalendarInterval</key>
<dict>
    <key>Hour</key>
    <integer>4</integer>
    <key>Minute</key>
    <integer>0</integer>
</dict>
```

### Option B: Interval-based (`StartInterval`)
Run periodically every $N$ seconds:
```xml
<!-- Every 1 hour (3600 seconds) -->
<key>StartInterval</key>
<integer>3600</integer>
```

### Option C: Run At Load
Run once as soon as the service is registered with `launchctl bootstrap`:
```xml
<key>RunAtLoad</key>
<true/>
```
