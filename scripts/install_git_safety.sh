#!/usr/bin/env bash
# Permanent fix for the recurring git-from-sandbox problem.
#
# The harness lives in a Cowork sandbox that CANNOT unlink files inside
# .git/ (Operation not permitted on .git/HEAD.lock, .git/ORIG_HEAD.lock,
# etc.). Running git from the sandbox is therefore unreliable: any
# interrupted git op leaves a lock the harness can't clean up, which
# wedges every subsequent run.
#
# This script installs two launchd LaunchAgents on the user's mac that
# together make git-sync work reliably:
#
#   1. com.harness.gitlock     — every 10s, sweeps stale .git/*.lock
#                                files. The agents run OUTSIDE the
#                                sandbox so they have permission.
#   2. com.harness.gitrunner   — every 30s, picks up commit-request
#                                markers the harness drops in
#                                <repo>/.git-sync-queue/, runs
#                                add/commit/push, deletes the marker.
#
# Usage (run ONCE from your terminal):
#   bash /Users/rfoxes/Stock-Trading-Agent/scripts/install_git_safety.sh
#
# Verify everything's running:
#   launchctl list | grep harness
#
# Watch what they do:
#   tail -f /tmp/harness-gitlock.log /tmp/harness-gitrunner.log
#
# Uninstall later:
#   launchctl unload ~/Library/LaunchAgents/com.harness.gitlock.plist
#   launchctl unload ~/Library/LaunchAgents/com.harness.gitrunner.plist
#   rm ~/Library/LaunchAgents/com.harness.git*.plist

set -e

REPO_ROOT="/Users/rfoxes/Stock-Trading-Agent"
AGENTS_DIR="${HOME}/Library/LaunchAgents"

declare -a JOBS=(
    "com.harness.gitlock"
    "com.harness.gitrunner"
)

mkdir -p "$AGENTS_DIR"

# Clean up the broken shell-function wrapper from the very first install (if any).
for rc in "${HOME}/.zshrc" "${HOME}/.bashrc" "${HOME}/.bash_profile"; do
    [ -f "$rc" ] || continue
    if grep -q "harness git-safety wrapper" "$rc" 2>/dev/null; then
        echo "Removing old shell-function wrapper from $rc..."
        sed -i.bak '/# >>> harness git-safety wrapper/,/# <<< harness git-safety wrapper/d' "$rc"
    fi
done

# Sweep any stale locks RIGHT NOW so the operator isn't blocked while the
# gitlock daemon is still spinning up.
find "${REPO_ROOT}/.git" -maxdepth 3 -name "*.lock" -type f -delete 2>/dev/null || true

# Make sure the queue dir exists.
mkdir -p "${REPO_ROOT}/.git-sync-queue"

# Make the runner script executable.
chmod +x "${REPO_ROOT}/scripts/process_git_sync_queue.sh"

for label in "${JOBS[@]}"; do
    src="${REPO_ROOT}/scripts/${label}.plist"
    dst="${AGENTS_DIR}/${label}.plist"
    if [ ! -f "$src" ]; then
        echo "ERROR: $src not found. Pull latest from origin." >&2
        exit 1
    fi
    # Unload any prior version (idempotent)
    if launchctl list 2>/dev/null | grep -q "$label"; then
        echo "Unloading existing $label..."
        launchctl unload "$dst" 2>/dev/null || true
    fi
    cp "$src" "$dst"
    launchctl load "$dst"
    echo "Installed $label"
done

# Verify.
sleep 1
all_good=1
for label in "${JOBS[@]}"; do
    if launchctl list 2>/dev/null | grep -q "$label"; then
        echo "  $label: running"
    else
        echo "  $label: NOT running" >&2
        all_good=0
    fi
done

if [ "$all_good" = "1" ]; then
    cat <<'EOF'

Installed and running.

What now happens automatically:
  - .git/*.lock files older than 60s are swept every 10s
    (logged to /tmp/harness-gitlock.log)
  - Commit markers the harness drops in .git-sync-queue/ are
    processed every 30s, committing + pushing on your behalf
    (logged to /tmp/harness-gitrunner.log)

You do NOT need to clear lock files by hand anymore. You do NOT need
to push manually after harness runs — markers stack up if a push
fails, and get retried automatically next cycle.

Verify any time:   launchctl list | grep harness
Watch live:        tail -f /tmp/harness-gitrunner.log
EOF
else
    echo ""
    echo "ERROR: one or more LaunchAgents failed to load." >&2
    echo "Try manually:" >&2
    for label in "${JOBS[@]}"; do
        echo "  launchctl load ${AGENTS_DIR}/${label}.plist" >&2
    done
    exit 1
fi
