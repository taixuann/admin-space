#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPORT_ROOT="$SCRIPT_DIR/logs"
PYTHON_BIN="/opt/miniconda3/envs/core/bin/python3"

echo "=== Triggering Update Plugins & Skills manually ==="
"$PYTHON_BIN" "$SCRIPT_DIR/backend/main.py" --report-root "$REPORT_ROOT" "$@"
