---
name: marketing-research-agent
description: Conduct structured marketing research and formulate a marketing strategy for any brand. Use when the user asks for competitor/market research, platform or trend analysis, audience insights, pricing benchmarks, historical/cultural fact-checking of content claims, keyword/SEO research, or a full marketing strategy. Follows a six-category research process with strict sourcing standards; research-tool usage is MCP-first with built-in fallback.
---

# Marketing Research Agent

Runs a complete marketing research pass for a brand and turns the findings into (or updates) a written marketing strategy. The process below is the canonical sequence — follow the steps in order and do not skip the intake or the write-down step.

**Core rule:** research findings always update a written, living document. A research session that isn't written down didn't happen.

## Step 0 — Brand Intake (always run first)

Before any research:

1. **Locate the brand's context docs.** Check `CLAUDE.md` and any `context/`, `docs/`, or brand-strategy Markdown files in the workspace. Read whatever exists on: brand identity/positioning, products & pricing, target audience, competitors, content strategy, and voice/style rules.
2. **Identify missing campaign-critical information.** At minimum, check whether the docs define:
   - Paid advertising strategy and budget
   - Partnership strategy (who to partner with, on what terms)
   - Audience demographics (age range, casual-vs-competitive or equivalent segmentation)
   - Trusted reference sources for fact-checking claims
   - Product pricing (locked vs. pending)
   - Primary platform(s) and posting cadence
3. **Ask the user to fill the gaps.** Anything missing from the list above must be put to the user as explicit questions (use AskUserQuestion when available) before research begins. If the user defers an answer, record it as an open item in the output doc — do not invent a value.
4. **Confirm scope.** Ask which research categories (Section 2) the user wants this session, unless they already specified.

## Step 1 — Research Tooling Rule

**MCP-first:** if any MCP research/search/scraping tool is connected (e.g., a search, crawler, or data MCP server), use it as the primary research tool and use it regularly throughout every category below.

**Fallback:** if no MCP tool is available, use any accessible built-in research tool (WebSearch, WebFetch). Never skip research because the preferred tool is absent.

## Step 2 — The Six Research Categories

Run the categories in scope. For each: gather → verify against the standards in Step 3 → write the finding into the output doc named below.

### 2.1 Competitor & Market Research
- **What:** Track the brand's named competitors and any newly spotted local/regional ones — pricing changes, new product lines, promotions.
- **Cadence:** Monthly light check; immediately if a competitor move is spotted informally (a follower mentions it, a promoted post appears in-feed, etc.).
- **Sources:** Competitor websites/social directly. Never draw conclusions from secondhand mentions without checking the source.
- **Output:** Competitor section of the brand's marketing strategy doc. If pricing shifts meaningfully, also flag it against the brand's product/pricing doc.

### 2.2 Platform & Trend Research
- **What:** Platform algorithm changes, format shifts (e.g., carousel vs. Reel weighting), and niche content trends — what's getting traction across creators in the brand's niche, not just the biggest account.
- **Cadence:** Monthly.
- **Sources:** Official platform/creator communications first; reputable social media marketing sources (Sprout Social, Buffer, Hootsuite-type analyses) as secondary. Cross-check anything that sounds like unverified SEO-blog speculation.
- **Output:** Content-reference or content-strategy section of the marketing strategy doc — only if the shift is significant enough to change format ratios or posting habits.

### 2.3 Historical / Cultural Fact-Checking
- **What:** Verify every historical, cultural, or etymological claim used in storytelling content before it is published.
- **Cadence:** Per-post, every time — not batched. One wrong published claim is a credibility cost worth avoiding entirely.
- **Sources:** Primary/reference sources over forums or unsourced blogs. Cross-check surprising claims across at least two independent sources.
- **Non-negotiable standards:**
  - Never publish a claim that hasn't been checked against an actual source in this pass — no claims from memory alone, even ones that "feel right."
  - Never reproduce source text verbatim — always paraphrase in the brand's own voice.
  - If a claim can't be verified confidently, drop it or soften the framing ("some historians believe...").
- **Output:** Add verified facts to the brand's glossary/fact-bank doc so they're reusable instead of re-researched.

### 2.4 Audience / Community Listening
- **What:** What the actual audience asks, says, and engages with — comment themes, DM questions, which content gets saved/shared most.
- **Cadence:** Light pass weekly; deeper look monthly.
- **Sources:** The brand's own first-party data (platform insights, comments, DMs) — not external research.
- **Output:** Target-audience section of the marketing strategy doc — feeds any planned audience-adjustment checkpoint.

### 2.5 Keyword / Caption SEO Research
- **What:** What terms the target audience actually searches on the platform — informs natural keyword language in captions (platform discovery is increasingly keyword-based).
- **Cadence:** Monthly, or when starting a new content series.
- **Sources:** The platform's own search/suggestion behavior; competitor caption language (for pattern recognition, not copying); the brand's locked terminology glossary if one exists.
- **Output:** Informal — feeds directly into caption drafting. Only update the glossary if a genuinely new standard term emerges.

### 2.6 Pricing Research
- **What:** Ongoing check of comparable product pricing (named competitors and new entrants) until the brand's own pricing is locked, then periodic re-checks.
- **Cadence:** Monthly until pricing is finalized; quarterly after that.
- **Sources:** Same as 2.1.
- **Output:** Pricing section of the brand's product doc.

## Step 3 — Research Standards (apply to every category)

- **Verify before publishing, not after.** Research happens before content goes into production.
- **Prefer primary sources.** Official sites, established references, and direct first-party data outrank secondhand summaries or forum claims.
- **Cross-check surprising claims.** The claims that sound like great hooks are exactly the ones most likely to be wrong internet factoids — check them twice.
- **Always paraphrase, never reproduce source text.** Applies to competitor copy, historical sources, and any other external text.
- **Log the source, even informally.** A one-line note ("per <site>, checked <YYYY-MM>") in the relevant file is enough — the next person or agent shouldn't have to re-verify from scratch.

## Step 4 — Cadence Summary

| Category | Cadence | Output |
|---|---|---|
| Competitor & market | Monthly + as-spotted | Marketing strategy doc (competitors), product doc (pricing flag) |
| Platform & trend | Monthly | Marketing strategy doc (content strategy/reference) |
| Historical/cultural fact-check | Per-post | Glossary / fact-bank doc |
| Audience/community listening | Weekly light, monthly deep | Marketing strategy doc (audience) |
| Keyword/SEO | Monthly or per new series | Caption drafting (informal) |
| Pricing | Monthly until locked, then quarterly | Product doc (pricing) |

## Step 5 — Escalation: When to Update Off-Cycle

Most findings wait for their normal cadence. Update the strategy immediately when:

- A competitor makes a major pricing or product move that directly undercuts or outpositions the brand
- A platform change materially affects the content mix (e.g., a format the brand relies on gets deprioritized)
- An already-published fact turns out to be wrong — correct it publicly and log it so it isn't repeated

## Step 6 — Formulate / Update the Strategy

After research, synthesize findings into the brand's marketing strategy document:

1. If the brand already has a strategy doc, **update it in place** — revise the affected sections, update its `Last updated:` date, and check off any resolved items in its "Open / To Be Defined" list.
2. If none exists, **create one** using the structure in [references/strategy-template.md](references/strategy-template.md).
3. Every claim in the strategy must trace to a research finding from Step 2 or an explicit user answer from Step 0 — never to an unverified assumption. Unresolved questions go in the "Open / To Be Defined" checklist, not in the body as fact.
4. Close the loop with the user: summarize what was researched, what changed in the docs, and which open items still need their input.
