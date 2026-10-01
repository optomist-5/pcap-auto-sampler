# SecOps Laboratory Operational Troubleshooting & Incident Post-Mortem
**Author:** Matt (optomist5)  
**Environment:** macOS (Apple Silicon) | Zsh Shell | Python 3.14 Virtual Environment  
**Repository Target:** `optomist-5/pcap-auto-sampler.git`  
**Security Standard:** Enterprise DevSecOps Hygiene & Sanitization Matrix  

---

## Executive Summary
This post-mortem documents real-time terminal errors, environment ambiguities, shell execution failures, and their technical resolutions encountered during the engineering of the `pcap-auto-sampler` threat detection pipeline. Documenting operational anomalies establishes root-cause analysis (RCA) patterns required for Tier-2/3 Security Operations Center (SOC) and DevSecOps engineering roles.

---

## Operational Incident & Troubleshooting Matrix

| Incident ID | Observed Error / Symptom | Technical Root Cause | Engineering Resolution & Prevention |
| :--- | :--- | :--- | :--- |
| **INC-001** | `zsh: event not found: /usr/bin/env` | Zsh history expansion treats exclamation marks (`!`) followed by text as an interactive event trigger. | Executed `setopt no_bang_hist` in `~/.zshrc` to permanently disable bang history expansion. |
| **INC-002** | `zsh: parse error near '}'` | Raw Python block containing closing braces (`}`) pasted directly into interactive Zsh shell. | Implemented `cat << 'EOF' > file.py` heredoc streaming to write code blocks directly to disk without shell parsing. |
| **INC-003** | `zsh: command not found: optomist5` | Prompt string (`optomist5 secops% `) manually typed or pasted back into the command line. | Corrected shell usage: prompt string is shell-generated output; commands are issued after the `% ` delimiter. |
| **INC-004** | Python REPL (`>>>`) launched unexpectedly | Executed Python binary path (`/Users/mq/secops/venv/bin/python3`) without a target script or argument. | Issued `exit()` or `Ctrl+D` to terminate interactive REPL and restore Zsh execution. |
| **INC-005** | `zsh: no such file or directory: ./sync_pipeline.sh` | Local script was missing from directory state following an uncommitted file cleanup sweep. | Re-architected `sync_pipeline.sh` directly on disk and set POSIX execution bits (`chmod +x`). |
| **INC-006** | Duplicate `pyvenv.cfg` detected | Both `~/secops/pyvenv.cfg` and `~/secops/venv/pyvenv.cfg` existed on disk simultaneously. | Purged root `pyvenv.cfg` to eliminate package path resolution ambiguity between root and virtual environment. |

---

## CompTIA Network+ & Security+ Exam Mapping
* **Network+ Domain 5.0 (Network Troubleshooting):** Identifying syntax errors, binary path mismatches, and execution permission flags (`chmod +x`).
* **Security+ Domain 4.0 (Security Operations):** Root Cause Analysis (RCA), post-mortem incident reporting, and environment isolation.

