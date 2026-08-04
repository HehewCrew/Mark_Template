# {{BRAND_NAME}} Style Guide

> Combined visual identity + voice & content guide for {{BRAND_NAME}}.
> Status: **nothing locked yet** — every visual/voice decision below must be made with the brand owner (via `/brand-onboarding` and the `designer` skill), then marked locked here.
> Last updated: {{DATE}}

---

## 1. Brand Personality

<!-- One vivid sentence of who the brand "sounds like" (Baydaq's example: "a warm, community-driven local chess friend — not a corporate store, not a stiff academy"), then the is/is-not lists. -->

{{BRAND_NAME}} sounds like **{{PERSONALITY_ONE_LINER}}**.

**We are:**
- {{PERSONALITY_TRAIT_1}}
- {{PERSONALITY_TRAIT_2}}
- {{PERSONALITY_TRAIT_3}}

**We are not:**
- {{ANTI_TRAIT_1}}
- {{ANTI_TRAIT_2}}
- {{ANTI_TRAIT_3}}

---

## 2. Visual Identity

*Colors, typography, and logo are **not yet locked**. Once locked, they become brand constants — no content or template may deviate without the owner updating this file first.*

### 2.1 Color Palette — "{{PALETTE_NAME}}"

<!-- 3–5 colors with roles. Strongest palettes have a story anchoring them to the product or brand world (Baydaq's palette IS its filament colors). Ask the owner what physical/real anchor the palette could trace to. -->

| Role | Name | Hex | Source / story |
|---|---|---|---|
| **Primary** | {{PRIMARY_COLOR_NAME}} | `{{PRIMARY_HEX}}` | {{PRIMARY_SOURCE}} |
| **Secondary / Accent** | {{SECONDARY_COLOR_NAME}} | `{{SECONDARY_HEX}}` | {{SECONDARY_SOURCE}} |
| Background | {{BG_COLOR_NAME}} | `{{BG_HEX}}` | {{BG_SOURCE}} |
| Text / Dark Accent | {{TEXT_COLOR_NAME}} | `{{TEXT_HEX}}` | {{TEXT_SOURCE}} |

**Usage notes:**
- Primary → CTAs, accents, highlights, the single emphasis per layout.
- Secondary → supporting surfaces, secondary highlights.
- Background → the dominant ground; decide deliberately between warm/cool/neutral.
- {{PALETTE_USAGE_NOTE}} <!-- what to avoid, e.g., "no neon/oversaturated colors — the palette should feel handmade and premium" -->

### 2.2 Typography

<!-- Two roles minimum: headline + body. Consider script/language support, licensing (Google Fonts = free), and whether the pairing is matched (same family) or contrast (display + clean sans). -->

| Role | Typeface | Style | Source / license |
|---|---|---|---|
| **Headlines** | {{HEADLINE_FONT}} | {{HEADLINE_FONT_STYLE}} | {{HEADLINE_FONT_SOURCE}} |
| **Body / Captions** | {{BODY_FONT}} | {{BODY_FONT_STYLE}} | {{BODY_FONT_SOURCE}} |

**Usage notes:**
- Headline font: series names, post titles, personality moments — used sparingly if it's a display face.
- Body font: all captions, UI text, small mobile sizes — readability first.
- Once locked, place the TTF/OTF files in `templates/logo/fonts/` so template/mockup tooling can embed them.

### 2.3 Imagery Style

- **Product photography:** {{PRODUCT_PHOTO_STYLE}}
- **Behind-the-scenes:** {{BTS_STYLE}} <!-- authentic/unpolished is usually welcome here -->
- **Informational graphics:** {{GRAPHICS_STYLE}} <!-- any recurring diagram/graphic type gets a locked spec in the designer skill once defined -->
- **Avoid:** {{IMAGERY_AVOID}} <!-- e.g., generic AI stock imagery disconnected from the actual product -->

### 2.4 Logo (Not Yet Designed)

<!-- Once designed: describe the concept, the canonical mark geometry, the lockups (stacked/horizontal/mark-only), color applications, and background variants. Final files live in templates/logo/. If generated programmatically, keep the generator script alongside so it can be regenerated rather than hand-edited. -->

**Concept:** {{LOGO_CONCEPT}}
**Lockups:** {{LOGO_LOCKUPS}}
**Files:** `templates/logo/` (once produced)

---

## 3. Voice & Tone

### 3.1 Core Voice Principles

1. {{VOICE_PRINCIPLE_1}} <!-- e.g., "talk like a fellow enthusiast, not a retailer" -->
2. {{VOICE_PRINCIPLE_2}} <!-- e.g., "teach without talking down" -->
3. {{VOICE_PRINCIPLE_3}} <!-- e.g., "celebrate the craft" -->
4. {{VOICE_PRINCIPLE_4}} <!-- e.g., "invite participation" -->

### 3.2 Tone by Content Pillar

| Content Type | Tone |
|---|---|
| {{PILLAR_1}} | {{PILLAR_1_TONE}} |
| {{PILLAR_2}} | {{PILLAR_2_TONE}} |
| {{PILLAR_3}} | {{PILLAR_3_TONE}} |

### 3.3 Language Guidelines

**Primary language:** {{PRIMARY_LANGUAGE}}

**Register/dialect usage:** {{DIALECT_POLICY}} <!-- when (if ever) informal register or local dialect is allowed — e.g., only in casual/engagement content, never in instructional terminology -->

**Rule of thumb:**
- {{LANGUAGE_RULE_1}}
- {{LANGUAGE_RULE_2}}

### 3.4 Sample Voice Snippets *(write during onboarding — illustrative, refined once the voice is tested)*

- **{{SERIES_1}} ({{REGISTER}}):** "{{SAMPLE_SNIPPET_1}}"
- **Community prompt ({{REGISTER}}):** "{{SAMPLE_SNIPPET_2}}"

---

## 4. Writing Style Rules

<!-- Micro-rules that settle recurring formatting arguments once. Add to this list as decisions accumulate — each with the decision date. Examples of the kind of rule that belongs here: numeral style, CTA register, emoji policy, capitalization. -->

- **Numerals:** {{NUMERAL_RULE}}
- **Engagement CTA phrasing:** {{CTA_RULE}}
- Keep captions scannable: short paragraphs, line breaks between ideas, emoji used sparingly and purposefully.
- Always use the standardized terminology from `Glossary.md` so terms stay consistent across all series.
- Every educational/informational post ends with an invitation to engage.
- Product mentions should feel earned, not forced — tied to story or craft, never interrupting content with sales language.

---

## 5. Do's and Don'ts

**Do:**
- {{DO_1}}
- {{DO_2}}
- Stay consistent with the locked palette across all visual assets (once locked)

**Don't:**
- {{DONT_1}}
- {{DONT_2}}
- Introduce colors/fonts outside the defined palette without updating this guide first

---

## 6. Open / To Be Defined

- [ ] Brand personality (Section 1)
- [ ] Color palette — lock hexes + the story behind them (Section 2.1)
- [ ] Typography pairing — lock fonts + put files in `templates/logo/fonts/` (Section 2.2)
- [ ] Imagery style rules (Section 2.3)
- [ ] Logo concept + final files (Section 2.4)
- [ ] Voice principles + tone table (Section 3)
- [ ] Language/register rules (Section 3.3)
- [ ] Sample voice snippets, reviewed by a native speaker of the target language
- [ ] Writing style micro-rules: numerals, CTA register, emoji policy (Section 4)
- [ ] Packaging and print style guide (if physical products)
- [ ] Video/Reel style specifics (music style, pacing, on-screen text style)

---

*This guide works alongside `Brand_Context.md`. Update both as decisions are finalized.*
