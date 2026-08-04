"""Configuration for the brand internal assistant bot.

All settings come from environment variables (or a .env file next to this
module). See .env.example for the full list.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from datetime import time
from pathlib import Path
from zoneinfo import ZoneInfo

BOT_DIR = Path(__file__).resolve().parent
DEFAULT_REPO_ROOT = BOT_DIR.parent  # the brand workspace folder


def _load_dotenv(path: Path) -> None:
    """Minimal .env loader — no extra dependency needed."""
    if not path.is_file():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


@dataclass
class Config:
    token: str
    allowed_user_ids: frozenset[int]
    repo_root: Path
    timezone: ZoneInfo
    reminder_time: time | None  # None disables the daily morning reminder
    draft_reminder_time: time | None  # None disables the nightly draft-status reminder
    git_sync_interval: int | None  # seconds; None disables the periodic git pull

    planner_path: Path = field(init=False)
    queue_dir: Path = field(init=False)
    analysis_dir: Path = field(init=False)
    state_path: Path = field(init=False)

    def __post_init__(self) -> None:
        self.planner_path = self.repo_root / "data" / "content_planner.md"
        self.queue_dir = self.repo_root / "social" / "queue"
        self.analysis_dir = self.repo_root / "presentations" / "data-analysis"
        self.state_path = BOT_DIR / "state" / "pushed.json"


def load_config() -> Config:
    _load_dotenv(BOT_DIR / ".env")

    token = os.environ.get("BRAND_BOT_TOKEN", "")
    if not token:
        raise SystemExit(
            "BRAND_BOT_TOKEN is not set. Create bot/.env from bot/.env.example "
            "and paste the token you got from @BotFather."
        )

    raw_ids = os.environ.get("BRAND_ALLOWED_USER_IDS", "")
    allowed = frozenset(
        int(part) for part in raw_ids.replace(";", ",").split(",") if part.strip()
    )

    repo_root = Path(os.environ.get("BRAND_REPO_ROOT", str(DEFAULT_REPO_ROOT)))
    if not (repo_root / "data" / "content_planner.md").is_file():
        raise SystemExit(
            f"BRAND_REPO_ROOT ({repo_root}) does not look like the brand workspace "
            "(data/content_planner.md not found)."
        )

    tz = ZoneInfo(os.environ.get("BRAND_TZ", "Africa/Tunis"))

    def _parse_time(raw: str) -> time | None:
        raw = raw.strip().lower()
        if raw in ("", "off", "none", "disabled"):
            return None
        hour, _, minute = raw.partition(":")
        return time(int(hour), int(minute or 0), tzinfo=tz)

    reminder = _parse_time(os.environ.get("BRAND_REMINDER_TIME", "08:00"))
    draft_reminder = _parse_time(os.environ.get("BRAND_DRAFT_REMINDER_TIME", "21:00"))

    git_sync_raw = os.environ.get("BRAND_GIT_SYNC_INTERVAL", "120").strip().lower()
    git_sync: int | None = None if git_sync_raw in ("", "off", "none", "disabled") else int(git_sync_raw)

    return Config(
        token=token,
        allowed_user_ids=allowed,
        repo_root=repo_root,
        timezone=tz,
        reminder_time=reminder,
        draft_reminder_time=draft_reminder,
        git_sync_interval=git_sync,
    )
