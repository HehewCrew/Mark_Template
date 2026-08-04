---
name: brand-onboarding
description: Interview the brand owner to define everything this workspace template leaves open — brand identity, products, marketing strategy, visual/voice style, terminology, process details — and write the answers into the living docs. Use on first contact with a fresh copy of this template, when the user asks to set up / onboard / configure the brand, or whenever docs still contain {{...}} placeholders. Resumable: tracks progress via each doc's Open/To Be Defined checklist and the remaining placeholders.
---

# Brand Onboarding — Define Everything With the Owner

This workspace is a **generic brand-marketing template**. Nothing in it is decided until the brand owner decides it. This skill runs the guided interview that turns the skeleton into a real brand workspace — and it is the enforcement mechanism for the core rule: **a placeholder is not a decision.**

## Ground rules

1. **Never invent brand facts.** Every `{{...}}` value is filled from the owner's answers or from research the owner confirms. If the owner defers, the item stays on the doc's "Open / To Be Defined" checklist — recorded, not guessed.
2. **Guide, don't just ask.** For every question, offer 2–4 concrete options with trade-offs (AskUserQuestion), grounded in the niche. The owner may not know what a "content pillar" is — explain each concept in one or two sentences before asking, and give an example (the docs' HTML comments contain examples from Baydaq, the chess brand this template was derived from — use them as illustrations, never as defaults).
3. **Research before proposing.** When a question benefits from real data (competitor landscape, growth benchmarks, platform best practices, palette conventions in the niche), do a quick research pass (or dispatch the `marketing-research-agent` skill) and present sourced options — "per <source>, checked <YYYY-MM>".
4. **Write down every answer immediately** in the owning doc: fill the `{{...}}` value, remove the instructional HTML comment if it's resolved, bump `Last updated:`, and check off the item in that doc's "Open / To Be Defined" list. A decision isn't real until it's written down.
5. **One topic block at a time.** Don't fire 30 questions at once; run the phases below in order, max 3–4 questions per AskUserQuestion call, and summarize what got locked after each phase.
6. **Resumable.** On invocation, first scan the docs (Grep for `{{` and unchecked `- [ ]` items) and report what's already defined vs. still open — then continue from the first open phase. Never re-ask what a doc already answers.

## Phase 0 — Session intake

- Ask for the brand's **name** first, then rename `{{BRAND_NAME}}` across all docs, and offer to rename the workspace folder itself.
- **Ask whether this is a new brand or an existing one.** This changes the mode of every later phase:
  - **New brand (launch mode):** questions are decisions to make — propose options, the owner picks.
  - **Existing brand (audit/import mode):** questions are facts to harvest first, decisions second. Ask for what already exists — logo/font/palette files, brand guidelines docs, live account handles, current product list + real pricing, existing posting habits, past performance data, known competitors — and **document reality as locked** before proposing anything. Only gaps and things the owner wants to change get the options treatment. Ask for existing asset files up front: logos → `templates/logo/`, fonts → `templates/logo/fonts/`, guideline docs/exports → `data/references/`, analytics exports → `data/analysis/`.
  - Record the mode at the top of `context/Brand_Context.md` so later sessions know it.
- Ask how much time/depth the owner wants today: full onboarding (all phases) or a minimum-viable pass (Phases 1, 3, 4 — enough to start producing content). Record the choice.
- Replace `{{DATE}}` placeholders with today's date as sections get filled (not before).

## Phase 1 — Brand fundamentals → `context/Brand_Context.md`

Interview: category, market + expansion horizon, core product/offer, primary content channel and its framing, one-line description, vision, positioning roadmap (Year 1 / Year 2 / long term), tagline (mark "suggested" until locked), key principle, business model & sequencing (what gets built first and what milestone unlocks the next investment), reference/research sources for content grounding.

**Sequencing question matters most** — walk the owner through the "community first, store second" idea and ask what the equivalent ordering is for their brand. **Existing brand:** the sequencing question becomes "where are you now, and what's the next milestone?" — record the current state (channels live, sales running or not) as fact, and the roadmap phases as what's *ahead*, not a from-zero plan.

## Phase 2 — Products → `context/Products.md`

