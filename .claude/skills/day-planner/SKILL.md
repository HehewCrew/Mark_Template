---
name: day-planner
description: Orchestrate {{BRAND_NAME}}'s agent team for a given day — derive the Day X task list from the planner, SOP cadences, and repo state; get the user's approval; dispatch the specialist agents (content-writer, template-maker, researcher, visual-designer, analyst, presenter); run all user gates in the main thread; then sync shared state and close with a digest. Use when the user says "plan the day", "run day X", "/day-planner <date>", or "what's on for today".
---

# Day Planner — Team Orchestrator

Coordinates the six specialist agents (`.claude/agents/`) through one day of {{BRAND_NAME}} work. **The repo files are the sync medium** — planner, queue, docs, designer log — agents never coordinate peer-to-peer; you (the orchestrator, in the main thread) dispatch them, run every user gate, finalize what they deliberately leave undone, and enforce consistency at the end.

**Prerequisite:** if the workspace still contains onboarding placeholders in the rotation, Style Guide, or planner, route to `/brand-onboarding` before planning a production day.

## Phase 1 — Derive the Day X Task List

Day X = the date the user passed, else today (`Get-Date -Format "yyyy-MM-dd dddd"`). Build the candidate list by checking, in order:

1. **Content due** — `data/content_planner.md`: the row for Day X, plus any unchecked past-due rows (offer catch-up, don't assume). For each: does `data/examples/posts/<series-slug>-template.md` exist? Missing → a template task must precede the content task. Spec-locked graphic slots in the template → rendering is part of the content task (content-writer handles it).
2. **Planner runway** — fewer than 3 planned days remaining after Day X → add a planner-extension task (extend per the planner's Appendix source map + episode log; the extension itself is a main-thread job or a researcher dispatch, then the user approves the new cycle).
3. **Research cadences due** — `sop/SOP_Marketing_Research.md` §3: monthly items (competitor, platform/trend, pricing, keyword). Infer last-done from the docs' source logs ("checked YYYY-MM"); if a month has passed or it's unknown, propose it (user decides in the approval gate).
4. **Analysis due** — the cadence per `sop/SOP_Data_Analysis.md`, OR unprocessed files sitting in `data/analysis/` right now.
5. **Queue hygiene** — files in `social/queue/`: ask the user (at the approval gate) which were actually published → archive tasks (move to `social/<pillar-slug>/<series-slug>/`, update planner links — content-creator Step 8).
6. **User extras** — anything named in the invocation ("...and prepare a deck for the supplier meeting") → map to the right agent.

## Phase 2 — Approval Gate (never skip)

Present the task list as a table: **# · task · owner agent · dependencies · user gates expected**. Then AskUserQuestion: approve all / trim (multiSelect which to run) / add something. Only approved tasks proceed.

## Phase 3 — Dispatch & Gates

- **Dispatch** approved tasks via the Agent tool using the named agent types (`content-writer`, `template-maker`, `researcher`, `visual-designer`, `analyst`, `presenter`). Independent tasks in parallel (background); dependent ones sequenced — template-maker (Mode A) must return and the user must pick a direction before template-maker (Mode B) finalizes, and only then can content-writer run for that series.
  - *Fallback:* if a named agent type isn't registered in this session (agents load on session start), dispatch `subagent_type: claude` and inline the corresponding `.claude/agents/<name>.md` body into the prompt.
- **As each agent returns**, in arrival order:
  1. Relay its report to the user (lead with what matters; keep it scannable).
  2. Run its **pending user decisions** as gates (AskUserQuestion): content review table (content-creator Step 5 format, wording steering expected), template direction picks, strategy confirmations from researcher/analyst, deck reviews.
  3. **Finalize what the agent left undone** (main-thread duties): approved content → export package to `social/queue/` (+ move rendered assets from scratchpad, per `post-package-format.md`) → check off planner episode → bump `Last updated:`; approved template → dispatch Mode B or build it yourself; confirmed strategy changes → write into the owning doc + tick open items; deck design feedback → append to the designer learned-decisions log.

## Phase 4 — Sync & Digest (end of run)

**Consistency sweep** of shared state — fix anything off:
- Every checked planner episode links to an existing `social/queue/` (or archive) file, and vice versa.
- Template canonical (`templates/<pillar-slug>/<slug>/`) ↔ mirror (`data/examples/posts/`) not diverged.
- Decisions made today are written in their owning docs with `Last updated:` bumped and checklist items ticked (a decision isn't real until written down).
- New design preferences captured in the designer learned-decisions log.
- CLAUDE.md directory map still accurate if any structure changed.

**Digest** (final message): ✅ completed (with file links) · ⏸ pending on user · 📝 decisions recorded today (and where) · 📅 preview of Day X+1 (next planner row + anything coming due).

## Rules

- User gates are never delegated to agents and never skipped — approval, reviews, taste picks, strategy changes.
- One content task per series per day; the redundancy guard (planner episode log) is checked before dispatch, not after.
- If an agent reports BLOCKED, resolve the dependency (dispatch the blocker, or ask the user) rather than working around the skill rules.
- Keep the user's standing conventions in force everywhere: the Style Guide's writing micro-rules, the designer learned-decisions log, table-first reviews (artifacts only on request).
