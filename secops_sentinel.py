#!/usr/bin/env python3
"""
==============================================================================
SECOPS SENTINEL PLATFORM - CORE CLI ENGINE
Operator: mq (optomist-5) | Environment: macOS Darwin
==============================================================================
"""
import os
import sys
import subprocess

def sys_metrics():
    print("📊 [SYSTEM METRICS]")
    os.system("uptime")
    os.system("df -h /")

def net_sockets():
    print("🌐 [ACTIVE SOCKETS]")
    os.system("lsof -i -P -n | grep LISTEN")

def scrub_vault():
    print("🧹 [VAULT SCRUBBER]")
    print("Scrubbing temporary files and cache entries...")
    os.system("rm -rf ~/.cache/tmp_* /tmp/secops_* 2>/dev/null || true")
    print("✅ Scrub complete.")

def main():
    if len(sys.argv) < 2 or sys.argv[1] in ["-h", "--help"]:
        print("Usage: python3 secops_sentinel.py [sys|net|scrub]")
        return
    
    cmd = sys.argv[1].lower()
    if cmd == "sys":
        sys_metrics()
    elif cmd == "net":
        net_sockets()
    elif cmd == "scrub":
        scrub_vault()
    else:
        print(f"Unknown command: {cmd}. Use 'sys', 'net', or 'scrub'.")

if __name__ == "__main__":
    main()
