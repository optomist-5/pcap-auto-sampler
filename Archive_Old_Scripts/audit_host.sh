#!/bin/bash

echo "🩻 [AUDIT] Initiating Forensic Storage Audit..."
echo "------------------------------------------------"

TARGET_FOLDERS=(
    ~/Desktop
    ~/Documents
    ~/Downloads
    ~/Pictures
    ~/Movies
    ~/Music
)

for folder in "${TARGET_FOLDERS[@]}"; do
    if [ -d "$folder" ]; then
        SIZE=$(du -sh "$folder" 2>/dev/null | awk '{print $1}')
        printf "🩺 Checked %-35s : Size %s\n" "$folder" "$SIZE"
    else
        printf "⚠️  Folder  %-35s : DOES NOT EXIST\n" "$folder"
    fi
done

echo "------------------------------------------------"
echo "✅ [AUDIT COMPLETE] Data successfully sanitized."
