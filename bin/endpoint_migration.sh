#!/bin/bash
echo "[*] Initiating Endpoint Harmonization..."

# 1. Purge
sed -i '' '/alias sentinel=/d' ~/.zshrc
sed -i '' '/alias prompt-os=/d' ~/.zshrc
sed -i '' '/alias extract-tm=/d' ~/.zshrc
sed -i '' '/alias rig=/d' ~/.zshrc
sed -i '' '/alias godmode=/d' ~/.zshrc
sed -i '' '/alias warden=/d' ~/.zshrc
sed -i '' '/# GOD MODE SEC-OPS ALIAS/d' ~/.zshrc
sed -i '' '/# ENDPOINT OPERATIONS CONTROL PLANE/d' ~/.zshrc

# 2. Inject
cat << 'INNER_EOF' >> ~/.zshrc

# ==============================================================================
# ENDPOINT OPERATIONS CONTROL PLANE (Enterprise Taxonomy 2026)
# ==============================================================================
alias audit-perimeter="~/secops/bin/warden.sh"
alias audit-sentinel="python3 ~/secops/secops_sentinel.py"
alias audit-dlp="python3 ~/secops/rig_sanitizer.py"
alias ops-backup="python3 ~/secops/triage_backup.py"
alias ops-purge="~/secops/phase3_purge.sh"
alias ops-halt-sync="~/secops/kill_onedrive.sh && ~/secops/kill_file_provider.sh"
alias dev-prompt="~/secops/secops_prompt_os.zsh"
alias dev-extract="cd ~/Desktop/TM_Extraction_Tools && sudo python3 tm_extractor.py"
alias dev-mri="python3 ~/secops/mri.py"
alias sys-dashboard="python3 ~/secops/godmode.py"
alias sys-config="python3 ~/secops/bin/rig.py"
INNER_EOF

echo "[+] 2026 Enterprise Taxonomy injected into ~/.zshrc."

# 3. Archive
mkdir -p ~/secops/Archive_Old_Scripts
mv ~/secops/triage_backup.sh ~/secops/Archive_Old_Scripts/ 2>/dev/null || true
mv ~/secops/secops_rig_audit.sh ~/secops/Archive_Old_Scripts/ 2>/dev/null || true
mv ~/secops/audit_host.sh ~/secops/Archive_Old_Scripts/ 2>/dev/null || true
echo "[+] Redundant scripts successfully archived."
echo "[*] Migration Complete!"
