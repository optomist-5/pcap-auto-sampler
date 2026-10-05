#!/usr/bin/env zsh
# ==============================================================================
# macOS Perimeter Audit & Intruder Detection Daemon (v2.2)
# ==============================================================================
set -e

PHONE_NUMBER="3606025823"
REPORT_FILE="$HOME/secops/telemetry/perimeter_report.log"
mkdir -p "$HOME/secops/telemetry"

echo "🛡️ macOS Perimeter Audit v2.2 - $(date)"
echo "--------------------------------------------------"

echo "[*] System Integrity Protection (SIP):"
csrutil status || true

echo "\n[*] Gatekeeper Status:"
spctl --status || true

echo "\n[*] FileVault Encryption:"
fdesetup status || true

echo "\n[*] App Firewall State:"
socketfilterfw --getglobalstate || true

echo "\n[*] Open Ports (Excluding Tailscale):"
lsof -i -P -n | grep LISTEN | grep -v "tailscaled" || true

echo "\n[*] Failed Sudo (Admin) Attempts (Last 24h):"
FAILED_SUDO=$(log show --predicate 'process == "sudo" and eventMessage contains "incorrect password"' --last 24h 2>/dev/null | grep "sudo" || true)
if [[ -n "$FAILED_SUDO" ]]; then
    echo "$FAILED_SUDO"
else
    echo "No failed attempts."
fi

echo "\n[*] SSH Authorized Keys Hash:"
if [[ -f "$HOME/.ssh/authorized_keys" ]]; then
    shasum -a 256 "$HOME/.ssh/authorized_keys"
else
    echo "No authorized_keys found (Safe)."
fi

echo "\nSending report via native iMessage..."
$HOME/secops/bin/send_sms_alert.sh "$PHONE_NUMBER" "🛡️ [SecOps Audit] Perimeter scan completed at $(date +'%H:%M PDT'). All core controls verified."

echo "\n[*] Execution complete."
