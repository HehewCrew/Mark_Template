---
name: content-creator
description: Prepare today's {{BRAND_NAME}} post — production-ready, not published. Use when the user asks to create, prepare, draft, or generate content/a post, or asks "what's today's post". Checks the planner for today's series, ensures a template exists (calls template-generator if not), sources the content from the reference material in data/references/, drafts in the brand's language per the Style Guide, gets user approval on the content and slide count, then exports a fill package and marks the episode done in the planner.
---

# Content Creator

Prepares one post end-to-end up to (not including) design production: scheduler → template → source-grounded content → drafting → **user review gate** → production-ready export package → planner check-off. All paths relative to repo root.

**Prerequisite:** onboarding must have defined the rotation (`context/Marketing_Strategy.md` §1.3), the Style Guide language/voice rules, and at least one series. If placeholders remain in those sections, stop and route to `/brand-onboarding` first.

**Scope limits, stated up front:**
- This skill does NOT create or publish the post — it produces a fill package the user takes into the production tool (`context/Marketing_Strategy.md` §7). If a production-tool MCP is ever connected, revise Step 6 to push directly.
- Reference material is **grounding, never copy**: paraphrase in the brand's voice, never reproduce source text verbatim, never scan/screenshot source imagery into posts. Facts and structures are fine; the author's words are not.

## Step 1 — Scheduler Check

1. Get today's date (`Get-Date -Format "yyyy-MM-dd dddd"`), or use the date/series the user passed as an argument.
2. Open `data/content_planner.md` — it anchors week parity and lists the planned episode per day: series, topic, source grounding, status.
3. Cross-check the series against the rotation in `context/Marketing_Strategy.md` §1.3 — the planner must agree with the rotation; if they conflict, the rotation wins and the planner gets fixed.
4. **Redundancy check:** if the planned episode is already checked `[x]` in the planner, do not regenerate it — plan the next episode for that series (per the planner's Appendix source map) and add it to the planner first.
5. If the planner has no entry for today (planner ran out), extend the planner by another cycle first, using the Appendix source→series map.

## Step 2 — Template Check

Look for `data/examples/posts/<series-slug>-template.md`.

- **Found** → its `{{...}}` slots define exactly what content to produce.
- **Missing** → invoke the `template-generator` skill (Skill tool) for this series and complete its full flow (3 mockups → user picks → confirmed template lands in `data/examples/posts/`). Only then continue.

## Step 3 — Source the Content

1. The planner entry names the source (reference material in `data/references/`, a verified fact from `context/Glossary.md` §6, or scoped web research). Read/verify it.
2. Extract the lesson/story: the idea, the key details, the "why it matters" — in your own words.
3. Historical/cultural/technical claims trigger the fact-check gate (`sop/SOP_Marketing_Research.md` §1.3): verify against a real source, cross-check surprising claims in two independent sources, soften or drop what can't be confirmed. Add verified facts to `context/Glossary.md` §6.
4. Episodes without reference-material grounding are grounded in web research + the Glossary §6 fact bank, with the fact-check gate applied to every claim.

## Step 4 — Draft the Post

Apply, in order:
- Story spine + hook type for this series (per the craft doc in `data/examples/`, once written — hook → stakes → build → payoff → CTA)
- The template's slot list — produce one value per `{{...}}` slot
- The Style Guide's language rules (§3.3), register rules for the CTA (§4), glossary-standard terms with the pairing rule on first mention, and every writing micro-rule in §4
- **Generated graphics — produce them, don't leave placeholders:** if the template has image slots for a spec-locked generated graphic (see the `designer` skill), render them per that spec and save alongside the draft. Accuracy of any factual diagram is a hard requirement.
- Slide count within the template's structure (default per the craft doc / template); caption with natural keyword language + engagement CTA
- No unconfirmed product facts (use `{{HOLDING_RESPONSE}}` from `context/Products.md`); no hard-sell

## Step 5 — User Review Gate (mandatory, never skip)

Present in one chat message, **before** any approval question:
1. **Source summary:** what the source says, paraphrased, with the reference — so the user can judge fidelity.
2. **The content table:** one row per slide — slide number, template slot, the drafted text, a gist in the user's working language if the content language differs. Caption and alt text as rows too. This table IS the default review format.
3. **Generated graphics (when present):** clickable file paths plus the data used to produce each — the user validates accuracy alongside the text.
4. **Slide count**, stated explicitly.

A rendered visual (filled-slides HTML via Artifact) is produced **only if the user asks for it** — don't generate one by default.

Then AskUserQuestion: approve / adjust specific slides / change slide count / reject topic. Expect per-post steering on wording (especially register/dialect if the Style Guide allows local flavor). Iterate until approved. Do not write the export package before approval.

## Step 6 — Export Package (production-ready)

Write `social/queue/<YYYY-MM-DD>-<series-slug>.md` using `references/post-package-format.md`: approved slot→text table (copy-paste ready), caption, alt text, the template + visual reference paths, and the pre-publish checklist (`sop/SOP.md` §2) as unchecked boxes for the user to run in the production tool.

## Step 7 — Mark Done & Maintain Docs

1. In `data/content_planner.md`: check the episode `[x]`, link the export package file, bump `Last updated:`.
2. If a new verified fact was added to the Glossary or any decision was made, write it into the owning doc now (a decision isn't real until written down).

## Step 8 — Archive After Publishing

When the user reports the post as actually published, move its package out of the queue into the pillar archive, mirroring the templates/ structure:
`social/queue/<date>-<series-slug>.md` → `social/<pillar-slug>/<series-slug>/<date>-<series-slug>.md`
(pillar slugs per `context/Marketing_Strategy.md` §1.1). Update the planner's episode-log link to the new path. The queue holds only unpublished, ready-to-produce posts.
