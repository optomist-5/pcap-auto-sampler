# Lab Incident Report & Triage: IPS Alert Storm & Process Allowlist Tuning
**Date:** Oct 07, 2026  
**System:** `secopslt` (~/CodeProjects/secops)  
**Severity:** P1-Critical (Simulated Infinite Alert Loop)

## 1. Incident Overview
An active Intrusion Prevention System (IPS) alert storm was triggered by legitimate background processes (`Google` on Port 7679 and `app_inkwe` on Port 57981).

## 2. Root Cause Analysis (RCA)
- **Auto-Restart Loop:** The XDR IPS engine (`xdr_agent.py --contain`) issued a `SIGKILL` to unlisted sockets. Because macOS `launchd` and application watchdogs automatically respawn killed processes under a new PID, an infinite kill-and-respawn loop ensued.
- **SMS Rate Spikes:** Unthrottled alerts were sent on each iteration, causing alert fatigue.

## 3. Engineering Remediation & Hardening
1. **Process & Socket Allowlisting:** Updated `xdr_agent.py` with `ALLOWED_PORTS` (e.g., 7679) and `ALLOWED_PROCESSES` (`Google`, `app_inkwe`, `rapportd`) to exempt verified services.
2. **Alert Rate-Limiting:** Integrated a 15-minute lockfile throttle (`/tmp/secops_sms_throttle.lock`) inside `send_sms_alert.sh` to cap alert velocity.
3. **Daemon Verification:** Re-registered `com.secops.perimeter.audit` and verified 15/15 Pass on `verify_audit_state.sh`.

## 4. Verification & Testing
- **Dry-Run Audit:** Verified zero false positives on active local listeners.
- **Plumbing Verification:** Spawned an isolated test listener (`python3 -m http.server 9998`), confirmed instant `SIGKILL` containment, and verified clean process termination without an auto-restart loop.
