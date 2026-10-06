#!/usr/bin/env python3
import os, sys, time, subprocess
from datetime import datetime

def run_cmd(cmd):
    try:
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return res.stdout.strip(), res.stderr.strip(), res.returncode
    except Exception as e:
        return "", str(e), 1

def Rogue_Process_Containment():
    print("\n🚨 === PLAYBOOK 1: ROGUE PROCESS & SOCKET CONTAINMENT ===")
    target = input("Enter Target Port or PID to isolate: ").strip()
    if not target: return
    out, _, _ = run_cmd(f"lsof -i :{target} -t") if target.isdigit() and len(target) <= 5 else (target, "", 0)
    pid = out.split()[0] if out else target
    proc_info, _, _ = run_cmd(f"ps -p {pid} -o pid,ppid,user,%cpu,%mem,start,command")
    print(f"\n📋 Process Telemetry:\n{proc_info}")
    if input(f"\n⚠️ Terminate PID {pid}? (y/N): ").strip().lower() == 'y':
        run_cmd(f"kill -STOP {pid}")
        time.sleep(1)
        run_cmd(f"kill -9 {pid}")
        print(f"✅ Process {pid} neutralized!")

def Persistence_LaunchDaemon_Hunter():
    print("\n🔍 === PLAYBOOK 2: PERSISTENCE HUNTER ===")
    for p in ["/Library/LaunchDaemons", "/Library/LaunchAgents", os.path.expanduser("~/Library/LaunchAgents")]:
        if os.path.exists(p):
            print(f"\n📁 Inspecting: {p}")
            for f in os.listdir(p):
                print(f"  ├─ {f}")

def Host_Network_Quarantine():
    print("\n🛡️ === PLAYBOOK 3: HOST NETWORK QUARANTINE ===")
    if input("⚠️ Isolate host from network via PF Firewall? (y/N): ").strip().lower() == 'y':
        run_cmd("echo 'block drop all\npass quick on lo0 all' | sudo pfctl -e -f - 2>/dev/null")
        print("✅ Host Network Isolation Enforced.")

def Rapid_Forensic_Triage_SBAR():
    print("\n📊 === PLAYBOOK 4: FORENSIC TRIAGE SBAR ===")
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sockets, _, _ = run_cmd("lsof -i -P -n | grep LISTEN | head -n 10")
    report = f"# 🚨 INCIDENT RESPONSE SBAR REPORT\n**Timestamp:** {now}\n\n## Background\nActive Listening Sockets:\n```\n{sockets}\n```"
    path = os.path.expanduser("~/secops/docs/IR_TRIAGE_SBAR_LATEST.md")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f: f.write(report)
    print(f"✅ SBAR generated at: {path}")

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "contain": Rogue_Process_Containment()
    elif cmd == "persistence": Persistence_LaunchDaemon_Hunter()
    elif cmd == "quarantine": Host_Network_Quarantine()
    elif cmd == "sbar": Rapid_Forensic_Triage_SBAR()
