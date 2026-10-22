#!/bin/bash
# run-sync.sh — Automated background runner for model-control & pqa index sync
set -euo pipefail

export PATH="/opt/miniconda3/envs/core/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/Users/tai/.local/bin:$PATH"

LOG_DIR="/Users/tai/.agents/automation/model-control/logs"
mkdir -p "$LOG_DIR"

echo "=== [$(date '+%Y-%m-%d %H:%M:%S')] Starting automated model-control sync ==="

# 1. Refresh today's tool catalog and apply a verified OpenCode default.
/opt/homebrew/bin/python3 /Users/tai/.agents/tools/opencode-free-router/backend/model_sync.py

/bin/bash /Users/tai/.agents/tools/opencode-free-router/model-control/index-if-needed.sh

echo "=== [$(date '+%Y-%m-%d %H:%M:%S')] Automated sync finished successfully ==="
