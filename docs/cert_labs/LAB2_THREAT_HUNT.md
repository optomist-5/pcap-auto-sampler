# Lab 2: Endpoint Threat Hunting & Host Baseline Audit

## Executive Summary
Executed live process memory scans and socket audits on macOS endpoint to identify and evict unauthorized background daemons and persistence hooks.

## Key Accomplishments
- Daemon Eviction: Completely purged Pearson OnVUE proctoring app remnants and terminated Perplexity background agents (ai.perplexity.xpc.plist).
- Forensic PDF Inspection: Evaluated 159 iCloud PDFs for /Launch, /JS, and /EmbeddedFiles exploit vectors. Proved all 159 documents 100% benign.
- Socket Baseline: Automated listening port inspections via secops_sentinel.py net.
