#!/usr/bin/env bash
# Silent Hourly Background Audit Daemon

LOG_FILE="$HOME/secops/logs/perimeter_daemon.log"
ERR_FILE="$HOME/secops/logs/perimeter_daemon_err.log"
mkdir -p "$HOME/secops/logs"

# Execute verification silently
SUMMARY=$(python3 $HOME/secops/secops_sentinel.py 2>> "$ERR_FILE")
EXIT_CODE=$?

TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")

if [ $EXIT_CODE -ne 0 ]; then
    # FAILURE DETECTED: Send high-priority alert text immediately
    ALERT_MSG="🚨 [SecOps Alert] Perimeter audit FAILED at $TIMESTAMP. Check $ERR_FILE"
    echo "[$TIMESTAMP] FAIL: Sending iMessage alert." >> "$LOG_FILE"
    $HOME/secops/scripts/send_sms_alert.sh "$ALERT_MSG" 2>/dev/null
else
    # SUCCESS: Log silently without sending SMS
    echo "[$TIMESTAMP] PASS: All controls verified cleanly (Silent Run)." >> "$LOG_FILE"
fi