Per product: contents/variants/materials, what's genuinely locked vs. open (a new brand's pricing usually stays open — that's fine, record it; an existing brand's real prices are facts — write them in as locked), the **selling story** (core hook + secondary hook — push the owner to find the one authentic detail competitors can't copy), competitor pricing benchmark (research this live), the **holding response** for questions arriving before specs are locked, and the content/launch tie-in.

## Phase 3 — Marketing strategy → `context/Marketing_Strategy.md`

The heaviest phase — take it in sub-blocks:
1. **Target audience** — who, which segments, and the post-launch adjustment checkpoint.
2. **Content pillars** (3–6, with % shares summing to 100 and kebab-case folder slugs) → then **create the matching pillar folders** under `social/` and note the slugs in `social/README.md`.
3. **Recurring series** per pillar (named, each with a slug) and the **posting cadence** rotation.
4. **Format & volume targets** + the priority success metrics.
5. **Growth benchmarks** — research realistic organic ranges for the niche/market; source-note them. **Existing brand:** the baseline is the account's own history — record current numbers and age, set the benchmark table as growth *from here*, and offer to run the `data-analyzer` on any past exports the owner can provide before setting targets.
6. **Competitors** — research the named competitors live; fill Section 5 with sourced pricing points. Also copy competitor names into `sop/SOP_Marketing_Research.md` §1.1.
7. **Content reference accounts**, **production tools** (one per format; leave open what isn't needed yet), **community guidelines/moderation approach**, expansion strategy.

## Phase 4 — Style guide → `context/Style_Guide.md`

**Existing brand with an established identity:** this phase is transcription, not design. Extract the palette hexes, fonts, and voice rules from the owner's existing assets/guidelines (ask for the files; sample colors from the logo if no guideline doc exists), write them in as **locked**, and confirm with the owner that what's written matches reality. Only propose options for what's genuinely missing or what the owner explicitly wants to rework.

For a new brand (or the gaps of an existing one) — taste decisions — always present rendered options, never just word descriptions:
1. **Brand personality** (the one-liner + is/is-not lists).
2. **Color palette** — propose 2–3 palettes as a rendered HTML swatch page (self-contained, published via Artifact when available). Ask whether the palette can anchor to something physical/real in the brand's world (material, place, product) — anchored palettes carry a story.
3. **Typography** — 2–3 pairings rendered with real sample copy in the brand's language; check script support and licensing (Google Fonts = safe default). Once locked, download the TTFs into `templates/logo/fonts/`.
4. **Voice & tone** — principles, tone-by-pillar table, language/register rules, 2–3 sample snippets in the brand's actual language.
5. **Writing micro-rules** — numerals, CTA register, emoji policy.
6. **Logo** — concept direction only during onboarding; actual design is a separate `designer`-skill session. Record the concept and mark files pending.

After locking visuals, record any graphic-spec decisions in the `designer` skill's spec section so all agents inherit them.

## Phase 5 — Terminology & glossary → `context/Glossary.md`

Ask whether the niche has technical vocabulary worth standardizing. If yes: define the term categories, the pairing/format rule, and seed the standard terms (verified against authoritative sources for the language/niche). If no: slim the file to the fact bank + note the decision.

## Phase 6 — Process details → `sop/` + `data/`

1. Fill `sop/SOP.md`'s tool/format slots and team-size assumption from Phase 3 answers.
2. Set the week anchor and plan Cycle 1 in `data/content_planner.md` (episodes grounded in the Phase 1 reference sources — build the Appendix source→series map if material exists in `data/references/`). **Existing brand:** the anchor is when this *workspace's* rotation starts, not a launch date — and seed the planner's episode log with recent already-published topics (from the owner or the account itself) so the redundancy guard knows what's been done.
3. Ask about automation appetite: if wanted, configure `.claude/automation/` per its README (scheduled research/analysis runs) — otherwise leave documented but disarmed.
4. **Ask whether they want the Telegram bot** (`bot/`, optional — the workspace is fully functional without it). Explain what it is in a sentence before asking: a phone-side reporter over the repo's own files that shows what's scheduled, delivers finished packages to your phone, and archives a package once you confirm it went live. It has no model in it — it only executes what you tapped.
   - **Yes** → walk them through `bot/README.md`: create the bot with @BotFather, copy `.env.example` to `.env` with the token, install the requirements, run it, then `/id` → allowlist → restart. Then set `PILLAR_SLUGS` in `bot/pillars.py` to the pillars locked in Phase 3, and add the Phase 3 series names to `_SERIES_BY_PILLAR` so `/posted` can pre-select a pillar.
   - **No / not yet** → leave `bot/` as it is and say it can be set up any time; nothing else in the workspace depends on it. Do not delete the folder.
   - Either way, never write a real token into any tracked file — it belongs only in `bot/.env`, which is gitignored.
5. Confirm `.mcp.json` (an Excel MCP is pre-registered for analytics parsing; add others as needed).

## Phase 7 — Close-out

1. Sweep: Grep all docs for remaining `{{` placeholders and unchecked onboarding items; list what's still open and where each is recorded.
2. Update `CLAUDE.md`: replace brand-name placeholders, correct the directory map if pillar folders/slugs were created, and — once no placeholders remain in a doc — remove that doc's "TEMPLATE STATUS" banner.
3. Final summary to the owner: what's locked (with file links), what's deliberately open, and the suggested next action (usually: run `template-generator` for the first series template, then `content-creator` for the first post).
