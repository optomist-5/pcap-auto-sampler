#!/usr/bin/env python3
import sys
import subprocess

def check_network():
    print("=== [SecOps Sentinel] Active TCP Sockets ===")
    subprocess.run("netstat -an -f inet | grep TCP", shell=True)

def check_system():
    print("=== [SecOps Sentinel] System Baseline ===")
    subprocess.run(["uptime"])
    subprocess.run(["df", "-h", "/"])

def main():
    if len(sys.argv) < 2:
        print("Usage: secops_sentinel.py [net|sys]")
        sys.exit(1)

    cmd = sys.argv[1].lower()
    if cmd in ["net", "nett"]:
        check_network()
    elif cmd in ["sys", "system"]:
        check_system()
    else:
        print(f"Unknown command: {cmd}")

if __name__ == "__main__":
    main()
