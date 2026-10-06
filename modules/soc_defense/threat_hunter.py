#!/usr/bin/env python3
"""
Universal Threat Hunting Engine (Resilient Field Extractor)
Parses network captures, flags multi-layer threats, plays audio alarms, 
and outputs Azure/SIEM-compliant telemetry.
"""

import json
import os
import subprocess
import sys
from datetime import datetime, timezone

# ANSI Color Palette
RED = "\033[1;31m"
GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
CYAN = "\033[1;36m"
RESET = "\033[0m"

def trigger_alert_audio():
    """Triggers native macOS notification audio."""
    os.system("afplay /System/Library/Sounds/Glass.aiff &")

def extract_field(data, field_name):
    """Recursively extracts a target field value from nested Tshark JSON dictionaries."""
    if isinstance(data, dict):
        if field_name in data:
            val = data[field_name]
            if isinstance(val, list) and len(val) > 0:
                return str(val[0])
            return str(val)
        for k, v in data.items():
            res = extract_field(v, field_name)
            if res:
                return res
    elif isinstance(data, list):
        for item in data:
            res = extract_field(item, field_name)
            if res:
                return res
    return None

def parse_pcap_with_tshark(pcap_path):
    """Parses binary PCAPs into structured JSON arrays via Tshark CLI."""
    if not os.path.exists(pcap_path):
        print(f"{RED}[-] Error: Target file '{pcap_path}' not found.{RESET}")
        return []

    cmd = ["tshark", "-r", pcap_path, "-T", "json"]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return json.loads(res.stdout) if res.stdout.strip() else []
    except Exception as e:
        print(f"{RED}[-] Tshark Parsing Failed: {e}{RESET}", file=sys.stderr)
        return []

def hunt_threats(packets):
    """Executes multi-layer threat detection rules against parsed frames."""
    alerts = []
    siem_payloads = []
    now_utc = datetime.now(timezone.utc).isoformat()

    for pkt in packets:
        try:
            layers = pkt["_source"]["layers"]
            
            # Extract frame number & IP addresses safely
            frame_num = extract_field(layers.get("frame", {}), "frame.number") or "0"
            ip_src = extract_field(layers.get("ip", {}), "ip.src") or "0.0.0.0"
            ip_dst = extract_field(layers.get("ip", {}), "ip.dst") or "0.0.0.0"

            # Vector 1: DNS Command & Control (C2) / Exfiltration
            if "dns" in layers:
                qname = extract_field(layers["dns"], "dns.qry.name")
                if qname:
                    is_long = len(qname) > 30
                    is_sus_tld = any(kw in qname for kw in [".ru", "beacon", "malicious", "exfil"])

                    if is_long or is_sus_tld:
                        alerts.append({
                            "vector": "DNS C2 / Tunneling",
                            "frame": frame_num,
                            "src": ip_src,
                            "dst": ip_dst,
                            "detail": qname,
                            "reason": "Abnormal query length or high-risk domain keyword."
                        })
                        siem_payloads.append({
                            "TimeGenerated": now_utc,
                            "SourceIp": ip_src,
                            "DestinationIp": ip_dst,
                            "ThreatCategory": "DNS_C2_Tunneling",
                            "Payload": qname,
                            "Severity": "High"
                        })

            # Vector 2: HTTP Web Attack Vectors
            if "http" in layers:
                uri = extract_field(layers["http"], "http.request.uri") or ""
                u_lower = uri.lower()

                sqli = ["' or '", "1=1", "union select", "drop table"]
                xss = ["<script>", "javascript:", "onerror="]
                traversal = ["../", "/etc/passwd", "win.ini"]

                detected_type = None
                if any(p in u_lower for p in sqli):
                    detected_type = "HTTP SQL Injection"
                elif any(p in u_lower for p in xss):
                    detected_type = "HTTP Cross-Site Scripting (XSS)"
                elif any(p in u_lower for p in traversal):
                    detected_type = "HTTP Directory Traversal"

                if detected_type:
                    alerts.append({
                        "vector": detected_type,
                        "frame": frame_num,
                        "src": ip_src,
                        "dst": ip_dst,
                        "detail": uri,
                        "reason": "Exploitation signature detected in HTTP request string."
                    })
                    siem_payloads.append({
                        "TimeGenerated": now_utc,
                        "SourceIp": ip_src,
                        "DestinationIp": ip_dst,
                        "ThreatCategory": detected_type.replace(" ", "_"),
                        "Payload": uri,
                        "Severity": "Critical"
                    })

        except Exception:
            continue

    return alerts, siem_payloads

def display_alerts(alerts):
    """Prints formatted alerts with terminal colors and triggers audio alarm."""
    if alerts:
        trigger_alert_audio()
        print(f"\n{RED}================ 🚨 CRITICAL THREATS DETECTED ({len(alerts)}) 🚨 ================{RESET}\n")
        for a in alerts:
            print(f"{RED}[{a['vector']}]{RESET} Frame #{a['frame']}")
            print(f"  ├─ Network Flow: {CYAN}{a['src']}{RESET} ──> {CYAN}{a['dst']}{RESET}")
            print(f"  ├─ Raw Payload:  {YELLOW}{a['detail']}{RESET}")
            print(f"  └─ Triage Note:  {a['reason']}\n")
    else:
        print(f"\n{GREEN}[+] Baseline verification complete: Zero threats identified.{RESET}\n")

def main():
    target_pcap = "sample_multi.pcap"
    print(f"[*] Ingesting target capture file: {CYAN}{target_pcap}{RESET}...")

    packets = parse_pcap_with_tshark(target_pcap)
    print(f"[+] Total packet frames ingested: {len(packets)}")

    alerts, siem_payloads = hunt_threats(packets)
    display_alerts(alerts)

    if siem_payloads:
        out_file = "azure_siem_ingest.json"
        with open(out_file, "w") as f:
            json.dump(siem_payloads, f, indent=2)
        print(f"{GREEN}[+] Exported {len(siem_payloads)} alerts to SIEM schema: '{out_file}'{RESET}\n")

if __name__ == "__main__":
    main()
