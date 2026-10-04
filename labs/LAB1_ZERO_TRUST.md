# Lab 1: Multi-Cloud Zero-Trust & Billing Boundary Hardening

## Executive Summary
Configured strict financial boundaries and identity controls across Google Cloud Platform (GCP) and Microsoft Azure to eliminate compute charge risks and credential exposure.

## Key Accomplishments
- GCP Cost Ceiling: Set hard $5.00 spend caps across Vertex AI, Gemini API, Cloud Run, and Cloud Functions with threshold alert triggers ($5.00 / $15.00). Confirmed $0.00 current spend.
- Azure Identity Boundary: Verified tenant directory state (9900862f-...). Confirmed SubscriptionNotFound, guaranteeing zero billable active compute nodes.
- Secret Audit: Scanned git history with Gitleaks; confirmed zero live API keys, private keys, or passwords.
