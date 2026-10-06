#!/usr/bin/env bash
# ==============================================================================
# SEC-OPS "RADIO" PEER-TO-PEER ALERT DISPATCHER
# Target: Workstation secopslt (~/secops)
# ==============================================================================

RECIPIENT="$1"
MESSAGE="$2"

MY_DEFAULT_ID="mquija9@icloud.com"

# If no recipient specified, default to primary user context
if [ -z "$RECIPIENT" ]; then
    echo "======================================================================"
    echo "                 SEC-OPS RADIO DISPATCH UTILITY                       "
    echo "======================================================================"
    echo " Usage:"
    echo "   radio <phone_number_or_email> \"<message>\""
    echo " Example:"
    echo "   radio 3605551234 \"Radio check over Tailscale mesh.\""
    echo "======================================================================"
    exit 1
fi

# Default fallback if no message passed
if [ -z "$MESSAGE" ]; then
    MESSAGE="Routine radio check signal from secopslt."
fi

FULL_PAYLOAD="📻 [Radio Dispatch]: $MESSAGE"
echo "[+] Transmitting payload to $RECIPIENT..."

osascript << APPLESCRIPT 2>/dev/null
tell application "Messages"
    set targetService to 1st service whose service type is iMessage
    set targetBuddy to buddy "$RECIPIENT" of targetService
    send "$FULL_PAYLOAD" to targetBuddy
end tell
APPLESCRIPT

if [ $? -eq 0 ]; then
    echo "✅ Radio transmission successfully sent to $RECIPIENT."
else
    echo "⚠️ Messages daemon dispatch attempted for $RECIPIENT."
fi
