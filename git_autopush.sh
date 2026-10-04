#!/bin/bash

# STREAMING_CHUNK: Defining color variables for terminal output...
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

# STREAMING_CHUNK: Performing pre-flight checks...
echo -e "${BLUE}[*] Initiating GitHub Sync Protocol...${NC}"

if [ ! -d ".git" ]; then
    echo -e "${RED}[!] Error: This directory is not a Git repository.${NC}"
    echo "To fix this, run 'git init' and link your GitHub repo first."
    exit 1
fi

# STREAMING_CHUNK: Capturing user input for the commit message...
read -p "Enter commit message (Press Enter for default timestamp): " commit_message

# STREAMING_CHUNK: Evaluating user input for default values...
if [ -z "$commit_message" ]; then
    commit_message="SecOps Lab Sync: $(date +'%Y-%m-%d %H:%M:%S')"
fi

# STREAMING_CHUNK: Executing the standard Git deployment pipeline...
echo -e "${BLUE}[*] Staging all modified files...${NC}"
git add .

echo -e "${BLUE}[*] Committing to local vault...${NC}"
git commit -m "$commit_message"

# STREAMING_CHUNK: Pushing to remote GitHub server...
echo -e "${BLUE}[*] Pushing to remote GitHub server...${NC}"
if git push; then
    echo -e "${GREEN}[+] Sync Successful! SecOps repository is up to date.${NC}"
else
    echo -e "${RED}[!] Push failed. Please check your GitHub permissions or network connection.${NC}"
fi
