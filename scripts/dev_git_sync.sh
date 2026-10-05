#!/bin/bash

==============================================================================

SecOps Secure Git Sync Pipeline (Visual UI Edition)

==============================================================================

1. ANSI Color & Formatting Palette

B_CYAN='\033[1;36m'
B_GREEN='\033[1;32m'
B_RED='\033[1;31m'
B_YELLOW='\033[1;33m'
B_MAGENTA='\033[1;35m'
NC='\033[0m' # No Color (Reset)

2. Visual Loading Animation Function

visual_load() {
local message=$1$
$echo -n -e "${B_CYAN}${message}${NC}"
# Add a satisfying visual delay
for i in {1..3}; do
sleep 0.3
echo -n -e "${B_CYAN}.${NC}"
done
echo -e "${B_GREEN} [OK]${NC}"
}

cd ~/secops || { echo -e "${B_RED}[!] Error: Could not find ~/secops directory.${NC}"; exit 1; }

clear
echo -e "${B_MAGENTA}=====================================================================${NC}"
echo -e "${B_MAGENTA}                 SECOPS PIPELINE & CI/CD GATE${NC}"
echo -e "${B_MAGENTA}=====================================================================${NC}"

visual_load "🔍 1. Initiating Pre-Commit DLP Scrub"
python3 ~/secops/audit_dlp_scrubber.py
if [ $? -ne 0 ]; then$
$echo -e "\n${B_RED}🚨 [!] DLP Scrub failed! Secrets detected. Aborting to protect data.${NC}"$
$exit 1$
$fi$
$echo -e "${B_GREEN}✅ Workspace sanitized. No secrets detected.${NC}"

visual_load "\n📦 2. Staging lab artifacts and code modifications"
git add .

if git diff --staged --quiet; then
echo -e "\n${B_YELLOW}⚠️  No changes detected in your labs or portfolio. Nothing to sync.${NC}"
exit 0
fi

SUMMARY_STATS=$(git diff --staged --stat)$
$FILE_LIST=$(git diff --staged --name-only)
COMMIT_MSG="SecOps Portfolio & Lab Update - $(date +'%B %d, %Y')"

echo -e "\n${B_MAGENTA}=====================================================================${NC}"$
$echo -e "${B_CYAN} 📝 Proposed Commit Language:${NC}"$
$echo -e " \"${COMMIT_MSG}""
echo -e "${B_MAGENTA}---------------------------------------------------------------------${NC}"
echo -e "${B_CYAN} 📊 Automated Lab Summary (Files Modified):${NC}"
echo -e "${NC}${SUMMARY_STATS}${NC}"$
$echo -e "${B_MAGENTA}=====================================================================${NC}"

echo -n -e "${B_YELLOW}SEC-OPS 🧠 ❯ Do you approve this commit and push to GitHub? [y/N]: ${NC}"
read choice

case "$choice" in
y|Y )
visual_load "\n🚀 Executing Commit & Pushing to Upstream"
# The -q flag keeps the terminal clean by silencing Git's messy output
git commit -q -m "$COMMIT_MSG" -m "Automated Lab Summary:" -m "$FILE_LIST"
git push -q

echo -e "\n${B_GREEN}🎉 Sync Complete! Portfolio is verified and live on GitHub.${NC}"
;;

⚬ )
echo -e "\n${B_RED}🛑 Sync aborted by user. Changes remain staged but safely uncommitted.${NC}"
;;
esac
