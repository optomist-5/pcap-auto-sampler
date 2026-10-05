#!/usr/bin/env zsh
# ==============================================================================
# Native Apple iMessage / SMS Dispatcher for SecOps Intrusion Alerts
# ==============================================================================

RAW_PHONE="${1:-"3606025823"}"
CLEAN_PHONE=$(echo "$RAW_PHONE" | tr -cd '0-9')

if [[ ${#CLEAN_PHONE} -eq 10 ]]; then
    TARGET_PHONE="+1${CLEAN_PHONE}"
else
    TARGET_PHONE="+${CLEAN_PHONE}"
fi

ALERT_MSG="${2:-"⚠️ [SecOps Alert] Perimeter anomaly detected on local host."}"

osascript - "$TARGET_PHONE" "$ALERT_MSG" << 'APPLESCRIPT'
on run {targetRecipient, messageText}
    tell application "Messages"
        send messageText to buddy targetRecipient
    end tell
end run
APPLESCRIPT
