#!/usr/bin/env python3
"""
Automated Network Traffic Sampler
Author: SOC Candidate Portfolio
Description: Captures a lightweight sample of local network traffic 
             and saves it to a timestamped PCAP file for routine analysis.
"""

import os
import sys
import time
from datetime import datetime
from scapy.all import sniff, wrpcap

INTERFACE = "en0"           # Default Wi-Fi interface on macOS
MAX_PACKETS = 2500          # Keeps file size small (~2-5 MB)
TIMEOUT = 300               # Hard timeout limit in seconds (5 minutes)
OUTPUT_DIR = "./captures"   # Destination folder for PCAP files

def check_privileges():
    """Verify script is running with elevated privileges required for raw sockets."""
    if os.geteuid() != 0:
        print("[-] Error: Root/sudo privileges are required to capture raw network frames.", file=sys.stderr)
        sys.exit(1)

def ensure_output_dir(directory: str):
    """Ensure the target capture directory exists."""
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
        print(f"[+] Output directory initialized: {directory}")

def run_capture(interface: str, max_packets: int, timeout: int, output_dir: str):
    """Execute network packet capture and save output to PCAP format."""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_filename = os.path.join(output_dir, f"sample_{timestamp}.pcap")
    
    print(f"[*] Starting packet capture on interface '{interface}'...")
    print(f"[*] Constraints: Max {max_packets} packets OR {timeout} seconds.")
    
    start_time = time.time()
    
    try:
        packets = sniff(iface=interface, count=max_packets, timeout=timeout)
        wrpcap(output_filename, packets)
        
        elapsed_time = round(time.time() - start_time, 2)
        file_size_kb = round(os.path.getsize(output_filename) / 1024, 2)
        
        print(f"[+] Capture completed successfully!")
        print(f"    ├── File Location: {output_filename}")
        print(f"    ├── Total Packets: {len(packets)}")
        print(f"    ├── File Size: {file_size_kb} KB")
        print(f"    └── Duration: {elapsed_time} seconds")
        
    except Exception as e:
        print(f"[-] Execution failure: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    check_privileges()
    ensure_output_dir(OUTPUT_DIR)
    run_capture(INTERFACE, MAX_PACKETS, TIMEOUT, OUTPUT_DIR)
