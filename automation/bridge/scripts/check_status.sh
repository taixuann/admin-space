#!/usr/bin/env bash
# Bridge - Fast CLI status checker (wrapper for bridge status)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BRIDGE_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

exec "${BRIDGE_DIR}/bin/bridge" status "$@"
