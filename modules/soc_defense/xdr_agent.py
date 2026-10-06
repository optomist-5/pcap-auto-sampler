#!/usr/bin/env python3
"""
SecOps Active XDR & IPS Containment Agent (v2026.2)
Enforces 4-Tier Triage & Native iMessage Alerts
"""

import os, sys, subprocess, signal

# Add module directory to Python path for seamless imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from siem_engine import log_event

# Approved systemic listening ports baseline
APPROVED_PORTS = {22, 80, 443, 53, 5353, 631}
# Standard benign macOS system processes
APPROVED_PROCESSES = {"rapportd", "mDNSResponder", "cupsd"}

def dispatch_imessage(tier, msg):
    """Sends native AppleScript iMessage alert to primary Apple ID."""
    script_path = os.path.expanduser('~/secops/scripts/send_sms_alert.sh')
    payload = f"[{tier}] {msg}"
    subprocess.run(f'"{script_path}" "{payload}"', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def audit_sockets_and_ips(auto_contain=False):
    print("\n🔍 [IDS Engine] Scanning open network sockets...")
    cmd = "lsof -i -P -n | grep LISTEN"
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    anomalies = []
    if res.stdout:
        for line in res.stdout.strip().split("\n"):
            parts = line.split()
            if len(parts) >= 9:
                proc = parts[0]
                pid = parts[1]
                addr = parts[8]
                if ":" in addr:
                    port_str = addr.split(":")[-1].split("->")[0]
                    if port_str.isdigit():
                        port = int(port_str)
                        if port not in APPROVED_PORTS and proc not in APPROVED_PROCESSES:
                            anomalies.append({'proc': proc, 'pid': int(pid), 'port': port, 'raw': line})

    if anomalies:
        print(f"\n🚨 [P1 CRITICAL DETECTED] {len(anomalies)} Unauthorized Socket(s) Active!")
        for item in anomalies:
            alert_msg = f"CRITICAL: Unauthorized Process '{item['proc']}' (PID: {item['pid']}) listening on Port {item['port']}!"
            print(f"   ❌ Threat: {alert_msg}")
            
            # Log to SIEM
            log_event("UNAUTHORIZED_LISTENING_PORT", "CRITICAL", "xdr_agent", alert_msg, "T1046", {"pid": item['pid'], "port": item['port']})
            
            # Dispatch P1 Alert to Phone
            dispatch_imessage("P1-CRITICAL 🚨", alert_msg)
            
            # IPS Active Response
            if auto_contain:
                print(f"   ⚡ [IPS ACTIVATED] Terminating rogue PID {item['pid']}...")
                try:
                    os.kill(item['pid'], signal.SIGKILL)
                    contain_msg = f"IPS Engine successfully terminated rogue PID {item['pid']} on Port {item['port']}."
                    print(f"   ✅ [IPS CONTAINED] {contain_msg}")
                    log_event("IPS_ACTIVE_CONTAINMENT", "HIGH", "xdr_agent", contain_msg, "T1562.001")
                    dispatch_imessage("P2-CONTAINED 🛡️", contain_msg)
                except Exception as e:
                    print(f"   ❌ [IPS ERROR] Failed to terminate PID {item['pid']}: {e}")
        return len(anomalies)
    else:
        print("✅ [IDS Engine] No unauthorized network sockets detected (P4 Silent Pass).")
        log_event("IDS_SOCKET_SCAN_CLEAN", "INFO", "xdr_agent", "Network socket scan completed cleanly.", "T1046")
        return 0

if __name__ == "__main__":
    auto_ips = "--contain" in sys.argv or "--ips" in sys.argv
    print("======================================================================")
    print("            SEC-OPS ACTIVE XDR / IDS / IPS THREAT ENGINE               ")
    print("======================================================================")
    print(f" Mode: {'IPS (Active Containment Enabled)' if auto_ips else 'IDS (Detection Only)'}")
    
    threat_count = audit_sockets_and_ips(auto_contain=auto_ips)
    print("\n======================================================================")
    sys.exit(1 if threat_count > 0 and not auto_ips else 0)
