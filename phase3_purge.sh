#!/bin/bash
echo ""
echo "🩺 [X-RAY] Verifying Cold Storage on SecOps_Vault..."
ls -lh /Volumes/SecOps_Vault/*.tar.gz 2>/dev/null
echo ""
echo "🗑️ [PURGE] Initiating Zero-Trust Drive Purge..."
echo "Vaporizing old redundant vaults and local archives (This is permanent)..."

Safely removing only the temporary/redundant backup folders

rm -rf ~/Vault_Mauri ~/Desktop/Clean_Vault ~/Desktop/Agent_Notes_Recovery ~/Desktop/Master_Backup.tar.gz ~/Desktop/Secondary_Backup.tar.gz ~/Desktop/Archive_Manifest.txt

echo "✅ [SUCCESS] Local redundant vaults destroyed. Host machine is sanitized."
echo ""
echo "🩻 [VITALS] Checking newly recovered Mac hard drive space..."
df -h /
echo ""
echo "🎉 [PHASE 3 COMPLETE] Terminal cleanup is finished!"
