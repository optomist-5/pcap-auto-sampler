# Enterprise Multi-Cloud Security Hardening & Workforce Identity Federation

## Executive Summary
This repository contains automated infrastructure-as-code (IaC) tooling and declarative security policy enforcing multi-cloud baselines across Google Cloud Platform (GCP) and Microsoft Azure.

The architecture demonstrates zero-trust workforce identity federation using Microsoft Entra ID via OIDC, enforcing defensive Organization Policy guardrails, and verifying negative security boundaries against unauthorized resource provisioning and key issuance.

---

## Security Guardrails & Defense-in-Depth Model

SecOps hardening is verified across two primary security abstraction layers:

### Layer 1: Identity & Access Management (IAM)
* **Zero Service Account Keys**: Banning user-managed service account keys mitigates credential leakage vectors in developer environments and CI/CD pipelines.
* **Workforce Pool Mapping**: Granting ephemeral, scope-limited roles (`roles/viewer`, `roles/iam.infrastructureAdmin`) via workforce identity assertions.

### Layer 2: Organization Policy Guardrails (Pre-execution Enforcement)
Even if an identity is granted temporary administrative permissions (e.g., `roles/compute.admin` or `roles/iam.serviceAccountKeyAdmin`), declarative organization policies prevent non-compliant infrastructure provisioning at the control plane level:

* **`constraints/compute.vmExternalIpAccess`**: Enforces `denyAll: true` on VM IPv4 public IP assignment.
* **`constraints/iam.disableServiceAccountKeyCreation`**: Globally blocks `.json` service account key downloads.
* **`constraints/iam.automaticIamGrantsForDefaultServiceAccounts`**: Prevents auto-assigning permissive `Editor` roles to default Compute and App Engine service accounts.

---

## Threat Detection & Engineering Insights

### 1. Dual-Layer Policy Evaluation Order
* **Finding**: IAM authorization is evaluated **before** Organization Policy constraints.
* **Engineering Insight**: If a federated user lacks the specific IAM permission (`iam.serviceAccountKeys.create`), the request fails at **Layer 1** with `PERMISSION_DENIED`. To validate that Layer 2 guardrails are working, identity permissions must be temporarily elevated to confirm that the platform rejects the request with `FAILED_PRECONDITION` (`constraints/iam.disableServiceAccountKeyCreation`).

### 2. Service Activation & Billing Dependencies
* **Finding**: Infrastructure APIs like `compute.googleapis.com` cannot be auto-enabled by federated workforce users lacking `serviceusage.services.enable`.
* **Engineering Insight**: Hardening automation pipelines must decouple project bootstrapping (billing account attachment and API enablement via admin service principals) from daily operational workforce workflows.

### 3. Threat Detection Monitoring Signals
Security Command Center (SCC) and Cloud Audit Logs should monitor for the following high-fidelity indicators:
* `google.iam.admin.v1.CreateServiceAccountKey` calls resulting in `FAILED_PRECONDITION`.
* `v1.compute.instances.insert` calls rejected due to `compute.vmExternalIpAccess` policy violations.
* Rapid identity context switches between administrative principals and federated workforce subjects.

---

## Execution Workflow

```bash
# 1. Initialize environment & attach billing
python setup_lab_environment.py

# 2. Execute master hardening suite
python lab_master_hardener.py

# 3. Authenticate as federated workforce principal
gcloud auth login --login-config=login-config.json

# 4. Verify negative policy constraint (Expected: BLOCKED by OrgPolicy)
gcloud compute instances create public-ip-test-vm \
  --zone=us-central1-a \
  --machine-type=e2-micro \
  --project=basic-decoder-510402-i2


---

### Step 2: Create Deployment Script (`deploy_to_github.sh`)

Now create the git automation script:

```bash
cat << 'EOF' > deploy_to_github.sh
#!/usr/bin/env zsh
set -e

echo "📦 Preparing files for Git deployment..."

# 1. Clean up temporary test artifacts
rm -f test-key.json tmp_policy.yaml

# 2. Add files to staging
git add README.md setup_lab_environment.py lab_master_hardener.py lab_hardening_audit.json

# 3. Commit with structured engineering summary
git commit -m "feat(secops): complete multi-cloud zero-trust hardening suite

- Implemented setup_lab_environment.py for dynamic billing link & API activation
- Executed lab_master_hardener.py across GCP multi-project environment
- Verified Entra ID OIDC Workforce Identity Federation
- Validated negative policy constraints for compute.vmExternalIpAccess & iam.disableServiceAccountKeyCreation
- Documented threat detection signals and dual-layer policy enforcement post-mortem"

# 4. Push to remote main branch
echo "🚀 Pushing changes to GitHub..."
git push origin main || git push origin HEAD

echo "✅ Repository updated and published successfully!"
