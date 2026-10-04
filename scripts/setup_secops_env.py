#!/usr/bin/env python3
"""
Master Workstation Provisioner & Auditor
Audits and installs all core CLI utilities, security binaries, and workspace safeguards.
"""

import os
import shutil
import subprocess
import sys

# Color Palette
GREEN = "\033[1;32m"
RED = "\033[1;31m"
YELLOW = "\033[1;33m"
CYAN = "\033[1;36m"
RESET = "\033[0m"

CORE_BREW_TOOLS = [
    "wireshark",     # Includes tshark binary
    "gitleaks",      # Pre-commit secret scanner
    "nmap",          # Network discovery & port scanner
    "jq",            # Command-line JSON processor
    "azure-cli",     # Azure cloud management
    "wget"           # File retriever
]

def check_command(cmd):
    return shutil.which(cmd) is not None

def audit_and_install():
    print(f"\n{CYAN}================ 🛡️ SECOPS WORKSTATION PROVISIONER 🛡️ ================{RESET}\n")
    missing_brew = []

    # 1. Audit Homebrew Tools
    for tool in CORE_BREW_TOOLS:
        check_cmd = "tshark" if tool == "wireshark" else ("az" if tool == "azure-cli" else tool)
        if check_command(check_cmd):
            print(f"  [{GREEN}INSTALLED{RESET}] {tool:<15} - Ready for operations")
        else:
            print(f"  [{RED}MISSING{RESET}]   {tool:<15} - Marked for installation")
            missing_brew.append(tool)

    # 2. Automatically Offer Installation
    if missing_brew:
        print(f"\n{YELLOW}[*] Missing {len(missing_brew)} required security tools.{RESET}")
        choice = input("Would you like to install them now via Homebrew? (y/N): ").strip().lower()
        if choice == 'y':
            print(f"\n{CYAN}[*] Running Homebrew installation...{RESET}")
            cmd = f"brew install {' '.join(missing_brew)}"
            subprocess.run(cmd, shell=True)
            print(f"{GREEN}[+] Workstation provisioned successfully!{RESET}")
    else:
        print(f"\n{GREEN}[🎉] GOD MODE CONFIRMED: All core tools installed and ready for threat hunting!{RESET}\n")

if __name__ == "__main__":
    audit_and_install()
