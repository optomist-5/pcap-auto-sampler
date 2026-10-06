#!/usr/bin/env bash
# macOS Native iMessage / SMS Alert Dispatcher

MESSAGE="$1"
if [ -z "$MESSAGE" ]; then
    MESSAGE="🛡️ [SecOps Telemetry] Default health check heartbeat from secopslt."
fi

# Target phone number or Apple ID associated with iMessage
# Resolves to primary user context or local device
TARGET_BUDDY="mquija9@icloud.com"

echo "[+] Dispatching alert via macOS Messages daemon..."

osascript << APPLESCRIPT 2>/dev/null
tell application "Messages"
    set targetService to 1st service whose service type is iMessage
    set targetBuddy to buddy "$TARGET_BUDDY" of targetService
    send "$MESSAGE" to targetBuddy
end tell
APPLESCRIPT

if [ $? -eq 0 ]; then
    echo "✅ Alert successfully dispatched to $TARGET_BUDDY."
else
    echo "⚠️ Messages daemon dispatch attempted."
fi
