# {{BRAND_NAME}} SOP — Marketing Research

> Standard Operating Procedure: how {{BRAND_NAME}} gathers and validates the information that feeds content, strategy, and product decisions — competitor moves, platform trends, factual claims, audience signals, and pricing.
> Companion to `SOP.md` (content production process). This file is the **input** side; that file is the **output** side.
> Last updated: {{DATE}}

---

## 0. Purpose

Every strategic claim in {{BRAND_NAME}}'s other files (pricing benchmarks, facts, audience assumptions, platform best practices) needs to stay current — none of it should quietly go stale. This SOP defines **what to research, how often, using what sources, and where the findings get written down.**

**Core rule:** research findings always update a living doc — a research session that isn't written down didn't happen, per the Document Maintenance principle in `SOP.md` Section 5.

---

## 1. Research Categories

### 1.1 Competitor & Market Research
- **What:** Track {{COMPETITOR_1}} and any newly spotted local/regional competitors — pricing changes, new product lines, promotions.
- **Cadence:** Monthly light check; immediately if a competitor move is spotted informally.
- **Sources:** Competitor websites/social directly. Avoid drawing conclusions from secondhand mentions without checking the source.
- **Output:** `context/Marketing_Strategy.md` Section 5. If pricing shifts meaningfully, flag it against `context/Products.md` Section 1.3.

### 1.2 Platform & Trend Research
- **What:** {{PRIMARY_PLATFORM}} algorithm changes, format shifts, and general niche content trends (what's getting traction across creators in the niche, not just the biggest account).
- **Cadence:** Monthly.
- **Sources:** Official platform/creator communications first; reputable social media marketing sources (Sprout Social, Buffer, Hootsuite-type analyses) as secondary; cross-check anything that sounds like unverified SEO-blog speculation.
- **Output:** `context/Marketing_Strategy.md` Section 6 or Section 1, if a shift is significant enough to change format ratios or posting habits.

### 1.3 Historical / Cultural / Technical Fact-Checking
- **What:** Verifying any factual claim used in storytelling or educational content before it's published.
- **Cadence:** Per-post, every time — not batched. A single wrong claim published to the community is a credibility cost worth avoiding entirely.
- **Sources:** Prefer primary/reference sources over forums or unsourced blog posts. Cross-check surprising claims across at least two independent sources.
- **Standards (non-negotiable):**
  - Never publish a claim that hasn't been checked against an actual source in this research pass — no claims from memory alone, even ones that "feel right."
  - Never reproduce source text verbatim — always paraphrase in {{BRAND_NAME}}'s own voice.
  - If a claim can't be verified confidently, either drop it or soften the framing ("some sources suggest...").
- **Output:** Add verified facts to `context/Glossary.md` Section 6 so they're reusable across future posts.

### 1.4 Audience / Community Listening
- **What:** What the actual audience is asking, saying, and engaging with — comment themes, DM questions, which series score best on the priority metrics.
- **Cadence:** Light pass weekly (part of `SOP.md` Step 6 monitoring); deeper look monthly (part of `SOP.md` Section 3 monthly review).
- **Sources:** Platform insights, comments, DMs — first-party data, not external research.
- **Output:** `context/Marketing_Strategy.md` Section 4 — feeds the audience-adjustment checkpoint defined there.

### 1.5 Keyword / Caption SEO Research
- **What:** What terms the target audience actually searches on the platform — informs natural keyword language in captions (platform discovery is increasingly keyword-based).
- **Cadence:** Monthly, or when starting a new content series.
- **Sources:** The platform's own search/suggestion behavior, competitor caption language (pattern recognition, not copying), the locked terminology in `context/Glossary.md`.
- **Output:** Informal — feeds directly into caption drafting (`SOP.md` Step 2); update the Glossary only if a genuinely new standard term emerges.

### 1.6 Pricing Research
- **What:** Ongoing check of comparable product pricing until {{BRAND_NAME}}'s own pricing is locked, then periodic re-checks after.
- **Cadence:** Monthly until `Products.md` Section 1.3 pricing is finalized; quarterly after that.
- **Sources:** Same as Section 1.1.
- **Output:** `context/Products.md` Section 1.3.

---

## 2. Research Standards (Apply to All Categories)

- **Verify before publishing, not after.** Research happens *before* content goes into production, not as a retroactive fact-check.
- **Prefer primary sources.** Official sites, established references, and direct first-party data outrank secondhand summaries or forum claims.
- **Cross-check surprising claims.** Anything that sounds like a great hook is exactly the kind of claim most likely to be a wrong internet factoid — check it twice.
- **Always paraphrase, never reproduce source text.** Applies to competitor copy, historical sources, and any other external text.
- **Log the source, even informally.** A one-line note ("per <source>, checked <YYYY-MM>") in the relevant file is enough — the next person (or agent) doesn't have to re-verify from scratch.

---

## 2.5 Monthly Automation (optional — set up after onboarding)

The monthly categories (1.1 competitor, 1.2 platform/trend, 1.5 keyword, 1.6 pricing) can run automatically via a scheduled job that launches Claude Code headless with `.claude/automation/monthly-research.cmd` (prompt: `.claude/automation/monthly-research-prompt.txt`; run log: `.claude/automation/research-runs.log`). See `.claude/automation/README.md` for setup.

- **Routine findings** are written directly into the owning docs per Section 1's output table.
- **Strategy-level proposals are never auto-applied** — they land in `data/research_reports/<YYYY-MM>-proposals.md` for the owner to review and decide; only owner-confirmed changes get written into the strategy docs.
- **If the machine is off at the scheduled time**, the run is skipped — the `/day-planner` skill's staleness check (source logs older than a month) is the catch-up mechanism, and the `.cmd` can be run manually anytime.
- Per-post fact-checking (1.3) and audience listening (1.4) are NOT part of this automation — they stay per-post / tied to first-party data.

## 3. Research Cadence Summary

| Category | Cadence | Output file |
|---|---|---|
| Competitor & market | Monthly + as-spotted | `Marketing_Strategy.md` Sec. 5, `Products.md` Sec. 1.3 |
| Platform & trend | Monthly | `Marketing_Strategy.md` Sec. 1 / 6 |
| Fact-checking | Per-post | `Glossary.md` Sec. 6 |
| Audience/community listening | Weekly light, monthly deep | `Marketing_Strategy.md` Sec. 4 |
| Keyword/SEO | Monthly or per new series | Caption drafting (informal) |
| Pricing | Monthly (until locked), then quarterly | `Products.md` Sec. 1.3 |

---

## 4. Escalation — When Research Should Trigger an Off-Cycle Update

Most research findings wait for their normal cadence, but a few situations justify updating strategy immediately:

- A competitor makes a major pricing or product move that directly undercuts or outpositions {{BRAND_NAME}}
- A platform change materially affects the content mix (e.g., a format the brand relies on gets deprioritized)
- A published fact turns out to be wrong — correct it publicly and note it in the Glossary so it isn't repeated

---

## 5. Open / To Be Defined

- [ ] Name the competitors to track (Section 1.1 — from `Marketing_Strategy.md` Section 5 once defined)
- [ ] Identify 2–3 go-to reference sources for fact-checking in this niche
- [ ] Decide whether/when to enable the monthly automation (Section 2.5)
- [ ] Revisit cadence once posting volume and community size grow

---

*This file works alongside `SOP.md` and the `context/` docs. Update as the research process evolves.*
