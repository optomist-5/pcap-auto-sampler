#!/usr/bin/env python3
import os
from datetime import datetime

def run_vault_audit():
    secops_dir = os.path.expanduser("~/secops")
    print("\n" + "="*50)
    print("🛡️  SECOPS VAULT RECONNAISSANCE AUDIT")
    print(f"📅 Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*50 + "\n")
    if not os.path.exists(secops_dir):
        print(f"[!] Critical Error: Directory {secops_dir} not found.")
        return
    loose_files = []
    directories = []
    backups = []
    core_folders = ['data', 'scripts', 'logs', 'reports', 'archive', 'docs']
    for item in os.listdir(secops_dir):
        full_path = os.path.join(secops_dir, item)
        if os.path.isdir(full_path):
            directories.append(item)
        elif os.path.isfile(full_path):
            if item.endswith(('.zip', '.tar.gz', '.tar')):
                backups.append(item)
            elif not item.startswith('.') and item != "vault_auditor.py":
                loose_files.append((item, full_path))
    print("📂 CURRENT DIRECTORIES:")
    for d in sorted(directories):
        status = " (Core)" if d in core_folders else " (Custom)"
        print(f"  ├── {d}{status}")
    print("\n📄 LOOSE FILES (Pending Organization):")
    if loose_files:
        for f, path in sorted(loose_files):
            if f.endswith('.md') or f.endswith('.pdf'):
                print(f"  ├── [DOC]  {f}")
            elif f.endswith('.py') or f.endswith('.sh') or f.endswith('.zsh'):
                print(f"  ├── [CODE] {f}")
            else:
                print(f"  ├── [MISC] {f}")
    else:
        print("  └── None! All files are neatly categorized.")
    print("\n📦 VAULT BACKUP STATUS:")
    if backups:
        for b in backups:
            print(f"  ├── {b}")
    else:
        print("  └── ⚠️ No .zip or .tar backups found in the root directory.")
    print("\n" + "="*50)
    print("Next Step: Review loose files to determine cleanup routing logic.")
    print("="*50 + "\n")

if __name__ == "__main__":
    run_vault_audit()
