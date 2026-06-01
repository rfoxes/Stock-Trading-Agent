"""Best-effort git commit + push so agents can persist their work to GitHub.

Each scheduled-task agent calls `cli git-sync --message "..."` as its final
action. The helper:

  1. Bootstraps git config (user.name / user.email) from settings — idempotent.
  2. Rewrites `origin` to HTTPS-with-token if GITHUB_TOKEN + GITHUB_USER are
     set in .env — also idempotent.
  3. Runs `git pull --rebase --autostash` to absorb any operator edits.
  4. Stages every change with `git add -A`.
  5. Commits with the provided message (skips silently if nothing's staged).
  6. Pushes to origin.

All steps are best-effort. A git failure does NOT fail the run — the agent
logs the issue in its handoff and continues. The harness's primary work is
trading and writing markdown; pushing to GitHub is a nice-to-have.
"""

from __future__ import annotations

import atexit
import logging
import os
import signal
import subprocess
import time
from pathlib import Path
from typing import Any

from quant_trading_system.config import Settings
from quant_trading_system.memory import _REPO_ROOT

logger = logging.getLogger(__name__)

DEFAULT_BRANCH = "main"

# How old a lock file must be for us to consider it stale and remove it.
# A lock newer than this could be a legitimate concurrent git process.
STALE_LOCK_AGE_SECONDS = 60  # 1 minute — git operations rarely take longer

# Known lock files git creates. We only sweep these; anything else stays.
LOCK_FILE_PATTERNS = (
    ".git/HEAD.lock",
    ".git/index.lock",
    ".git/packed-refs.lock",
    ".git/ORIG_HEAD.lock",
    ".git/FETCH_HEAD.lock",
    ".git/MERGE_HEAD.lock",
    ".git/CHERRY_PICK_HEAD.lock",
    ".git/REVERT_HEAD.lock",
)


def _run(cmd: list[str], cwd: Path, *, capture: bool = True) -> tuple[int, str, str]:
    """Run a git command, return (rc, stdout, stderr). Never raises."""
    try:
        proc = subprocess.run(
            cmd, cwd=str(cwd),
            capture_output=capture, text=True, timeout=60,
        )
        return proc.returncode, proc.stdout or "", proc.stderr or ""
    except subprocess.TimeoutExpired:
        return 124, "", "timeout"
    except FileNotFoundError as e:
        return 127, "", f"command not found: {e}"
    except Exception as e:
        return 1, "", f"subprocess error: {e}"


def _is_git_repo(root: Path) -> bool:
    return (root / ".git").exists()


def _sweep_all_locks_unconditional(root: Path) -> list[str]:
    """Aggressively remove ALL .git lock files regardless of age.

    Used by signal handlers and atexit hooks: when this process is dying or
    has just died, any lock it created is by definition stale. We want to
    leave the repo clean for the next operation (whether harness or
    operator).
    """
    removed: list[str] = []
    candidates: list[Path] = [root / p for p in LOCK_FILE_PATTERNS]
    for sub in (".git/refs/heads", ".git/refs/remotes", ".git/refs/tags"):
        d = root / sub
        if d.exists():
            for p in d.rglob("*.lock"):
                candidates.append(p)
    for p in candidates:
        if not p.exists():
            continue
        try:
            p.unlink()
            removed.append(str(p.relative_to(root)))
        except OSError:
            pass
    return removed


def _install_cleanup_handlers(root: Path) -> None:
    """Wire SIGTERM / SIGINT / atexit so we never leave a lock behind.

    Idempotent — multiple installs collapse to one handler chain.
    """
    cleaned = {"done": False}

    def _cleanup(*_args: Any) -> None:
        if cleaned["done"]:
            return
        cleaned["done"] = True
        try:
            _sweep_all_locks_unconditional(root)
        except Exception:
            pass

    atexit.register(_cleanup)
    # Only install signal handlers on the main thread; in worker threads
    # signal.signal raises ValueError.
    try:
        signal.signal(signal.SIGTERM, lambda *a: (_cleanup(), os._exit(143)))
        signal.signal(signal.SIGINT, lambda *a: (_cleanup(), os._exit(130)))
    except (ValueError, AttributeError):
        pass


def _sweep_stale_locks(root: Path) -> tuple[list[str], list[str]]:
    """Remove .git lock files older than STALE_LOCK_AGE_SECONDS.

    Locks newer than the threshold are left alone (they might be from a
    legitimate concurrent process). Returns (removed, kept_too_recent)
    so the caller can log + warn appropriately.
    """
    removed: list[str] = []
    kept: list[str] = []
    now = time.time()
    # Fixed-name locks
    candidates: list[Path] = [root / p for p in LOCK_FILE_PATTERNS]
    # Per-ref locks under refs/heads, refs/remotes, refs/tags
    for sub in (".git/refs/heads", ".git/refs/remotes", ".git/refs/tags"):
        d = root / sub
        if d.exists():
            for p in d.rglob("*.lock"):
                candidates.append(p)
    for p in candidates:
        if not p.exists():
            continue
        try:
            age = now - p.stat().st_mtime
        except OSError:
            continue
        rel = str(p.relative_to(root))
        if age < STALE_LOCK_AGE_SECONDS:
            kept.append(f"{rel} (age {int(age)}s)")
            continue
        try:
            p.unlink()
            removed.append(f"{rel} (age {int(age)}s)")
        except OSError as e:
            kept.append(f"{rel} (unlink failed: {e})")
    return removed, kept


