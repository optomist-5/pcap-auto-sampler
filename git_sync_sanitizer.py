#!/usr/bin/env python3
import os, sys, re, subprocess
from datetime import datetime

GITHUB_USER = "Optomist-5"
REPO_NAME = "security-plus-pbq-labs"
REMOTE_URL = f"git@github.com:{GITHUB_USER}/{REPO_NAME}.git"

SENSITIVE_PATTERNS = [
    (re.compile(r'/Users/mq/'), '$HOME/'),
    (re.compile(r'ghp_[a-zA-Z0-9]{36}'), 'ghp_REDACTED_PAT_TOKEN'),
]

def run_cmd(cmd):
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"[-] Warning/Error: {res.stderr.strip()}", file=sys.stderr)
        return False
    if res.stdout.strip():
        print(f"[+] {res.stdout.strip()}")
    return True

def enforce_gitignore():
    rules = "venv/\nsecops/\n.env\n*.pat\n*.token\ntoken.json\n*.pcap\n*.pcapng\n.DS_Store\n"
    with open(".gitignore", "w") as f:
        f.write(rules)

def sanitize_file(filepath):
    if not filepath.endswith(('.py', '.md', '.json', '.sh', '.txt')) or "git_sync_sanitizer.py" in filepath:
        return
    try:
        with open(filepath, 'r') as f:
            content = f.read()
        sanitized = content
        for pattern, replacement in SENSITIVE_PATTERNS:
            sanitized = pattern.sub(replacement, sanitized)
        if sanitized != content:
            with open(filepath, 'w') as f:
                f.write(sanitized)
            print(f"[+] Sanitized: {filepath}")
    except Exception:
        pass

def main():
    enforce_gitignore()
    for root, _, files in os.walk("."):
        if "venv" in root or "secops" in root or ".git" in root:
            continue
        for file in files:
            sanitize_file(os.path.join(root, file))

    if not os.path.exists(".git"):
        run_cmd("git init")
        run_cmd("git branch -M main")

    run_cmd("git remote remove origin 2>/dev/null")
    run_cmd(f"git remote add origin {REMOTE_URL}")

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("[*] Staging, committing, and pushing sanitized files...")
    run_cmd("git add .")
    run_cmd(f'git commit -m "feat(pbq): sanitize PII and sync labs [{timestamp}]"')
    run_cmd("git push -u origin main")

if __name__ == "__main__":
    main()
