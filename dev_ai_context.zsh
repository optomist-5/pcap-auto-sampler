#!/bin/zsh
set -e
SECOPS_DIR="$HOME/secops"
DATA_DIR="$SECOPS_DIR/data"
JSON_PAYLOAD="$DATA_DIR/gcp_inventory.json"

echo "🟢 [Module 1] Initializing Environment..."
CURRENT_COST=$(jq -r '.finops_metrics.current_billing_cycle_usd' "$JSON_PAYLOAD")
BUDGET_LIMIT=$(jq -r '.finops_metrics.budget_limit_usd' "$JSON_PAYLOAD")

echo "   -> Current Cost: \$${CURRENT_COST} / \$${BUDGET_LIMIT}"

echo "🟢 [Module 3 & 4] SecOps Deep Audit..."
find "$SECOPS_DIR" -type d -exec chmod 700 {} \;
find "$SECOPS_DIR" -type f -exec chmod 600 {} \;
chmod 700 "$0"

echo "🟢 [Module 6] Pipeline Complete."
