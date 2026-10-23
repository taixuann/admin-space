# Operating Contract for AI Agents: {{SERVICE_TITLE}} (`{{LABEL}}`)

This contract defines strict rules, boundaries, and operational procedures for any AI agent interacting with this automation service.

---

## 1. Scope & Invariants

1. **Local Authority:** This directory (`{{WORKING_DIR}}`) owns the execution logic and documentation for `{{LABEL}}`. Do not touch unrelated files or parent projects without explicit scope authorization.
2. **Never Edit LaunchAgents Directly:** Always modify the source plist `{{LABEL}}.plist` inside this directory first. Never make out-of-sync edits directly in `~/Library/LaunchAgents/`.
3. **Plutil Lint Required:** Before deploying any `.plist` file, run `plutil -lint {{LABEL}}.plist`. Never attempt to bootstrap a plist with invalid syntax or unresolved XML tags.
4. **Bootout Before Bootstrap:** When updating a service in `launchd`, always bootout the existing job before bootstrapping the new plist:
   ```bash
   launchctl bootout gui/$(id -u)/{{LABEL}} 2>/dev/null || true
   launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/{{LABEL}}.plist
   ```
5. **No Blind Completion:** After modifying scripts or the plist, ALWAYS trigger a test run via `launchctl kickstart -k gui/$(id -u)/{{LABEL}}` or execute `bash scripts/run.sh`. Inspect `logs/stderr.log` and verify the exit code is `0`.
6. **Documentation Sync:** Any change to schedule, environment, or command MUST be reflected synchronously in both `README.md` and `AGENTS.md`.

---

## 2. Directory Layout & Boundaries

```text
{{DIR_NAME}}/
├── README.md               # User-facing runbook (human manual commands)
├── AGENTS.md               # THIS CONTRACT (agent instructions)
├── scripts/
│   ├── run.sh              # Environment wrapper (MUST maintain PATH & locking)
│   └── {{MAIN_TASK_FILE}}  # Main logic
├── logs/                   # Log directory (MUST be gitignored)
└── {{LABEL}}.plist         # Tracked plist source
```

---

## 3. Safe Verification Checklist for Agents

Before reporting any task related to this service as complete:
- [ ] `plutil -lint {{LABEL}}.plist` returns OK.
- [ ] `scripts/run.sh` has executable permissions (`chmod +x scripts/run.sh`).
- [ ] Test execution completed without throwing error codes (`echo $?` is 0).
- [ ] `logs/stderr.log` contains no fatal errors or unhandled tracebacks.
- [ ] `launchctl list | grep "{{LABEL}}"` confirms the service is registered with exit code 0.
- [ ] `README.md` reflects current configuration.
