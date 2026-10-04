#!/usr/bin/env python3
import shutil
from pathlib import Path

GREEN = "\033[92m"; RED = "\033[91m"; YELLOW = "\033[93m"; CYAN = "\033[96m"; BOLD = "\033[1m"; RESET = "\033[0m"

TOOLSET = {
    "Core Environment": [
        ("brew", "Homebrew Package Manager"),
        ("git", "Version Control System"),
        ("python3", "Python 3 Runtime"),
        ("gitleaks", "Git Secret Scanner"),
        ("jq", "JSON Processor"),
        ("wget", "File Retriever"),
    ],
    "Networking & Traffic Analysis": [
        ("nmap", "Network Scanner"),
        ("tshark", "Terminal Packet Analyzer"),
        ("tcpdump", "Packet Interceptor"),
    ],
    "Multi-Cloud CLIs": [
        ("az", "Azure Management CLI"),
        ("gcloud", "Google Cloud SDK CLI"),
        ("docker", "Docker Container Engine"),
    ],
    "GUI Applications": [
        ("/Applications/Visual Studio Code.app", "VS Code IDE"),
        ("/Applications/Wireshark.app", "Wireshark GUI"),
    ],
}

def run_audit():
    print(f"\n{CYAN}{BOLD}=== MACBOOK SECOPS WORKSTATION AUDIT ==={RESET}\n")
    total, installed = 0, 0
    for category, tools in TOOLSET.items():
        print(f"{BOLD}---> {category}{RESET}")
        for tool_path, desc in tools:
            total += 1
            is_present = Path(tool_path).exists() if tool_path.startswith("/Applications") else (shutil.which(tool_path) is not None)
            if is_present:
                installed += 1
                print(f"  [{GREEN}INSTALLED{RESET}] {tool_path:<35} - {desc}")
            else:
                print(f"  [{RED}MISSING{RESET}]   {YELLOW}{tool_path:<35}{RESET} - {desc}")
        print()
    print(f"{BOLD}AUDIT SCORE: {installed}/{total} Tools Verified ({(installed/total)*100:.1f}%){RESET}\n")

if __name__ == "__main__":
    run_audit()
