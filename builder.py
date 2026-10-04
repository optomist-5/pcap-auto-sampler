#!/usr/bin/env python3
import os

target_dir = os.path.expanduser("~/secops")
file_path = os.path.join(target_dir, "secops_prompt_os.zsh")

script_payload = r"""#!/bin/zsh
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
"""

os.makedirs(target_dir, exist_ok=True)
with open(file_path, "w") as f:
    f.write(script_payload)
os.chmod(file_path, 0o700)
print("[+] Deployment successful. Ready to run.")
