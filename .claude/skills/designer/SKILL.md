---
name: designer
description: The visual authority for how {{BRAND_NAME}}'s visuals look — recurring brand graphics, diagrams, AND presentation design (layouts, color usage, typography scale). Use when creating or reviewing any brand graphic, when asked how visual elements should look, or when another skill (template-generator, content-creator, presentator) needs an undefined visual aspect decided. Holds the locked graphic specs, the presentation design system, and the learned-decisions log of user design preferences.
---

# Designer — Visual Spec & Design Authority

The single source of truth for how {{BRAND_NAME}}'s visuals look, downstream of the locked palette/typography in `context/Style_Guide.md` §2.

**Scope:** locked specs for recurring brand graphics (below), the Presentation Design System (near the end), and the Learned decisions log — where every user design preference gets recorded so no design note has to be given twice. When another skill hits an undefined visual question, it comes here: define it (with the user when it's taste), write it down in the right section, then apply it.

## Recurring Brand Graphics (specs locked here as they're decided)

<!-- If the brand produces any graphic repeatedly (a diagram type, a chart style, a product-shot frame, a quote card…), its exact spec gets locked here so it renders pixel-identical every time: colors (hex), stroke widths, coordinate/label conventions, orientation rules. Baydaq's example was a chess-board renderer with locked square colors, piece colors, and arrow styling. -->

*(none defined yet — created during onboarding or the first time a recurring graphic is needed)*

**When a recurring graphic is defined:**
- Render options for the user to pick from (taste decisions are the owner's), then record the locked spec here.
- If it's produced programmatically, the generator script lives in `templates/<asset>/generator/` with a README; production assets always come from the script so styling stays identical.
- Colors outside the Style Guide palette are allowed ONLY if recorded here as asset-specific (e.g., "this hue is board-only — it does not join the general palette").

## Annotation / emphasis defaults

<!-- Cross-asset conventions: arrow/marker styling, highlight treatment, label typography. Fill during first use; Baydaq's learned rule: markers slim (~7% of the local cell size), ~75% opacity, never covering content — understated wins. -->

*(to be defined with the user on first need)*

## Rules for other agents

1. Any post/template containing a spec-locked graphic follows this file — template-generator and content-creator defer here.
2. Never restyle a locked recurring graphic per-post — locked graphics ARE brand furniture, like the logo.
3. Factual accuracy of any diagram is a hard requirement — a wrong diagram is a credibility cost (same standard as the fact-check gate).
4. Graphics are always produced fresh from the spec — never screenshot/scan source imagery (copyright + off-brand).
5. When a skill needs a visual decision this file doesn't cover: propose options, let the user pick if it's a matter of taste, then record the decision here (in the right section) before applying it. No ad-hoc visual choices that live only in one deliverable.

## Presentation Design System

Baseline for decks built by the `presentator` skill (16:9, self-contained HTML). Starting defaults — refined over time via the Learned decisions log below:

- **Canvas:** 16:9 slides, the Style Guide's background color; the text/dark color for a full-bleed cover/section-divider variant (light logo lockup on it).
- **Typography:** the headline font for slide titles only; the body font for everything else (body, labels, data). If a deck's language doesn't suit the headline font, use the body font in bold for titles instead.
- **Color usage:** the primary color for accents, key numbers, and the single emphasis per slide; the secondary color for supporting surfaces (cards, table headers); never more than one primary-emphasized element per slide.
- **Layout:** generous margins, one idea per slide, content weighted per the language's reading direction; tables and charts get the full slide width rather than being squeezed beside text.
- **Charts:** dataviz-skill conventions recolored to the palette; source note in small body-font under every data slide.
- **Understatement rule:** default to understated — thin rules, small markers, no heavy shadows or decorative flourishes — unless the brand personality (Style Guide §1) explicitly calls for bold.

### Learned decisions log

*Appended by `presentator` (and any skill) after user reviews — dated, phrased as reusable rules. The user should never have to give the same design note twice.*

*(empty — starts accumulating from the first design review)*
