# Native macOS Living-off-the-Land (LotL) & Zero-Trust SecOps Platform
### Production Endpoint Containment, Privilege Isolation & Operational Reliability
[Architecture Documentation](./docs/) | [Incident Post-Mortems](./docs/cert_labs/) | [License: MIT](./LICENSE)

---

## 🛡️ Executive Summary
This repository contains a hardened, zero-trust host security platform engineered natively on macOS Apple Silicon. It operates entirely using native UNIX and macOS subsystems ("Living off the Land") without relying on third-party commercial endpoint agents.

Key capabilities include:
1. **Host-Level Intrusion Prevention (IPS):** Real-time socket monitoring (`lsof`), automated rogue process termination (`SIGKILL`), and dynamic `pfctl` packet-filtering network isolation.
2. **Multi-Tier Surveillance & Alert Fatigue Mitigation:** Decoupled silent background watchdogs (`launchd`) running hourly scans from a centralized **09:00 AM Warden executive briefing** (`warden.sh`).
3. **Multi-Cloud Zero-Trust IAM Architecture:** Air-gapped **3-Account Privilege Isolation Matrix** governing administrative boundaries across Entra ID, Azure, GCP, and Google Workspace.
4. **Resilience Engineering:** Automated SMS notification throttles via lockfile mechanics (`/tmp/secops_sms_throttle.lock`) to prevent notification storms.

---

## 📐 Architecture & Subsystems



┌────────────────────────────────────────────────────────────────────────┐
│                   MACOS ENDPOINT SECURITY CONTROLS                     │
└────────────────────────────────────────────────────────────────────────┘
│
┌────────────────────────────┼────────────────────────────┐
▼                            ▼                            ▼
[Hourly Silent Watchdog]   [Warden 09:00 Digest]       [Active IPS Engine]
com.secops.perimeter.audit com.secops.warden.plist secops_sentinel.py

⚬ Runs audit_perimeter.sh   - Runs warden.sh           - Inspects TCP/UDP

⚬ Silent log heartbeats     - 15/15 control check      - Socket allowlisting

⚬ 0 noise on clean state    - Dispatches morning SMS   - Instant SIGKILL


---

## 📂 Repository Layout & Verified Modules

```text
├── bin/
│   └── warden.sh                  # 09:00 AM Daily Briefing & Health Verifier
├── scripts/
│   ├── secops_sentinel.py         # Autonomous socket inspection & containment engine
│   ├── verify_audit_state.sh      # 15/15 Zero-Trust verification test suite
│   ├── audit_perimeter.sh         # Silent hourly watchdog executor
│   ├── send_sms_alert.sh          # Alert delivery with 15-minute lockfile throttle
│   └── sync_github.sh             # Cloud archive and Git sync pipeline
├── docs/
│   └── cert_labs/
│       ├── LAB_ALERT_STORM_TRIAGE.md        # Triage post-mortem: IPS auto-restart loops
│       └── LAB2_ENDPOINT_THREAT_HUNT.md     # EDR socket audit & process lineage


🔬 Featured Production Retrospective

⚬ Incident Post-Mortem: IPS Alert Storm & Allowlist Tuning: Detailed technical post-mortem analyzing an automated kill-and-respawn cascade caused by launchd supervision, and the engineering of process allowlists and cooldown lockfiles to eliminate alert fatigue.
