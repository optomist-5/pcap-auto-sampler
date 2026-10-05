#!/usr/bin/env python3
import os
import sys

def clear_screen():
    os.system('clear')

def print_header():
    print("=====================================================================")
    print("             ENDPOINT OPERATIONS CONTROL PLANE (v2026.2)             ")
    print("=====================================================================")
    print(" Select an operation to execute. Press Ctrl+C or 0 to exit.")
    print("---------------------------------------------------------------------")

def print_menu():
    print("\n[ DETECTION & TELEMETRY ] (Living off the land)")
    print("  [1] audit-perimeter     : Native macOS Telemetry & Firewall Audit")
    print("  [2] audit-threat-hunter : Sentinel Automated Log Parsing")
    print("  [3] audit-dlp-scrubber  : PII & Secret Scanner")

    print("\n[ OPERATIONS & RECOVERY ]")
    print("  [4] ops-secure-backup   : Execute Air-Gapped SSD Sync")
    print("  [5] ops-halt-sync       : Tactical Killswitch (Halt Cloud Daemons)")
    print("  [6] ops-system-purge    : Deep-Clean Memory & Caches")

    print("\n[ ENGINEERING & DIAGNOSTICS ]")
    print("  [7] dev-ai-context      : Launch LLM Context Engine")
    print("  [8] dev-threat-model    : Extract Threat Models")
    print("  [9] dev-dfir-image      : Execute Digital Forensic Imaging")

    print("\n[ VIRTUALIZATION & CONTAINERS ] (Safe Sandboxed Labs)")
    print("  [11] vm-kali-desktop    : Launch Kali Linux VM (via UTM)")
    print("  [12] vm-ubuntu-cli      : Launch Ubuntu Server (via Multipass)")
    print("  [13] cnt-docker-start   : Start Docker Container Engine")

    print("\n[ ADVANCED SOC & DFIR ]")
    print("  [14] soc-net-capture    : Launch Network Packet Capture (Wireshark)")
    print("  [15] dfir-artifacts     : Collect macOS Artifacts (Plists & Logs)")

    print("\n[ SYSTEM CONTROL ]")
    print("  [10] sys-env-config     : Load Workstation Environment Variables")
    print("  [0]  Exit Control Plane")
    print("=====================================================================")

def execute_command(choice):
    commands = {
        '1': "~/secops/bin/audit_perimeter.sh",
        '2': "python3 ~/secops/audit_threat_hunter.py",
        '3': "python3 ~/secops/audit_dlp_scrubber.py",
        '4': "python3 ~/secops/ops_secure_backup.py",
        '5': "~/secops/ops_halt_sync_daemons.sh",
        '6': "~/secops/ops_system_purge.sh",
        '7': "~/secops/dev_ai_context.zsh",
        '8': "cd ~/Desktop/TM_Extraction_Tools && sudo python3 dev_threat_modeler.py",
        '9': "python3 ~/secops/dev_dfir_imager.py",
        '10': "python3 ~/secops/bin/sys_env_config.py",
        
        # --- NEW ADDITIONS ---
        '11': "open -a UTM || echo '[!] UTM not installed. Download from mac.getutm.app'", 
        '12': "multipass shell primary || echo '[!] Multipass not found. Download from multipass.run'",
        '13': "open -a Docker || echo '[!] Docker not installed. Download from docker.com'",
        '14': "open -a Wireshark || sudo tcpdump -i en0 -c 100", 
        '15': "mkdir -p ~/Desktop/DFIR_Collection && cp -r /Library/Preferences/SystemConfiguration ~/Desktop/DFIR_Collection/ 2>/dev/null && echo 'Artifacts collected to Desktop!'"
    }

    if choice == '0':
        print("\n[*] Exiting Control Plane. Stay secure.")
        sys.exit(0)
    elif choice in commands:
        print(f"\n[*] Executing: {commands[choice]}\n")
        os.system(commands[choice])
        print("\n[*] Execution complete. Press Enter to return to the menu.")
        input()
    else:
        print("\n[!] Invalid selection. Please try again.")
        input("Press Enter to continue...")

def main():
    while True:
        clear_screen()
        print_header()
        print_menu()
        try:
            choice = input("\nSEC-OPS 🧠 ❯ ")
            execute_command(choice)
        except KeyboardInterrupt:
            print("\n\n[*] Exiting Control Plane. Stay secure.")
            sys.exit(0)

if __name__ == "__main__":
    main()
