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

import logging
import os
import subprocess
from pathlib import Path
from typing import Any

from quant_trading_system.config import Settings
from quant_trading_system.memory import _REPO_ROOT

logger = logging.getLogger(__name__)

DEFAULT_BRANCH = "main"


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
