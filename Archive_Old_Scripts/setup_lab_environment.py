import subprocess
import sys
from datetime import datetime, timezone

GCP_PROJECTS = ["basic-decoder-510402-i2", "velvety-setup-510402-p2"]
BILLING_ACCOUNT_ID = "0165F7-1D9535-59155C"

def run_cmd(command):
    """Executes shell commands safely and returns execution status."""
    try:
        res = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"  [SUCCESS] -> {command[:85]}...")
        return True, res.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"  [ERROR] {e.stderr.strip()}")
        return False, e.stderr.strip()

def setup_project(project_id, billing_id):
    """Links billing accounts and enables baseline cloud infrastructure APIs."""
    print(f"\n⚙️ --- INITIALIZING INFRASTRUCTURE: {project_id} ---")
    
    # 1. Attach Active Billing Account
    run_cmd(f"gcloud billing projects link {project_id} --billing-account={billing_id}")

    # 2. Enable Baseline Security & Compute APIs
    apis = [
        "compute.googleapis.com",
        "orgpolicy.googleapis.com",
        "securitycenter.googleapis.com",
        "logging.googleapis.com"
    ]
    for api in apis:
        run_cmd(f"gcloud services enable {api} --project={project_id}")

if __name__ == "__main__":
    timestamp = datetime.now(timezone.utc).isoformat()
    print(f"🚀 [{timestamp}] Starting Multi-Cloud Infrastructure Initialization...")

    for project in GCP_PROJECTS:
        setup_project(project, BILLING_ACCOUNT_ID)
        
    print("\n✅ Infrastructure Initialization Complete. Billing linked & Core APIs activated.")
