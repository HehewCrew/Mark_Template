---
name: data-analyzer
description: Analyze {{BRAND_NAME}}'s platform analytics — export files dropped in data/analysis/ (or, once connected, live data via a platform-analytics MCP). Use when the user asks to analyze data, run the monthly review numbers, build a performance dashboard, or interpret an analytics export. Executes sop/SOP_Data_Analysis.md end-to-end.
---

# Data Analyzer

**First action, every run: open and read `sop/SOP_Data_Analysis.md` and follow its Section 1 workflow (Steps 1–7) in order.** That SOP is the canonical process and always wins over this file if they ever disagree — this skill only adds the agent-side mechanics the SOP doesn't specify. Cadence: per the SOP (default monthly, as part of the `sop/SOP.md` §3 review).

## Agent mechanics per SOP step

**SOP Step 1 (Collect the Inputs):**
- The intake folder is **`data/analysis/`** — the user drops unprocessed exports there. Scan it and list what's found (filenames + dates).
- Ask via AskUserQuestion for whatever the filenames/request don't answer: export source/type, time range + comparison baseline, objective.
- Empty folder and no analytics MCP connected → stop and tell the user what to export and where to drop it.

**SOP Step 2 (Brand Context):** read the exact sections the SOP names; additionally join posts to episodes/series via `data/content_planner.md` dates.

**SOP Step 3 (Acquire):**
- **Preferred:** the `excel` MCP server (registered in `.mcp.json`). Load its tools via ToolSearch ("excel sheet read"); list sheets first, then read with pagination.
- **Fallback when the MCP isn't available in-session:** Node `xlsx` package in the scratchpad (`npm install xlsx`, convert to JSON), or ask the user for a CSV export. Never skip the analysis because the preferred tool is absent.
- **Once a platform-analytics MCP is connected** (open item in the SOP): pull account/media insights live for ad-hoc questions; file exports remain the audited record for the monthly run.

**SOP Steps 4–5 (Analyze, Insights):** apply the SOP's standards (Section 2) strictly — priority metrics normalized per reach, compare within series first, one period is noise. Present insights in chat as tables + short prose. **Gate: strategy-changing conclusions (rotation weights, format ratios, audience rebalance) need user confirmation via AskUserQuestion before any living doc is edited** — then write the confirmed decision into the owning doc and tick related open items.

**SOP Step 6 (Dashboard):** self-contained HTML per the SOP's design rules; fonts embedded base64 via the technique in `.claude/skills/template-generator/references/mockup-page-guide.md`; **load the `dataviz` skill before writing chart code**; publish via Artifact for immediate viewing.

**SOP Step 7 (Output):** write to `presentations/data-analysis/<YYYY-MM>/` exactly as the SOP specifies, then **move the processed export out of `data/analysis/` into that output folder** — the intake folder holds only unprocessed files.

## Maintenance rule

If the analysis reveals the SOP itself needs adjusting (new export columns, changed units, a better workflow step), update `sop/SOP_Data_Analysis.md` — including its column-mapping open item after the first real export — not this file. This skill changes only when the *agent mechanics* (tools, folders) change.
