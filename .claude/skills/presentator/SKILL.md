---
name: presentator
description: Create {{BRAND_NAME}} presentations on demand — pitch decks, monthly review decks, partner/supplier briefs, strategy summaries. Use when the user asks for a presentation, deck, or slides on any topic. Sources concrete numbers by invoking the data-analyzer skill, defers all visual decisions to the designer skill (and asks it to define anything undefined), and feeds the user's review changes back into designer so preferences stick.
---

# Presentator

Builds a presentation from a user need, on demand. Not tied to a cadence. All paths relative to repo root.

## Step 1 — Intake

Pin down before building (ask via AskUserQuestion only for what the request doesn't say):
- **Purpose & audience:** who sees this and what should they do afterwards (investor/partner pitch, internal monthly review, supplier brief…)? Tone follows audience — but always within the brand voice (`context/Style_Guide.md` §3).
- **Language:** the brand's content language vs. the local business language may differ — this is the user's call per deck.
- **Scope & length:** target slide count and the 3–5 key messages.
- **Data needs:** does it require concrete performance numbers?

## Step 2 — Source the Content

- **Analysis/numbers needed → invoke the `data-analyzer` skill** (Skill tool) and use its outputs (insights + charts from `presentations/data-analysis/`). Never hand-invent metrics; if fresh data is needed, data-analyzer's intake handles it (files in `data/analysis/`).
- **Brand/product/strategy facts** come from the `context/` docs — cross-check `Products.md` open items before stating product facts (pricing that isn't locked stays out or is marked "TBD"; the holding-response rule applies to decks too).
- **Historical/cultural claims** pass the fact-check gate (`sop/SOP_Marketing_Research.md` §1.3).

## Step 3 — Design (defer to designer)

1. Read the **Presentation Design System** section of `.claude/skills/designer/SKILL.md` — including its **Learned decisions log** — and apply it as-is.
2. **Anything visual the designer skill doesn't yet define** (a layout pattern, a chart treatment, a cover style, an icon approach…) → invoke the `designer` skill to define it *before* building: present the options, let the user pick if it's taste, then **write the decision into designer's Presentation Design System** so it's defined forever after. Presentator never makes ad-hoc visual choices that live only in one deck.

## Step 4 — Build

- Self-contained HTML deck (16:9 slides), brand fonts embedded base64 (technique: `.claude/skills/template-generator/references/mockup-page-guide.md`), locked palette only, keyboard/scroll navigation between slides.
- Charts follow the `dataviz` skill (load it before chart code) recolored to the brand palette.
- Save to `presentations/<YYYY-MM-DD>-<topic-slug>/deck.html` (+ any assets alongside). Publish via Artifact for review.

## Step 5 — Review Gate

Present the deck (artifact link) + a slide-by-slide outline table in chat. Iterate on the user's feedback — content edits and design edits alike — republishing to the same artifact URL until approved.

## Step 6 — Feedback Capture (the anti-repetition loop)

After approval, sort every change the user made or requested during review:
- **Design preferences** (spacing, layout choices, color usage, typography sizes, chart style, "less of X, more of Y") → append to the **Learned decisions log** in `.claude/skills/designer/SKILL.md`, dated, phrased as a rule. Next deck starts from these — the user should never have to give the same design note twice.
- **Standing content/tone rules** → the owning doc (`Style_Guide.md` for voice, etc.), per the decisions-are-written-down rule.
- **One-off content edits** (this deck's wording/data) → nothing to record.
