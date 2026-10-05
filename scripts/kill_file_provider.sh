#!/bin/bash

pluginkit -r com.microsoft.OneDrive-mac.FileProvider 2>/dev/null

chflags -R nouchg ~/Library/CloudStorage/OneDrive-* 2>/dev/null

rm -rf ~/Library/CloudStorage/OneDrive-* 2>/dev/null

killall Finder

echo "✅ [SUCCESS] Locks severed and folders deleted."
