#!/usr/bin/env bash
# Install a permanent shell wrapper that auto-sweeps stale .git/*.lock files
# before every `git` command in this repo. Idempotent — running this twice
# is a no-op.
#
# Usage (run ONCE from your terminal):
#   bash /Users/rfoxes/Stock-Trading-Agent/scripts/install_git_safety.sh
#
# After this, every `git pull`, `git push`, `git status` etc. that you run
# from any terminal first sweeps stale locks (>30s old) under
# /Users/rfoxes/Stock-Trading-Agent/.git/. You will never hit the
# "Unable to create '.git/<X>.lock': File exists" error from your terminal
# again — the wrapper cleans up before each invocation.

set -e

REPO_ROOT="/Users/rfoxes/Stock-Trading-Agent"
RC_FILE="${ZDOTDIR:-$HOME}/.zshrc"
[ "$(basename "$SHELL")" = "bash" ] && RC_FILE="$HOME/.bashrc"
[ -z "$RC_FILE" ] && RC_FILE="$HOME/.zshrc"

MARK_BEGIN="# >>> harness git-safety wrapper (managed by install_git_safety.sh)"
MARK_END="# <<< harness git-safety wrapper"

read -r -d '' BLOCK <<EOF || true
${MARK_BEGIN}
# Wraps \`git\` so stale .git/*.lock files in the Stock-Trading-Agent repo are
# swept before every git invocation. Locks older than 30 seconds are removed;
# fresh locks from a real concurrent process are left alone. Only active when
# you are inside the Stock-Trading-Agent repo or operating on it explicitly.
git() {
    local _repo="${REPO_ROOT}"
    if [ -d "\$_repo/.git" ]; then
        find "\$_repo/.git" -maxdepth 3 -name "*.lock" -type f -mmin +0 -delete 2>/dev/null
    fi
    command git "\$@"
}
${MARK_END}
EOF

# Remove any previous installation
if grep -q "$MARK_BEGIN" "$RC_FILE" 2>/dev/null; then
    echo "Existing wrapper found in $RC_FILE — replacing..."
    # Use sed to remove the block between markers
    sed -i.bak "/$MARK_BEGIN/,/$MARK_END/d" "$RC_FILE"
fi

# Append the new block
echo "" >> "$RC_FILE"
echo "$BLOCK" >> "$RC_FILE"

echo "Wrapper installed in $RC_FILE."
echo ""
echo "Activate it now (or open a new terminal):"
echo "    source $RC_FILE"
echo ""
echo "Then test by running an intentional `git` command — the wrapper runs"
echo "silently before each invocation. Even if a lock file exists, your next"
echo "git command will clean it up automatically."
