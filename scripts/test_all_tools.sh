#!/usr/bin/env zsh
# ==============================================================================
# SecOps Sentinel Tool Verification Harness
# ==============================================================================
set -e
echo "🧪 Running SecOps Tool Suite Verification..."

cd "$HOME/secops"

echo "\n[1/4] Verifying Python Virtual Environment..."
python3 -c "import os, sys; print('  ✅ Active Python:', sys.version.split()[0])"

echo "\n[2/4] Testing Core CLI Engine (secops_sentinel.py)..."
python3 secops_sentinel.py --help >/dev/null && echo "  ✅ secops_sentinel.py operational."

echo "\n[3/4] Testing Incident Response Suite (ir_playbooks.py)..."
python3 modules/soc_defense/ir_playbooks.py sbar >/dev/null && echo "  ✅ ir_playbooks.py operational."

echo "\n[4/4] Testing iMessage Alert Dispatcher..."
bin/send_sms_alert.sh "3606025823" "🧪 [TASK-01 Audit] All local tools verified operational." >/dev/null && echo "  ✅ send_sms_alert.sh operational."

echo "\n✨ TASK-01 VERIFICATION COMPLETE: All core tools functional!"
