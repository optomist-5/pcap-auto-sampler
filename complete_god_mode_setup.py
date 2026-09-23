#!/usr/bin/env python3
"""
Master 100% SecOps Environment Installer & Auditor
Automatically detects and installs any missing tools to finalize God Mode setup.
"""

import shutil
import subprocess
from pathlib import Path

GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"

TOOLSET = [
    ("brew", "brew", "Homebrew Package Manager", False),
    ("git", "git", "Version Control System", False),
    ("python3", "python", "Python 3 Runtime", False),
    ("gitleaks", "gitleaks", "Git Secret Scanner", False),
    ("jq", "jq", "JSON Processor", False),
    ("wget", "wget", "File Retriever", False),
    ("nmap", "nmap", "Network Scanner", False),
    ("tshark", "wireshark", "Terminal Packet Analyzer", False),
    ("tcpdump", "tcpdump", "Packet Interceptor", False),
    ("az", "azure-cli", "Azure Management CLI", False),
    ("gcloud", "google-cloud-sdk", "Google Cloud SDK CLI", True),
    ("docker", "docker", "Docker Container Engine", True),
    ("/Applications/Visual Studio Code.app", "visual-studio-code", "VS Code IDE", True),
    ("/Applications/Wireshark.app", "wireshark", "Wireshark GUI", True),
]

def check_tool(identifier):
    if identifier.startswith("/Applications"):
        return Path(identifier).exists()
    return shutil.which(identifier) is not None

def run_installation_and_audit():
    print(f"\n{CYAN}{BOLD}=== MACBOOK SECOPS 100% WORKSTATION PROVISIONER ==={RESET}\n")
    
    missing_casks = []
    missing_formulae = []

    for tool_id, pkg_name, desc, is_cask in TOOLSET:
        if not check_tool(tool_id):
            if is_cask:
                missing_casks.append(pkg_name)
            else:
                missing_formulae.append(pkg_name)

    if missing_formulae or missing_casks:
        print(f"{YELLOW}[*] Installing missing dependencies...{RESET}\n")
        if missing_formulae:
            subprocess.run(f"brew install {' '.join(missing_formulae)}", shell=True)
        if missing_casks:
            subprocess.run(f"brew install --cask {' '.join(missing_casks)}", shell=True)
        print(f"\n{GREEN}[+] Installations completed successfully!{RESET}\n")

    # Re-Audit Workspace
    installed_count = 0
    total_tools = len(TOOLSET)

    print(f"{BOLD}---> Final Workstation Audit Status:{RESET}")
    for tool_id, pkg_name, desc, is_cask in TOOLSET:
        if check_tool(tool_id):
            installed_count += 1
            print(f"  [{GREEN}INSTALLED{RESET}] {tool_id:<40} - {desc}")
        else:
            print(f"  [{RED}MISSING{RESET}]   {YELLOW}{tool_id:<40}{RESET} - {desc}")

    score = (installed_count / total_tools) * 100
    print(f"\n{BOLD}" + "=" * 70 + f"{RESET}")
    print(f"{BOLD}FINAL AUDIT SCORE: {installed_count}/{total_tools} Tools Verified ({score:.1f}%){RESET}")
    print(f"{BOLD}" + "=" * 70 + f"{RESET}\n")

    if score == 100.0:
        print(f"{GREEN}{BOLD}🎉 GOD MODE CONFIRMED: 100% Workstation Readiness Achieved!{RESET}\n")

if __name__ == "__main__":
    run_installation_and_audit()
