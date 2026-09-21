# Executive Retrospective: Automated PCAP Ingestion Pipeline

**Author:** Matt (`optomist-5`)  
**Target Domain:** Security Operations Center (SOC) / Threat Detection Engineering  
**Completion Date:** September 20, 2026  
**Repository:** [https://github.com/optomist-5/pcap-auto-sampler](https://github.com/optomist-5/pcap-auto-sampler)

---

## 1. Project Overview & Architectural Intent
This project builds a lightweight, self-sustaining network traffic sampling pipeline designed to run periodically on edge endpoints. Full-packet capture (FPC) across enterprise networks generates terabytes of data daily, quickly overwhelming storage infrastructure and SIEM ingestion limits. 

By implementing an automated sampling baseline (capturing 2,500 packets or 300 seconds of activity weekly), this project demonstrates an enterprise-relevant strategy for:
- **Protocol Baseline Ingestion:** Capturing recurring broadcast, multicast, DNS, and TLS handshake patterns without filling disk arrays.
- **Detection Engineering Testing:** Providing clean, lightweight `.pcap` baseline samples to validate threat detection rules (e.g., Snort/Zeek/Sigma) against real environment background noise.
- **Storage-Conscious Audit Logging:** Maintaining rolling historical captures (< 5 MB per sample) for post-incident threat hunting.

---

## 2. Technical Stack & Implementation Mechanics

| Layer | Component | Technical Role |
| :--- | :--- | :--- |
| **Language & Engine** | Python 3 + `Scapy` | Raw socket creation, packet filter execution, and PCAP writing (`wrpcap`). |
| **Operating System** | macOS / Unix (`en0`) | Native network interface binding for raw frame ingestion. |
| **System Automation** | Root `crontab` | Low-level daemon scheduling (`0 2 * * 0`) running tasks with elevated privileges. |
| **Version Control** | Git + GitHub | Operational code tracking, `.gitignore` artifact exclusion, and MIT licensing. |
| **Authentication** | Personal Access Token (PAT) | Cryptographically scoped token auth (`repo` permissions) replacing deprecated password auth. |

---

## 3. Key Operational Learnings & Troubleshooting Log

### A. Terminal Execution vs. File Content Separation
- **Challenge:** Directly pasting raw Python code or configuration parameters into the Zsh command line caused syntax errors (`command not found: #`, `2.5.0 not found`).
- **Resolution:** Implemented `cat << 'EOF'` heredoc redirection to safely stream code blocks into disk files without Zsh attempting to evaluate lines as shell commands.

### B. Linux / macOS Security Boundaries
- **Challenge:** Network socket sniffing requires administrative (`root`) privileges. Standard user cron jobs fail silently when attempting raw packet capture.
- **Resolution:** Bound the Python virtual environment executable (`/Users/mq/pcap-auto-sampler/venv/bin/python3`) inside the **root crontab** (`sudo crontab -e`). Recognized that `sudo` requires the local macOS administrator screen-unlock password, distinct from web authentication tokens.

### C. Git Version Control & Repository Reconciliation
- **Challenge:** Pushing code was initially blocked due to two factors: GitHub's deprecation of plain password authentication over HTTPS, and a remote-branch conflict caused by GitHub generating a default `LICENSE` file online.
- **Resolution:** Configured local merge strategies (`git config pull.rebase false`), executed an unrelated-history pull (`git pull origin main --allow-unrelated-histories --no-edit`), and authenticated using a scoped Personal Access Token (`ghp_...`).

---

## 4. Verification & Operational Status
- **Manual Capture Validation:** Tested on interface `en0`; captured 1,245 frames (532.97 KB) stored in timestamped format (`./captures/sample_2026-09-20_19-52-23.pcap`).
- **Cron Active Verification:** Confirmed active via `sudo crontab -l` to execute every Sunday at 02:00 AM (`0 2 * * 0`).
- **GitHub Deployment:** Codebase, documentation, `.gitignore` rules, and MIT license synchronized with `origin/main`.
