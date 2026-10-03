import os
import datetime
import logging
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_daily_curriculum(current_date):
    """
    Returns specific, day-by-day theory content, lab 1 focus, and lab 2 integration content
    for every day from Oct 1, 2026 through April 1, 2027.
    """
    d0 = datetime.date(2026, 10, 1)
    day_num = (current_date - d0).days + 1

    # -------------------------------------------------------------------------
    # PHASE 1: Security+ (SY0-701) Core Phase [Oct 01, 2026 - Oct 20, 2026]
    # -------------------------------------------------------------------------
    if current_date <= datetime.date(2026, 10, 20):
        phase_title = "Security+ (SY0-701) Core Phase"
        doc_link = "https://www.comptia.org/certifications/security"
        
        sec_plus_schedule = {
            1: (
                "• Professor Messer SY0-701 Videos: Domain 1.1-1.3 (General Security Concepts)\n• Key Focus: CIA Triad, Non-Repudiation, Security Controls (Technical, Managerial, Operational)",
                "• Lab 1: IP Subnetting Mathematics, CIDR Notation & VLSM Calculations",
                "• Lab 2: CLI Subnet Verification (`ip -4 a`, `ifconfig`, `netstat -rn`, `lsof -i -P -n`)"
            ),
            2: (
                "• Professor Messer SY0-701 Videos: Domain 1.4-1.6 (Cryptographic Concepts & PKI)\n• Key Focus: Symmetric vs Asymmetric, Hashing, Digital Certificates, CA Lifecycle",
                "• Lab 1: OpenSSL RSA/ECC Key Pair Generation & Certificate Signing Request (CSR) Creation",
                "• Lab 2: Certificate Chain Validation, TLS Cipher Suite Auditing & SNI Testing (`openssl s_client`)"
            ),
            3: (
                "• Review & Knowledge Check: Port Numbers, Protocols, & Subnetting Reinforcement\n• Practice Questions: Domain 1 & 2 Drills\n• Flashcards: SSH(22), HTTPS(443), DNS(53), LDAP(389), RDP(3389)",
                "• Lab 1: Native Network Socket Triage & Process Inspection (`netstat`, `lsof`, `fuser`)",
                "• Lab 2: CLI Packet Capture & Protocol Filtering using `tshark` and `tcpdump`"
            ),
            4: (
                "• Professor Messer SY0-701 Videos: Domain 2.1-2.3 (Threat Vectors & Vulnerabilities)\n• Key Focus: Malware Types, Social Engineering, Supply Chain Risks, Zero-Day Exploits",
                "• Lab 1: Linux Operating System Hardening & `/var/log/auth.log` Failed SSH Triage",
                "• Lab 2: Nginx Access Log Parsing for 500-Series Error Spikes & Client Anomalies"
            ),
            5: (
                "• Professor Messer SY0-701 Videos: Domain 2.4-2.6 (Attacks & Vulnerability Scanning)\n• Key Focus: Phishing, AiTM Proxies, Buffer Overflows, SQLi, XSS, CSRF",
                "• Lab 1: Python Security Automation: Inbox Forwarding Exfiltration Rule Auditor",
                "• Lab 2: String Parsing, Regex Capture Groups & Unstructured Telemetry Normalization"
            ),
            6: (
                "• Professor Messer SY0-701 Videos: Domain 3.1-3.3 (Security Architecture & Resilience)\n• Key Focus: Network Segmentation, Zero Trust Architecture, Cloud Workloads, Redundancy",
                "• Lab 1: Nmap Stealth TCP SYN Port Scanning & Remote Service Fingerprinting",
                "• Lab 2: Nmap NSE Script Engine Execution for Vulnerability & Web Header Detection"
            ),
            7: (
                "• Professor Messer SY0-701 Videos: Domain 3.4-3.6 (Identity Boundaries & Access Control)\n• Key Focus: IAM, Federated Identity, SAML, OAuth2, OIDC, ABAC, RBAC",
                "• Lab 1: Offline Credential Recovery using `hashcat` (Cisco Type 9 / PBKDF2-SHA256)",
                "• Lab 2: `john` Unshadow Pipeline Execution & Linux `/etc/shadow` Hash Cracking"
            ),
            8: (
                "• Professor Messer SY0-701 Videos: Domain 4.1-4.3 (Security Operations & Incident Response)\n• Key Focus: SIEM, SOAR, EDR, Incident Handling Lifecycle, Containment Strategies",
                "• Lab 1: High-Throughput SHA-256 Cryptographic Engine & Base64 Stream Parser (Java/Python)",
                "• Lab 2: Standalone Native JWT Decoder & Claim Introspection Script"
            ),
            9: (
                "• Professor Messer SY0-701 Videos: Domain 4.4-4.6 (Digital Forensics & Evidence Handling)\n• Key Focus: Volatile Memory, Disk Imaging, Chain of Custody, Order of Volatility",
                "• Lab 1: AWS S3 & Azure Blob Storage Public Access Policy Auditing via CLI",
                "• Lab 2: Storage Bucket Security Configurations & Data Leak Prevention Verification"
            ),
            10: (
                "• Mid-Point Assessment & Knowledge Drill: Domains 1 & 2 Comprehensive PBQs\n• Deep Dive: Reviewing Incorrect Answers & Identifying Gap Modules",
                "• Lab 1: Volatile Memory Acquisition & Process Tree Analysis using `Volatility 3`",
                "• Lab 2: Memory Network Socket Interrogation & Code Injection Detection (`malfind`)"
            ),
            11: (
                "• Domain 3 Deep Dive: Identity Architecture, FIDO2 Passkeys, & Session Security\n• Key Focus: Device-Bound Session Credentials (DBSC) & Cookie Theft Mitigation",
                "• Lab 1: Web Application Attack Surface Reduction & HTTP Security Headers Analysis",
                "• Lab 2: OWASP Top 10 Injection Vectors & Client-Side Cookie Security Flags"
            ),
            12: (
                "• Domain 4 Deep Dive: SIEM Alert Normalization & Log Telemetry Stream Joining\n• Key Focus: In-Memory Hash Joins, Inner Joins, and Left Outer Joins",
                "• Lab 1: File Modification Timeline Generation (`find -mmin -120` & `sha256sum`)",
                "• Lab 2: Interrogating Active Process Sockets & Command Lines (`lsof`, `netstat`)"
            ),
            13: (
                "• Domain 5 Deep Dive: Security Program Management, Risk Assessment & Regulatory Audits\n• Key Focus: SOC 2 Type II Criteria, ISO 27001 Controls, GDPR Article 32 Alignment",
                "• Lab 1: Custom Zsh Shell Environment Hardening (`.zshrc` Security Configurations)",
                "• Lab 2: Shell Execution Safety, Command Alias Engineering & History Sanitization"
            ),
            14: (
                "• Speed Run: Common Port Numbers, Protocol Headers, RFC Standards & Cryptographic Modes\n• Key Focus: Fast Recall for Exam Day",
                "• Lab 1: Multithreaded Python Target Evaluation Engine (`ThreadPoolExecutor`)",
                "• Lab 2: Concurrent Queue Processing, Exception Handling & JSON Output Storage"
            ),
            15: (
                "• Comprehensive PBQ Drill: Network Topologies, Firewall Rule Statements & WAF Rules\n• Focus: Performance-Based Questions Mastery",
                "• Lab 1: Firewall Rule Analysis & Packet Inspection using `tshark` Filters",
                "• Lab 2: HTTP POST Payload Extraction & TLS Handshake Debugging"
            ),
            16: (
                "• Comprehensive PBQ Drill: Cryptographic Hashes, Digital Signatures & PKI Hierarchies\n• Focus: Performance-Based Questions Mastery",
                "• Lab 1: OpenSSL Connection Verification & SNI Host Handshake Debugging",
                "• Lab 2: DH Parameter Generation, Key Extraction & PKCS#12 File Conversion"
            ),
            17: (
                "• Comprehensive PBQ Drill: Incident Response Protocols, Host Isolation & Account Revocation\n• Focus: Performance-Based Questions Mastery",
                "• Lab 1: Linux File Permission Auditing & SUID/SGID Executable Discovery",
                "• Lab 2: Process Locking Removal & Signal-Based Termination (`fuser -k`, `kill -9`)"
            ),
            18: (
                "• Comprehensive PBQ Drill: Cloud IAM Policies, Least Privilege, & Role-Based Access Control\n• Focus: Performance-Based Questions Mastery",
                "• Lab 1: Native Python JWT Claim Extractor & Signature Verification Engine",
                "• Lab 2: In-Memory Hash Join Performance Benchmark for Large Telemetry Feeds"
            ),
            19: (
                "• Exam Simulation 1: Full-Length SY0-701 Practice Test (90 Questions, 90 Minutes)\n• Target Score: 95% Correct",
                "• Lab 1: Targeted Gap Remediation: Re-executing Weakest Domain Labs",
                "• Lab 2: Terminal PBQ Speed Runs & Interactive Scenario Drills"
            ),
            20: (
                "• Exam Simulation 2: Final PBQ Mastery & Comprehensive Domain Review\n• OCT 20 PASS-GATE VERIFICATION DAY",
                "• Lab 1: Final Security Lab Sandbox Verification & Git Repository Synchronization",
                "• Lab 2: Post-Exam Transition Check & AZ-104 Environment Readiness Verification"
            )
        }
        b1, b2, b3 = sec_plus_schedule.get(day_num, (
            "• Security+ Core Review & Exam Prep", 
            "• Terminal Security CLI Lab", 
            "• Integrated Hands-On Lab"
        ))
        return phase_title, doc_link, b1, b2, b3

    # -------------------------------------------------------------------------
    # PHASE 2: AZ-104 Azure Administrator Phase [Oct 21, 2026 - Nov 30, 2026]
    # -------------------------------------------------------------------------
    elif current_date <= datetime.date(2026, 11, 30):
        phase_title = "AZ-104 Azure Administrator Phase"
        doc_link = "https://learn.microsoft.com/credentials/certifications/azure-administrator/"
        az_day = (current_date - datetime.date(2026, 10, 21)).days + 1
        
        b1 = f"• AZ-104 Day {az_day}: Microsoft Learn Azure Administration Curriculum\n• Module Focus: Azure Identities, Governance, Storage, Compute, & Virtual Networking"
        b2 = f"• Lab 1 (AZ-104 Day {az_day}): Azure CLI / PowerShell Automation & Resource Management"
        b3 = f"• Lab 2 (AZ-104 Day {az_day}): Cloud Infrastructure Deployment & Architecture Verification"
        return phase_title, doc_link, b1, b2, b3

    # -------------------------------------------------------------------------
    # PHASE 3: SC-200 Security Operations Analyst Phase [Dec 01, 2026 - Jan 15, 2027]
    # -------------------------------------------------------------------------
    elif current_date <= datetime.date(2027, 1, 15):
        phase_title = "SC-200 Security Operations Analyst Phase"
        doc_link = "https://learn.microsoft.com/credentials/certifications/security-operations-analyst/"
        sc200_day = (current_date - datetime.date(2026, 12, 1)).days + 1
        
        b1 = f"• SC-200 Day {sc200_day}: Microsoft Sentinel, KQL, & Defender for Endpoint Curriculum\n• Focus: Threat Hunting, Incident Response, & SOAR Playbooks"
        b2 = f"• Lab 1 (SC-200 Day {sc200_day}): Kusto Query Language (KQL) Telemetry Analysis"
        b3 = f"• Lab 2 (SC-200 Day {sc200_day}): Live Sentinel Analytic Rule Authoring & SOAR Logic App Execution"
        return phase_title, doc_link, b1, b2, b3

    # -------------------------------------------------------------------------
    # PHASE 4: SC-300 Identity & Access Administrator Phase [Jan 16, 2027 - Feb 15, 2027]
    # -------------------------------------------------------------------------
    elif current_date <= datetime.date(2027, 2, 15):
        phase_title = "SC-300 Identity & Access Administrator Phase"
        doc_link = "https://learn.microsoft.com/credentials/certifications/identity-and-access-administrator/"
        sc300_day = (current_date - datetime.date(2027, 1, 16)).days + 1
        
        b1 = f"• SC-300 Day {sc300_day}: Entra ID Architecture, PIM, & Governance Curriculum\n• Focus: FIDO2 Passkeys, Conditional Access, Entitlement Management"
        b2 = f"• Lab 1 (SC-300 Day {sc300_day}): Entra ID Directory Synchronization & Custom RBAC"
        b3 = f"• Lab 2 (SC-300 Day {sc300_day}): Risk-Based Conditional Access & PIM Time-Bound Role Enforcement"
        return phase_title, doc_link, b1, b2, b3

    # -------------------------------------------------------------------------
    # PHASE 5: SC-500 Security Administration Phase [Feb 16, 2027 - Apr 01, 2027]
    # -------------------------------------------------------------------------
    else:
        phase_title = "SC-500 Security Administration & Architecture Phase"
        doc_link = "https://learn.microsoft.com/credentials/certifications/security-administrator/"
        sc500_day = (current_date - datetime.date(2027, 2, 16)).days + 1
        
        b1 = f"• SC-500 Day {sc500_day}: Noviascentia Labs Enterprise Multi-Cloud Architecture\n• Focus: 3-Account Privilege Isolation Matrix, Edge DNS Null Profiles, Purview DLP"
        b2 = f"• Lab 1 (SC-500 Day {sc500_day}): Air-Gapped SecOps Engineering Profile & Session Isolation"
        b3 = f"• Lab 2 (SC-500 Day {sc500_day}): Edge Perimeter Null SPF/DMARC Reject & SaaS Data Exfiltration Lockdown"
        return phase_title, doc_link, b1, b2, b3


