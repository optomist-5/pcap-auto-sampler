#!/bin/bash

STREAMING_CHUNK: Defining color variables for terminal output...

We use ANSI escape codes here to give your terminal that clinical/SecOps color-coding.

GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

STREAMING_CHUNK: Performing pre-flight checks...

echo -e "${BLUE}[*] Initiating GitHub Sync Protocol...${NC}"

Check if the current folder is actually a tracked Git repository.

The "-d" flag checks if a directory named ".git" exists.

if [ ! -d ".git" ]; then
echo -e "${RED}[!] Error: This directory is not a Git repository.${NC}"
echo "To fix this, run 'git init' and link your GitHub repo first."
exit 1
fi

STREAMING_CHUNK: Capturing user input for the commit message...

The 'read' command pauses the script and waits for you to type something.

read -p "Enter commit message (Press Enter for default timestamp): " commit_message

If the string (-z) is empty (meaning you just hit Enter), we auto-generate a clinical timestamp.

if [ -z "$commit_message" ]; then
commit_message="SecOps Lab Sync: $(date +'%Y-%m-%d %H:%M:%S')"
fi

STREAMING_CHUNK: Executing the standard Git deployment pipeline...

echo -e "${BLUE}[*] Staging all modified files...${NC}"
git add .

echo -e "${BLUE}[*] Committing to local vault...${NC}"
git commit -m "$commit_message"

echo -e "${BLUE}[*] Pushing to remote GitHub server...${NC}"

We use an 'if' statement on the 'git push'. If it succeeds, it prints green. If it fails, it prints red.

if git push; then
echo -e "${GREEN}[+] Sync Successful! SecOps repository is up to date.${NC}"
else
echo -e "${RED}[!] Push failed. Please check your GitHub permissions or network connection.${NC}"
fi
