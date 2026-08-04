"""brand internal assistant bot.

Private Telegram bot for the brand content workflow:

  /today     — today's planned episode from data/content_planner.md
  /week      — the current planner week with done-status
  /next      — next scheduled episode after today
  /queue     — packages waiting in social/queue/
  /send      — deliver a social/queue/ package's actual files to this chat
  /posted    — confirm a queue package went live: archive its .md to
               social/<pillar>/, delete the rest of the package, check its
               planner box, log the archive path, and commit+push exactly
               those changes
  /analytics — latest presentations/data-analysis/ digest + its files
  /file      — deliver any single file from the repo, by relative path
  /id        — your Telegram user id (for the allowlist)

Plus two scheduled reminders (Tunis time by default) and a periodic git sync:
  - Daily morning briefing (BRAND_REMINDER_TIME, default 08:00): today's
    episode + queue count, plus any same-day solution-reveal reminder (a
    "<date>-<series-slug>-solution.*" asset queued for a puzzle series).
  - Nightly draft-status reminder (BRAND_DRAFT_REMINDER_TIME, default
    21:00): if tomorrow's episode isn't drafted yet, says so — series,
    topic, and whether a template already exists for it. Also flags
    uncommitted local changes the cloud runs can't see.
  - Git sync (BRAND_GIT_SYNC_INTERVAL, default 120s): pulls (--ff-only) so
    the bot's view of the repo stays current; alerts once on failure.

Both reminders also fire once on startup if the day's fixed time was
missed (added 2026-07-22 — the host PC is shut down overnight, so a fixed
cron time is unreliable; see _run_once_today). Whichever fires first
(startup catch-up or the actual cron time) wins for the day; PushState
(bot/state/, keyed "daily-reminder"/"draft-reminder") tracks it so the
other doesn't double-send. /test bypasses this and always fires both.

Runs on long-polling — no public URL required.

Run:  python bot.py   (from the bot/ folder, after filling in .env)
"""

from __future__ import annotations

import html
import logging
import re
from datetime import date, datetime, timedelta
from pathlib import Path
from uuid import uuid4

from telegram import Bot, BotCommand, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

import gitops
from config import Config, load_config
from pillars import PILLAR_LABELS, PILLAR_SLUGS, guess_pillar
from planner import (
    Episode,
    episode_for,
    mark_done_and_log,
    next_planned,
    parse_planner,
    week_of,
)
from repo import (
    TELEGRAM_MAX_DOCUMENT_BYTES,
    QueueItem,
    archive_queue_item,
    exclude_unwanted,
    auto_push_photos,
    extract_caption,
    files_under,
    find_queue_package,
    FIX_FIELDS,
    latest_analysis,
    list_dir_relative,
    package_approved,
    queue_item_date,
    queue_items,
    queue_signature,
    solution_reveals_for,
    split_deliverables,
    resolve_safe_path,
    write_fix_request,
)
from state import PushState


logging.basicConfig(
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(),
        # File log matters when running headless under pythonw.exe (no console).
        logging.FileHandler(Path(__file__).resolve().parent / "bot.log", encoding="utf-8"),
    ],
)
logging.getLogger("httpx").setLevel(logging.WARNING)
log = logging.getLogger("brand-bot")

CFG: Config  # set in main()


def _e(text: str) -> str:
    return html.escape(text, quote=False)


def _today() -> date:
    return datetime.now(CFG.timezone).date()


def _fmt_episode(ep: Episode, label: str) -> str:
    status = "✅ done" if ep.done else "⬜ not published yet"
    return (
        f"<b>{_e(label)}</b> — {ep.when:%a %Y-%m-%d}\n"
        f"📚 Series: <b>{_e(ep.series)}</b>\n"
        f"✏️ Topic: {_e(ep.topic)}\n"
        f"📖 Source: {_e(ep.source)}\n"
        f"Status: {status}"
    )


def _today_message() -> str:
    episodes = parse_planner(CFG.planner_path)
    today = _today()
    ep = episode_for(episodes, today)
    if ep is None:
        nxt = next_planned(episodes, today)
        # Fri/Sun carry no slot under the Discovery Push weekly schedule
        # (Marketing Strategy §1.3, 2026-07-17) — say so, rather than
        # reading like a planner gap. Mon=0 … Fri=4, Sun=6.
        if today.weekday() in (4, 6):
            msg = f"😌 Rest day ({today:%a %Y-%m-%d}) — no slot on the Discovery Push schedule."
        else:
            msg = f"No episode is scheduled for today ({today:%a %Y-%m-%d})."
        if nxt:
            msg += "\n\n" + _fmt_episode(nxt, "Next planned")
        else:
            msg += "\nThe planner has no upcoming episodes — time to plan the next cycle."
        return msg
    return _fmt_episode(ep, "Today's episode")


