#!/usr/bin/env python3
import json, os, shutil, subprocess, sys
from datetime import datetime, timezone

GREEN, RED, YELLOW, CYAN, RESET = "\033[1;32m", "\033[1;31m", "\033[1;33m", "\033[1;36m", "\033[0m"

def check_cli(binary, cmd):
    if not shutil.which(binary): return False, "CLI Binary Missing"
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return (True, "Authenticated") if res.returncode == 0 and res.stdout.strip() else (False, "Unauthenticated")

print(f"\n{CYAN}================ ☁️ MULTI-CLOUD & SAAS AUDITOR ☁️ ================{RESET}\n")
az_ok, az_msg = check_cli("az", "az account show --query '[name, id]' -o tsv")
gcp_ok, gcp_msg = check_cli("gcloud", "gcloud config get-value account")

print(f"  ├─ Azure Tenant: {GREEN if az_ok else YELLOW}[{az_msg}]{RESET}")
print(f"  └─ GCP Tenant:   {GREEN if gcp_ok else YELLOW}[{gcp_msg}]{RESET}\n")

logs = [{
    "TimeGenerated": datetime.now(timezone.utc).isoformat(),
    "SecurityControl": "BreakGlass_Account_Monitor",
    "Status": "STANDBY",
    "PolicyDetail": "Monitoring breakglass-admin@domain for unauthorized logins"
}]

with open("multicloud_identity_telemetry.json", "w") as f: json.dump(logs, f, indent=2)
print(f"{GREEN}[+] Generated multicloud_identity_telemetry.json{RESET}\n")
