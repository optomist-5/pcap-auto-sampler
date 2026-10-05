#!/bin/bash
echo "[*] Renaming files to explicit enterprise standards..."

# Rename the backend files
mv ~/secops/bin/warden.sh ~/secops/bin/audit_perimeter.sh 2>/dev/null
mv ~/secops/secops_sentinel.py ~/secops/audit_threat_hunter.py 2>/dev/null
mv ~/secops/rig_sanitizer.py ~/secops/audit_dlp_scrubber.py 2>/dev/null

mv ~/secops/triage_backup.py ~/secops/ops_secure_backup.py 2>/dev/null
mv ~/secops/phase3_purge.sh ~/secops/ops_system_purge.sh 2>/dev/null
mv ~/secops/secops_prompt_os.zsh ~/secops/dev_ai_context.zsh 2>/dev/null
mv ~/secops/mri.py ~/secops/dev_dfir_imager.py 2>/dev/null
mv ~/secops/godmode.py ~/secops/sys_ops_dashboard.py 2>/dev/null
mv ~/secops/bin/rig.py ~/secops/bin/sys_env_config.py 2>/dev/null

# Combine the two halt scripts into one clean file
cat ~/secops/kill_onedrive.sh ~/secops/kill_file_provider.sh > ~/secops/ops_halt_sync_daemons.sh 2>/dev/null
chmod +x ~/secops/ops_halt_sync_daemons.sh

# Remove the old aliases from .zshrc
sed -i '' '/# ENDPOINT OPERATIONS CONTROL PLANE/,$d' ~/.zshrc

# Inject the new exact matching aliases
cat << 'INNER_EOF' >> ~/.zshrc
# ==============================================================================
# ENDPOINT OPERATIONS CONTROL PLANE (Enterprise Taxonomy 2026)
# ==============================================================================
alias audit-perimeter="~/secops/bin/audit_perimeter.sh"
alias audit-threat-hunter="python3 ~/secops/audit_threat_hunter.py"
alias audit-dlp-scrubber="python3 ~/secops/audit_dlp_scrubber.py"

alias ops-secure-backup="python3 ~/secops/ops_secure_backup.py"
alias ops-halt-sync="~/secops/ops_halt_sync_daemons.sh"
alias ops-system-purge="~/secops/ops_system_purge.sh"

alias dev-ai-context="~/secops/dev_ai_context.zsh"
alias dev-threat-model="cd ~/Desktop/TM_Extraction_Tools && sudo python3 dev_threat_modeler.py"
alias dev-dfir-image="python3 ~/secops/dev_dfir_imager.py"

alias sys-dashboard="python3 ~/secops/sys_ops_dashboard.py"
alias sys-env-config="python3 ~/secops/bin/sys_env_config.py"
INNER_EOF

echo "[+] Files renamed and aliases updated successfully."
