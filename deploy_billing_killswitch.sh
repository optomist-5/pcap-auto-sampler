#!/usr/bin/env zsh
set -e

PROJECT_ID="basic-decoder-510402-i2"
BILLING_ACCOUNT_ID="0165F7-1D9535-59155C"
TOPIC_NAME="billing-budget-alerts"
FUNCTION_NAME="auto-unlink-billing"
REGION="us-central1"

echo "🚀 [1/4] Setting active account to Admin..."
gcloud config set account it-manager@noviascentialabs.com
gcloud config set project $PROJECT_ID

echo "🔧 [2/4] Enabling required Cloud Functions and Pub/Sub APIs..."
gcloud services enable cloudfunctions.googleapis.com cloudbuild.googleapis.com pubsub.googleapis.com billingbudgets.googleapis.com --project=$PROJECT_ID

echo "📬 [3/4] Creating Pub/Sub topic for billing alerts..."
if ! gcloud pubsub topics describe $TOPIC_NAME --project=$PROJECT_ID >/dev/null 2>&1; then
  gcloud pubsub topics create $TOPIC_NAME --project=$PROJECT_ID
fi

echo "📦 [4/4] Writing Cloud Function kill-switch code..."
mkdir -p /tmp/killswitch_code
cat << 'CODE' > /tmp/killswitch_code/main.py
import base64
import json
import google.auth
from googleapiclient.discovery import build

PROJECTS_TO_DISABLE = ["basic-decoder-510402-i2", "velvety-setup-510402-p2"]

def stop_billing(event, context):
    """Triggered by Pub/Sub message when billing budget threshold is breached."""
    if 'data' in event:
        pubsub_message = base64.b64decode(event['data']).decode('utf-8')
        data = json.loads(pubsub_message)
        cost_amount = data.get('costAmount', 0)
        budget_amount = data.get('budgetAmount', 0)
        
        print(f"⚠️ Billing alert triggered! Current Cost: ${cost_amount}, Budget: ${budget_amount}")
        
        if cost_amount > 0:
            credentials, _ = google.auth.default()
            billing_client = build('cloudbilling', 'v1', credentials=credentials)
            
            for project_id in PROJECTS_TO_DISABLE:
                project_name = f"projects/{project_id}"
                print(f"🛑 Emergency unlinking billing for {project_id}...")
                body = {'billingAccountName': ''} # Empty string disables billing
                try:
                    billing_client.projects().updateBillingInfo(name=project_name, body=body).execute()
                    print(f"✅ Successfully unlinked billing from {project_id}.")
                except Exception as e:
                    print(f"❌ Failed to unlink billing for {project_id}: {str(e)}")
CODE

cat << 'CODE' > /tmp/killswitch_code/requirements.txt
google-api-python-client>=2.0.0
google-auth>=2.0.0
CODE

echo "⚡ Deploying Cloud Function '$FUNCTION_NAME'..."
gcloud functions deploy $FUNCTION_NAME \
  --project=$PROJECT_ID \
  --region=$REGION \
  --runtime=python310 \
  --trigger-topic=$TOPIC_NAME \
  --entry-point=stop_billing \
  --quiet

echo "✅ Billing Kill-Switch active! Any budget trigger will instantly unlink project billing."
