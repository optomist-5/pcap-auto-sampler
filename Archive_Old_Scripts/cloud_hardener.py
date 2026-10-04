import os
import subprocess
import tempfile

GCP_PROJECT_ID = "velvety-setup-510402-p2"

def run_cmd(command):
    """Executes CLI commands securely and outputs standard status."""
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"  [SUCCESS] -> {command[:90]}...")
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"  [ERROR] {e.stderr.strip()}")
        return None

def harden_gcp(project_id):
    print(f"\n🔒 --- HARDENING GCP PROJECT: {project_id} ---")
    
    # 0. Enable Organization Policy API
    run_cmd(f"gcloud services enable orgpolicy.googleapis.com --project={project_id}")

    # 1. Enforce Uniform Bucket-Level Access (Storage)
    run_cmd(f"gcloud storage buckets list --project={project_id} --format='value(name)' | "
            f"xargs -I {{}} gcloud storage buckets update gs://{{}} --uniform-bucket-level-access")

    # 2. Block Public External IPs on VM Instances (Correct V2 oneof schema)
    yaml_content = f"""name: projects/{project_id}/policies/compute.vmExternalIpAccess
spec:
  rules:
  - denyAll: true
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as tmp:
        tmp.write(yaml_content)
        tmp_path = tmp.name

    try:
        run_cmd(f"gcloud org-policies set-policy {tmp_path}")
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

    # 3. Disable Service Account Key Creation (Boolean Constraint)
    run_cmd(f"gcloud resource-manager org-policies enable-enforce "
            f"iam.disableServiceAccountKeyCreation --project={project_id}")

    # 4. Enable Security Command Center API
    run_cmd(f"gcloud services enable securitycenter.googleapis.com --project={project_id}")

if __name__ == "__main__":
    harden_gcp(GCP_PROJECT_ID)
