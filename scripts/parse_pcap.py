#!/usr/bin/env python3
"""
Lab 3: Multi-Vector Threat Detector
Extracts network telemetry, flags C2 and Web attacks, and triggers audio alerts.
"""

import json
import os
import subprocess
import sys

# Terminal Color Palette (ANSI Escape Codes)
RED = "\033[1;31m"
GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
CYAN = "\033[1;36m"
RESET = "\033[0m"

def trigger_audio_alert():
    """Fires a macOS native audio chime."""
    os.system("afplay /System/Library/Sounds/Glass.aiff &")

def extract_pcap_json(pcap_file):
    """Executes Tshark to extract network telemetry in JSON format."""
    tshark_cmd = ["tshark", "-r", pcap_file, "-T", "json"]

    try:
        result = subprocess.run(tshark_cmd, capture_output=True, text=True, check=True)
        return json.loads(result.stdout) if result.stdout.strip() else []
    except subprocess.CalledProcessError as e:
        print(f"[-] Tshark execution error: {e}", file=sys.stderr)
        return []
    except json.JSONDecodeError as e:
        print(f"[-] Failed to parse JSON output: {e}", file=sys.stderr)
        return []

def analyze_network_threats(packet_list):
    """Inspects DNS and HTTP layers for multi-vector threat patterns."""
    alerts = []
    
    for packet in packet_list:
        try:
            layers = packet["_source"]["layers"]
            frame_num = layers["frame"]["frame.number"][0]
            
            ip_src = layers.get("ip", {}).get("ip.src", ["Unknown"])[0]
            ip_dst = layers.get("ip", {}).get("ip.dst", ["Unknown"])[0]

            # 1. DNS C2 / Tunneling Detection
            if "dns" in layers:
                dns_layer = layers["dns"]
                if "Queries" in dns_layer:
                    qname = dns_layer["Queries"]["dns.qry.name"][0]
                    
                    is_long = len(qname) > 30
                    is_suspicious_tld = any(kw in qname for kw in [".ru", "malicious", "beacon", "exfil"])

                    if is_long or is_suspicious_tld:
                        alerts.append({
                            "type": "DNS C2 / Tunneling",
                            "frame": frame_num,
                            "src": ip_src,
                            "dst": ip_dst,
                            "detail": qname,
                            "reason": "Suspicious query length or high-risk domain keyword."
                        })

            # 2. HTTP Web Attack Detection (SQLi, XSS, Path Traversal)
            if "http" in layers:
                http_layer = layers["http"]
                uri = http_layer.get("http.request.uri", [""])[0]
                payload_lower = uri.lower()

                sqli_patterns = ["' or '", "1=1", "union select", "drop table"]
                xss_patterns = ["<script>", "javascript:", "onerror="]
                traversal_patterns = ["../", "/etc/passwd", "win.ini"]

                if any(p in payload_lower for p in sqli_patterns):
                    alerts.append({
                        "type": "HTTP SQL Injection",
                        "frame": frame_num,
                        "src": ip_src,
                        "dst": ip_dst,
                        "detail": uri,
                        "reason": "SQL syntax pattern detected in HTTP request URI."
                    })
                elif any(p in payload_lower for p in xss_patterns):
                    alerts.append({
                        "type": "HTTP Cross-Site Scripting (XSS)",
                        "frame": frame_num,
                        "src": ip_src,
                        "dst": ip_dst,
                        "detail": uri,
                        "reason": "Script injection tag detected in HTTP request."
                    })
                elif any(p in payload_lower for p in traversal_patterns):
                    alerts.append({
                        "type": "HTTP Directory Traversal",
                        "frame": frame_num,
                        "src": ip_src,
                        "dst": ip_dst,
                        "detail": uri,
                        "reason": "Path traversal pattern detected."
                    })

        except Exception:
            continue

    return alerts

def display_alerts(anomalies):
    """Displays highlighted alerts and triggers audio notifications."""
    if anomalies:
        trigger_audio_alert()
        print(f"\n{RED}================ 🚨 THREAT ALERTS DETECTED ({len(anomalies)}) 🚨 ================{RESET}\n")
        for alert in anomalies:
            print(f"{RED}[CRITICAL - {alert['type']}]{RESET} Frame #{alert['frame']}")
            print(f"  ├─ Source:      {CYAN}{alert['src']}{RESET} ──> Destination: {CYAN}{alert['dst']}{RESET}")
            print(f"  ├─ Payload/URI: {YELLOW}{alert['detail']}{RESET}")
            print(f"  └─ Analysis:    {alert['reason']}\n")
    else:
        print(f"\n{GREEN}[+] No anomalies detected. Network baseline clear.{RESET}\n")

def main():
    pcap_file = "sample_multi.pcap"
    print(f"[*] Analyzing {pcap_file} for multi-vector threats...")
    
    packets = extract_pcap_json(pcap_file)
    print(f"[+] Total packets parsed: {len(packets)}")

    anomalies = analyze_network_threats(packets)
    display_alerts(anomalies)

if __name__ == "__main__":
    main()
