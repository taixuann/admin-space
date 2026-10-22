#!/usr/bin/env bash
# Bridge - Launch local server and open in browser

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BRIDGE_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
PORT="${1:-8768}"

echo "Starting Bridge Dashboard on port ${PORT}..."
# Open in browser on macOS
(sleep 1 && open "http://127.0.0.1:${PORT}/") &

python3 "${BRIDGE_DIR}/backend/server.py" "${PORT}"
