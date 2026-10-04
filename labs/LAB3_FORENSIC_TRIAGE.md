# Lab 3: Vault Sanitization & Forensics Engine

## Executive Summary
Built an automated Python vault sanitizer and interactive CLI to scrub legacy user archives while preserving valid user data.

## Key Accomplishments
- Vault Scrubbing: Scanned ~/Vault_Mauri and automatically purged 12,827 junk/session files (Citrix .ica tokens, browser caches, orphaned .plist logs).
- Preservation & Cleanup: Preserved 3.1 GB clean user archive in ~/Vault_Mauri and reclaimed 3.2 GB of dead OS restore dumps from Desktop.
