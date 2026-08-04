"""Read-only parser for data/content_planner.md.

The planner is a set of Markdown tables under week headings like:

    ## Cycle 1 — Week 1 (2026-07-06 → 2026-07-12)

    | Day | Date | Series | Episode topic | Source grounding | Done |
    |---|---|---|---|---|---|
    | Mon | 07-06 | Move of the Day | ... | ... | [ ] |

Dates inside rows are MM-DD; the year comes from the enclosing week heading.

Mostly read-only: the bot only writes here via mark_done_and_log(), called
when a queue package is confirmed posted — mirroring content-creator
SKILL.md Step 8 (check the episode's Done box, log the archive path) so
archiving via the bot needs no separate Claude Code session.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path

WEEK_HEADING_RE = re.compile(r"^##\s+(.+?)\s*\((\d{4})-(\d{2})-(\d{2})")
ROW_RE = re.compile(
    r"^\|\s*(?P<day>[A-Za-z]{3})\s*\|\s*(?P<date>\d{2}-\d{2})\s*\|"
    r"\s*(?P<series>[^|]+?)\s*\|\s*(?P<topic>[^|]+?)\s*\|"
    r"\s*(?P<source>[^|]+?)\s*\|\s*(?P<done>\[.?\])\s*\|"
)


@dataclass(frozen=True)
class Episode:
    when: date
    day: str
    series: str
    topic: str
    source: str
    done: bool
    week: str  # heading text of the week the episode belongs to


def parse_planner(path: Path) -> list[Episode]:
    episodes: list[Episode] = []
    week_label = ""
    week_start: date | None = None

    for line in path.read_text(encoding="utf-8").splitlines():
        heading = WEEK_HEADING_RE.match(line)
        if heading:
            week_label = heading.group(1)
            week_start = date(
                int(heading.group(2)), int(heading.group(3)), int(heading.group(4))
            )
            continue

        row = ROW_RE.match(line)
        if not row or week_start is None:
            continue

        month, day_num = (int(p) for p in row.group("date").split("-"))
        year = week_start.year
        # A week table can only cover dates at/after its start; if the month
        # is earlier than the week's start month we crossed a year boundary.
        if month < week_start.month:
            year += 1

        episodes.append(
            Episode(
                when=date(year, month, day_num),
                day=row.group("day"),
                series=row.group("series"),
                topic=row.group("topic"),
                source=row.group("source"),
                done="x" in row.group("done").lower(),
                week=week_label,
            )
        )

    return episodes


def episode_for(episodes: list[Episode], when: date) -> Episode | None:
    return next((e for e in episodes if e.when == when), None)


def week_of(episodes: list[Episode], when: date) -> list[Episode]:
    """All episodes in the same planner week (same heading) as `when`."""
    today = episode_for(episodes, when)
    if today is None:
        return []
    return [e for e in episodes if e.week == today.week]


def next_planned(episodes: list[Episode], when: date) -> Episode | None:
    """The next scheduled episode strictly after `when`."""
    future = sorted((e for e in episodes if e.when > when), key=lambda e: e.when)
    return future[0] if future else None


EPISODE_LOG_HEADING = "## Episode log (all-time, prevents redundancy)"
_PLACEHOLDER_RE = re.compile(r"^\*\(none yet.*\)\*\s*$")
_REDUNDANCY_MARKER = "**Redundancy rule:**"
_BACKTICK_PATH_RE = re.compile(r"`[^`]*`")


def _entry_date_prefix(when: date) -> str:
    # Deliberately just the date, not "date — series:" — a human-written
    # entry (content-creator Step 7) and this module's own machine-written
    # entry (Step 8) almost never agree on series-name punctuation (planner
    # rows carry swap annotations like "*(swapped in from 07-07...)*" that a
    # human writing the log by hand naturally leaves out), which used to
    # make the old prefix match silently fail and append a duplicate entry
    # instead of updating the existing one. The date is unique per episode
    # and both writers always lead with it — see content-creator SKILL.md
    # Step 7's "shared contract" note.
    return f"- **{when:%Y-%m-%d} —"


def _update_path_in_entry(line: str, archive_rel_path: str) -> tuple[str, bool]:
    """Point an existing log entry's archive reference at `archive_rel_path`,
    preserving everything else about the line (a human-written entry may
    carry rich prose — sources, fact-checks — that a blind overwrite would
    destroy). Replaces the last backtick-quoted path if one exists (however
    it's introduced — "→ `path`", "Package: `path`", ...); otherwise appends
    an arrow-reference at the end."""
    new_ref = f"`{archive_rel_path}`"
    matches = list(_BACKTICK_PATH_RE.finditer(line))
    if matches:
        last = matches[-1]
        if line[last.start():last.end()] == new_ref:
            return line, False
        return line[:last.start()] + new_ref + line[last.end():], True
    suffix = f" → {new_ref}"
    if line.rstrip().endswith(suffix.strip()):
        return line, False
    return line.rstrip() + suffix, True


def _append_episode_log(lines: list[str], entry: str) -> list[str]:
    out: list[str] = []
    in_log_section = False
    inserted = False
    for line in lines:
        if line.strip() == EPISODE_LOG_HEADING:
            in_log_section = True
            out.append(line)
            continue
        if in_log_section and not inserted:
            if _PLACEHOLDER_RE.match(line.strip()):
                out.append(entry)
                inserted = True
                continue
            if line.strip().startswith(_REDUNDANCY_MARKER):
                if out and out[-1].strip():
                    out.append("")
                out.append(entry)
                out.append("")
                out.append(line)
                inserted = True
                continue
        out.append(line)
    return out


def mark_done_and_log(planner_path: Path, ep: Episode, archive_rel_path: str) -> bool:
    """Check `ep`'s Done box (idempotent — never un-checks) and upsert its
    Episode-log entry to point at `archive_rel_path`.

    The upsert matters because the entry is written twice in the post's
    lifecycle with different paths: first at export/approval time linking
    the `social/queue/` package (content-creator Step 7, written by hand),
    then again at posted/archive time re-linking to `social/<pillar>/...`
    (Step 8, this function). Matching is by DATE ONLY (see
    `_entry_date_prefix`) — when a match is found, only its archive-path
    reference is updated in place (`_update_path_in_entry`), so a human's
    prose (sources, fact-checks, production notes) survives untouched.
    Only when no entry exists yet for this date does this function append
    its own fully machine-generated line. The Done checkbox flips once;
    the log entry's path gets refreshed in place.

    Returns True if the file changed. Locates the row by
    "| Day | MM-DD | Series |" — day+date+series together are unique.
    """
    lines = planner_path.read_text(encoding="utf-8").splitlines()
    changed = False

    if not ep.done:
        anchor = f"| {ep.day} | {ep.when:%m-%d} | {ep.series} |"
        row_found = False
        for i, line in enumerate(lines):
            if anchor in line:
                lines[i] = re.sub(r"\[\s?\]\s*\|\s*$", "[x] |", line)
                row_found = True
                changed = True
                break
        if not row_found:
            raise ValueError(f"Could not locate planner row for {ep.when} ({ep.series})")

    date_prefix = _entry_date_prefix(ep.when)

    # Upsert within the Episode log section only (stop at the next ## heading).
    in_log_section = False
    upserted = False
    for i, line in enumerate(lines):
        if line.strip() == EPISODE_LOG_HEADING:
            in_log_section = True
            continue
        if in_log_section and line.startswith("## "):
            break
        if in_log_section and line.strip().startswith(date_prefix):
            new_line, line_changed = _update_path_in_entry(line, archive_rel_path)
            if line_changed:
                lines[i] = new_line
                changed = True
            upserted = True
            break

    if not upserted:
        entry = (
            f"{date_prefix} {ep.series}:** {ep.topic} "
            f"(*source: {ep.source}*) → `{archive_rel_path}`"
        )
        lines = _append_episode_log(lines, entry)
        changed = True

    if changed:
        planner_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return changed