async def _send_file(bot: Bot, chat_id: int, path: Path, caption: str | None = None) -> None:
    size = path.stat().st_size
    if size > TELEGRAM_MAX_DOCUMENT_BYTES:
        await bot.send_message(
            chat_id=chat_id,
            text=f"⚠️ {_e(path.name)} is {size / 1_048_576:.1f} MB — over Telegram's "
            "50 MB bot upload limit, skipping.",
        )
        return
    with path.open("rb") as fh:
        await bot.send_document(chat_id=chat_id, document=fh, filename=path.name, caption=caption)


async def _send_video(bot: Bot, chat_id: int, path: Path, caption: str | None = None) -> None:
    """Send a locally-assembled video (A Game on Board's compose-video.mjs
    output) as an actual playable video message, not a generic document —
    same 50 MB size guard as _send_file. Distinct from a VIDEO_LINK_SUFFIX
    package, which has no local file to send at all."""
    size = path.stat().st_size
    if size > TELEGRAM_MAX_DOCUMENT_BYTES:
        await bot.send_message(
            chat_id=chat_id,
            text=f"⚠️ {_e(path.name)} is {size / 1_048_576:.1f} MB — over Telegram's "
            "50 MB bot upload limit, skipping.",
        )
        return
    with path.open("rb") as fh:
        await bot.send_video(chat_id=chat_id, video=fh, filename=path.name, caption=caption)


async def _send_files(bot: Bot, chat_id: int, paths: list[Path], header: str) -> None:
    await bot.send_message(chat_id=chat_id, text=header, parse_mode=ParseMode.HTML)
    if not paths:
        await bot.send_message(chat_id=chat_id, text="(no files found)")
        return
    for p in paths:
        await _send_file(bot, chat_id, p)


def _build_pillar_keyboard(token: str, guessed: str | None) -> InlineKeyboardMarkup:
    rows: list[list[InlineKeyboardButton]] = []
    row: list[InlineKeyboardButton] = []
    for slug in PILLAR_SLUGS:
        label = PILLAR_LABELS[slug]
        if slug == guessed:
            label = f"⭐ {label}"
        row.append(InlineKeyboardButton(label, callback_data=f"posted:{token}:{slug}"))
        if len(row) == 2:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    return InlineKeyboardMarkup(rows)


def _guess_pillar_for_item(item: QueueItem) -> tuple[str | None, bool]:
    when = queue_item_date(item)
    episode = episode_for(parse_planner(CFG.planner_path), when) if when else None
    return guess_pillar(episode.series) if episode else (None, False)


async def _offer_mark_posted(context: ContextTypes.DEFAULT_TYPE, chat_id: int, item: QueueItem) -> None:
    guessed, exact = _guess_pillar_for_item(item)

    token = uuid4().hex[:8]
    context.application.bot_data.setdefault("pending_posts", {})[token] = {"item_name": item.name}

    if guessed and exact:
        # Series maps to exactly one known pillar — one tap confirms, with
        # an escape hatch for the rare case it's wrong (found 2026-07-08:
        # showing all 5 pillar buttons every time was pure friction once
        # the series→pillar mapping is unambiguous).
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(f"✅ Posted ({PILLAR_LABELS[guessed]})", callback_data=f"posted:{token}:{guessed}")],
            [InlineKeyboardButton("Different pillar…", callback_data=f"posted-more:{token}")],
        ])
        text = f"Mark <b>{_e(item.name)}</b> as posted:"
    else:
        hint = (
            f" (guessing <b>{_e(PILLAR_LABELS[guessed])}</b> ⭐ — tap it to confirm, or pick another)"
            if guessed
            else ""
        )
        keyboard = _build_pillar_keyboard(token, guessed)
        text = f"Mark <b>{_e(item.name)}</b> as posted{hint}:"

    await context.bot.send_message(
        chat_id=chat_id, text=text, parse_mode=ParseMode.HTML, reply_markup=keyboard
    )


async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "the brand internal assistant reporting for duty. ♟️\n\n"
        "/today — today's planned episode\n"
        "/week — this week's schedule\n"
        "/next — next scheduled episode\n"
        "/queue — content queue status\n"
        "/send <name> — deliver a queue package's photos + video link here\n"
        "/posted <name> — mark a package posted (archives the .md, deletes "
        "the exports, updates the planner, commits + pushes)\n"
        "/analytics — latest analytics digest + files\n"
        "/file <path> — deliver any repo file by relative path\n"
        "/test — fire the morning briefing, draft-status check, and "
        "content-ready check right now, for testing\n"
        "/id — your Telegram user id\n\n"
        "Every morning you get today's episode + queue count. Every night, "
        "if tomorrow's episode isn't drafted yet, you get a reminder saying "
        "so (with its template status). And once a queue package has an "
        "actual photo or a *-video-link.txt* in it, you get a \"content "
        "ready\" message — photos attached, video as a link — with a "
        "one-tap \"mark as posted\" option. .md/.svg files are never pushed."
    )


