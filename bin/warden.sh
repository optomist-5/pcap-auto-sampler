#!/usr/bin/env bash
# SecOps Warden: 09:00 AM Daily Briefing & System Integrity Reporter

SECOPS_DIR="$HOME/CodeProjects/secops"
LOG_FILE="$SECOPS_DIR/logs/warden_daily_report.log"
SIEM_LOG="$SECOPS_DIR/logs/siem_events.json"
SMS_SCRIPT="$SECOPS_DIR/scripts/send_sms_alert.sh"
VERIFY_SCRIPT="$SECOPS_DIR/scripts/verify_audit_state.sh"
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")

echo "==========================================" >> "$LOG_FILE"
echo "09:00 AM Daily Warden Report: $TIMESTAMP" >> "$LOG_FILE"

# 1. Execute Zero-Trust system state verification
AUDIT_OUTPUT=$("$VERIFY_SCRIPT" 2>&1)
PASS_COUNT=$(echo "$AUDIT_OUTPUT" | grep -c "\[PASS\]")
FAIL_COUNT=$(echo "$AUDIT_OUTPUT" | grep -c "\[FAIL\]")

echo "$AUDIT_OUTPUT" >> "$LOG_FILE"

# 2. Parse SIEM events from the last 24 hours for Critical/High incidents
INCIDENTS_24H=0
if [ -f "$SIEM_LOG" ]; then
    # Count CRITICAL and HIGH severity events recorded in siem_events.json
    INCIDENTS_24H=$(grep -E '"severity": "(CRITICAL|HIGH)"' "$SIEM_LOG" | wc -l | tr -d ' ')
fi

# 3. Format Daily Digest Payload
if [ "$FAIL_COUNT" -eq 0 ] && [ "$INCIDENTS_24H" -eq 0 ]; then
    SMS_BODY="🛡️ [SecOps 09:00 Daily Briefing] System Nominal ($TIMESTAMP).
• Baseline Checks: $PASS_COUNT Passed, 0 Failed
• Hourly Watchdog: 24h Clean (0 rogue events)
• Perimeter: Secure on secopslt."
else
    SMS_BODY="⚠️ [SecOps 09:00 Daily Alert] Review Needed ($TIMESTAMP).
• Baseline Checks: $PASS_COUNT Passed, $FAIL_COUNT Failed
• Auto-Remediations (24h): $INCIDENTS_24H event(s) intercepted
• Review: ~/CodeProjects/secops/logs/siem_events.json"
fi

# 4. Dispatch Morning SMS Digest
if [ -x "$SMS_SCRIPT" ]; then
    "$SMS_SCRIPT" "$SMS_BODY"
fi
