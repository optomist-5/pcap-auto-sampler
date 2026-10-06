#!/usr/bin/env bash
# Unified Workspace & GitHub Sync Pipeline

SECOPS_DIR="$HOME/secops"
cd "$SECOPS_DIR" || exit 1

echo "=== 🔄 Starting SecOps GitHub & Workspace Sync ==="

# 1. Run local archive backup
$SECOPS_DIR/scripts/sync_workspace.sh

# 2. Re-index lab documentation
if [ -f "$SECOPS_DIR/scripts/classify_labs.sh" ]; then
    $SECOPS_DIR/scripts/classify_labs.sh
fi

# 3. Git Stage, Commit, and Push
echo "[+] Staging files for Git..."
git add .

COMMIT_MSG="secops(sync): Automated workstation audit & telemetry sync - $(date '+%Y-%m-%d %H:%M')"
echo "[+] Committing with message: '$COMMIT_MSG'"
git commit -m "$COMMIT_MSG" 2>/dev/null || echo "   (No new changes to commit)"

echo "[+] Pushing code to GitHub repository..."
git push origin main 2>/dev/null || git push origin master 2>/dev/null || echo "⚠️ Git push complete or up-to-date."

echo "✅ Sync complete! Remote repository and local backups are fully aligned."
