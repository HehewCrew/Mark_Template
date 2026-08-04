"""Read-only views over the brand workspace, plus the two write operations the
bot performs: archiving a queue package after it's confirmed posted, and
logging a post-hoc correction request (/fix) for an interactive session to
apply later.

Everything else here only reads paths under repo_root.
"""

from __future__ import annotations

import re
import shutil
import subprocess
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path

TELEGRAM_MAX_DOCUMENT_BYTES = 50 * 1024 * 1024  # Bot API upload limit

# content-creator's Step 6 naming convention: social/queue/<YYYY-MM-DD>-<series-slug>.md
# plus sibling board PNGs sharing the same prefix (e.g. ...-board-1.png) — loose files,
# not a subfolder. See .claude/skills/content-creator/SKILL.md Steps 6 & 8.
DATE_SLUG_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})-(.+)$")


def files_under(path: Path) -> list[Path]:
    if path.is_file():
        return [path]
    return sorted(p for p in path.rglob("*") if p.is_file() and not p.name.startswith("."))


@dataclass(frozen=True)
class QueueItem:
    name: str  # display name: the "<date>-<series-slug>" prefix, or a folder/file name
    slug: str  # series-slug — used as the archive subfolder name
    files: tuple[Path, ...]
    source_dir: Path | None  # set only for directory-style packages (defensive fallback)
    modified: datetime


def queue_items(queue_dir: Path) -> list[QueueItem]:
    """Post packages sitting in social/queue/ awaiting production/publishing.

    Groups loose sibling files sharing a "<date>-<series-slug>" prefix (the
    real content-creator convention) into one package; a subfolder (not part
    of that convention, but handled defensively) is its own package too.
    """
    if not queue_dir.is_dir():
        return []

    entries = [p for p in queue_dir.iterdir() if not p.name.startswith(".")]
    dirs = [p for p in entries if p.is_dir()]
    loose_files = [p for p in entries if p.is_file()]

    items: list[QueueItem] = []

    for d in dirs:
        files = files_under(d)
        stamp = max((f.stat().st_mtime for f in files), default=d.stat().st_mtime)
        m = DATE_SLUG_RE.match(d.name)
        slug = m.group(2) if m else d.name
        items.append(
            QueueItem(
                name=d.name, slug=slug, files=tuple(files), source_dir=d,
                modified=datetime.fromtimestamp(stamp),
            )
        )

    md_files = [p for p in loose_files if p.suffix.lower() == ".md" and DATE_SLUG_RE.match(p.stem)]
    consumed: set[Path] = set()
    for md in md_files:
        prefix = md.stem
        slug = DATE_SLUG_RE.match(prefix).group(2)
        siblings = [p for p in loose_files if p.stem == prefix or p.stem.startswith(prefix + "-")]
        consumed.update(siblings)
        stamp = max(f.stat().st_mtime for f in siblings)
        items.append(
            QueueItem(
                name=prefix, slug=slug, files=tuple(sorted(siblings)), source_dir=None,
                modified=datetime.fromtimestamp(stamp),
            )
        )

    # Any loose file that never attached to a package — surface it standalone
    # rather than silently drop it.
    for p in loose_files:
        if p not in consumed:
            items.append(
                QueueItem(
                    name=p.name, slug=p.stem, files=(p,), source_dir=None,
                    modified=datetime.fromtimestamp(p.stat().st_mtime),
                )
            )

    return sorted(items, key=lambda i: i.modified)


def find_queue_package(queue_dir: Path, query: str) -> tuple[QueueItem | None, list[QueueItem]]:
    """Case-insensitive substring match on package name.

    Returns (match, candidates) — match is set only on an unambiguous single
    hit; otherwise candidates holds whatever partially matched (for a
    "did you mean" reply).
    """
    query = query.strip().lower()
    items = queue_items(queue_dir)
    hits = [i for i in items if query in i.name.lower()]
    if len(hits) == 1:
        return hits[0], hits
    return None, hits


def queue_item_date(item: QueueItem) -> date | None:
    """The episode date encoded in a "<date>-<series-slug>" package name, if any."""
    m = DATE_SLUG_RE.match(item.name)
    if not m:
        return None
    return date.fromisoformat(m.group(1))


def solution_reveals_for(queue_dir: Path, when: date) -> list[Path]:
    """Standalone "<date>-<series-slug>-solution.*" assets due on `when` — e.g.
    a puzzle series' answer image queued the day before, to be posted as a
    Story once its own reveal date arrives (see the brand Challenge's
    solution-reveal mechanism). Surfaced separately from queue_items() since
    these are a same-day reminder, not a package to archive. Excludes the
    .svg source alongside each .png so the briefing doesn't list the same
    reveal twice — only the sendable file is worth a mention."""
    if not queue_dir.is_dir():
        return []
    matches = queue_dir.glob(f"{when:%Y-%m-%d}-*-solution.*")
    return sorted(p for p in matches if p.suffix.lower() not in NEVER_SEND_SUFFIXES)


