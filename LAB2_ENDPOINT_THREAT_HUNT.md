# Lab 2: macOS Endpoint Threat Hunting & Socket Audit

**Author:** Matt (`optomist-5`)  
**Target Domain:** Endpoint Detection & Response (EDR) / Threat Hunting  
**Completion Date:** September 21, 2026  
**Repository:** [https://github.com/optomist-5/pcap-auto-sampler](https://github.com/optomist-5/pcap-auto-sampler)

---

## 1. Executive Summary & Objective
This lab establishes an operational baseline for macOS endpoint triage. Rather than relying on automated black-box cleanup utilities, this project applies native Unix forensic commands (`launchctl`, `lsof`, `ps`, `csrutil`) to audit background persistence mechanisms, investigate open network sockets, verify process lineage, and validate core operating system integrity controls.

---

## 2. Technical Audit Framework & Commands

| Audit Domain | Native Unix Command | Forensic Purpose |
| :--- | :--- | :--- |
| **Persistence Mechanics** | `ls -la ~/Library/LaunchAgents /Library/LaunchAgents /Library/LaunchDaemons` | Inspect background jobs configured to run at user login or system boot with `root` privileges. |
| **Active Sockets** | `sudo lsof -i -P -n \| grep LISTEN` | Audit open network ports bound to local or external network interfaces. |
| **Process Lineage** | `ps aux \| grep <PID>` | Trace process IDs to their full executable path on disk to verify binary authenticity. |
| **OS Integrity** | `csrutil status`, `spctl --status`, `fdesetup status` | Confirm enforcement of System Integrity Protection (SIP), Gatekeeper, and FileVault disk encryption. |

---

## 3. Investigation Findings & Forensic Deductions

### A. Persistence Analysis
- **Microsoft Defender & DLP:** Identified active daemons (`com.microsoft.wdav.*`, `com.microsoft.fresno.*`). Verified as legitimate personal Microsoft 365 security software providing active endpoint file scanning.
- **Grammarly Desktop:** Identified user agents (`com.grammarly.ProjectLlama.*`). Confirmed `ProjectLlama` as Grammarly's internal macOS application framework.

### B. Network Socket Correlation
- **Loopback Sockets (`127.0.0.1`):** Discovered process `app_inkwe` listening on TCP port `49222`. Traced via PID correlation (`ps aux`) to `/Applications/Grammarly Desktop.app/.../app_inkwell`.
- **Inter-Process Communication (IPC):** Validated that `app_inkwell` uses local loopback sockets to transmit text analysis data between the visual UI and background rendering helper.
- **Network-Exposed Sockets (`*`):** Identified `rapportd` (AirDrop/Continuity) and `ControlCenter` (AirPlay Receiver on ports 5000/7000).

### C. OS Protection Verification
- **SIP:** Active (`csrutil status: enabled`). Kernel files protected from modification.
- **Gatekeeper:** Active (`spctl: assessments enabled`). Enforces code signing and notarization.
- **FileVault:** Active (`fdesetup: FileVault is On`). XTS-AES full-disk encryption enforced at rest.

---

## 4. SOC Takeaways & Methodology
This lab demonstrates the primary EDR triage lifecycle:
1. **Detect** open ports (`lsof`).
2. **Correlate** ports to PIDs (`ps`).
3. **Verify** execution paths against known baseline applications.
4. **Validate** native kernel and disk protection mechanisms.
