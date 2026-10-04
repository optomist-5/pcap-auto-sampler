#!/usr/bin/env bash
echo "=== 1. Desktop Data Snapshot Size ==="
du -sh /Users/mq/Desktop/Data 2>/dev/null || echo "Not found"

echo ""
echo "=== 2. iCloud Mobile Documents Size ==="
du -sh "$HOME/Library/Mobile Documents/com~apple~CloudDocs" 2>/dev/null

echo ""
echo "=== 3. CloudStorage Mirrors Size ==="
du -sh ~/Library/CloudStorage/* 2>/dev/null

echo ""
echo "=== 4. Top 10 Heaviest Folders in Home ==="
du -sh ~/* 2>/dev/null | sort -hr | head -10
