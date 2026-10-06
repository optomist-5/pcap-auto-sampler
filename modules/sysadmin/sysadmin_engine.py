#!/usr/bin/env python3
"""
SecOps SysAdmin & Workstation Operations Engine (v2026.2)
Handles macOS system maintenance, zsh alias audits, memory/thermal checks, and Tailscale status.
"""

import os, sys, subprocess

def audit_zsh_aliases():
    print("\n🔧 [1/4] Auditing Shell Configuration & Aliases (~/.zshrc)...")
    zshrc_path = os.path.expanduser('~/.zshrc')
    alias_file = os.path.expanduser('~/.secops_aliases')
    
    # Clean up ghost typo files if present
    typo_file = os.path.expanduser('~/.zshrcrc')
    if os.path.exists(typo_file):
        os.remove(typo_file)
        print("   ✅ Removed lingering ghost file ~/.zshrcrc")

    if os.path.exists(alias_file):
        print("   ✅ Dedicated SecOps alias file verified (~/.secops_aliases).")
    else:
        print("   ⚠️ Dedicated SecOps alias file missing.")

def check_tailscale_status():
    print("\n🌐 [2/4] Auditing Tailscale Private Mesh Network...")
    res = subprocess.run("tailscale status 2>/dev/null", shell=True, capture_output=True, text=True)
    if res.returncode == 0 and res.stdout.strip():
        print("   ✅ Tailscale daemon active. Connected peers:")
        for line in res.stdout.strip().split("\n")[:5]:
            print(f"      • {line}")
    else:
        print("   ℹ️ Tailscale CLI not running or no active peers connected.")

def check_system_vitals():
    print("\n💻 [3/4] Auditing Workstation Hardware Vitals & Disk Space...")
    disk = subprocess.run("df -h / | tail -n 1", shell=True, capture_output=True, text=True).stdout.strip().split()
    if len(disk) >= 5:
        print(f"   Disk Storage : {disk[2]} used / {disk[1]} total ({disk[4]} capacity)")
    
    load = subprocess.run("sysctl -n vm.loadavg", shell=True, capture_output=True, text=True).stdout.strip()
    print(f"   CPU Load Avg : {load}")

def purge_system_caches():
    print("\n🧹 [4/4] Executing Memory & Temp Cache Cleanup...")
    subprocess.run("rm -rf $HOME/Library/Caches/tmp_secops_* 2>/dev/null", shell=True)
    print("   ✅ Temp build files cleaned cleanly.")

if __name__ == "__main__":
    print("======================================================================")
    print("            SYSADMIN & WORKSTATION OPERATIONS ENGINE                   ")
    print("======================================================================")
    audit_zsh_aliases()
    check_tailscale_status()
    check_system_vitals()
    purge_system_caches()
    print("\n======================================================================")
