#!/usr/bin/env zsh
# ==============================================================================
# Legacy Script Auditor & Function Preservation Scanner
# ==============================================================================
set -e

echo "🔍 [TASK-02] Scanning workspace for all Python & Shell scripts..."

cd "$HOME/secops"

echo "\n📁 Active Scripts in ~/secops:"
find . -maxdepth 3 \( -name "*.py" -o -name "*.sh" \) ! -path "*/.venv/*" | sort

echo "\n📦 Archived Scripts in Archive_Old_Scripts/:"
if [ -d "Archive_Old_Scripts" ]; then
    ls -la Archive_Old_Scripts/
fi

echo "\n🔎 Checking for unique functions in archived files:"
grep -rnE "^def |function |alias " Archive_Old_Scripts/ 2>/dev/null || echo "No orphaned functions found."

echo "\n✨ TASK-02 AUDIT COMPLETE."
