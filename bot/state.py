"""Tiny JSON-backed store keyed by a caller-chosen string (e.g.
"git-pull-failure", "ready:<package-name>"). Tracks two signatures per key:
"seen" (observed on the last poll) and "sent" (already delivered). A caller
can debounce a still-settling package by only acting once "seen" has held
steady across two consecutive polls and differs from "sent" — see
content_ready_check in bot.py. Simpler callers (alerts) just use "sent" on
its own to suppress an unresolved failure firing every poll.
"""

from __future__ import annotations

import json
from pathlib import Path


class PushState:
    def __init__(self, path: Path):
        self.path = path
        self._data: dict[str, dict[str, str]] = {"seen": {}, "sent": {}}
        if path.is_file():
            try:
                loaded = json.loads(path.read_text(encoding="utf-8"))
                self._data["seen"] = loaded.get("seen", {})
                self._data["sent"] = loaded.get("sent", {})
            except (json.JSONDecodeError, OSError):
                pass

    def seen(self, key: str) -> str | None:
        return self._data["seen"].get(key)

    def sent(self, key: str) -> str | None:
        return self._data["sent"].get(key)

    def mark_seen(self, key: str, signature: str) -> None:
        self._data["seen"][key] = signature
        self._save()

    def mark_sent(self, key: str, signature: str) -> None:
        self._data["sent"][key] = signature
        self._save()

    def _save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(self._data, indent=2), encoding="utf-8")
