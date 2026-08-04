"""Thin git wrapper for the bot's repo sync — no Telegram coupling here.

Two directions, both deliberately narrow:
- Down: pull_ff_only on the periodic git-sync tick. Fast-forward only: a
  stray local edit that diverged from origin must fail loudly with the
  working tree untouched — never auto-merge, never overwrite local work.
- Up: commit_and_push, used by the /posted archive flow and (added
  2026-07-22) the /fix correction-request flow — each call scoped to only
  the exact paths that flow touched. The bot must never sweep an
  interactive session's in-progress edits into an unattended commit. A
  rejected push is reported, not resolved (no rebase, no force).
"""

from __future__ import annotations

import subprocess
from pathlib import Path


def _run(repo_root: Path, *args: str, timeout: int = 60) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", *args],
        cwd=repo_root,
        capture_output=True,
        text=True,
        timeout=timeout,
    )


def has_repo(repo_root: Path) -> bool:
    return (repo_root / ".git").is_dir()


def pull_ff_only(repo_root: Path) -> subprocess.CompletedProcess:
    return _run(repo_root, "pull", "--ff-only")


def dirty_files(repo_root: Path) -> list[str]:
    """Porcelain status lines — non-empty means uncommitted local work
    (which the nightly cloud runs, reading GitHub, cannot see)."""
    result = _run(repo_root, "status", "--porcelain")
    if result.returncode != 0:
        return []
    return [line for line in result.stdout.splitlines() if line.strip()]


def tracked_files(repo_root: Path, subdir: str) -> set[str]:
    """Repo-relative POSIX paths git currently tracks under subdir."""
    result = _run(repo_root, "ls-files", "-z", "--", subdir)
    if result.returncode != 0:
        return set()
    return {p for p in result.stdout.split("\0") if p}


def commit_and_push(repo_root: Path, paths: list[str], message: str) -> tuple[bool, str]:
    """Commit exactly `paths` (repo-relative pathspecs — additions and
    deletions alike) and push. Pulls --ff-only first to shrink the
    divergence window; on any failure it stops and reports rather than
    resolving (the working tree keeps the changes either way).
    Returns (ok, human-readable note)."""
    pull = pull_ff_only(repo_root)
    if pull.returncode != 0:
        detail = (pull.stderr or pull.stdout).strip()[-300:]
        return False, f"pull failed before committing ({detail})"

    add = _run(repo_root, "add", "-A", "--", *paths)
    if add.returncode != 0:
        detail = (add.stderr or add.stdout).strip()[-300:]
        return False, f"add failed ({detail})"

    commit = _run(repo_root, "commit", "-m", message, "--", *paths)
    if commit.returncode != 0:
        out = (commit.stderr or commit.stdout).strip()
        # Phrasing varies: "nothing to commit", "nothing added to commit",
        # "no changes added to commit" — all mean the same no-op.
        if "nothing to commit" in out or "added to commit" in out:
            return True, "nothing new to commit"
        return False, f"commit failed ({out[-300:]})"

    push = _run(repo_root, "push", timeout=120)
    if push.returncode != 0:
        detail = (push.stderr or push.stdout).strip()[-300:]
        return False, f"commit created locally but push failed ({detail})"
    return True, "committed and pushed"
