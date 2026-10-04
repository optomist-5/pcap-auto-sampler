#!/usr/bin/env zsh
# Daily CySA+ Morning Warmup Script

PROJECT_DIR="$HOME/pcap-auto-sampler"
cd "$PROJECT_DIR" || exit 1

# 1. Activate Virtual Environment
source venv/bin/activate

echo "=================================================="
echo " [1/3] Generating Fresh Multi-Protocol PCAP Data  "
echo "=================================================="

python3 -c "
from scapy.all import IP, TCP, UDP, ICMP, ARP, DNS, DNSQR, Raw, wrpcap

pkts = [
    ARP(op=1, pdst='192.168.1.1'),
    IP(dst='1.1.1.1')/ICMP(),
    IP(dst='8.8.8.8')/UDP(dport=53)/DNS(rd=1, qd=DNSQR(qname='example.com')),
    IP(dst='93.184.216.34')/TCP(dport=80, flags='PA')/Raw(b'GET /login.php HTTP/1.1\r\nHost: example.com\r\n\r\n'),
    IP(dst='185.220.101.5')/UDP(dport=53)/DNS(rd=1, qd=DNSQR(qname='v1-exfil-a3f91b82c9e47d10a.malicious-beacon.ru'))
]

wrpcap('sample_multi.pcap', pkts)
"
cp sample_multi.pcap sample.pcap

echo "=================================================="
echo " [2/3] Launching Wireshark GUI App                 "
echo "=================================================="
open -a Wireshark sample_multi.pcap

echo "=================================================="
echo " [3/3] Executing Terminal Python JSON Parser       "
echo "=================================================="
python3 parse_pcap.py

echo ""
echo "[+] Morning Lab Loaded Successfully!"
echo "[+] Wireshark GUI is open for visual inspection."
echo "[+] Terminal output above displays parsed JSON fields."
