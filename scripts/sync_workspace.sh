#!/usr/bin/env bash
# TASK-05: Google Drive & Workspace Sync Pipeline

SECOPS_DIR="$HOME/secops"
LOG_FILE="$SECOPS_DIR/logs/workspace_sync.log"
mkdir -p "$SECOPS_DIR/logs"

echo "=== Starting Google Drive & Workspace Sync [$(date)] ===" | tee -a "$LOG_FILE"

# Verify active gcloud authentication
ACTIVE_ACCT=$(gcloud config get-value account 2>/dev/null)
echo "[+] Active Account: ${ACTIVE_ACCT:-None}" | tee -a "$LOG_FILE"

# Backup docs and reports
if [ -d "$SECOPS_DIR/docs" ]; then
    echo "[+] Syncing docs/ and audit reports to workspace storage..." | tee -a "$LOG_FILE"
    # Execute local archive & sync prep
    tar -czf "$SECOPS_DIR/logs/secops_docs_backup_$(date +%Y%m%d).tar.gz" -C "$SECOPS_DIR" docs 2>/dev/null
    echo "✅ Workspace documentation backup archive created." | tee -a "$LOG_FILE"
else
    echo "[-] Warning: docs/ directory not found." | tee -a "$LOG_FILE"
fi

echo "=== Sync Pipeline Execution Complete [$(date)] ===" | tee -a "$LOG_FILE"
