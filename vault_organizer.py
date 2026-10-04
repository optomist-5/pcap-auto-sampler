#!/usr/bin/env python3
import os
import shutil
import zipfile
from datetime import datetime

SECOPS_DIR = os.path.expanduser("~/secops")
DOCS_DIR = os.path.join(SECOPS_DIR, "docs")
SCRIPTS_DIR = os.path.join(SECOPS_DIR, "scripts")
ARCHIVE_DIR = os.path.join(SECOPS_DIR, "archive")

DOCS_TO_MOVE = [
    "LAB2_ENDPOINT_THREAT_HUNT.md",
    "NetworkPlus_SOC_Project_Master_Guide.pdf",
    "PROJECT_SUMMARY.md",
    "TROUBLESHOOTING_POSTMORTEM.md"
]

SCRIPTS_TO_MOVE = [
    "secops-clean.sh",
    "secops_sentinel.py",
    "sentinel_docgen.py"
]

def organize_files():
    print("\n" + "="*50)
    print("🧹 SECOPS VAULT ORGANIZER & BACKUP")
    print("="*50 + "\n")

    os.makedirs(DOCS_DIR, exist_ok=True)
    os.makedirs(SCRIPTS_DIR, exist_ok=True)
    os.makedirs(ARCHIVE_DIR, exist_ok=True)

    print("📂 Organizing Documents...")
    for doc in DOCS_TO_MOVE:
        src = os.path.join(SECOPS_DIR, doc)
        dest = os.path.join(DOCS_DIR, doc)
        if os.path.exists(src):
            shutil.move(src, dest)
            print(f"  ├── Moved: {doc} -> docs/")

    print("\n⚙️  Organizing Scripts...")
    for script in SCRIPTS_TO_MOVE:
        src = os.path.join(SECOPS_DIR, script)
        dest = os.path.join(SCRIPTS_DIR, script)
        if os.path.exists(src):
            shutil.move(src, dest)
            print(f"  ├── Moved: {script} -> scripts/")

def create_vault_backup():
    timestamp = datetime.now().strftime('%Y%m%d_%H%M')
    zip_filename = f"secops_vault_backup_{timestamp}.zip"
    zip_filepath = os.path.join(ARCHIVE_DIR, zip_filename)
    print(f"\n📦 Initiating Vault Backup...")
    
    with zipfile.ZipFile(zip_filepath, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(SECOPS_DIR):
            dirs[:] = [d for d in dirs if d not in ['.git', '.venv', 'archive']]
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, start=os.path.dirname(SECOPS_DIR))
                zipf.write(file_path, arcname)
    print(f"  └── 🟢 Success! Vault archived at: archive/{zip_filename}")
    print("\n" + "="*50)
    print("Nightly Cleanup Complete. System is Secure.")
    print("="*50 + "\n")

if __name__ == "__main__":
    organize_files()
    create_vault_backup()
