# Telegram assistant bot — optional

**Entirely optional.** The workspace works without it. Skip this folder unless you
want the workflow reachable from your phone; nothing else depends on it.

It is a **reporter over the repo's own files**, not a second source of truth. It reads
`data/content_planner.md` and `social/queue/`, and it has exactly two write paths —
`/posted` (archive a published package) and `/fix` (log a correction request).

## Why there is no model in it

The bot has **no LLM in the loop at all**. It executes only what you tapped, or writes
down what you typed for a later Claude Code session to act on. That is deliberate: a
wrong guess here would edit the planner or archive the wrong package, and a bot that
refuses is worth more than one that improvises. When inputs don't line up, it says so
and stops.

## Setup

1. **Create the bot.** Message [@BotFather](https://t.me/BotFather) on Telegram, send
   `/newbot`, and keep the token it gives you.
2. **Configure it.** Copy `.env.example` to `.env` and paste the token in. `.env` is
   gitignored — never commit it, and treat the token like a password.
3. **Install and run:**
   ```bash
   python -m venv .venv
   .venv/Scripts/pip install -r requirements.txt   # Linux/macOS: .venv/bin/pip
   .venv/Scripts/python bot.py
   ```
4. **Allowlist yourself.** Send `/id` to the bot, put the number in
   `BRAND_ALLOWED_USER_IDS`, and restart. Until you do, the bot answers `/id` and
   refuses everything else — an empty allowlist means nobody, not everybody.

## Commands

| Command | What it does |
|---|---|
| `/today` `/week` `/next` | What's scheduled, from `data/content_planner.md` |
| `/queue` | Packages waiting in `social/queue/` |
| `/send <name>` | Deliver a package's photos and video to this chat |
| `/posted <name>` | Confirm it went live: archive the build sheet to `social/<pillar>/<series>/`, update the planner, then commit and push exactly those changes |
| `/fix <name> <caption\|photo\|phrase> <text>` | Log a correction for a package that already shipped. The bot can't make the change itself — it writes a marker for a later Claude Code session to pick up |
| `/analytics` | Digest of the latest run under `presentations/data-analysis/` |
| `/file <path>` | Deliver any repo file by path |
| `/id` | Your Telegram user id — how you discover what to allowlist |
| `/test` | Fire the scheduled checks now, bypassing their debounce |

Plus, on a schedule: a **morning briefing** (today's episode + queue count), a **nightly
draft check** (is tomorrow's episode drafted yet?), a **content-ready push** when a
package lands in the queue, and a periodic `git pull` so it sees work done elsewhere.
Each is switched off by setting its variable to `off`.

## Adapting it to your brand

- **`pillars.py`** — set `PILLAR_SLUGS` to the pillars in `context/Marketing_Strategy.md`
  §1.1, since those are also the folder names under `social/`. Adding series names to
  `_SERIES_BY_PILLAR` lets `/posted` pre-select a pillar; leaving it empty just means you
  pick from the full list each time.
- **Package layout** — `repo.py` expects the format in
  `.claude/skills/content-creator/references/post-package-format.md`. Change that format
  and `repo.py` needs to follow.

## What was deliberately left out

The brand this was extracted from had a narrated-video pipeline (`/voiceover`, `/build`,
`/script`) that assembled Reels from recorded audio snippets. It is not here, because it
drove a series-specific frame generator — shipping it would ship code that cannot run.
The commands, `voiceover_build.py`, and the audio-intake handler were removed together;
everything above is the part that generalises.
