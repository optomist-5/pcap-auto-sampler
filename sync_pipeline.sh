#!/usr/bin/env bash
set -e

# Enforce strict gitignore boundaries
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

# Explicitly set SSH remote URL
git remote set-url origin git@github.com:optomist-5/pcap-auto-sampler.git

# Stage, commit, and push over SSH
git add .
git commit -m "feat(pipeline): sync workspace state [$(date +'%Y-%m-%d %H:%M:%S')]" || echo "[!] Nothing new to commit."
git push -u origin main
