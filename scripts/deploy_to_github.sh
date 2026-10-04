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
