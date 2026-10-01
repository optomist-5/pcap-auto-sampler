#!/usr/bin/env bash
set -e

# Enforce strict gitignore hygiene
cat << 'GI' > .gitignore
venv/
secops/
bin/
lib/
include/
pyvenv.cfg
.env
*.pat
*.token
token.json
*.pcap
*.pcapng
.DS_Store
GI

# Set remote origin URL to SSH
git remote set-url origin git@github.com:optomist-5/pcap-auto-sampler.git

# Stage, commit, and push
git add .
git commit -m "feat(telemetry): sync multi-cloud security masterpiece & audit modules [$(date +'%Y-%m-%d %H:%M:%S')]" || echo "[!] Nothing new to commit."
git push -u origin main
