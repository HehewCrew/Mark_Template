---
name: template-generator
description: Sketch and finalize a reusable content template for a {{BRAND_NAME}} series, a product presentation, or a video structure. Use when the user asks to create, sketch, mock up, or design a template, carousel/post/video layout, series design, or product presentation. Generates 3 visual mockup directions (HTML, real brand fonts), lets the user pick one, then emits a production build sheet + visual reference into templates/.
---

# Template Generator

Turns a content need into a production-ready template in four steps: gather references → fill gaps with the user → present 3 visual mockup directions → build the chosen one into a build sheet + visual reference. All paths below are relative to the repo root.

**Prerequisite:** the Style Guide's palette and typography must be locked (`context/Style_Guide.md` §2) and the font files present in `templates/logo/fonts/`. If not, stop and route to `/brand-onboarding` — a template built on placeholder visuals is worthless.

**Honest constraint stated up front:** most design tools (e.g., Canva) have no external-template import. "Production-ready" means a build sheet precise enough to recreate the design in the tool **once** (using its brand-kit workflow, per `context/Marketing_Strategy.md` §7), after which the user duplicates it inside the tool for every future post. The HTML visual reference is the picture they rebuild against.

## Step 0 — Intake & References

Classify the input, then read the matching sources:

| Input type | How to recognize | Required reading |
|---|---|---|
| **Series content** | Names a series or a pillar | `context/Marketing_Strategy.md` §1 (series list, cadence, format targets) + the series' tone row in `context/Style_Guide.md` §3.2 |
| **Product presentation** | Mentions a product, showcase, catalog, launch | `context/Products.md` (selling story, what's locked vs. open) — never template unconfirmed facts as fixed text; give them `{{...}}` slots instead |
| **Video structure from reference** | Input is a video link or file | WebFetch the link for caption/metadata (you cannot watch video — say so). Then ask the user to describe the beats/scenes worth templating. |

**Always read, for every input type:**
- Everything in `data/examples/` — the reference library, including the craft/best-practices doc (story spine, hook types, format-selection rules) once it exists.
- `context/Style_Guide.md` §2 (locked palette, typography, imagery style) and §3 (voice).
- `context/Glossary.md` for any technical term appearing in sample text.

**If `data/examples/` has nothing relevant** to the requested template type, design the mockups entirely new from the context docs alone — and tell the user that's what happened.

## Step 1 — Ask What the Docs Don't Answer

Use AskUserQuestion for genuinely open parameters only (don't re-ask what a doc already decides). Typical gaps:
- **Format & canvas:** per the platform's current sizes (e.g., carousel 1080×1350 / square 1080×1080 / vertical video 1080×1920 — video templates cover the cover frame and recurring on-screen text styling, not the edit itself)
- **Slide/scene count** (default per the craft doc)
- **Language register:** per `context/Style_Guide.md` §3.3
- Any series-specific must-have (recurring segment, diagram slot, episode-numbering policy — check the Style Guide's writing rules for standing decisions)

## Step 2 — Three Mockup Directions

Build ONE self-contained HTML page showing three visually distinct directions — vary layout and color-weighting, never the palette itself. Each direction shows the cover + one representative body slide at the correct aspect ratio.

Follow `references/mockup-page-guide.md` for the mechanics (font-embedding, text-direction setup, slide frames). Non-negotiables:
- Fonts: the locked pairing embedded as base64 data URIs from `templates/logo/fonts/` — no CDN links, no fallback fonts doing the real work
- Colors: ONLY the locked palette from `context/Style_Guide.md` §2.1
- Logo: inline the brand SVG from `templates/logo/` when it exists
- Sample text: correct text direction for the brand's language, glossary-standard terms with the pairing rule — real illustrative copy, never lorem ipsum
- Label each direction A / B / C with a one-line design rationale

Save to `templates/<pillar-slug>/<slug>/<slug>-mockups.html` — `<pillar-slug>` per `context/Marketing_Strategy.md` §1.1; `<slug>` = kebab-case of the series/product. Publish via the Artifact tool when available so the user sees it rendered; otherwise tell them to open the file in a browser. Then AskUserQuestion: pick A, B, or C (repeat each option's rationale in its description). Iterate if the user asks for changes before choosing.

## Step 3 — Final Template (after selection)

Produce both files in `templates/<pillar-slug>/<slug>/`:

1. **`<slug>-template.md`** — the build sheet, using the skeleton in `references/build-sheet-template.md`: canvas size; one element table per slide/frame (element, position, font + size in px, color hex, `{{PLACEHOLDER}}` slot); one-time recreation steps in the production tool; batch-production workflow; pre-publish pointer to `sop/SOP.md` §2.
2. **`<slug>-final.html`** — the chosen direction expanded to ALL slides/frames (not just cover + one body), same self-contained technique as the mockups page. This is the visual the user rebuilds against.

Placeholder convention: `{{HOOK}}`, `{{BODY_1}}`, `{{TERM}}`, `{{CTA}}`, `{{HOLDING_RESPONSE}}` — every variable text region is a named slot; fixed brand furniture (logo, series wordmark, palette blocks) is not.

3. **Publish to the reference library** — once the user confirms the final template, copy the build sheet to `data/examples/posts/<slug>-template.md` (flat — no pillar subfolders there). This folder is the reference library downstream content agents read, so every confirmed template must land there. Add one line at the top of the copy: `> Canonical source: templates/<pillar-slug>/<slug>/<slug>-template.md — edit there and re-copy; do not edit this file directly.`

## Step 4 — Document Maintenance (repo rules)

- Keep `CLAUDE.md`'s directory description accurate when the first content template lands in `templates/`.
- **Sync rule:** if a template in `templates/<pillar-slug>/<slug>/` is later revised, re-copy the build sheet to `data/examples/posts/` in the same edit — the two files must never diverge.
- If building the template settles a previously open decision (e.g., video on-screen text styling), write the decision into the owning doc, bump its `Last updated:`, and tick the checklist item. A decision isn't real until it's written down.

## Guardrails (fail QC if violated)

1. Locked palette and fonts only — introducing any other color/typeface requires the user updating the Style Guide first.
2. Glossary-standard terms with the pairing rule (`context/Glossary.md`).
3. Language/register rules per `context/Style_Guide.md` §3.3.
4. No hard-sell slots ("Shop now", price flashes) in any template if the brand's sequencing principle defers direct sales — product templates sell through the selling story per `context/Products.md` §1.2.
5. Unconfirmed product facts (pricing, specs) never appear as fixed template text — only as `{{...}}` slots, defaulting to the holding response.
6. Sample copy in mockups is illustrative: flag that final captions still pass any native-speaker review and the fact-check gate (`sop/SOP_Marketing_Research.md` §1.3) before publishing.
