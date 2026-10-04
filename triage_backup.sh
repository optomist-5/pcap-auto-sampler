#!/bin/bash
echo ""
echo "🏥 [TRIAGE] Initiating procedure: Cold Storage: Extras & Keys"
echo "🩺 Monitoring vital signs (This may take several minutes)..."
echo ""

START=$(date +%s)

Fallback text in case clipboard strips emojis

SPINNER=("SCANNING" "PACKING." "PACKING.." "PACKING..." "SECURING" "SAVING..")
i=0

Run tar and capture output line by line safely

tar -czvf /Volumes/SecOps_Vault/Extras_and_Keys_2026.tar.gz ~/Downloads ~/Movies ~/Music ~/.ssh ~/.zshrc ~/.aws ~/Library/Application\ Support/MobileSync/Backup 2>&1 | while read -r line; do

# Extract first 70 chars to keep terminal neat
short_line="${line:0:70}"

# Print spinner and line, \r overwrites the line
printf "\r[%s] %-70s" "${SPINNER[$((i%6))]}" "$short_line"

i=$((i+1))
done

END=$(date +%s)$
$ELAPSED=$((END-START))
MINS=$((ELAPSED/60))$
$SECS=$((ELAPSED%60))

echo ""
echo ""
echo "✅ [DISCHARGE] Procedure complete! The data is stable."
echo "⏱️  Total Operation Time: $MINS minutes,$SECS seconds."
echo ""
