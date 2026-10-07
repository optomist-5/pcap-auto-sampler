#!/usr/bin/env bash
# SecOps Cold Storage Lifecycle & Annual Rollover Engine

VAULT="$HOME/CodeProjects/ColdStorage_Vault"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
YEAR=$(date +%Y)

echo "=== 📂 SecOps Cold Storage & Lifecycle Manager [$TIMESTAMP] ==="

# 1. Ensure Segmented Directory Structure Exists
mkdir -p "$VAULT/01_pcaps_network" "$VAULT/02_siem_telemetry" "$VAULT/03_process_forensics" "$VAULT/04_grc_audit_reports" "$VAULT/05_version_snapshots" "$VAULT/06_annual_archives"

# 2. Sort & Route Active Telemetry Dumps into Segmented Vault Folders
cp $HOME/CodeProjects/secops/logs/siem_events.json "$VAULT/02_siem_telemetry/siem_events_$TIMESTAMP.json" 2>/dev/null
cp $HOME/CodeProjects/secops/logs/*.log "$VAULT/04_grc_audit_reports/" 2>/dev/null

# 3. Compress Files into Annual Rollup Archive
ARCHIVE_TAR="$VAULT/06_annual_archives/secops_annual_$YEAR.tar.gz"
tar -czf "$ARCHIVE_TAR" -C "$VAULT" 01_pcaps_network 02_siem_telemetry 03_process_forensics 04_grc_audit_reports 05_version_snapshots 2>/dev/null

echo "✅ Telemetry sorted into segmented vault folders."
echo "✅ Annual rollup archive updated: $ARCHIVE_TAR"
echo "   Archive Size: $(du -h "$ARCHIVE_TAR" 2>/dev/null | cut -f1)"
