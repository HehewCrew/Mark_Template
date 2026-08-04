# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

This is **not a codebase** — there is no build system, tests, or app dependencies. It is a living set of Markdown documents that define the brand, product, marketing, and process strategy for **{{BRAND_NAME}}**, plus the Claude Code skills/agents that operate on them. Work here consists of drafting/editing content strategy, brand copy, and content plans — not writing or running application code.

## ⚠️ Template status — onboarding comes first

This workspace started from a generic brand template. **Any `{{...}}` placeholder in any doc is an undefined decision, not a value.** Standing rules until onboarding is complete:

1. **At the start of a session, check for placeholders** (grep the docs for `{{`). If any remain, tell the user which areas are still undefined and offer to run the `/brand-onboarding` skill — it interviews the owner, guides them through every open decision with concrete options, and writes the answers into the docs. It handles both **new brands** (decisions to make) and **existing brands** (reality to audit and import first — existing assets, identity, pricing, and history get documented as locked before anything is proposed).
2. **Never treat a placeholder or an HTML-comment example as a decision.** The comments contain illustrations from the brand this template was derived from — they are teaching aids, never defaults.
3. **Never produce publishable content, templates, or strategy claims on top of undefined fundamentals** (palette, voice, rotation, audience). Route to `/brand-onboarding` first.
4. When a section becomes fully defined, remove its "TEMPLATE STATUS" banner and check off the matching items in its "Open / To Be Defined" list.

## Directory map

`context/` — the living strategy docs (see Document map below). `sop/` — the process docs. `ads/` is an empty placeholder for future ad creative. `presentations/` holds on-demand decks (`presentations/<YYYY-MM-DD>-<topic-slug>/`, built by the presentator skill) and `presentations/data-analysis/<YYYY-MM>/` — analytics dashboards + insights produced per `sop/SOP_Data_Analysis.md`. `social/` holds prepared and published social content: `social/queue/` — production-ready post packages awaiting publishing (produced by the content-creator skill); once published, each package is archived to `social/<pillar-slug>/<series-slug>/` (pillar folders are created during onboarding from `Marketing_Strategy.md` §1.1). `data/` holds: `data/examples/` — content-generation reference material (craft docs plus `data/examples/posts/`, the confirmed-template library read by content agents); `data/references/` — copies of the brand's grounding sources (paraphrase only, never verbatim); `data/content_planner.md` — the episode schedule + done-log consumed by the content-creator skill; `data/analysis/` — intake folder for unprocessed analytics exports, consumed by the data-analyzer skill (processed files move to `presentations/data-analysis/`); and `data/research_reports/` — monthly strategy-proposal reports from the automated research run awaiting user review. `templates/logo/` holds the brand logo files + `templates/logo/fonts/` the brand font files once locked; `templates/<pillar-slug>/<series-slug>/` holds confirmed content templates grouped by content pillar — build sheet + HTML visual reference, produced by the template-generator skill; each confirmed build sheet is mirrored to `data/examples/posts/` (flat) for content agents — the `templates/` copy is canonical.

**Agent team:** `.claude/agents/` defines six specialists wrapping the project skills — content-writer, template-maker, researcher, visual-designer, analyst, presenter — orchestrated by the `/day-planner` skill (derive Day X task list → user approval → dispatch → main-thread user gates → sync). Subagents never talk to the user; all approvals/reviews/taste decisions happen in the main thread. **The repo files are the team's sync medium**: `data/content_planner.md` (schedule + done-log), `social/queue/` (content output), the `context/`+`sop/` docs (decisions), and the designer skill's learned-decisions log (preferences).

## Document map — read this first

There is no single source of truth file; instead, the interlinked docs each own one concern. Before editing anything, know which file governs the question at hand:

| File | Owns |
|---|---|
| `context/Brand_Context.md` | Brand identity, vision/positioning roadmap, business model & sequencing, reference sources |
| `context/Products.md` | Product catalog, pricing, selling story, sales channel/sequencing |
| `context/Marketing_Strategy.md` | Content pillars/series/cadence, growth benchmarks, expansion strategy, target audience, competitor landscape, production tools, community moderation guidelines |
| `context/Style_Guide.md` | Visual identity (colors/type/logo/imagery) and voice & tone rules |
| `context/Glossary.md` | Standardized terminology — the canonical term list for all content — plus the verified-facts bank |
| `sop/SOP.md` | Weekly content production process (plan → draft → produce → QC → publish → monitor) and the pre-publish checklist |
| `sop/SOP_Marketing_Research.md` | How/when/where research (competitor, platform, historical, audience, SEO, pricing) is gathered and which living doc each finding feeds |
| `sop/SOP_Data_Analysis.md` | How analytics exports become insights + a branded HTML dashboard |

Each file's header cross-references the others — when editing one, check whether the change invalidates a claim in a companion file.

## Core rules that constrain any edit

- **A decision isn't real until it's written down.** `sop/SOP.md` Section 5: if a decision was made in chat/conversation, it must be written into the relevant living doc immediately, and the corresponding open item checked off in that file's "Open / To Be Defined" list. Don't leave decisions implicit.
- **Locked brand constants — once defined in `Style_Guide.md`, do not alter without explicit instruction:** colors, typography, and terminology. Until they are defined, they are not "flexible" — they are blocking (see the onboarding rules above).
- **Terminology rule:** always use the "{{BRAND_NAME}} standard" term from `context/Glossary.md`, never an alternate, even when multiple valid terms exist — with the pairing/format rule applied on first mention, if one is defined.
- **Language rule:** per `Style_Guide.md` §3.3 — respect the register/dialect boundaries it defines per content type.
- **Sequencing principle:** per `Brand_Context.md` §3 — if the brand defers direct selling (e.g., "community first, store second"), don't draft content or product copy that leads with a hard sell.
- **Don't state unconfirmed product facts** (pricing, specs) as settled — check `Products.md`'s "Open / To Be Defined" section before writing product copy; use the standing holding response for questions that aren't locked yet.
- **Historical/cultural claims** (used in storytelling content) must be checked against a real source before publishing, cross-checked across at least two sources if surprising, and always paraphrased — never quoted verbatim from a source. Verified facts get added to `Glossary.md` Section 6 for reuse.

## Editing conventions

- Every doc has a `Last updated:` date near the top — update it when making substantive edits.
- Each file ends with an "Open / To Be Defined" checklist — resolved items get checked off (`[x]`) rather than deleted, so history of what's been decided is visible.
- Keep companion-file cross-references (the `>` blockquote near the top of each file) accurate if a file's scope changes.
- Keep this file's directory map accurate when the structure changes (pillar folders created, first template landed, etc.).
