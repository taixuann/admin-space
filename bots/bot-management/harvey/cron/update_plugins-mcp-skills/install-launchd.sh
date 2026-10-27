#!/bin/bash
set -euo pipefail

LABEL="com.tai.update-plugins-mcp-skills"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLIST_SRC="$SCRIPT_DIR/launchd.plist"
PLIST_DST="$HOME/Library/LaunchAgents/$LABEL.plist"

echo "=== Installing $LABEL ==="

# Check source
if [ ! -f "$PLIST_SRC" ]; then
    echo "Error: Source plist not found at $PLIST_SRC" >&2
    exit 1
fi

# Bootout if already loaded
if launchctl print "gui/$(id -u)/$LABEL" >/dev/null 2>&1; then
    echo "Booting out existing instance..."
    launchctl bootout "gui/$(id -u)/$LABEL" || true
fi

# Copy plist
echo "Copying plist to $PLIST_DST..."
cp "$PLIST_SRC" "$PLIST_DST"

# Bootstrap
echo "Bootstrapping service..."
launchctl bootstrap "gui/$(id -u)" "$PLIST_DST"

echo "✓ Successfully deployed and bootstrapped $LABEL"
