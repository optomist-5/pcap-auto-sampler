import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY

def build_pdf():
    pdf_filename = "NetworkPlus_SOC_Project_Master_Guide.pdf"
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()
    
    # Custom Palette
    PRIMARY = colors.HexColor("#1A365D")   # Deep Navy
    SECONDARY = colors.HexColor("#2B6CB0") # Slate Blue
    DARK_NEUTRAL = colors.HexColor("#2D3748") # Dark Grey Body
    LIGHT_BG = colors.HexColor("#F7FAFC")   # Soft Off-White
    BORDER_COLOR = colors.HexColor("#E2E8F0")
    ACCENT = colors.HexColor("#C53030")   # Crimson Accent

    # Custom Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=PRIMARY,
        alignment=TA_LEFT,
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=SECONDARY,
        spaceAfter=15
    )

    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=PRIMARY,
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=SECONDARY,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=DARK_NEUTRAL,
        alignment=TA_LEFT,
        spaceAfter=6
    )

    code_style = ParagraphStyle(
        'CodeSnippet',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#1A202C"),
        backColor=colors.HexColor("#EDF2F7"),
        borderColor=BORDER_COLOR,
        borderWidth=0.5,
        borderPadding=6,
        spaceBefore=4,
        spaceAfter=6,
        borderRadius=3
    )

    story = []

    # Title Banner
    story.append(Paragraph("Network+ &amp; SOC Ingestion Pipeline Master Guide", title_style))
    story.append(Paragraph("<b>Author:</b> Matt (optomist-5) &nbsp;|&nbsp; <b>Domain:</b> Threat Detection &amp; Security Engineering &nbsp;|&nbsp; <b>Date:</b> September 2026", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceAfter=12))

    # MODULE 1
    story.append(Paragraph("Module 1: Wireless Security &amp; 802.11 Protocol Mechanics", h1_style))
    story.append(Paragraph(
        "Modern wireless communications operate under the IEEE 802.11 standard. Understanding wireless vulnerabilities requires analyzing the distinction between frame types, encryption protocols, and management message integrity.",
        body_style
    ))

    story.append(Paragraph("802.11 Frame Architecture &amp; Management Vulnerabilities", h2_style))
    story.append(Paragraph(
        "802.11 traffic is divided into three functional frame types:<br/>"
        "1. <b>Data Frames:</b> Carry payload data across the wireless medium.<br/>"
        "2. <b>Control Frames:</b> Assist with data delivery (e.g., RTS, CTS, ACK).<br/>"
        "3. <b>Management Frames:</b> Supervise network joins, leaves, and capability advertisements (e.g., Beacons, Probe Requests/Responses, Authentication, Association, Disassociation, and Deauthentication).",
        body_style
    ))
    story.append(Paragraph(
        "<b>The Core Vulnerability:</b> In legacy Wi-Fi standards (802.11a/b/g/n/ac), management frames are transmitted in plaintext and lack cryptographic signatures. An attacker can construct spoofed 802.11 management frames containing the target client's or Access Point's MAC address to force immediate disconnection.",
        body_style
    ))

    story.append(Paragraph("Attack Vector Deep Dive &amp; Enterprise Defense", h2_style))
    story.append(Paragraph(
        "<b>Deauthentication Attack:</b> A active Layer 2 Denial of Service (DoS) attack where forged deauthentication frames force client disconnections. Attackers leverage this to kick users off legitimate APs and force them to connect to an 'Evil Twin' rogue AP broadcasting an identical SSID.<br/>"
        "<b>Protected Management Frames (PMF / 802.11w):</b> Adds cryptographic protection (via AES-CMAC or HMAC-SHA256) to management frames. Clients drop unauthenticated deauthentication frames.<br/>"
        "<b>WPA3 Mandate:</b> WPA3 strictly mandates 802.11w PMF support, eliminating plaintext deauthentication attacks.",
        body_style
    ))

    # MODULE 2
    story.append(Spacer(1, 8))
    story.append(Paragraph("Module 2: Network Traffic Capture &amp; Baseline Engineering", h1_style))
    story.append(Paragraph(
        "Full Packet Capture (FPC) records every payload byte traversing a link. While invaluable during forensic investigations, enterprise links (10Gbps+) generate terabytes of data daily, overwhelming SIEM storage arrays.",
        body_style
    ))
    story.append(Paragraph(
        "<b>SOC Ingestion Trade-off:</b> Security Operations Centers employ statistical sampling to archive baseline captures (e.g., 2,500 packets per week) to establish network noise baselines, validate Snort/Zeek detection rules, and retain audit logs without exhausting disk quotas.",
        body_style
    ))

    story.append(Paragraph("Python Scapy Implementation Code", h2_style))
    story.append(Paragraph("The complete operational packet capture script executed on interface <code>en0</code>:", body_style))
    
    code_text = (
        "#!/usr/bin/env python3<br/>"
        "import os, sys, time<br/>"
        "from datetime import datetime<br/>"
        "from scapy.all import sniff, wrpcap<br/><br/>"
        "INTERFACE = 'en0'&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# macOS Wi-Fi Interface<br/>"
        "MAX_PACKETS = 2500&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# Target Sample Size<br/>"
        "TIMEOUT = 300&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# 5-minute timeout guard<br/>"
        "OUTPUT_DIR = './captures'<br/><br/>"
        "def check_privileges():<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;if os.geteuid() != 0:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;print('[-] Root/sudo required for raw sockets.', file=sys.stderr)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;sys.exit(1)<br/><br/>"
        "def run_capture():<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;os.makedirs(OUTPUT_DIR, exist_ok=True)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;out_file = os.path.join(OUTPUT_DIR, f'sample_{timestamp}.pcap')<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;packets = sniff(iface=INTERFACE, count=MAX_PACKETS, timeout=TIMEOUT)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;wrpcap(out_file, packets)<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;print(f'[+] Saved {len(packets)} packets to {out_file}')<br/><br/>"
        "if __name__ == '__main__':<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;check_privileges()<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;run_capture()"
    )
    story.append(Paragraph(code_text, code_style))

    # MODULE 3
    story.append(Spacer(1, 8))
    story.append(Paragraph("Module 3: Unix Administration &amp; Daemon Scheduling", h1_style))
    story.append(Paragraph(
        "Automating security scripts requires proper Unix privilege management and background execution daemons.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Raw Socket Privileges:</b> Capturing packets bypasses standard OS socket abstractions, opening raw network drivers. This requires EUID 0 (root). Running scripts without <code>sudo</code> results in permission denied errors.<br/>"
        "<b>Root Crontab Execution:</b> Standard user cron jobs fail when attempting raw packet capture. The job must be registered under the root user crontab (<code>sudo crontab -e</code>).<br/>"
        "<b>Cron Expression Breakdown (<code>0 2 * * 0</code>):</b><br/>"
        "&nbsp;&nbsp;• <code>0</code>: Minute 0<br/>"
        "&nbsp;&nbsp;• <code>2</code>: 02:00 AM<br/>"
        "&nbsp;&nbsp;• <code>*</code>: Every day of month<br/>"
        "&nbsp;&nbsp;• <code>*</code>: Every month<br/>"
        "&nbsp;&nbsp;• <code>0</code>: Sunday<br/>"
        "<b>Command Entry:</b><br/>"
        "<code>0 2 * * 0 /Users/mq/pcap-auto-sampler/venv/bin/python3 /Users/mq/pcap-auto-sampler/capture.py &gt;&gt; /var/log/pcap_sampler.log 2&gt;&amp;1</code>",
        body_style
    ))

    # PAGE BREAK FOR CLEAN RETROSPECTIVE TABLE
    story.append(PageBreak())

    # MODULE 4
    story.append(Paragraph("Module 4: Version Control, Authentication &amp; Identity", h1_style))
    story.append(Paragraph(
        "Modern DevSecOps workflows mandate strict access controls, repository hygiene, and license tracking.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Personal Access Tokens (PAT):</b> GitHub deprecated basic password authentication over HTTPS for command-line operations. Developers must generate cryptographically scoped PATs (e.g., <code>ghp_...</code>) with specific permissions (<code>repo</code>).<br/>"
        "<b>Repository Hygiene (<code>.gitignore</code>):</b> Raw <code>.pcap</code> files and virtual environments (<code>venv/</code>) must be excluded from Git tracking to avoid committing sensitive user traffic payloads or bloated binaries.<br/>"
        "<b>MIT Licensing:</b> A permissive open-source license protecting authors from liability while permitting public review and professional evaluation.",
        body_style
    ))

    # MODULE 5
    story.append(Spacer(1, 8))
    story.append(Paragraph("Module 5: Comprehensive Troubleshooting &amp; Root Cause Matrix", h1_style))
    story.append(Paragraph(
        "A detailed retrospective log documenting operational errors encountered during execution, technical root causes, and resolutions:",
        body_style
    ))

    table_data = [
        [
            Paragraph("<b>Error Observed</b>", body_style),
            Paragraph("<b>Technical Root Cause</b>", body_style),
            Paragraph("<b>Engineering Resolution</b>", body_style)
        ],
        [
            Paragraph("<code>zsh: command not found: #</code><br/><code>zsh: 2.5.0 not found</code>", body_style),
            Paragraph("Multi-line configuration text pasted directly into Zsh prompt; shell evaluated text as commands.", body_style),
            Paragraph("Implemented <code>cat &lt;&lt; 'EOF' &gt; file</code> heredoc streaming to write clean disk files.", body_style)
        ],
        [
            Paragraph("Prompt stuck at <code>heredoc&gt;</code>", body_style),
            Paragraph("Unclosed quotes or pasting tutorial text into active heredoc stream.", body_style),
            Paragraph("Issued <code>Ctrl+C</code> (SIGINT) to interrupt Zsh execution and reset terminal prompt.", body_style)
        ],
        [
            Paragraph("Terminal un-responsive on password entry", body_style),
            Paragraph("macOS Terminal intentionally suppresses character echoing on <code>sudo</code> for security.", body_style),
            Paragraph("Pasted password via <code>Cmd+V</code> and pressed Enter regardless of blank display.", body_style)
        ],
        [
            Paragraph("<code>remote: Invalid username or token</code>", body_style),
            Paragraph("Basic account password used for Git HTTPS push instead of Personal Access Token.", body_style),
            Paragraph("Generated classic PAT with <code>repo</code> scope on GitHub; pasted token string as password.", body_style)
        ],
        [
            Paragraph("<code>fatal: Need to specify how to reconcile divergent branches</code>", body_style),
            Paragraph("Remote repo initialized with web-generated <code>LICENSE</code>, creating disconnected commit trees.", body_style),
            Paragraph("Set <code>git config pull.rebase false</code> and pulled with <code>--allow-unrelated-histories</code>.", body_style)
        ],
        [
            Paragraph("<code>sudo: 3 incorrect password attempts</code>", body_style),
            Paragraph("Pasting GitHub PAT (<code>ghp_...</code>) into <code>sudo</code> prompt instead of local Mac password.", body_style),
            Paragraph("Entered local macOS user unlock password required by system PAM authentication.", body_style)
        ]
    ]

    t = Table(table_data, colWidths=[130, 200, 210])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), LIGHT_BG),
        ('TEXTCOLOR', (0, 0), (-1, 0), PRIMARY),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(t)

    # MODULE 6
    story.append(Spacer(1, 10))
    story.append(Paragraph("Module 6: CompTIA Network+ &amp; Security+ Exam Mapping", h1_style))
    story.append(Paragraph(
        "<b>Exam Objectives Directly Reinforced by this Project:</b><br/>"
        "• <b>Network+ Domain 2.0 (Network Operations):</b> Monitoring baseline traffic, capturing PCAP files, analyzing packet metrics.<br/>"
        "• <b>Network+ Domain 4.0 (Network Security):</b> 802.11 wireless security standards (WPA2 vs WPA3, 802.11w PMF, rogue APs, deauthentication attacks).<br/>"
        "• <b>Security+ Domain 1.0 (Threats &amp; Vulnerabilities):</b> Wireless attack vectors, Layer 2 spoofing, DoS mechanics.<br/>"
        "• <b>Security+ Domain 3.0 (Security Architecture):</b> Secure authentication mechanisms, API token scopes, least privilege authorization.",
        body_style
    ))

    doc.build(story)
    print(f"[+] Master Guide PDF generated successfully: {pdf_filename}")

if __name__ == "__main__":
    build_pdf()