async def cmd_today(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(_today_message(), parse_mode=ParseMode.HTML)


async def cmd_next(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    nxt = next_planned(parse_planner(CFG.planner_path), _today())
    if nxt is None:
        await update.message.reply_text(
            "Nothing scheduled after today — the planner needs its next cycle."
        )
        return
    await update.message.reply_text(
        _fmt_episode(nxt, "Next episode"), parse_mode=ParseMode.HTML
    )


async def cmd_week(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    episodes = parse_planner(CFG.planner_path)
    today = _today()
    week = week_of(episodes, today)
    if not week:
        await update.message.reply_text(
            f"Today ({today:%Y-%m-%d}) isn't inside any planner week. "
            "Check data/content_planner.md."
        )
        return
    done = sum(1 for e in week if e.done)
    lines = [f"<b>{_e(week[0].week)}</b> — {done}/{len(week)} done\n"]
    for e in week:
        mark = "✅" if e.done else ("👉" if e.when == today else "⬜")
        lines.append(f"{mark} <b>{e.when:%a %m-%d}</b> · {_e(e.series)} — {_e(e.topic)}")
    await update.message.reply_text("\n".join(lines), parse_mode=ParseMode.HTML)


async def cmd_queue(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    items = queue_items(CFG.queue_dir)
    if not items:
        await update.message.reply_text(
            "social/queue/ is empty — nothing is waiting to be produced or published."
        )
        return
    lines = [f"<b>Content queue</b> — {len(items)} package(s) waiting\n"]
    for item in items:
        lines.append(
            f"📦 <b>{_e(item.name)}</b> — {len(item.files)} file(s), "
            f"last touched {item.modified:%Y-%m-%d %H:%M}"
        )
    lines.append("\nUse /send &lt;name&gt; to have a package delivered here, or /posted &lt;name&gt; once it's live.")
    await update.message.reply_text("\n".join(lines), parse_mode=ParseMode.HTML)


async def cmd_send(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = " ".join(context.args).strip()
    chat_id = update.effective_chat.id
    if not query:
        items = queue_items(CFG.queue_dir)
        if not items:
            await update.message.reply_text("social/queue/ is empty — nothing to send.")
            return
        names = "\n".join(f"• {_e(i.name)}" for i in items)
        await update.message.reply_text(
            f"Usage: /send &lt;package name&gt;\n\nAvailable packages:\n{names}",
            parse_mode=ParseMode.HTML,
        )
        return

    match, candidates = find_queue_package(CFG.queue_dir, query)
    if match is None:
        if not candidates:
            await update.message.reply_text(f"No queue package matches '{_e(query)}'.")
        else:
            names = "\n".join(f"• {_e(i.name)}" for i in candidates)
            await update.message.reply_text(
                f"Multiple packages match '{_e(query)}' — be more specific:\n{names}",
                parse_mode=ParseMode.HTML,
            )
        return

    photos, video = split_deliverables(list(match.files))
    lines = [f"📦 <b>{_e(match.name)}</b>"]
    if photos:
        lines.append(f"🖼 {len(photos)} photo(s) below")
    if isinstance(video, Path):
        lines.append("🎬 Video below")
    elif video:
        lines.append(f"🎬 Video: {_e(video)}")
    if not photos and not video:
        lines.append("(no photos or video in this package yet)")
    await context.bot.send_message(chat_id=chat_id, text="\n".join(lines), parse_mode=ParseMode.HTML)
    for p in photos:
        await _send_file(context.bot, chat_id, p)
    if isinstance(video, Path):
        await _send_video(context.bot, chat_id, video)
    caption = extract_caption(list(match.files))
    if caption:
        await context.bot.send_message(
            chat_id=chat_id, text=f"📝 <b>Caption:</b>\n\n{_e(caption)}", parse_mode=ParseMode.HTML
        )
    await _offer_mark_posted(context, chat_id, match)


async def cmd_posted(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = " ".join(context.args).strip()
    chat_id = update.effective_chat.id
    if not query:
        await update.message.reply_text("Usage: /posted <package name>")
        return

    match, candidates = find_queue_package(CFG.queue_dir, query)
    if match is None:
        if not candidates:
            await update.message.reply_text(f"No queue package matches '{_e(query)}'.")
        else:
            names = "\n".join(f"• {_e(i.name)}" for i in candidates)
            await update.message.reply_text(
                f"Multiple packages match '{_e(query)}' — be more specific:\n{names}",
                parse_mode=ParseMode.HTML,
            )
        return

    await _offer_mark_posted(context, chat_id, match)


async def cmd_fix(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Post-hoc correction (added 2026-07-22) — replaces the pre-publish
    review gate for A Game on Board / Move of the Day / Common Mistakes
    (Tactic in 60 Seconds and every other series still get reviewed before
    they're queued, so this command isn't their fix path).
    Usage: /fix <package name> <caption|photo|phrase> <text>
    (for phrase: <old text> -> <new text>). Logs the request as a
    .fix-<name>.md marker (repo.write_fix_request) and commits+pushes it —
    a second scoped bot write path alongside /posted's archive flow, since
    the bot has no LLM in the loop and can't apply the fix itself; a later
    interactive Claude Code session reads the marker and dispatches
    content-writer to make the actual change."""
    args = context.args
    chat_id = update.effective_chat.id
    if len(args) < 3:
        await update.message.reply_text(
            "Usage: /fix <package name> <caption|photo|phrase> <text>\n\n"
            "For phrase corrections: /fix <name> phrase <old text> -> <new text>"
        )
        return

    query, field, *rest = args
    field = field.lower()
    text = " ".join(rest).strip()
    if field not in FIX_FIELDS:
        await update.message.reply_text(
            f"Unknown field '{_e(field)}' — use one of: {', '.join(FIX_FIELDS)}"
        )
        return
    if not text:
        await update.message.reply_text("Give me the corrected text after the field name.")
        return
    if field == "phrase" and "->" not in text:
        await update.message.reply_text(
            "For phrase corrections, use: /fix <name> phrase <old text> -> <new text>"
        )
        return

    match, candidates = find_queue_package(CFG.queue_dir, query)
    if match is None:
        if not candidates:
            await update.message.reply_text(f"No queue package matches '{_e(query)}'.")
        else:
            names = "\n".join(f"• {_e(i.name)}" for i in candidates)
            await update.message.reply_text(
                f"Multiple packages match '{_e(query)}' — be more specific:\n{names}",
                parse_mode=ParseMode.HTML,
            )
        return

    marker = write_fix_request(CFG.queue_dir, match.name, field, text)

    git_note = ""
    if gitops.has_repo(CFG.repo_root):
        rel = marker.relative_to(CFG.repo_root).as_posix()
        ok, note = gitops.commit_and_push(
            CFG.repo_root, [rel], f"Fix request: {match.name} — {field} (via bot)",
        )
        if ok:
            git_note = f"\n🔄 Git: {note}."
        else:
            log.error("Fix-request git sync failed for %s: %s", match.name, note)
            git_note = f"\n⚠️ Git: {note}. Logged locally — commit/push it from a Claude Code session."

    await update.message.reply_text(
        f"📝 Logged a <b>{_e(field)}</b> fix for '{_e(match.name)}' — "
        f"will be applied in the next Claude Code session.{_e(git_note)}",
        parse_mode=ParseMode.HTML,
    )


async def on_pillar_more(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """"Different pillar…" escape hatch from the single-button confirm —
    swaps in the full 5-pillar keyboard, still starring the guess."""
    query = update.callback_query
    if update.effective_user.id not in CFG.allowed_user_ids:
        await query.answer("Not authorized", show_alert=True)
        return
    await query.answer()

    _, token = query.data.split(":", 1)
    pending = context.application.bot_data.get("pending_posts", {})
    entry = pending.get(token)
    if entry is None:
        await query.edit_message_text("This confirmation expired — run /send or /posted again.")
        return

    match, _ = find_queue_package(CFG.queue_dir, entry["item_name"])
    guessed = _guess_pillar_for_item(match)[0] if match is not None else None
    await query.edit_message_reply_markup(reply_markup=_build_pillar_keyboard(token, guessed))


async def on_pillar_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if update.effective_user.id not in CFG.allowed_user_ids:
        await query.answer("Not authorized", show_alert=True)
        return
    await query.answer()

    _, token, pillar = query.data.split(":", 2)
    pending = context.application.bot_data.get("pending_posts", {})
    entry = pending.pop(token, None)
    if entry is None:
        await query.edit_message_text("This confirmation expired — run /send or /posted again.")
        return

    match, _ = find_queue_package(CFG.queue_dir, entry["item_name"])
    if match is None:
        await query.edit_message_text(
            f"'{_e(entry['item_name'])}' is no longer in the queue — already archived?"
        )
        return

    # Snapshot which queue files git tracks BEFORE the archive deletes them —
    # their deletions must be staged; untracked ones vanish without a trace.
    # Also note the .md's own name now, since after the move only its
    # *directory* is easy to recover (the archive folder accumulates one
    # .md per episode over a series' lifetime, so the folder alone doesn't
    # identify which file this run just added).
    queue_rels = [f.relative_to(CFG.repo_root).as_posix() for f in match.files]
    tracked = gitops.tracked_files(CFG.repo_root, "social/queue") if gitops.has_repo(CFG.repo_root) else set()
    deleted_tracked = [r for r in queue_rels if r in tracked]
    md_names = [f.name for f in match.files if f.suffix.lower() == ".md"]

    try:
        dest_dir = archive_queue_item(match, CFG.repo_root, pillar)
    except OSError:
        log.exception("Failed to archive queue item %s", match.name)
        await query.edit_message_text(
            f"⚠️ Couldn't move '{_e(match.name)}' — check bot.log (maybe already archived?)."
        )
        return
    rel_dest = dest_dir.relative_to(CFG.repo_root).as_posix()
    # Precise archived-file path (matches the convention used by manual
    # content-creator Step 7 planner entries) rather than just the folder.
    rel_dest_file = f"{rel_dest}/{md_names[0]}" if md_names else f"{rel_dest}/"

    planner_note = ""
    when = queue_item_date(match)
    episode = episode_for(parse_planner(CFG.planner_path), when) if when else None
    if episode is not None:
        try:
            changed = mark_done_and_log(CFG.planner_path, episode, rel_dest_file)
            planner_note = (
                "\n📋 Planner updated (done-box + archive link)."
                if changed
                else "\n📋 Planner already up to date for this episode."
            )
        except ValueError:
            log.exception("Failed to update planner for %s", match.name)
            planner_note = "\n⚠️ Couldn't locate this episode's row in the planner — check it manually."
    else:
        planner_note = "\n⚠️ No matching planner episode found for this date — planner left untouched."

    # Commit + push exactly what this flow touched (never a blanket commit —
    # in-progress session edits elsewhere in the tree must stay out of it).
    git_note = ""
    if gitops.has_repo(CFG.repo_root):
        pathspecs = [*deleted_tracked, rel_dest, "data/content_planner.md"]
        ok, note = gitops.commit_and_push(
            CFG.repo_root,
            pathspecs,
            f"Posted: {match.name} — archived to {rel_dest}/ (via bot)",
        )
        if ok:
            git_note = f"\n🔄 Git: {note}."
        else:
            log.error("Post-archive git sync failed for %s: %s", match.name, note)
            git_note = (
                f"\n⚠️ Git: {note}. The archive is done locally — "
                "commit/push it from a Claude Code session."
            )

    await query.edit_message_text(
        f"✅ Archived to <code>{_e(rel_dest)}/</code> as <b>{_e(PILLAR_LABELS[pillar])}</b>."
        f"{_e(planner_note)}{_e(git_note)}",
        parse_mode=ParseMode.HTML,
    )


async def cmd_analytics(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    digest = latest_analysis(CFG.analysis_dir)
    if digest is None:
        await update.message.reply_text(
            "No analytics runs yet — presentations/data-analysis/ is empty. "
            "Drop an Instagram export into data/analysis/ and run the "
            "data-analyzer skill first."
        )
        return
    await update.message.reply_text(
        f"<b>Latest analysis — {_e(digest.month)}</b>\n\n{_e(digest.summary)}",
        parse_mode=ParseMode.HTML,
    )
    files = exclude_unwanted(files_under(digest.path))
    if files:
        await _send_files(
            context.bot, update.effective_chat.id, files, f"📊 Files from {_e(digest.month)}:"
        )


async def cmd_file(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    rel = " ".join(context.args).strip()
    chat_id = update.effective_chat.id
    if not rel:
        await update.message.reply_text(
            "Usage: /file <path relative to the brand workspace root>\n"
            "e.g. /file social/queue/2026-07-06-move-of-the-day.md\n"
            "Point it at a folder to list what's inside."
        )
        return

    target = resolve_safe_path(CFG.repo_root, rel)
    if target is None:
        await update.message.reply_text("That path escapes the brand workspace — refusing.")
        return
    if not target.exists():
        await update.message.reply_text(f"Not found: {_e(rel)}")
        return
    if target.is_dir():
        names = list_dir_relative(CFG.repo_root, target)
        listing = "\n".join(f"• {n}" for n in names) or "(empty folder)"
        await update.message.reply_text(
            f"📁 <b>{_e(rel)}</b>\n{_e(listing)}", parse_mode=ParseMode.HTML
        )
        return
    await _send_file(context.bot, chat_id, target)


async def cmd_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"Your Telegram user id: {update.effective_user.id}")


async def unauthorized(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Anyone not on the allowlist gets their id and nothing else."""
    if update.effective_user and update.message:
        log.warning("Rejected user %s (@%s)", update.effective_user.id,
                    update.effective_user.username)
        await update.message.reply_text(
            "This is a private the brand bot. If it's yours, add this id to "
            f"BRAND_ALLOWED_USER_IDS in bot/.env: {update.effective_user.id}"
        )


async def daily_reminder(context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = "☀️ صباح الخير! the brand daily briefing:\n\n" + _today_message()
    pending = len(queue_items(CFG.queue_dir))
    msg += f"\n\n📦 Queue: {pending} package(s) waiting."
    for solution in solution_reveals_for(CFG.queue_dir, _today()):
        msg += f"\n\n🧩 Also planned today: post the solution as a Story — <code>{_e(solution.name)}</code> (grab it with /send)."
    for user_id in CFG.allowed_user_ids:
        try:
            await context.bot.send_message(
                chat_id=user_id, text=msg, parse_mode=ParseMode.HTML
            )
        except Exception:
            log.exception("Failed to send daily reminder to %s", user_id)


async def _broadcast(context: ContextTypes.DEFAULT_TYPE, text: str, **kwargs) -> None:
    for user_id in CFG.allowed_user_ids:
        try:
            await context.bot.send_message(chat_id=user_id, text=text, **kwargs)
        except Exception:
            log.exception("Broadcast failed to %s", user_id)


async def _alert_once(context: ContextTypes.DEFAULT_TYPE, key: str, text: str) -> None:
    """Broadcast an alert, suppressing exact repeats (keyed by text) so an
    unresolved failure doesn't re-fire every poll — but a changed error does."""
    state: PushState = context.application.bot_data["push_state"]
    if state.sent(key) == text:
        return
    await _broadcast(context, text, parse_mode=ParseMode.HTML)
    state.mark_sent(key, text)


async def _git_pull(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Fast-forward-only pull so cloud-routine commits land locally before
    /today, /queue, etc. read the filesystem. Never merges: divergent
    history fails loudly with the working tree untouched."""
    if not gitops.has_repo(CFG.repo_root):
        return  # pre-migration window — not an error
    try:
        result = gitops.pull_ff_only(CFG.repo_root)
    except Exception as exc:
        log.exception("git pull crashed")
        await _alert_once(context, "git-pull-failure", f"⚠️ <b>git pull crashed:</b> {_e(str(exc)[:500])}")
        return
    if result.returncode != 0:
        detail = (result.stderr or result.stdout).strip()[-800:]
        log.error("git pull --ff-only failed: %s", detail)
        await _alert_once(
            context,
            "git-pull-failure",
            "⚠️ <b>git pull failed</b> — local repo may be out of sync with GitHub.\n"
            f"<code>{_e(detail)}</code>\n\nResolve manually (likely a local edit conflicting "
            "with a cloud-routine commit) before trusting /queue or /today.",
        )


async def _announce_content_ready(
    context: ContextTypes.DEFAULT_TYPE, item: QueueItem, *, test: bool = False
) -> bool:
    """Send the "content ready" notification for one queue item — photos as
    files, a video as its link (see repo.split_deliverables), then the
    caption (if the package's .md has one) as its own follow-up message
    (added 2026-07-08 — it silently never reached the phone before, since
    the .md itself is never sent). Returns False (nothing sent) if the
    package has no photos and no video link yet.

    Once the package is APPROVED (decided 2026-07-13), raw board PNGs are
    dropped from this automatic push — see repo.auto_push_photos — since by
    then the user has already used them (in-session or in Canva); only a
    finished, postable asset (or a video link) still triggers the ping.
    /send and /queue are unaffected — they always include board assets too."""
    files = list(item.files)
    photos = auto_push_photos(files, package_approved(files))
    _, video = split_deliverables(files)
    if not photos and not video:
        return False

    prefix = "🧪 <b>[Test]</b> " if test else ""
    lines = [f"{prefix}🎉 <b>Content ready:</b> {_e(item.name)}"]
    if photos:
        lines.append(f"🖼 {len(photos)} photo(s) below")
    if isinstance(video, Path):
        lines.append("🎬 Video below")
    elif video:
        lines.append(f"🎬 Video: {_e(video)}")
    header = "\n".join(lines)
    caption = extract_caption(list(item.files))
    for user_id in CFG.allowed_user_ids:
        try:
            await context.bot.send_message(chat_id=user_id, text=header, parse_mode=ParseMode.HTML)
            for p in photos:
                await _send_file(context.bot, user_id, p)
            if isinstance(video, Path):
                await _send_video(context.bot, user_id, video)
            if caption:
                await context.bot.send_message(
                    chat_id=user_id, text=f"📝 <b>Caption:</b>\n\n{_e(caption)}", parse_mode=ParseMode.HTML
                )
        except Exception:
            log.exception("Content-ready delivery failed for %s to %s", item.name, user_id)
    for user_id in CFG.allowed_user_ids:
        try:
            await _offer_mark_posted(context, user_id, item)
        except Exception:
            log.exception("Failed to offer mark-posted for %s to %s", item.name, user_id)
    return True


async def content_ready_check(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Once a queue package's files have held steady across two consecutive
    polls (debounces a still-being-copied export) and haven't been announced
    yet, announce it. Silent if nothing deliverable is in it yet (e.g. only
    a caption .md so far, photos still to come)."""
    state: PushState = context.application.bot_data["push_state"]
    for item in queue_items(CFG.queue_dir):
        key = f"ready:{item.name}"
        sig = queue_signature(item)
        if sig == "empty":
            continue
        if state.seen(key) != sig:
            state.mark_seen(key, sig)
            continue
        if state.sent(key) == sig:
            continue
        if await _announce_content_ready(context, item):
            state.mark_sent(key, sig)


async def _periodic_tick(context: ContextTypes.DEFAULT_TYPE) -> None:
    await _git_pull(context)
    await content_ready_check(context)


async def cmd_test(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Manually fire all three scheduled notifications right now. Content-ready
    bypasses the two-poll debounce (so it doesn't need a real settle-wait) but
    still only sends for packages that actually have a photo or video link."""
    await update.message.reply_text("🧪 Running the daily briefing, draft-status check, and content-ready check now…")
    await daily_reminder(context)
    await draft_reminder(context)
    sent_any = False
    for item in queue_items(CFG.queue_dir):
        if await _announce_content_ready(context, item, test=True):
            sent_any = True
    if not sent_any:
        await update.message.reply_text(
            "🧪 Content-ready: nothing in social/queue/ has a photo or a "
            "*-video-link.txt* yet, so there's nothing to preview there. "
            "Drop a test .png (or a *-video-link.txt*) into social/queue/ "
            "and run /test again."
        )


def _slugify_series(series: str) -> str:
    """"Opening Spotlight *(swapped in from 07-08 — see note below)*" -> "opening-spotlight".
    Strips any trailing "(...)"/"*..." annotation the planner adds, then kebab-cases
    the rest — matches the templates/<pillar>/<slug>/ naming convention exactly."""
    base = re.split(r"[(*]", series, maxsplit=1)[0].strip()
    return re.sub(r"[^a-z0-9]+", "-", base.lower()).strip("-")


async def draft_reminder(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Nightly check (replaces the old auto-drafting/approval flow, removed
    2026-07-08): is tomorrow's episode drafted yet? If not, say so — and
    whether a template already exists for its series, since that's the
    first blocker either way. Also warns when the local tree has
    uncommitted changes, since the nightly cloud runs read GitHub and
    can't see unpushed work (added 2026-07-08)."""
    parts: list[str] = []

    tomorrow = _today() + timedelta(days=1)
    ep = episode_for(parse_planner(CFG.planner_path), tomorrow)
    if ep is not None and not ep.done:
        prefix = f"{tomorrow:%Y-%m-%d}-{_slugify_series(ep.series)}"
        already_drafted = (
            any(CFG.queue_dir.glob(f"{prefix}*"))
            or (CFG.queue_dir / f".draft-{prefix}.md").is_file()
        )
        if not already_drafted:
            pillar = guess_pillar(ep.series)[0]
            template_dir = CFG.repo_root / "templates" / pillar / _slugify_series(ep.series) if pillar else None
            has_template = template_dir is not None and template_dir.is_dir() and any(template_dir.iterdir())
            template_note = "✅ Template ready" if has_template else "🚧 No template yet — run template-generator first"
            parts.append(
                f"📝 <b>Tomorrow isn't drafted yet</b> — {tomorrow:%a %Y-%m-%d}\n"
                f"📚 Series: <b>{_e(ep.series)}</b>\n"
                f"✏️ Topic: {_e(ep.topic)}\n"
                f"{template_note}"
            )

    if gitops.has_repo(CFG.repo_root):
        dirty = gitops.dirty_files(CFG.repo_root)
        if dirty:
            parts.append(
                f"⚠️ <b>{len(dirty)} uncommitted change(s)</b> in the local repo — "
                "the nightly cloud runs read GitHub, so this work stays invisible "
                "to them until it's committed and pushed from a Claude Code session."
            )

    if parts:
        await _broadcast(context, "\n\n".join(parts), parse_mode=ParseMode.HTML)


async def _run_once_today(context: ContextTypes.DEFAULT_TYPE, key: str, func) -> None:
    """Run `func(context)` at most once per calendar day, tracked via
    PushState. Added 2026-07-22: the PC is shut down overnight, so a fixed
    cron time (BRAND_REMINDER_TIME/BRAND_DRAFT_REMINDER_TIME) was silently
    skipped most days — this lets a missed reminder fire the moment the bot
    next starts, while still no-opping if the actual cron time also lands
    later the same day (whichever fires first wins; /test bypasses this
    entirely by calling daily_reminder/draft_reminder directly)."""
    state: PushState = context.application.bot_data["push_state"]
    today_str = _today().isoformat()
    if state.sent(key) == today_str:
        return
    await func(context)
    state.mark_sent(key, today_str)


async def _daily_reminder_once_today(context: ContextTypes.DEFAULT_TYPE) -> None:
    await _run_once_today(context, "daily-reminder", daily_reminder)


async def _draft_reminder_once_today(context: ContextTypes.DEFAULT_TYPE) -> None:
    await _run_once_today(context, "draft-reminder", draft_reminder)


def main() -> None:
    global CFG
    CFG = load_config()

    if not CFG.allowed_user_ids:
        log.warning(
            "BRAND_ALLOWED_USER_IDS is empty — the bot will answer /id to anyone "
            "but nothing else. Message the bot, grab your id, and add it to .env."
        )

    # Single source for both the handlers and the Telegram command menu
    # (name, handler, menu description). The description is what shows in
    # Telegram's "/" autocomplete + the menu button — without set_my_commands
    # (below) the commands still work when typed, but none appear in the UI.
    commands = [
        ("today", cmd_today, "Today's planned episode"),
        ("week", cmd_week, "This week's schedule + done-status"),
        ("next", cmd_next, "Next scheduled episode"),
        ("queue", cmd_queue, "Packages waiting in social/queue/"),
        ("send", cmd_send, "Deliver a queue package's files here"),
        ("posted", cmd_posted, "Mark a package posted (archive + planner)"),
        ("fix", cmd_fix, "Log a correction for a queued package"),
        ("analytics", cmd_analytics, "Latest analytics digest + files"),
        ("file", cmd_file, "Deliver any repo file by path"),
        ("test", cmd_test, "Fire the scheduled checks now"),
        ("help", cmd_start, "Show the command list"),
    ]

    async def _set_command_menu(application: Application) -> None:
        try:
            await application.bot.set_my_commands(
                [BotCommand(name, desc) for name, _, desc in commands]
                + [BotCommand("id", "Show your Telegram user id")]
            )
        except Exception:
            log.exception("Failed to set the command menu")

    app = Application.builder().token(CFG.token).post_init(_set_command_menu).build()
    app.bot_data["push_state"] = PushState(CFG.state_path)

    allowed = filters.User(user_id=CFG.allowed_user_ids) if CFG.allowed_user_ids else filters.User(user_id=[])
    app.add_handler(CommandHandler("start", cmd_start, filters=allowed))
    for name, handler, _ in commands:
        app.add_handler(CommandHandler(name, handler, filters=allowed))
    # /id works for everyone — it's how you discover the id to allowlist.
    app.add_handler(CommandHandler("id", cmd_id))
    app.add_handler(CallbackQueryHandler(on_pillar_more, pattern=r"^posted-more:"))
    app.add_handler(CallbackQueryHandler(on_pillar_choice, pattern=r"^posted:"))
    app.add_handler(MessageHandler(~allowed, unauthorized))

    if CFG.reminder_time is not None and CFG.allowed_user_ids:
        app.job_queue.run_daily(_daily_reminder_once_today, time=CFG.reminder_time)
        app.job_queue.run_once(_daily_reminder_once_today, when=5)
        log.info("Daily reminder scheduled at %s (%s) + startup catch-up", CFG.reminder_time, CFG.timezone)

    if CFG.draft_reminder_time is not None and CFG.allowed_user_ids:
        app.job_queue.run_daily(_draft_reminder_once_today, time=CFG.draft_reminder_time)
        app.job_queue.run_once(_draft_reminder_once_today, when=10)
        log.info("Draft-status reminder scheduled at %s (%s) + startup catch-up", CFG.draft_reminder_time, CFG.timezone)

    if CFG.git_sync_interval is not None and CFG.allowed_user_ids:
        app.job_queue.run_repeating(
            _periodic_tick, interval=CFG.git_sync_interval, first=30
        )
        log.info("Git sync + content-ready check enabled every %ss", CFG.git_sync_interval)

    log.info("the brand bot starting (long-polling). Repo root: %s", CFG.repo_root)
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
