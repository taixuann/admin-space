#!/bin/bash
set -euo pipefail

LABEL="com.tai.update-plugins-mcp-skills"
PLIST_DST="$HOME/Library/LaunchAgents/$LABEL.plist"

echo "=== Uninstalling $LABEL ==="

if launchctl print "gui/$(id -u)/$LABEL" >/dev/null 2>&1; then
    echo "Booting out $LABEL..."
    launchctl bootout "gui/$(id -u)/$LABEL" || true
fi

if [ -f "$PLIST_DST" ]; then
    echo "Removing $PLIST_DST..."
    rm -f "$PLIST_DST"
fi

echo "✓ Successfully uninstalled $LABEL"