# Nothing here ever gets pushed to Telegram — not worth a phone notification
# (found 2026-07-08). .md/.svg apply everywhere files get sent (queue
# packages, analytics); PHOTO_SUFFIXES/VIDEO_LINK_SUFFIX are specific to
# what a finished content package actually contains.
NEVER_SEND_SUFFIXES = (".md", ".svg")
PHOTO_SUFFIXES = (".png", ".jpg", ".jpeg")
# Reels/Canva video exports are too big/impractical to upload through the bot —
# paste the shareable download link in a "<date>-<slug>-video-link.txt"
# sibling instead (first line = the URL) and the bot relays that instead of
# the file. See sop/Baydaq_SOP.md.
VIDEO_LINK_SUFFIX = "-video-link.txt"
# A locally-assembled video (ffmpeg, no Canva/Higgsfield) is small enough
# (well under the 50 MB bot limit) to send as the actual file instead of a
# link — A Game on Board's compose-video.mjs (standardized 2026-07-21, after
# Higgsfield was dropped from that series) and Move of the Day/Common
# Mistakes' compose-video.mjs (added 2026-07-22, a still image held for a
# fixed duration, replacing their Canva video-import step) both produce one.
VIDEO_FILE_SUFFIXES = (".mp4",)

# content-creator's board-diagram convention (post-package-format.md): raw
# per-slot board PNGs meant to be pasted into Canva during production, e.g.
# "2026-07-13-move-of-the-day-board-1.png" — NOT the finished, postable asset.
BOARD_ASSET_RE = re.compile(r"-board-\d+$", re.IGNORECASE)
# The 5-second photo+advice format's compose-post.mjs output (templates/photo/
# generator/): a still "plate" — background photo + wordmark/headline burned
# in — that still has to be imported into Canva as a 5s video (+ audio) and
# exported. Found 2026-07-13: this was first named "...-final.png" and wrongly
# treated as postable; renamed to "-plate" so it reads as an intermediate,
# same as a board PNG, not the finished Reel.
PLATE_ASSET_RE = re.compile(r"-plate$", re.IGNORECASE)
# The package .md's "> Status: ..." line (post-package-format.md convention).
STATUS_APPROVED_RE = re.compile(r"status\s*:.*\bapproved\b", re.IGNORECASE)


def is_board_asset(path: Path) -> bool:
    return bool(BOARD_ASSET_RE.search(path.stem))


def is_plate_asset(path: Path) -> bool:
    return bool(PLATE_ASSET_RE.search(path.stem))


def package_approved(files: list[Path]) -> bool:
    """Whether the package's .md build sheet's "> Status: ..." line says
    APPROVED (decided 2026-07-13: the review-confirmation signal the bot
    reads to decide whether raw board assets still need an automatic push —
    see auto_push_photos). Defaults to False — treated as still-in-review —
    if there's no .md or no recognizable Status line, so an unreadable/odd
    package never silently withholds delivery."""
    md_files = [f for f in files if f.suffix.lower() == ".md"]
    if not md_files:
        return False
    try:
        head = md_files[0].read_text(encoding="utf-8", errors="replace").splitlines()[:10]
    except OSError:
        return False
    return any(STATUS_APPROVED_RE.search(line) for line in head)


def video_has_audio(path: Path) -> bool:
    """True if the video file already has a muxed audio track — i.e. the
    user's recorded voice-over has already been added via A Game on Board's
    add-voiceover.mjs (added 2026-07-22). Used to decide whether the
    voice-over script still needs to accompany the video when delivering
    it: needed while the video is silent (so the user has something to
    record from), redundant once the narration is actually baked in.
    Probes the file directly via ffprobe rather than trusting any state,
    since that's the only thing that can't drift out of sync with reality."""
    try:
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "a",
             "-show_entries", "stream=codec_type", "-of", "csv=p=0", str(path)],
            capture_output=True, text=True, timeout=10,
        )
    except (OSError, subprocess.TimeoutExpired):
        return False  # can't tell — safer to assume "not yet" so the script still gets attached
    return "audio" in result.stdout


