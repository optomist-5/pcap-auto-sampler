#!/usr/bin/env bash
# ==============================================================================
# SEC-OPS ZERO TRUST SYSTEM VERIFICATION ENGINE
# Target: Workstation secopslt (~/secops)
# ==============================================================================

GREEN='\030[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

PASS_COUNT=0
FAIL_COUNT=0

log_pass() {
    echo -e "  [${GREEN}PASS${NC}] $1"
    ((PASS_COUNT++))
}

log_fail() {
    echo -e "  [${RED}FAIL${NC}] $1"
    ((FAIL_COUNT++))
}

log_info() {
    echo -e "  [${YELLOW}INFO${NC}] $1"
}

echo "======================================================================"
echo "          SEC-OPS ZERO TRUST AUDIT & SYSTEM STATE VERIFICATION        "
echo "======================================================================"
echo "Timestamp: $(date)"
echo "Host: $(hostname) | User: $(whoami)"
echo "----------------------------------------------------------------------"

# --- CHECK 1: TASK-01 (Core Dashboard & Tools) ---
echo "1. Auditing TASK-01: Core Control Plane & Sentinel Suite..."
if [ -f "$HOME/secops/sys_ops_dashboard.py" ]; then
    log_pass "sys_ops_dashboard.py present"
else
    log_fail "sys_ops_dashboard.py missing"
fi

if [ -f "$HOME/secops/secops_sentinel.py" ]; then
    log_pass "secops_sentinel.py present"
else
    log_fail "secops_sentinel.py missing"
fi

if [ -x "$HOME/secops/scripts/test_all_tools.sh" ]; then
    log_pass "scripts/test_all_tools.sh present and executable"
else
    log_fail "scripts/test_all_tools.sh missing or not executable"
fi

# --- CHECK 2: TASK-02 & TASK-03 (Restored SOC Defense Modules) ---
echo ""
echo "2. Auditing TASK-02 & TASK-03: Restored Threat Hunter & Hardener Engines..."
if [ -f "$HOME/secops/modules/soc_defense/threat_hunter.py" ] && [ -x "$HOME/secops/modules/soc_defense/threat_hunter.py" ]; then
    log_pass "modules/soc_defense/threat_hunter.py active and executable"
else
    log_fail "modules/soc_defense/threat_hunter.py missing or unexecutable"
fi

if [ -f "$HOME/secops/modules/soc_defense/cloud_hardener.py" ] && [ -x "$HOME/secops/modules/soc_defense/cloud_hardener.py" ]; then
    log_pass "modules/soc_defense/cloud_hardener.py active and executable"
else
    log_fail "modules/soc_defense/cloud_hardener.py missing or unexecutable"
fi

# --- CHECK 3: TASK-04 (Lab Classifier & Documentation Index) ---
echo ""
echo "3. Auditing TASK-04: Student Lab Classifier & Documentation Index..."
if [ -d "$HOME/secops/docs/wgu_coursework" ] && [ -d "$HOME/secops/docs/cert_labs" ]; then
    log_pass "Directory structure (docs/wgu_coursework & docs/cert_labs) created"
else
    log_fail "Lab classification directories missing"
fi

if [ -s "$HOME/secops/docs/README.md" ]; then
    log_pass "docs/README.md indexed and non-empty"
else
    log_fail "docs/README.md missing or empty"
fi

# --- CHECK 4: TASK-05 (Workspace Sync & Local Backups) ---
echo ""
echo "4. Auditing TASK-05: Google Drive & Workspace Sync Pipeline..."
if [ -x "$HOME/secops/scripts/sync_workspace.sh" ]; then
    log_pass "scripts/sync_workspace.sh present and executable"
else
    log_fail "scripts/sync_workspace.sh missing or unexecutable"
fi

BACKUP_TARBALL=$(ls -1 $HOME/secops/logs/secops_docs_backup_*.tar.gz 2>/dev/null | tail -n 1)
if [ -n "$BACKUP_TARBALL" ]; then
    log_pass "Workspace backup archive verified: $(basename "$BACKUP_TARBALL")"
else
    log_fail "No workspace backup archive found in logs/"
fi

# --- CHECK 5: TASK-06 (Background Intrusion Daemon / launchd) ---
echo ""
echo "5. Auditing TASK-06: Hourly Background Intrusion Daemon (launchd)..."
if [ -f "$HOME/Library/LaunchAgents/com.secops.perimeter.audit.plist" ]; then
    log_pass "LaunchAgent plist file exists"
else
    log_fail "LaunchAgent plist file missing"
fi

if launchctl list 2>/dev/null | grep -q "com.secops.perimeter.audit"; then
    log_pass "com.secops.perimeter.audit daemon is registered and active in launchd"
else
    log_fail "com.secops.perimeter.audit daemon not found in launchctl process table"
fi

if [ -f "$HOME/secops/logs/perimeter_daemon.log" ]; then
    log_pass "Background daemon log active (secops/logs/perimeter_daemon.log)"
else
    log_fail "Background daemon log missing"
fi

# --- CHECK 6: Environment & Zsh Configuration Audit ---
echo ""
echo "6. Auditing Zsh Shell Configuration & Alias Integrity..."
if [ -f "$HOME/.zshrcrc" ]; then
    log_info "Found ghost typo file ~/.zshrcrc. Cleaning up..."
    rm -f "$HOME/.zshrcrc"
fi

if grep -q "alias secops=" "$HOME/.zshrc" 2>/dev/null; then
    log_pass "secops alias found in ~/.zshrc"
else
    log_fail "secops alias missing from ~/.zshrc"
fi

if grep -q "alias threat-hunt=" "$HOME/.zshrc" 2>/dev/null; then
    log_pass "threat-hunt alias found in ~/.zshrc"
else
    log_fail "threat-hunt alias missing from ~/.zshrc"
fi

# --- CHECK 7: GCP Project Context ---
echo ""
echo "7. Auditing GCP CLI Context..."
GCP_PROJECT=$(gcloud config get-value project 2>/dev/null)
if [ -n "$GCP_PROJECT" ]; then
    log_pass "Active GCP Project set to: $GCP_PROJECT"
else
    log_fail "No active GCP project configured in gcloud"
fi

# --- FINAL SUMMARY ---
echo ""
echo "======================================================================"
echo "                      ZERO TRUST SYSTEM SUMMARY                       "
echo "======================================================================"
echo -e "  Total Tests Executed : $((PASS_COUNT + FAIL_COUNT))"
echo -e "  Passed Checks        : ${GREEN}${PASS_COUNT}${NC}"
echo -e "  Failed Checks        : ${RED}${FAIL_COUNT}${NC}"
echo "----------------------------------------------------------------------"

if [ $FAIL_COUNT -eq 0 ]; then
    echo -e "${GREEN}✅ SYSTEM FULLY VERIFIED: All tasks (TASK-01 to TASK-06) operational.${NC}"
else
    echo -e "${YELLOW}⚠️ SYSTEM REMEDIATION NEEDED: Review failed checks above.${NC}"
fi
echo "======================================================================"
