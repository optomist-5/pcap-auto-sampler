#!/bin/bash
# ==============================================================================
# SecOps Arsenal Inventory Scanner
# Description: Discovers and maps all custom tools, scripts, and aliases.
# ==============================================================================

REPORT="/tmp/secops_inventory.txt"

echo "==================================================" > "$REPORT"
echo "🔍 SEC-OPS ARSENAL AUDIT - $(date)" >> "$REPORT"
echo "==================================================" >> "$REPORT"

echo -e "\n[*] 1. ACTIVE TERMINAL ALIASES (Your 'God Mode' Commands):" >> "$REPORT"
grep "^alias" ~/.zshrc >> "$REPORT" || echo "No aliases found." >> "$REPORT"

echo -e "\n[*] 2. BASH/ZSH EXECUTABLE SCRIPTS:" >> "$REPORT"
find ~/secops -type f -name "*.sh" -o -name "*.zsh" 2>/dev/null | sed "s|$HOME/||" >> "$REPORT"

echo -e "\n[*] 3. PYTHON TOOLS & MODULES:" >> "$REPORT"
find ~/secops -type f -name "*.py" 2>/dev/null | sed "s|$HOME/||" >> "$REPORT"

echo -e "\n[*] 4. CONFIGURATION & ENVIRONMENT FILES:" >> "$REPORT"
find ~/secops -type f \( -name "*.env" -o -name "*.plist" \) 2>/dev/null | sed "s|$HOME/||" >> "$REPORT"

echo -e "\n==================================================" >> "$REPORT"
echo "Audit complete." >> "$REPORT"

# Output the results to the terminal
cat "$REPORT"
