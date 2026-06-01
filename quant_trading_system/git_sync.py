"""Best-effort git commit + push, dispatched to an out-of-sandbox runner.

Architectural note
------------------
The harness runs inside a Cowork sandbox that has read/write access to the
user's workspace BUT cannot unlink files inside ``.git/`` (Operation not
permitted on ``.git/HEAD.lock``, ``.git/ORIG_HEAD.lock``, etc.). Running git
directly from the sandbox is therefore unreliable: any interrupted git
operation leaves a lock file that the harness itself cannot clean up, which
wedges every subsequent run.

Rather than fight the permission boundary, this module is now write-only.
``git_sync`` drops a small JSON marker into ``.git-sync-queue/`` describing
the commit the harness wants made. A launchd LaunchAgent on the user's mac
(``com.harness.gitrunner``, installed by ``scripts/install_git_safety.sh``)
polls the queue every 30 seconds, runs ``git add / commit / push`` from
outside the sandbox where it has full permission, and removes the marker on
success. A second LaunchAgent (``com.harness.gitlock``) sweeps stale
``.git/*.lock`` files every 10 seconds as a safety net.

If the launchd agents are not installed, markers simply accumulate in the
queue. The operator can either install the agents or process the queue
manually with ``scripts/process_git_sync_queue.sh``.
"""

from __future__ import annotations

import json
import logging
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from quant_trading_system.config import Settings
from quant_trading_system.memory import _REPO_ROOT

logger = logging.getLogger(__name__)

DEFAULT_BRANCH = "main"
QUEUE_DIRNAME = ".git-sync-queue"


def _is_git_repo(root: Path) -> bool:
    return (root / ".git").exists()


def _queue_dir(root: Path) -> Path:
    d = root / QUEUE_DIRNAME
    d.mkdir(parents=True, exist_ok=True)
    return d


def _local_iso_now() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def _marker_filename(agent: str) -> str:
    # Sortable, unique-per-call. Two runs in the same second get distinct
    # markers via PID + monotonic ns suffix.
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    suffix = f"{os.getpid()}-{time.monotonic_ns() % 1_000_000:06d}"
    return f"{ts}_{agent}_{suffix}.json"


def git_sync(
    settings: Settings,
    *,
    message: str,
    agent: str = "manual",
    push: bool = True,
    pull_first: bool = True,
) -> dict[str, Any]:
    """Queue a commit request for the out-of-sandbox git-runner daemon.

    Does NOT run git. Writes a JSON marker into ``<repo>/.git-sync-queue/``
    that the launchd ``com.harness.gitrunner`` agent picks up. Returns
    immediately. Idempotent: every call appends a new marker.

    Parameters
    ----------
    message : str
        Commit message. The agent's daily prompts already include the
        ``[agent yyyy-mm-dd]`` prefix; nothing is added here.
    agent : str
        Which agent is requesting the sync. Used in the marker filename
        and recorded in the JSON payload for the runner's log.
    push : bool
        Hint to the runner: should it push after commit? Default True.
    pull_first : bool
        Hint to the runner: should it ``git pull --rebase`` before
        committing? Default True.

    Returns
    -------
    dict
        Structured result the agent writes into its handoff. Includes
        ``ok``, ``queued`` (the marker file path), and a short
        ``steps`` list. No git commands have been run at return time.
    """
    root = _REPO_ROOT
    out: dict[str, Any] = {
        "ok": True,
        "repo": str(root),
        "queued": None,
        "steps": [],
        # These three are kept for backward-compat with old handoffs that
        # read them. The runner sets the real values; from the harness'
        # point of view we haven't done anything yet.
        "committed": False,
        "pushed": False,
    }

    if not _is_git_repo(root):
        out["ok"] = False
        out["error"] = f"not a git repo: {root}"
        return out

    queue_dir = _queue_dir(root)
    marker_path = queue_dir / _marker_filename(agent)
    payload = {
        "agent": agent,
        "message": message,
        "branch": DEFAULT_BRANCH,
        "push": bool(push),
        "pull_first": bool(pull_first),
        "created_at": _local_iso_now(),
        # The runner uses these to bootstrap config + token-auth origin if
        # the user hasn't already. Never log GITHUB_TOKEN — the runner
        # reads it directly from .env, not from the marker.
        "author_name": settings.GITHUB_AUTHOR_NAME,
        "author_email": settings.GITHUB_AUTHOR_EMAIL,
    }
    try:
        marker_path.write_text(
            json.dumps(payload, indent=2, sort_keys=True),
            encoding="utf-8",
        )
        out["queued"] = str(marker_path.relative_to(root))
        out["steps"].append(
            f"queued commit request at {marker_path.name} "
            f"(agent={agent}); the launchd git-runner will pick it up "
            f"within ~30s. If markers stack up in {QUEUE_DIRNAME}/ the "
            f"runner is not installed — run scripts/install_git_safety.sh "
            f"once from a real terminal."
        )
    except OSError as e:
        out["ok"] = False
        out["error"] = f"could not write queue marker: {e}"
        return out

    return out
