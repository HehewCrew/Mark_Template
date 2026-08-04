# {{BRAND_NAME}} SOP — Data Analysis

> Standard Operating Procedure: how analytics exports get turned into insights and a branded dashboard.
> Companion to `SOP.md` (Section 3 monthly review ritual — this SOP is how that review's data work actually gets done) and `SOP_Marketing_Research.md` §1.4 (audience/community listening — this is the deep-dive side of it).
> Input: analytics export files ({{EXPORT_FORMAT}} — e.g., .xls/.xlsx from the platform's insights export), dropped in `data/analysis/` (unprocessed intake — files move to the output folder once analyzed). Output: `presentations/data-analysis/`.
> Executed by the `data-analyzer` skill (`.claude/skills/data-analyzer/SKILL.md`) — this SOP is the canonical process; the skill holds the agent mechanics.
> Last updated: {{DATE}}

---

## 0. Purpose

{{BRAND_NAME}}'s strategy files make claims that only real data can confirm or correct: the growth benchmarks (`context/Marketing_Strategy.md` §2), the priority metrics (§1.4), and the audience-adjustment checkpoint (§4.1). This SOP defines the repeatable workflow that turns raw analytics exports into decisions written back into those files.

---

## 1. Workflow

### Step 1 — Collect the Inputs
Before touching the data, pin down three things (ask the user for whatever is missing):
- **Data source:** what export is this? Column meanings differ per source.
- **Time range:** the period covered, and what it should be compared against (previous period, launch-to-date, the §2 benchmark row for the account's age).
- **Analysis objectives:** what question is being asked — routine monthly review? the §4.1 audience checkpoint? a specific anomaly? Objectives decide which metrics matter this pass.

### Step 2 — Load the Brand Context
Check the relevant brand files in `context/` as needed for the objective:
- `Marketing_Strategy.md` §1.4 — the metrics that count as success — never rank posts by likes alone.
- §2 — growth benchmark table for pace sanity-checks.
- §1.2–1.3 + §4 — the series/pillar structure and which audience segment each series serves — per-series analysis must map back to these tables.
- §4.1 — the rebalance playbook: what signal justifies shifting series weights.
- `data/content_planner.md` — which episodes actually ran in the period (join key: post date ↔ planner rows).

### Step 3 — Acquire the Data
Parse the provided export file(s) **via an MCP tool when one is connected** (an Excel/spreadsheet MCP server is pre-registered in `.mcp.json` — preferred, per the MCP-first rule used across skills). **Fallback when no MCP is available:** any accessible parsing route — e.g., a Node script with the `xlsx` package in the scratchpad, or converting to CSV first. Never skip the analysis because the preferred tool is absent. Validate before analyzing: row counts, date range actually matches Step 1, no duplicated exports, units understood (exports mix counts, percentages, and durations).

### Step 4 — Analyze
- **Calculate metrics** per post and aggregated per series and per pillar — the priority metrics from §1.4 plus reach, profile visits, follows attributed. Normalize by reach where comparing posts of different exposure (saves *per reach*, not raw saves).
- **Detect trends:** period-over-period movement per series; day-of-week and format patterns; growth vs. the §2 benchmark row.
- **Identify anomalies:** outlier posts (top/bottom performers vs. their series' average), sudden drops/spikes, and posts whose performance contradicts the series' expected audience segment — these are exactly the §4.1 rebalance signals.

### Step 5 — Generate Insights
Summarize in three buckets, each tied to an action:
- **What is working** — series/formats/topics to keep or increase.
- **What is declining** — with a hypothesis (fatigue? wrong slot? format mismatch?), not just the number.
- **Next steps** — concrete, owner-ready actions: rotation weight changes (per §4.1), format shifts, topics to repeat.
Every insight that changes strategy must be written into the owning living doc (a decision isn't real until it's written down).

### Step 6 — Build the Dashboard
Create an **interactive HTML dashboard** using the brand's design system:
- Locked palette and typography per `context/Style_Guide.md` §2, fonts embedded as base64 data URIs per the technique in `.claude/skills/template-generator/references/mockup-page-guide.md`.
- Self-contained single file (no CDN dependencies) so it opens anywhere and can be published as an artifact.
- Content: KPI tiles for the §1.4 priority metrics, per-series comparison chart, trend lines vs. benchmark, top/bottom posts table, and the period's insight summary in plain language.
- Build with the `dataviz` skill's guidance when available (load it before writing chart code).

### Step 7 — Output
Save the deliverables to **`presentations/data-analysis/<YYYY-MM>/`** (kebab-case folder; one subfolder per analysis period):
- `dashboard.html` — the interactive dashboard
- `insights.md` — the Step 5 summary with source export filename(s) and time range logged ("per <export>, period <range>, analyzed <date>")
- the source export file(s) copied alongside, so the analysis is reproducible
Then update the living docs per Step 5 and note the analysis in the monthly review (`SOP.md` §3).

---

## 1.5 Monthly Automation & Data Reminder (optional — set up after onboarding)

Two scheduled jobs can automate the monthly cadence (see `.claude/automation/README.md` for setup):

- **Data reminder — ~1 week before the run:** a plain script (`.claude/automation/analysis-data-reminder.ps1`, no LLM) checks whether `data/analysis/` holds an unprocessed export OR a platform-analytics MCP is connected in `.mcp.json`. If **neither**, it pops a visible Windows notification telling the owner to export insights into `data/analysis/` before the run date. If either source exists, it stays silent.
- **Monthly analysis run:** launches Claude Code headless (`.claude/automation/monthly-analysis.cmd`, prompt: `monthly-analysis-prompt.txt`, log: `analysis-runs.log`) to run this SOP for the month just ended. Data preference order: files in `data/analysis/` → platform MCP → neither = write `presentations/data-analysis/<YYYY-MM>/SKIPPED.md` and stop (never fabricate).
- **Headless gate conversion:** strategy-changing recommendations are never auto-applied — they land in the period's `insights.md` under "Proposed strategy changes — awaiting user decision", for review like the research proposals.
- **If the machine is off** at a scheduled time, that occurrence is skipped — `/day-planner`'s due-work check is the catch-up, and both scripts can be run manually anytime.

## 2. Standards

- **Priority metrics rank posts** — normalized per reach; likes and raw follower count are context, not verdicts.
- **Compare like with like** — different formats and different audience-segment series are different games; compare within series first, across series second.
- **One period is noise, a trend is signal** — don't rebalance the rotation on a single week's data; flag early signals, act on repeated ones.
- **Log the source** — every insight traces to a named export file and date range.

---

## 3. Open / To Be Defined

- [ ] Confirm the platform's actual export format and record the column-name/unit mapping here after the first real export
- [ ] Platform-analytics MCP (live insights) — set up once the account exists (existing brands can evaluate immediately); until then, manual exports are the data path
- [ ] Dashboard template: after the first build, save the HTML skeleton as a reusable starting point (possibly under `templates/`)
- [ ] Decide the analysis cadence (default: monthly, as part of `SOP.md` §3)
- [ ] Decide whether/when to enable the monthly automation (Section 1.5)

---

*Works alongside `SOP.md`, `SOP_Marketing_Research.md`, and `context/Marketing_Strategy.md`. Update as the analysis workflow matures.*
