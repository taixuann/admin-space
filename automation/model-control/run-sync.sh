#!/bin/bash
# run-sync.sh — Automated wrapper calling installed CLI package
set -euo pipefail
export PATH="/Users/tai/.local/bin:$PATH"
exec "/Users/tai/.local/bin/opencode-model-router" --sync --space all "$@"