def auto_push_photos(files: list[Path], approved: bool) -> list[Path]:
    """Photos worth an *automatic* content-ready push (decided 2026-07-13).

    Raw board PNGs (BOARD_ASSET_RE) and the photo+advice format's still
    "plate" (PLATE_ASSET_RE) are both production ingredients, not the
    postable asset — a board still needs manual Canva assembly, a plate
    still needs to become a Canva video. While the episode is still in
    review, pushing them is useful (nobody's seen them yet). Once the
    package is APPROVED, the user has already used them themselves
    (in-session or in Canva), so re-pushing is redundant noise; only an
    actual finished, postable asset (a Canva export image, or a video via
    its -video-link.txt, handled separately in split_deliverables) should
    trigger the automatic ping from then on. On-demand delivery (/send,
    /queue) is unaffected — it always includes everything, since asking is
    an explicit request."""
    photos = [f for f in files if f.suffix.lower() in PHOTO_SUFFIXES]
    if approved:
        photos = [f for f in photos if not is_board_asset(f) and not is_plate_asset(f)]
    return sorted(photos)


def exclude_unwanted(files: list[Path]) -> list[Path]:
    return [f for f in files if f.suffix.lower() not in NEVER_SEND_SUFFIXES]


def split_deliverables(files: list[Path]) -> tuple[list[Path], Path | str | None]:
    """From a package's files, pick out what's actually worth sending to
    Telegram: photo files, and a video — either a local `.mp4` (A Game on
    Board's compose-video.mjs output, sent as the actual file since it's
    small) or, failing that, the URL inside a "<prefix>-video-link.txt"
    sibling (a Canva/Higgsfield export hosted elsewhere, relayed as a link).
    A local video file takes precedence if somehow both are present.
    Everything else (.md, .svg, anything unrecognized) is dropped silently."""
    photos: list[Path] = []
    video_file: Path | None = None
    video_url: str | None = None
    for f in files:
        if f.suffix.lower() in VIDEO_FILE_SUFFIXES:
            video_file = f
        elif f.name.endswith(VIDEO_LINK_SUFFIX):
            try:
                lines = f.read_text(encoding="utf-8", errors="replace").strip().splitlines()
                video_url = lines[0] if lines else None
            except OSError:
                pass
        elif f.suffix.lower() in PHOTO_SUFFIXES:
            photos.append(f)
    return sorted(photos), (video_file or video_url)


CAPTION_HEADING_RE = re.compile(r"^##\s*Caption\b", re.IGNORECASE)
_NEXT_HEADING_RE = re.compile(r"^##\s+\S")


def _extract_section(files: list[Path], heading_re: re.Pattern[str]) -> str | None:
    """Shared logic behind extract_caption/extract_voiceover_script: pull the
    body of one "## <heading>" section out of a package's .md build sheet,
    stopping at the next "## " heading. Returns None if there's no .md or no
    matching heading."""
    md_files = [f for f in files if f.suffix.lower() == ".md"]
    if not md_files:
        return None
    try:
        lines = md_files[0].read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return None

    start = next((i for i, line in enumerate(lines) if heading_re.match(line.strip())), None)
    if start is None:
        return None
    body: list[str] = []
    for line in lines[start + 1:]:
        if _NEXT_HEADING_RE.match(line.strip()):
            break
        body.append(line)
    text = "\n".join(body).strip()
    return text or None


def extract_caption(files: list[Path]) -> str | None:
    """Pull the "## Caption (copy-paste)" section out of a package's .md
    build sheet (see content-creator's references/post-package-format.md).
    Returns the caption text (stripped), or None if there's no .md file or
    no such section — the .md itself is never sent to Telegram (see
    NEVER_SEND_SUFFIXES), so this is the one piece of its content that is,
    since the caption is needed by hand at publish time (found 2026-07-08:
    it silently never reached the phone otherwise)."""
    return _extract_section(files, CAPTION_HEADING_RE)


VOICEOVER_HEADING_RE = re.compile(r"^##\s*Voice-over Script\b", re.IGNORECASE)


def extract_voiceover_script(files: list[Path]) -> str | None:
    """Pull the "## Voice-over Script (Tunisian dialect)" section out of a
    package's .md build sheet — the A Game on Board series only (decided
    2026-07-17). Written into the package in the same pass as the local
    compose-video.mjs assembly (revised 2026-07-22 — no Higgsfield since
    2026-07-21; see Marketing Strategy §7 step 4), but callers should still
    treat None as "not ready yet," not an error — older or partial packages
    may lack it. Same never-send-the-.md-itself reasoning as the caption."""
    return _extract_section(files, VOICEOVER_HEADING_RE)


# Post-hoc correction (added 2026-07-22, replaces the pre-publish review gate
# for A Game on Board / Move of the Day / Common Mistakes — see CLAUDE.md and
# Marketing_Strategy.md §7): the user flags a problem with an
# already-queued package via /fix instead of approving before it ships.
FIX_FIELDS = ("caption", "photo", "phrase")


