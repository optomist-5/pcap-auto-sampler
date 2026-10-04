#!/bin/bash
echo "==================================================="
echo " 🔍 SECOPS RIG & ENVIRONMENT AUDIT (For SBAR) "
echo "==================================================="
echo ""
echo "🛡️  1. EDR / AV STATUS:"
if pgrep -x "wdavdaemon_unprivileged" > /dev/null
then
    echo "   [!] ALERT: Microsoft Defender is running!"
else
    echo "   [CLEAN] No interfering Defender daemons detected."
fi
echo ""
echo "📁 2. STORAGE & VAULT STATUS:"
df -h | grep -E "SecOps_Vault" > /dev/null
if [ $? -eq 0 ]; then
    echo "   [MOUNTED] SecOps_Vault is active."
    ls -ld /Volumes/SecOps_Vault/Virtual_Machines 2>/dev/null >/dev/null && echo "   [VERIFIED] Virtual_Machines directory exists." || echo "   [!] Virtual_Machines directory not yet created."
else
    echo "   [!] SecOps_Vault not currently mounted."
fi
echo ""
echo "🌐 3. ACTIVE LISTENING PORTS (Top 5):"
lsof -i -P -n 2>/dev/null | grep LISTEN | awk '{print "   -", $1, $3, $9}' | head -n 5
echo ""
echo "==================================================="
echo " ✅ AUDIT COMPLETE."
echo "==================================================="
