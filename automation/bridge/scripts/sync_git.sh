#!/usr/bin/env bash
# Bridge - Run git synchronization across workspaces (wrapper for bridge sync github)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BRIDGE_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

exec "${BRIDGE_DIR}/bin/bridge" sync github "$@"
