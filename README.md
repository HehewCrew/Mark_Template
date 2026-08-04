# Brand Workspace Template

A generic, reusable Claude Code workspace for running a brand's content & marketing operation — derived from the structure proven with Baydaq. Everything brand-specific is a `{{...}}` placeholder; **nothing is decided until the brand owner decides it.**

## How to use it for a new brand

1. **Copy this folder** and rename it to the brand's name (e.g., `workspace/Mark/MyBrand`).
2. **Open it in Claude Code** and run **`/brand-onboarding`** — Claude interviews you through every open decision (brand identity, products, marketing strategy, visual/voice style, terminology, process), always offering concrete researched options, and writes your answers into the docs. It's resumable: stop anytime, continue later.
   - Works for **new brands** (launch mode: every question is a decision to make) and **existing brands** (audit mode: your current identity, assets, pricing, accounts, and history are harvested and documented as locked first — only gaps and things you want to change get the options treatment).
3. Anything you defer stays tracked in each doc's **"Open / To Be Defined"** checklist — Claude will keep surfacing what's still undefined and will refuse to build publishable content on top of undefined fundamentals.
4. Once onboarded, the daily workflow is: **`/day-planner`** (orchestrates the agent team for the day) or the individual skills below.

## What's inside

| Area | Contents |
|---|---|
| `context/` | The 5 living strategy docs: Brand_Context, Products, Marketing_Strategy, Style_Guide, Glossary |
| `sop/` | Process docs: weekly content production, marketing research, data analysis |
| `data/` | Content planner, reference sources, examples/template library, analytics intake, research reports |
| `social/` | Post queue + published-content archive (pillar folders created at onboarding) |
| `templates/` | Logo/fonts + confirmed per-series content templates |
| `presentations/`, `ads/` | Decks & dashboards; future ad creative |
| `.claude/skills/` | brand-onboarding, content-creator, template-generator, marketing-research-agent, data-analyzer, designer, presentator, day-planner |
| `.claude/agents/` | Six specialist subagents orchestrated by /day-planner |
| `.claude/automation/` | Optional scheduled monthly research/analysis runs (disarmed until you register the tasks — see its README) |
| `bot/` | **Optional** Telegram assistant — the workflow on your phone. No model in it: it reports over the repo's files and only executes what you tapped. Set up during onboarding or any time later; nothing depends on it (see `bot/README.md`) |

## Operating principles (baked into every skill)

- **A decision isn't real until it's written down** in the owning doc, with its checklist item ticked.
- **A placeholder is not a decision** — examples in the docs' comments are illustrations, never defaults.
- **Verify before publishing** — every factual claim passes the fact-check gate; always paraphrase, never copy.
- **The owner holds every gate** — approvals, reviews, and taste decisions are never automated away.
