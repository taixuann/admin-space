#!/bin/bash
set -euo pipefail

LABEL="com.tai.update-plugins-mcp-skills"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPORT_ROOT="$SCRIPT_DIR/logs"
RESULT_FILE="$REPORT_ROOT/latest-result.json"

echo "=== Status for $LABEL ==="

if launchctl print "gui/$(id -u)/$LABEL" >/dev/null 2>&1; then
    echo "✓ launchd state: LOADED & ACTIVE"
else
    echo "⚠ launchd state: NOT LOADED in launchd"
fi

if [ -f "$RESULT_FILE" ]; then
    echo "--- Latest Result: $RESULT_FILE ---"
    cat "$RESULT_FILE"
else
    echo "No latest-result.json found yet at $RESULT_FILE"
fi

if [ -f "$REPORT_ROOT/stdout.log" ]; then
    echo -e "\n--- Last 10 lines of stdout.log ---"
    tail -n 10 "$REPORT_ROOT/stdout.log"
fi

if [ -f "$REPORT_ROOT/stderr.log" ]; then
    echo -e "\n--- Last 10 lines of stderr.log ---"
    tail -n 10 "$REPORT_ROOT/stderr.log"
fi
