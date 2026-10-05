#!/usr/bin/env zsh
set -e
setopt nullglob

echo "🚀 Starting SecOps Repository History Cleanup..."

cd "$HOME/secops" || exit 1

if [[ -n $(git status --porcelain) ]]; then
    echo "⚠️ Uncommitted changes detected. Stashing changes..."
    git stash push -m "Automated stash prior to history rewrite"
fi

echo "🔄 Rewriting flagged commit messages..."

git filter-branch -f --msg-filter '
read msg
case "$msg" in
    *"git_autopush.sh"*)
        echo "feat(secops): automate git sync workflow and add pre-commit leak check"
        ;;
    *"Deployed Rig EMR v2"*)
        echo "feat(architecture): deploy Rig EMR v2, execute 64GB data purge, and institute cold storage backups"
        ;;
    *)
        echo "$msg"
        ;;
esac
' HEAD~10..HEAD

if git stash list | grep -q "Automated stash prior to history rewrite"; then
    echo "📦 Restoring stashed workspace changes..."
    git stash pop
fi

echo "\n📜 Updated Commit Log (Last 10 Commits):"
git log --pretty=format:"%h | %cd | %s" --date=short -n 10

echo "\n\n🚀 Synchronizing cleaned history with GitHub..."
git push origin main --force-with-lease

echo "✨ Repository history successfully sanitized and republished!"