def _bootstrap_config(settings: Settings, root: Path) -> list[str]:
    """Set user.name + user.email if not already set. Returns log lines."""
    log: list[str] = []
    rc, out, _ = _run(["git", "config", "user.name"], root)
    if rc != 0 or not out.strip():
        rc, _, err = _run(["git", "config", "user.name", settings.GITHUB_AUTHOR_NAME], root)
        log.append(f"set user.name={settings.GITHUB_AUTHOR_NAME!r} (rc={rc})")
    rc, out, _ = _run(["git", "config", "user.email"], root)
    if rc != 0 or not out.strip():
        rc, _, err = _run(["git", "config", "user.email", settings.GITHUB_AUTHOR_EMAIL], root)
        log.append(f"set user.email={settings.GITHUB_AUTHOR_EMAIL!r} (rc={rc})")
    return log


def _configure_origin_with_token(settings: Settings, root: Path) -> list[str]:
    """If GITHUB_TOKEN + GITHUB_USER are set, rewrite origin to embed the token.

    Idempotent. Only rewrites when the remote is missing the token. Returns
    log lines (without exposing the token).
    """
    log: list[str] = []
    if not (settings.GITHUB_TOKEN and settings.GITHUB_USER):
        return log
    rc, out, _ = _run(["git", "remote", "get-url", "origin"], root)
    if rc != 0:
        log.append("origin not configured; skipping URL rewrite")
        return log
    current = out.strip()
    if not current.startswith("https://"):
        # Don't touch SSH remotes or other configurations
        log.append("origin is not HTTPS; leaving URL alone")
        return log
    # Strip any existing user:token@ prefix to keep this idempotent
    after_scheme = current[len("https://"):]
    host_and_path = after_scheme.split("@", 1)[-1]
    target = f"https://{settings.GITHUB_USER}:{settings.GITHUB_TOKEN}@{host_and_path}"
    if current == target:
        return log  # already correct
    rc, _, err = _run(["git", "remote", "set-url", "origin", target], root)
    log.append(
        f"rewrote origin to HTTPS-with-token (rc={rc}); "
        f"host={host_and_path}"
    )
    return log


def _current_branch(root: Path) -> str:
    rc, out, _ = _run(["git", "rev-parse", "--abbrev-ref", "HEAD"], root)
    if rc == 0 and out.strip():
        return out.strip()
    return DEFAULT_BRANCH


def git_sync(
    settings: Settings,
    *,
    message: str,
    push: bool = True,
    pull_first: bool = True,
) -> dict[str, Any]:
    """The whole flow: bootstrap config, pull, add, commit, push.

    Returns a structured result the agent can read.
    """
    root = _REPO_ROOT
    out: dict[str, Any] = {
        "ok": True,
        "repo": str(root),
        "steps": [],
        "committed": False,
        "pushed": False,
    }

    if not _is_git_repo(root):
        out["ok"] = False
        out["error"] = f"not a git repo: {root}"
        return out

    # Install cleanup handlers so SIGTERM / SIGINT / interpreter exit never
    # leaves a stale lock behind. Belt-and-suspenders with the stale sweep
    # below.
    _install_cleanup_handlers(root)

    # Self-heal stale .git/*.lock files from previously-killed git processes.
    # Locks newer than STALE_LOCK_AGE_SECONDS are left alone (legitimate concurrency).
    removed_locks, kept_locks = _sweep_stale_locks(root)
    if removed_locks:
        out["steps"].append(
            f"removed stale locks: {', '.join(removed_locks)}"
        )
    if kept_locks:
        out["steps"].append(
            f"WARNING: recent lock files present, not removing: "
            f"{', '.join(kept_locks)}"
        )
        # If there's a recent HEAD.lock or index.lock, git operations will
        # almost certainly fail. Report and bail rather than wedging.
        critical = [
            k for k in kept_locks
            if k.startswith((".git/HEAD.lock", ".git/index.lock"))
        ]
        if critical:
            out["ok"] = False
            out["error"] = (
                f"recent git lock(s) present: {critical}. "
                "A concurrent git process may be running, or the lock is <5min "
                "old. Wait or remove the lock(s) manually if no process is live."
            )
            return out

    out["steps"].extend(_bootstrap_config(settings, root))
    out["steps"].extend(_configure_origin_with_token(settings, root))

    branch = _current_branch(root)
    out["branch"] = branch

    if pull_first:
        rc, stdout, stderr = _run(
            ["git", "pull", "--rebase", "--autostash", "origin", branch], root,
        )
        out["steps"].append(f"pull rc={rc}; {(stderr or stdout).strip()[:200]}")
        if rc != 0:
            # Don't bail — a missing upstream or first-time push is fine.
            out["pull_warning"] = (stderr or stdout).strip()[:500]

    rc, _, _ = _run(["git", "add", "-A"], root)
    out["steps"].append(f"add -A rc={rc}")

    # Check if anything is staged
    rc, stdout, _ = _run(["git", "diff", "--cached", "--name-only"], root)
    staged = [line for line in stdout.splitlines() if line.strip()]
    out["staged_files"] = staged[:50]
    out["staged_count"] = len(staged)

    if not staged:
        out["steps"].append("nothing to commit")
        return out

    rc, stdout, stderr = _run(
        ["git", "commit", "-m", message], root,
    )
    out["steps"].append(f"commit rc={rc}; {(stderr or stdout).strip()[:200]}")
    if rc != 0:
        out["ok"] = False
        out["error"] = (stderr or stdout).strip()[:500]
        return out
    out["committed"] = True

    if push:
        rc, stdout, stderr = _run(
            ["git", "push", "origin", branch], root,
        )
        out["steps"].append(f"push rc={rc}; {(stderr or stdout).strip()[:200]}")
        if rc != 0:
            out["ok"] = False
            out["error"] = (stderr or stdout).strip()[:500]
            out["push_failed_but_committed_locally"] = True
            return out
        out["pushed"] = True

    return out
