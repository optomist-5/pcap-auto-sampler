import json
import os
import subprocess
import tempfile
from datetime import datetime, timezone

GCP_PROJECTS = ["basic-decoder-510402-i2", "velvety-setup-510402-p2"]
AZURE_SUB_ID = os.getenv("AZURE_SUBSCRIPTION_ID", "YOUR_AZURE_SUBSCRIPTION_ID")

AUDIT_LOG = {
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "gcp_results": [],
    "azure_results": []
}

def run_cmd(command):
    """Executes shell commands safely and captures output."""
    try:
        res = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"  [SUCCESS] -> {command[:80]}...")
        return True, res.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"  [ERROR] {e.stderr.strip()}")
        return False, e.stderr.strip()

def harden_gcp_project(project_id):
    print(f"\n🔒 --- [GCP] Hardening Project: {project_id} ---")
    project_audit = {"project_id": project_id, "controls": []}

    # 1. Enable Required APIs
    apis = ["orgpolicy.googleapis.com", "securitycenter.googleapis.com", "logging.googleapis.com"]
    for api in apis:
        success, _ = run_cmd(f"gcloud services enable {api} --project={project_id}")
        project_audit["controls"].append({"control": f"API: {api}", "status": "SUCCESS" if success else "FAILED"})

    # 2. Enforce Uniform Bucket-Level Access
    cmd = (f"gcloud storage buckets list --project={project_id} --format='value(name)' | "
           f"xargs -I {{}} gcloud storage buckets update gs://{{}} --uniform-bucket-level-access")
    success, _ = run_cmd(cmd)
    project_audit["controls"].append({"control": "Storage: Uniform Bucket-Level Access", "status": "SUCCESS" if success else "FAILED"})

    # 3. Block VM External Public IPs (Org Policy V2)
    v2_policy = f"""name: projects/{project_id}/policies/compute.vmExternalIpAccess
spec:
  rules:
  - denyAll: true
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as tmp:
        tmp.write(v2_policy)
        tmp_path = tmp.name
    
    try:
        success, _ = run_cmd(f"gcloud org-policies set-policy {tmp_path}")
        project_audit["controls"].append({"control": "Compute: Block External IPs", "status": "SUCCESS" if success else "FAILED"})
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

    # 4. Disable Service Account Key Creation
    success, _ = run_cmd(f"gcloud resource-manager org-policies enable-enforce iam.disableServiceAccountKeyCreation --project={project_id}")
    project_audit["controls"].append({"control": "IAM: Block SA Key Creation", "status": "SUCCESS" if success else "FAILED"})

    # 5. Disable Automatic SA Role Grants
    success, _ = run_cmd(f"gcloud resource-manager org-policies enable-enforce iam.automaticIamGrantsForDefaultServiceAccounts --project={project_id}")
    project_audit["controls"].append({"control": "IAM: Block Automatic SA Grants", "status": "SUCCESS" if success else "FAILED"})

    AUDIT_LOG["gcp_results"].append(project_audit)

def harden_azure_subscription(sub_id):
    print(f"\n🔒 --- [AZURE] Hardening Subscription: {sub_id} ---")
    sub_audit = {"subscription_id": sub_id, "controls": []}

    success, _ = run_cmd(f"az account set --subscription {sub_id}")
    if not success:
        print("  [SKIP] Azure subscription not active or not found.")
        return

    # Restrict Storage Accounts (TLS 1.2 & Disable Public Access)
    success, sa_list = run_cmd("az storage account list --query '[].name' -o tsv")
    if success and sa_list:
        for sa in sa_list.split():
            run_cmd(f"az storage account update --name {sa} --min-tls-version TLS1_2 --allow-blob-public-access false")
        sub_audit["controls"].append({"control": "Storage: Enforce TLS 1.2 & Disable Public Access", "status": "SUCCESS"})

    # Enable Defender for Cloud
    run_cmd("az security pricing create --name VirtualMachines --tier Standard")
    run_cmd("az security pricing create --name StorageAccounts --tier Standard")
    sub_audit["controls"].append({"control": "Defender: Compute & Storage Standard Tiers", "status": "SUCCESS"})

    # Require HTTPS on Web Apps
    success, web_apps = run_cmd("az webapp list --query '[].{name:name, rg:resourceGroup}' -o json")
    if success and web_apps and web_apps != "[]":
        apps = json.loads(web_apps)
        for app in apps:
            run_cmd(f"az webapp update --name {app['name']} --resource-group {app['rg']} --https-only true")
        sub_audit["controls"].append({"control": "App Services: Enforce HTTPS Only", "status": "SUCCESS"})

    AUDIT_LOG["azure_results"].append(sub_audit)

if __name__ == "__main__":
    print("🚀 Starting Cybersecurity Lab Master Hardening Run...")

    for project in GCP_PROJECTS:
        harden_gcp_project(project)

    if AZURE_SUB_ID and AZURE_SUB_ID != "YOUR_AZURE_SUBSCRIPTION_ID":
        harden_azure_subscription(AZURE_SUB_ID)

    with open("lab_hardening_audit.json", "w") as f:
        json.dump(AUDIT_LOG, f, indent=2)

    print("\n✅ Execution Complete. Audit log exported to 'lab_hardening_audit.json'.")