def generate_schedule_blocks(start_date, end_date, dry_run=True):
    """
    Generates all granular daily blocks for the certification roadmap.
    If dry_run is True, it prints the planned events to stdout instead of inserting them into Google Calendar.
    """
    service = None
    if not dry_run:
        token_path = 'token.json'
        if os.path.exists(token_path):
            user_creds = Credentials.from_authorized_user_file(
                token_path, 
                ['https://www.googleapis.com/auth/calendar']
            )
            service = build('calendar', 'v3', credentials=user_creds)
        else:
            logging.error("token.json not found! Unable to connect to Google Calendar API.")
            return

    current_date = start_date
    total_events_planned = 0

    while current_date <= end_date:
        date_str = current_date.isoformat()
        
        phase_title, doc_link, block1_content, block2_lab_content, block3_lab_content = get_daily_curriculum(current_date)

        # ---------------------------------------------------------------------
        # Daily Schedule Blocks Definition (8 Events Per Day)
        # ---------------------------------------------------------------------
        blocks = [
            {
                'summary': f'☀️ Sovereign Wake Up & Metabolic Baseline [{phase_title}]',
                'description': (
                    "• Morning Meditation & Mindful Reset.\n"
                    "• Morning sunlight & black coffee.\n"
                    "• High-protein breakfast (25g Protein Bowl).\n"
                    "• Start Water Liter 1 of 4.\n"
                    "• GUARDRAIL: Zero weed, zero news, zero social media."
                ),
                'start_time': f"{date_str}T09:00:00",
                'end_time': f"{date_str}T11:00:00"
            },
            {
                'summary': '🧘 11:00 AM Mindfulness Checkpoint & Break 1',
                'description': (
                    "• CHECKPOINT: Did you complete morning mindfulness during 09:00-11:00?\n"
                    "• IF NOT: Execute 20 minutes of mindfulness/meditation now during Break 1.\n"
                    "• Hydration: Prepare Water Liter 2 of 4."
                ),
                'start_time': f"{date_str}T11:00:00",
                'end_time': f"{date_str}T11:30:00"
            },
            {
                'summary': f'📚 Block 1: {phase_title} Theory & Knowledge Study',
                'description': (
                    f"{block1_content}\n"
                    "• Documentation Link: " + doc_link + "\n"
                    "• Finish Water Liter 2 of 4.\n"
                    "• GUARDRAIL: Zero weed/news/socials; single-tab focus."
                ),
                'start_time': f"{date_str}T11:30:00",
                'end_time': f"{date_str}T13:30:00"
            },
            {
                'summary': '💡 01:30 PM (13:30) AI Knowledge & PBQ/Skills Assessment Prompt',
                'description': (
                    "• END OF BLOCK 1 REMINDER:\n"
                    "• Ask AI: 'What is my current percentage score in knowledge and PBQs/skills "
                    "(e.g., KQL, Subnetting, IAM) for this current period?'"
                ),
                'start_time': f"{date_str}T13:30:00",
                'end_time': f"{date_str}T14:00:00"
            },
            {
                'summary': '💻 Block 2: Hands-On Lab 1 (Terminal & CLI)',
                'description': (
                    f"{block2_lab_content}\n"
                    "• Terminal execution & CLI security tooling.\n"
                    "• MANDATE: Commit to GitHub via pre-made pathway (SecOps venv).\n"
                    "• Verify local environments and script outputs."
                ),
                'start_time': f"{date_str}T14:00:00",
                'end_time': f"{date_str}T16:00:00"
            },
            {
                'summary': '🧪 Block 3: Lab Intensive 2 (Theory + Lab Integration)',
                'description': (
                    f"{block3_lab_content}\n"
                    "• Deep technical lab integrations & practical scenarios.\n"
                    "• SUBSTANCE RULE: Zero weed prior to 05:15 PM earliest (weekdays)."
                ),
                'start_time': f"{date_str}T17:00:00",
                'end_time': f"{date_str}T19:00:00"
            },
            {
                'summary': '🔄 Block 4: Operational Closeout, Git Commit & Audit',
                'description': (
                    "• Finalize GitHub commits (`git push`).\n"
                    "• Visually inspect cloud infrastructure & GitHub repos.\n"
                    "• Review and adjust tomorrow's schedule."
                ),
                'start_time': f"{date_str}T19:00:00",
                'end_time': f"{date_str}T20:00:00"
            },
            {
                'summary': '📊 10:00 PM (22:00) Interactive Audit Sweep, Spiritual & Fitness Check',
                'description': (
                    "• Evening Spiritual Time: Did you complete 20 minutes of dedicated spiritual reflection?\n"
                    "• Apple Fitness Check: Progress toward 12,500 steps (Apple Health) & 1,050 active kcal (Apple Watch).\n"
                    "• Hydration Check: 4.0L total water achieved.\n"
                    "• Auto-schedule reinsertion blocks for any missed core deliverables."
                ),
                'start_time': f"{date_str}T22:00:00",
                'end_time': f"{date_str}T22:15:00"
            }
        ]

        for block in blocks:
            total_events_planned += 1
            if dry_run:
                print(f"[DRY RUN] {date_str} | {block['start_time']} - {block['end_time']}")
                print(f"  Summary: {block['summary']}")
                print(f"  Details: {block['description'].replace('\n', ' | ')}")
                print("-" * 80)
            else:
                event_blueprint = {
                    'summary': block['summary'],
                    'description': block['description'],
                    'start': {'dateTime': block['start_time'] + "-07:00", 'timeZone': 'America/Los_Angeles'},
                    'end': {'dateTime': block['end_time'] + "-07:00", 'timeZone': 'America/Los_Angeles'},
                    'reminders': {'useDefault': False, 'overrides': [{'method': 'popup', 'minutes': 10}]}
                }
                created = service.events().insert(calendarId='primary', body=event_blueprint).execute()
                logging.info(f"Created Event: {block['summary']} ({created.get('htmlLink')})")

        current_date += datetime.timedelta(days=1)

    logging.info(f"Schedule processing complete. Total events planned: {total_events_planned}")


