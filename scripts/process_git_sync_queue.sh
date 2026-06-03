#!/usr/bin/env bash
# Process pending git-sync requests written by the harness.
#
# The harness sandbox cannot run git (it can't unlink .git/*.lock files).
# Instead, each agent's `cli git-sync` call drops a JSON marker into
# <repo>/.git-sync-queue/. This script — run from the user's mac, OUTSIDE
# the sandbox, by a launchd LaunchAgent (`com.harness.gitrunner`) — picks
# up each marker, runs the commit + push, and removes the marker on
# success.
#
# Designed to be safe to run from a cron-like polling agent every 30s:
#   - holds a flock so two invocations don't trample each other
#   - leaves markers in place on failure so we retry next cycle
#   - is idempotent on partial state (already-committed nothing-to-push, etc.)
#
# Can also be run by hand:   bash scripts/process_git_sync_queue.sh
#
# Logs to /tmp/harness-gitrunner.log via the plist's StandardOutPath.

set -u

REPO_ROOT="/Users/rfoxes/Stock-Trading-Agent"
QUEUE_DIR="${REPO_ROOT}/.git-sync-queue"
LOCK_DIR="/tmp/harness-gitrunner.lockd"
LOG_PREFIX="$(date '+%Y-%m-%dT%H:%M:%S%z') gitrunner:"

cd "$REPO_ROOT" || { echo "$LOG_PREFIX cannot cd $REPO_ROOT"; exit 1; }

# Single-instance guard — mkdir is atomic on POSIX (works on macOS without
# requiring flock, which ships with Linux util-linux but not with macOS).
# If the lockdir already exists and is older than 5 minutes, it's stale
# (a prior run crashed before the trap fired) and we forcibly reclaim it.
if ! mkdir "$LOCK_DIR" 2>/dev/null; then
    if [ -n "$(find "$LOCK_DIR" -maxdepth 0 -mmin +5 2>/dev/null)" ]; then
        echo "$LOG_PREFIX reclaiming stale lock $LOCK_DIR"
        rmdir "$LOCK_DIR" 2>/dev/null || true
        mkdir "$LOCK_DIR" 2>/dev/null || exit 0
    else
        # Another invocation is processing the queue. Quiet exit.
        exit 0
    fi
fi
trap 'rmdir "$LOCK_DIR" 2>/dev/null || true' EXIT

# Nothing to do?
if [ ! -d "$QUEUE_DIR" ]; then
    exit 0
fi
markers=()
while IFS= read -r -d '' f; do
    markers+=("$f")
done < <(find "$QUEUE_DIR" -maxdepth 1 -type f -name "*.json" -print0 | sort -z)

if [ "${#markers[@]}" -eq 0 ]; then
    exit 0
fi

echo "$LOG_PREFIX found ${#markers[@]} pending marker(s)"

# Load .env so GITHUB_TOKEN / GITHUB_USER / GITHUB_AUTHOR_* are available.
if [ -f "${REPO_ROOT}/.env" ]; then
    set -a
    # shellcheck disable=SC1091
    . "${REPO_ROOT}/.env"
    set +a
fi

# Bootstrap git config (idempotent).
if [ -n "${GITHUB_AUTHOR_NAME:-}" ]; then
    git config user.name  "${GITHUB_AUTHOR_NAME}"
fi
if [ -n "${GITHUB_AUTHOR_EMAIL:-}" ]; then
    git config user.email "${GITHUB_AUTHOR_EMAIL}"
fi

# Rewrite origin to embed the token (idempotent).
if [ -n "${GITHUB_TOKEN:-}" ] && [ -n "${GITHUB_USER:-}" ]; then
    current="$(git remote get-url origin 2>/dev/null || true)"
    case "$current" in
        https://*)
            # Strip any existing user:token@ prefix
            after_scheme="${current#https://}"
            host_and_path="${after_scheme##*@}"
            target="https://${GITHUB_USER}:${GITHUB_TOKEN}@${host_and_path}"
            if [ "$current" != "$target" ]; then
                git remote set-url origin "$target" >/dev/null 2>&1 || true
            fi
            ;;
    esac
fi

# Sweep any stale locks before we start — belt-and-suspenders with the
# com.harness.gitlock sweeper. We're outside the sandbox, so this works.
find "${REPO_ROOT}/.git" -maxdepth 3 -name "*.lock" -type f -mmin +1 -delete 2>/dev/null || true

# Process each marker in chronological order (filename starts with ISO ts).
processed=0
failed=0
for marker in "${markers[@]}"; do
    name="$(basename "$marker")"
    # Parse fields with a tiny python helper to avoid sed/jq fragility.
    parsed=$(/usr/bin/python3 - "$marker" <<'PY' 2>/dev/null
import json, sys
try:
    with open(sys.argv[1], "r", encoding="utf-8") as f:
        d = json.load(f)
except Exception as e:
    print(f"PARSE_ERROR\t{e}")
    sys.exit(0)
print("OK")
print(d.get("agent", "manual"))
print(d.get("branch", "main"))
print("1" if d.get("push", True) else "0")
print("1" if d.get("pull_first", True) else "0")
# Message LAST and unescaped — newlines preserved as literal \n.
msg = d.get("message", "")
print(msg.replace("\r", "").replace("\n", " "))
PY
)
    if [ -z "$parsed" ]; then
        echo "$LOG_PREFIX $name: empty parse output; skipping"
        failed=$((failed+1))
        continue
    fi
    first_line="$(echo "$parsed" | head -n1)"
    if [ "$first_line" != "OK" ]; then
        echo "$LOG_PREFIX $name: $first_line"
        failed=$((failed+1))
        continue
    fi
    agent="$(echo "$parsed" | sed -n '2p')"
    branch="$(echo "$parsed" | sed -n '3p')"
    do_push="$(echo "$parsed" | sed -n '4p')"
    do_pull="$(echo "$parsed" | sed -n '5p')"
    message="$(echo "$parsed" | sed -n '6p')"

    echo "$LOG_PREFIX processing $name agent=$agent branch=$branch"

    # Pull first to absorb operator edits (best-effort).
    if [ "$do_pull" = "1" ]; then
        if ! git pull --rebase --autostash origin "$branch" >>/tmp/harness-gitrunner.log 2>&1; then
            echo "$LOG_PREFIX $name: pull failed (continuing — may be first push)"
        fi
    fi

    git add -A
    # Anything staged?
    if git diff --cached --quiet; then
        echo "$LOG_PREFIX $name: nothing staged, treating as no-op success"
        rm -f -- "$marker"
        processed=$((processed+1))
        continue
    fi

    if ! git commit -m "$message" >>/tmp/harness-gitrunner.log 2>&1; then
        echo "$LOG_PREFIX $name: commit failed; leaving marker for retry"
        failed=$((failed+1))
        continue
    fi

    if [ "$do_push" = "1" ]; then
        if ! git push origin "$branch" >>/tmp/harness-gitrunner.log 2>&1; then
            echo "$LOG_PREFIX $name: push failed; leaving marker for retry (commit is local)"
            failed=$((failed+1))
            continue
        fi
    fi

    rm -f -- "$marker"
    processed=$((processed+1))
    echo "$LOG_PREFIX $name: done"
done

echo "$LOG_PREFIX cycle complete: processed=$processed failed=$failed"
