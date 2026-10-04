#!/usr/bin/env zsh
# macOS System & Application Cache Sanitizer

echo "=== SecOps Sentinel | macOS System File Sanitizer ==="

# 1. Clear User Caches & Diagnostic Logs
echo "[*] Purging User Caches and Crash Reports..."
rm -rf ~/Library/Caches/* 2>/dev/null
rm -rf ~/Library/Logs/DiagnosticReports/* 2>/dev/null
rm -rf ~/Library/Logs/CrashReporter/* 2>/dev/null

# 2. Flush DNS Cache
echo "[*] Flushing macOS Directory Service DNS Cache..."
sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder 2>/dev/null

# 3. Clean Native Mail Drafts/Temporary Downloads
echo "[*] Cleaning Native Mail Lost Downloads..."
rm -rf ~/Library/Containers/com.apple.mail/Data/Library/Mail\ Downloads/* 2>/dev/null

# 4. Remove Orphaned Xcode / Simulator Artifacts (if present)
echo "[*] Cleaning Xcode DerivedData..."
rm -rf ~/Library/Developer/Xcode/DerivedData/* 2>/dev/null

# 5. Empty System Trash
echo "[*] Emptying Trash..."
rm -rf ~/.Trash/* 2>/dev/null

echo "✔ System Sanitization Complete!"