def purge_existing_schedule(start_date, end_date):
    """
    Safely searches for and removes previous automated schedule events within the date range.
    """
    token_path = 'token.json'
    if not os.path.exists(token_path):
        logging.error("token.json not found! Cannot purge existing events.")
        return

    user_creds = Credentials.from_authorized_user_file(token_path, ['https://www.googleapis.com/auth/calendar'])
    service = build('calendar', 'v3', credentials=user_creds)

    time_min = f"{start_date.isoformat()}T00:00:00-07:00"
    time_max = f"{end_date.isoformat()}T23:59:59-07:00"

    logging.info(f"Searching for existing automated events between {time_min} and {time_max}...")

    events_result = service.events().list(
        calendarId='primary', 
        timeMin=time_min, 
        timeMax=time_max,
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    events = events_result.get('items', [])
    deleted_count = 0

    for event in events:
        summary = event.get('summary', '')
        if any(marker in summary for marker in ["Sovereign Wake Up", "Block 1:", "Block 2:", "Block 3:", "Block 4:", "Interactive Audit Sweep", "Mindfulness Checkpoint"]):
            event_id = event['id']
            service.events().delete(calendarId='primary', eventId=event_id).execute()
            deleted_count += 1
            logging.info(f"Deleted Event: {summary} (ID: {event_id})")

    logging.info(f"Purge complete. Total automated events deleted: {deleted_count}")


if __name__ == "__main__":
    START = datetime.date(2026, 10, 1)
    END = datetime.date(2027, 4, 1)

    print("===================================================================")
    print("           MASTER CERTIFICATION SCHEDULE DRY RUN PREVIEW           ")
    print("===================================================================")
    generate_schedule_blocks(START, END, dry_run=False)
