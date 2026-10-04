#!/usr/bin/env zsh
# macOS System & Application Cache Sanitizer

# Disable Zsh interactive wildcard confirmation prompts
setopt RM_STAR_SILENT

echo "=== SecOps Sentinel | macOS System File Sanitizer ==="

# 1. Clear User Caches & Diagnostic Logs
echo "[*] Purging User Caches and Crash Reports..."
command rm -rf ~/Library/Caches/* 2>/dev/null
command rm -rf ~/Library/Logs/DiagnosticReports/* 2>/dev/null
command rm -rf ~/Library/Logs/CrashReporter/* 2>/dev/null

# 2. Purge System Logs & ASL Databases
echo "[*] Cleaning System Log files..."
sudo log erase --all 2>/dev/null

# 3. Flush DNS Cache & Reset mDNSResponder
echo "[*] Flushing macOS Directory Service DNS Cache..."
sudo dscacheutil -flushcache
sudo killall -HUP mDNSResponder 2>/dev/null

# 4. Clean Native Mail Temporary Downloads
echo "[*] Cleaning Native Mail Lost Downloads..."
command rm -rf ~/Library/Containers/com.apple.mail/Data/Library/Mail\ Downloads/* 2>/dev/null

# 5. Remove Xcode / Simulator Artifacts
if [[ -d ~/Library/Developer/Xcode/DerivedData ]]; then
    echo "[*] Cleaning Xcode DerivedData..."
    command rm -rf ~/Library/Developer/Xcode/DerivedData/* 2>/dev/null
fi

# 6. Empty Trash
echo "[*] Emptying Trash..."
command rm -rf ~/.Trash/* 2>/dev/null

# 7. Purge Inactive Memory (RAM)
echo "[*] Purging inactive RAM memory..."
sudo purge 2>/dev/null

echo "✔ System Sanitization Complete!"
