#!/usr/bin/env python3
import os, sys, subprocess

def clear():
    os.system('clear' if os.name == 'posix' else 'cls')

def header():
    print("======================================================================")
    print("             ENDPOINT OPERATIONS & SOC CONTROL PLANE (v2026.2)         ")
    print("======================================================================")
    print(" Workstation: secopslt | Operator: Matt Quijada (mquija9@noviascentialabs.com)")
    print("----------------------------------------------------------------------")

def main_menu():
    clear()
    header()
    print(" [ TELEMETRY & DETECTION ]")
    print("  [1]  audit-perimeter     : macOS Native Firewall & Telemetry Audit")
    print("  [2]  threat-hunter       : PCAP Packet Parser & Anomaly Detection")
    print("  [3]  cloud-hardener      : GCP & Azure Subscription Zero-Trust Hardening")
    print("  [4]  dlp-scrubber        : PII & Credential Scanner")
    print("")
    print(" [ MULTI-CLOUD & IAM AUTOMATION ]")
    print("  [5]  iam-audit-engine    : Entra ID, GCP & Workspace Directory Audit")
    print("  [6]  gcloud-context      : Verify Active GCP Project & ADC Tokens")
    print("")
    print(" [ STUDENT LABS & DOCUMENTATION ]")
    print("  [7]  classify-labs       : Sort WGU Coursework & Cert Labs")
    print("  [8]  view-readme         : Display Master Documentation Index")
    print("")
    print(" [ SYSTEM CONTROL & SYNC ]")
    print("  [9]  verify-all          : Run Zero-Trust 15-Point System Audit")
    print("  [10] sync-github         : Push Code to GitHub & Sync Workspace Backup")
    print("  [0]  exit                : Exit Control Plane")
    print("======================================================================")

def run_cmd(cmd):
    print(f"\n▶ Running: {cmd}\n")
    subprocess.run(cmd, shell=True)
    input("\nPress Enter to return to main menu...")

while True:
    main_menu()
    choice = input("SEC-OPS 🧠 ❯ ").strip()
    if choice == '1':
        run_cmd(f"{os.path.expanduser('~/secops/scripts/test_all_tools.sh')}")
    elif choice == '2':
        run_cmd(f"python3 {os.path.expanduser('~/secops/modules/soc_defense/threat_hunter.py')} --help")
    elif choice == '3':
        run_cmd(f"python3 {os.path.expanduser('~/secops/modules/soc_defense/cloud_hardener.py')} --help")
    elif choice == '4':
        run_cmd(f"python3 {os.path.expanduser('~/secops/secops_sentinel.py')}")
    elif choice == '5':
        run_cmd(f"python3 {os.path.expanduser('~/secops/modules/iam_directory/iam_audit_engine.py')}")
    elif choice == '6':
        run_cmd("gcloud config get-value project && gcloud auth list")
    elif choice == '7':
        run_cmd(f"{os.path.expanduser('~/secops/scripts/classify_labs.sh')}")
    elif choice == '8':
        run_cmd(f"cat {os.path.expanduser('~/secops/docs/README.md')}")
    elif choice == '9':
        run_cmd(f"{os.path.expanduser('~/secops/scripts/verify_audit_state.sh')}")
    elif choice == '10':
        run_cmd(f"{os.path.expanduser('~/secops/scripts/sync_github.sh')}")
    elif choice in ['0', 'exit', 'q']:
        print("\n[*] Exiting Control Plane. Stay secure.")
        sys.exit(0)
