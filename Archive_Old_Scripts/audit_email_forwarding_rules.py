#!/usr/bin/env python3
"""
Mailbox Exfiltration Audit Module
Parses M365/Workspace inbox rules in JSON format to detect unauthorized external forwarding.
"""
import json
import sys

def audit_email_forwarding_rules(export_file_path: str) -> None:
    try:
        with open(export_file_path, 'r', encoding='utf-8') as f:
            rules_data = json.load(f)
            
        print("[+] Initiating Mailbox Exfiltration Audit...")
        alert_count = 0
        
        for rule in rules_data:
            rule_id = rule.get("id", "N/A")
            user_principal = rule.get("user_principal", "UNKNOWN")
            forward_target = rule.get("forwardTo", "")
            redirect_target = rule.get("redirectTo", "")
            
            destination = forward_target or redirect_target
            if destination and not destination.endswith("@yourcompany.com"):
                print(f"[ALERT] Unauthorized External Forwarding Rule Identified!")
                print(f"        Account: {user_principal}")
                print(f"        Rule Identifier: {rule_id}")
                print(f"        Exfiltration Address: {destination}\n")
                alert_count += 1
                    
        print(f"[+] Audit complete. Total suspicious rules identified: {alert_count}")
        
    except Exception as err:
        print(f"[-] Execution Error during inbox rule audit: {str(err)}")
        sys.exit(1)

if __name__ == "__main__":
    target_file = sys.argv[1] if len(sys.argv) > 1 else "multicloud_identity_telemetry.json"
    audit_email_forwarding_rules(target_file)
