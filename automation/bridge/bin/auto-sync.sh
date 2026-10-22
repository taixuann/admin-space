#!/usr/bin/env bash
# ==============================================================================
# Bridge Daily Automation Sync Script
# Runs unattended via macOS LaunchAgent at 04:00 AM daily or manually via CLI.
# Fault-Tolerant & Network Resilient:
#   - Process lock protection against overlapping runs with stale-lock recovery
#   - Automatic network connectivity polling on wake (up to 60s)
#   - Automatic local git commit even if offline
#   - Robust retries for GitHub push and Google Drive rclone sync
# ==============================================================================
set -euo pipefail

# Ensure robust PATH for miniconda, homebrew, system binaries, and user tools
export PATH="/opt/miniconda3/envs/core/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:${HOME}/.local/bin:${PATH}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BRIDGE_BIN="${SCRIPT_DIR}/bridge"
LOG_DIR="$(dirname "${SCRIPT_DIR}")/logs"
mkdir -p "${LOG_DIR}"

# 1. Process Concurrency & Interruption Lock
LOCK_FILE="/tmp/bridge_sync.lock"
if [ -f "${LOCK_FILE}" ]; then
    OLD_PID=$(cat "${LOCK_FILE}" 2>/dev/null || true)
    if [ -n "${OLD_PID}" ] && kill -0 "${OLD_PID}" 2>/dev/null; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] Bridge sync is already running with PID ${OLD_PID}. Exiting safely."
        exit 0
    else
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] Stale lockfile detected from dead PID ${OLD_PID}. Cleaning up."
        rm -f "${LOCK_FILE}"
    fi
fi

echo "$$" > "${LOCK_FILE}"
cleanup() {
    rm -f "${LOCK_FILE}"
}
trap cleanup EXIT INT TERM

TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
echo "======================================================================"
echo "[${TIMESTAMP}] Starting Bridge Daily Unattended Automation"
echo "======================================================================"

# 2. Network Connectivity Pre-flight Polling
wait_for_network() {
    local max_retries=12
    local count=0
    echo "Checking internet connectivity..."
    while ! curl -s --connect-timeout 4 --head https://www.google.com >/dev/null 2>&1 && \
          ! curl -s --connect-timeout 4 --head https://github.com >/dev/null 2>&1; do
        count=$((count + 1))
        if [ "$count" -ge "$max_retries" ]; then
            echo "Warning: Internet connection unavailable after 60s. Proceeding in offline-tolerant mode." >&2
            return 1
        fi
        echo "Network unavailable or machine waking up. Retrying in 5s (${count}/${max_retries})..."
        sleep 5
    done
    echo "Internet connectivity verified."
    return 0
}

wait_for_network || true

# 3. Safe Fast-Forward Pull for Wiki / Ingestion Updates
echo ""
echo ">>> [1/3] Safe Pulling Wiki / Pull-Enabled Repositories (--ff-only)..."
if "${BRIDGE_BIN}" sync github --pull "$@"; then
    echo ">>> Safe pull completed cleanly."
else
    echo ">>> Safe pull notice / check required (check logs/github-sync.log)." >&2
fi

# 4. Sync Tracked GitHub Repositories (Commit & Push)
echo ""
echo ">>> [2/3] Synchronizing Tracked GitHub Repositories..."
if "${BRIDGE_BIN}" sync github "$@"; then
    echo ">>> GitHub sync completed successfully."
else
    echo ">>> GitHub sync encountered warnings or errors (check logs/github-sync.log)." >&2
fi

# 5. Sync Google Drive 1:1 Cloud Profiles
echo ""
echo ">>> [3/3] Synchronizing Google Drive 1:1 Cloud Profiles..."
if "${BRIDGE_BIN}" sync drive "$@"; then
    echo ">>> Google Drive sync completed successfully."
else
    echo ">>> Google Drive sync encountered warnings or errors (check logs/drive-sync.log)." >&2
fi

END_TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
echo ""
echo "======================================================================"
echo "[${END_TIMESTAMP}] Bridge Daily Unattended Automation Finished"
echo "======================================================================"