def write_fix_request(queue_dir: Path, item_name: str, field: str, text: str) -> Path:
    """Log a correction request as social/queue/.fix-<item_name>.md — the
    same async marker-file convention this repo already uses for handoffs
    between the bot (no LLM in the loop, can't apply the fix itself) and a
    later interactive Claude Code session (which dispatches content-writer
    to actually make the change, per its agent instructions' "post-hoc
    correction" duty). Appends rather than overwrites, so more than one
    request before the next interactive session doesn't clobber the last.
    `field` must be one of FIX_FIELDS ("phrase" text is "<old> -> <new>")."""
    path = queue_dir / f".fix-{item_name}.md"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    entry = f"## {field} — requested {timestamp}\n\n{text}\n\n"
    with path.open("a", encoding="utf-8") as fh:
        fh.write(entry)
    return path


def _signature_of_files(files: list[Path]) -> str:
    """Cheap fingerprint: file count + latest mtime + total size — good enough
    to detect "this package changed since we last looked" without hashing
    contents."""
    if not files:
        return "empty"
    latest = max(f.stat().st_mtime for f in files)
    total = sum(f.stat().st_size for f in files)
    return f"{len(files)}:{latest:.0f}:{total}"


def queue_signature(item: QueueItem) -> str:
    return _signature_of_files(list(item.files))


def archive_queue_item(item: QueueItem, repo_root: Path, pillar: str) -> Path:
    """Archive a published queue package, mirroring content-creator SKILL.md
    Step 8: only the .md build sheet(s) move to social/<pillar>/<slug>/;
    every other file (Canva slide exports, board PNGs/SVGs, video-link txt)
    is deleted — the published post lives on Instagram/Canva, and boards
    regenerate from the FEN in the build sheet (decided 2026-07-08).
    Returns the destination dir."""
    dest_dir = repo_root / "social" / pillar / item.slug
    dest_dir.mkdir(parents=True, exist_ok=True)
    for f in item.files:
        if f.suffix.lower() == ".md":
            shutil.move(str(f), str(dest_dir / f.name))
        else:
            f.unlink()
    if item.source_dir is not None:
        # Directory-style package (defensive fallback): mds are out, the
        # rest is deleted — drop the now-spent folder.
        shutil.rmtree(item.source_dir, ignore_errors=True)
    return dest_dir


@dataclass(frozen=True)
class AnalysisDigest:
    month: str  # folder name, e.g. "2026-07"
    path: Path
    summary: str  # first ~30 lines of the insights doc, or a file listing


def _latest_month_dir(analysis_dir: Path) -> Path | None:
    if not analysis_dir.is_dir():
        return None
    months = sorted(
        (d for d in analysis_dir.iterdir() if d.is_dir() and not d.name.startswith(".")),
        key=lambda d: d.name,
    )
    return months[-1] if months else None


def latest_analysis(analysis_dir: Path, max_lines: int = 30) -> AnalysisDigest | None:
    """Newest presentations/data-analysis/<YYYY-MM>/ folder, summarized."""
    latest = _latest_month_dir(analysis_dir)
    if latest is None:
        return None

    md_files = sorted(latest.glob("*.md"))
    if md_files:
        lines = md_files[0].read_text(encoding="utf-8", errors="replace").splitlines()
        body = "\n".join(lines[:max_lines])
        if len(lines) > max_lines:
            body += f"\n… ({len(lines) - max_lines} more lines in {md_files[0].name})"
        return AnalysisDigest(month=latest.name, path=latest, summary=body)

    names = [p.name for p in sorted(latest.iterdir()) if not p.name.startswith(".")]
    listing = "\n".join(f"• {n}" for n in names) or "(empty folder)"
    return AnalysisDigest(month=latest.name, path=latest, summary=listing)


def resolve_safe_path(repo_root: Path, rel_path: str) -> Path | None:
    """Resolve a user-supplied path against repo_root, refusing any escape."""
    repo_root = repo_root.resolve()
    candidate = (repo_root / rel_path).resolve()
    try:
        candidate.relative_to(repo_root)
    except ValueError:
        return None
    return candidate


def list_dir_relative(repo_root: Path, dir_path: Path) -> list[str]:
    """Non-recursive listing of dir_path, names relative-friendly (dirs suffixed '/')."""
    entries = sorted(dir_path.iterdir(), key=lambda p: (p.is_file(), p.name.lower()))
    return [f"{p.name}/" if p.is_dir() else p.name for p in entries if not p.name.startswith(".")]
