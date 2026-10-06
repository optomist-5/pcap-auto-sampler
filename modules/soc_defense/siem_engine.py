#!/usr/bin/env python3
"""
SecOps Enterprise SIEM Engine (v2026.2)
Central Log Normalization, Event Correlation & MITRE ATT&CK Mapper
"""

import os, sys, json, datetime

SIEM_LOG_PATH = os.path.expanduser('~/secops/logs/siem_events.json')

def log_event(event_type, severity, source, description, mitre_ttp="T1000", details=None):
    """
    Normalizes security events into standard JSON schema.
    """
    event = {
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "host": os.uname().nodename,
        "event_type": event_type,
        "severity": severity,  # CRITICAL, HIGH, MEDIUM, LOW, INFO
        "source_module": source,
        "mitre_ttp": mitre_ttp,
        "description": description,
        "details": details or {}
    }
    
    os.makedirs(os.path.dirname(SIEM_LOG_PATH), exist_ok=True)
    
    with open(SIEM_LOG_PATH, 'a') as f:
        f.write(json.dumps(event) + "\n")
        
    return event

def display_recent_events(limit=10):
    """
    Renders recent SIEM events in structured format.
    """
    print("\n======================================================================")
    print("                 SEC-OPS CENTRAL SIEM TELEMETRY DASHBOARD             ")
    print("======================================================================")
    if not os.path.exists(SIEM_LOG_PATH):
        print("   [!] No SIEM telemetry events recorded yet.")
        print("======================================================================")
        return

    events = []
    with open(SIEM_LOG_PATH, 'r') as f:
        for line in f:
            if line.strip():
                try:
                    events.append(json.loads(line.strip()))
                except json.JSONDecodeError:
                    continue

    recent = events[-limit:]
    recent.reverse()

    for idx, ev in enumerate(recent, 1):
        sev = ev.get('severity', 'INFO')
        icon = "🚨" if sev in ["CRITICAL", "HIGH"] else "⚠️" if sev == "MEDIUM" else "ℹ️"
        print(f" {icon} [{ev['timestamp'][:19]}] [{sev}] {ev['event_type']} (MITRE: {ev['mitre_ttp']})")
        print(f"    Source: {ev['source_module']} | Host: {ev['host']}")
        print(f"    Description: {ev['description']}")
        if ev.get('details'):
            print(f"    Details: {json.dumps(ev['details'])}")
        print(" --------------------------------------------------------------------")
    print("======================================================================")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--show":
        display_recent_events()
    else:
        log_event("SIEM_INITIALIZATION", "INFO", "siem_engine", "SIEM Event Logger active.", "T1082")
        print("✅ SIEM Engine initialized. Telemetry pipeline ready.")
