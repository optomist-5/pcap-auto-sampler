#!/usr/bin/env python3
import os, sys, subprocess

def clear():
    os.system('clear' if os.name == 'posix' else 'cls')

def header():
    print("======================================================================")
    print("          ENDPOINT OPERATIONS & XDR/SIEM CONTROL PLANE (v2026.2)       ")
    print("======================================================================")
    print(" Workstation: secopslt | Operator: Matt Quijada (mquija9@noviascentialabs.com)")
    print(" Framework: Native XDR / IDS / IPS / SIEM Active Telemetry Architecture")
    print("----------------------------------------------------------------------")

def main_menu():
    clear()
    header()
    print(" [ ENTERPRISE XDR / IDS / IPS / SIEM ENGINE ]")
    print("  [1]  audit-perimeter     : macOS Native Firewall & Telemetry Audit")
    print("  [2]  xdr-ids-scan        : Run IDS Perimeter Socket & Persistence Scan")
    print("  [3]  xdr-ips-contain     : Run Active IPS Engine (Auto-Terminate Threats)")
    print("  [4]  siem-dashboard      : Display Central SIEM Event Telemetry Log")
    print("  [5]  threat-hunter       : PCAP Packet Parser & Anomaly Detection")
    print("  [6]  cloud-hardener      : GCP & Azure Subscription Zero-Trust Hardening")
    print("  [7]  dlp-scrubber        : PII & Credential Scanner")
    print("")
    print(" [ SYSADMIN & OS OPERATIONS ]")
    print("  [8]  sysadmin-vitals     : Workstation Hardware, Storage & Alias Audit")
    print("  [9]  tailscale-status    : Inspect Private Mesh Network Peering")
    print("  [10] ops-system-purge    : Deep-Clean Temp Caches & Build Files")
    print("")
    print(" [ COMMUNICATIONS & RADIO DISPATCH ]")
    print("  [11] radio-dispatch      : Transmit iMessage/Radio Signal (MQ, Mau, Custom)")
    print("")
    print(" [ MULTI-CLOUD & IAM AUTOMATION ]")
    print("  [12] iam-audit-engine    : Entra ID, GCP & Workspace Directory Audit")
    print("  [13] gcloud-context      : Verify Active GCP Project & ADC Tokens")
    print("")
    print(" [ ADVANCED SOC & DFIR DIAGNOSTICS ]")
    print("  [14] dfir-artifacts     : Collect macOS Persistence & Log Artifacts")
    print("  [15] soc-net-capture    : Inspect Active Network Connections & Sockets")
    print("")
    print(" [ STUDENT LABS & DOCUMENTATION ]")
    print("  [16] classify-labs       : Sort WGU Coursework & Cert Labs")
    print("  [17] view-readme         : Display Master Documentation Index")
    print("")
    print(" [ SYSTEM CONTROL & SYNC ]")
    print("  [18] verify-all          : Run Zero-Trust 15-Point System Audit")
    print("  [19] sync-github         : Push Code to GitHub & Sync Workspace Backup")
    print("  [0]  exit                : Exit Control Plane")
    print("======================================================================")

def run_cmd(cmd):
    print(f"\n▶ Running: {cmd}\n")
    subprocess.run(cmd, shell=True)
    input("\nPress Enter to return to main menu...")

def interactive_radio():
    print("\n📻 --- SEC-OPS RADIO DISPATCHER ---")
    print("Select Recipient Preset or Enter Custom Contact:")
    print("  [1] Radio MQ  (Self - mquija9@icloud.com)")
    print("  [2] Radio Mau (Husband - Enter Phone # or Apple ID)")
    print("  [3] Custom Target (Enter Phone Number or Email)")
    
    choice = input("\nSelect Option [1-3]: ").strip()
    
    if choice == '1':
        recipient = "mquija9@icloud.com"
    elif choice == '2':
        recipient = input("Enter Mau's Phone Number or Apple ID: ").strip()
    elif choice == '3':
        recipient = input("Enter Recipient Phone Number or Email: ").strip()
    else:
        print("Invalid selection.")
        input("Press Enter to return...")
        return

    if not recipient:
        print("❌ Error: Recipient cannot be empty.")
        input("Press Enter to return...")
        return

    msg = input(f"Enter Radio Message for [{recipient}]: ").strip()
    if not msg:
        msg = "Routine radio check signal from secopslt."

    script_path = os.path.expanduser('~/secops/scripts/radio.sh')
    subprocess.run(f'"{script_path}" "{recipient}" "{msg}"', shell=True)
    input("\nPress Enter to return to main menu...")

while True:
    main_menu()
    choice = input("SEC-OPS 🧠 ❯ ").strip()
    if choice == '1':
        run_cmd(f"{os.path.expanduser('~/secops/scripts/test_all_tools.sh')}")
    elif choice == '2':
        run_cmd(f"python3 {os.path.expanduser('~/secops/modules/soc_defense/xdr_agent.py')}")
    elif choice == '3':
        run_cmd(f"python3 {os.path.expanduser('~/secops/modules/soc_defense/xdr_agent.py')} --contain")
    elif choice == '4':
        run_cmd(f"python3 {os.path.expanduser('~/secops/modules/soc_defense/siem_engine.py')} --show")
    elif choice == '5':
        run_cmd(f"python3 {os.path.expanduser('~/secops/modules/soc_defense/threat_hunter.py')} --help")
    elif choice == '6':
        run_cmd(f"python3 {os.path.expanduser('~/secops/modules/soc_defense/cloud_hardener.py')} --help")
    elif choice == '7':
        run_cmd(f"python3 {os.path.expanduser('~/secops/secops_sentinel.py')}")
    elif choice == '8':
        run_cmd(f"python3 {os.path.expanduser('~/secops/modules/sysadmin/sysadmin_engine.py')}")
    elif choice == '9':
        run_cmd("tailscale status 2>/dev/null || echo 'Tailscale CLI not active.'")
    elif choice == '10':
        run_cmd("rm -rf $HOME/Library/Caches/tmp_secops_* 2>/dev/null && echo '✅ Cache purged.'")
    elif choice == '11':
        interactive_radio()
    elif choice == '12':
        run_cmd(f"python3 {os.path.expanduser('~/secops/modules/iam_directory/iam_audit_engine.py')}")
    elif choice == '13':
        run_cmd("gcloud config get-value project && gcloud auth list")
    elif choice == '14':
        run_cmd("ls -la $HOME/Library/LaunchAgents")
    elif choice == '15':
        run_cmd("lsof -i -P -n | grep LISTEN")
    elif choice == '16':
        run_cmd(f"{os.path.expanduser('~/secops/scripts/classify_labs.sh')}")
    elif choice == '17':
        run_cmd(f"cat {os.path.expanduser('~/secops/docs/README.md')}")
    elif choice == '18':
        run_cmd(f"{os.path.expanduser('~/secops/scripts/verify_audit_state.sh')}")
    elif choice == '19':
        run_cmd(f"{os.path.expanduser('~/secops/scripts/sync_github.sh')}")
    elif choice in ['0', 'exit', 'q']:
        print("\n[*] Exiting Control Plane. Stay secure.")
        sys.exit(0)
