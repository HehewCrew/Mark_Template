# .claude/automation/ — Scheduled Headless Runs (optional)

Automates the monthly cadences via Windows Task Scheduler. **Disarmed by default** — nothing runs until you register the tasks. Set up during/after onboarding (`sop/SOP_Marketing_Research.md` §2.5 and `sop/SOP_Data_Analysis.md` §1.5 describe the behavior).

All scripts resolve the project folder from their own location — no paths to edit when the workspace is copied/renamed.

## The jobs

| Task | Script | Suggested schedule | What it does |
|---|---|---|---|
| Monthly marketing research | `monthly-research.cmd` | 1st of month, morning | Headless Claude Code run: monthly research categories; routine findings → docs; strategy proposals → `data/research_reports/<YYYY-MM>-proposals.md` |
| Analysis data reminder | `analysis-data-reminder.ps1` | ~24th of month | No LLM — pops a Windows notification if no analytics export is waiting in `data/analysis/` and no analytics MCP is connected |
| Monthly data analysis | `monthly-analysis.cmd` | 1st of month, morning (after research) | Headless Claude Code run of `sop/SOP_Data_Analysis.md`; never fabricates — writes `SKIPPED.md` if no data |

## Register with Task Scheduler (run once, elevated not required)

```powershell
$auto = "<absolute path to this folder>"
schtasks /Create /TN "{{BRAND_NAME}} Monthly Marketing Research" /TR "`"$auto\monthly-research.cmd`"" /SC MONTHLY /D 1 /ST 09:03
schtasks /Create /TN "{{BRAND_NAME}} Analysis Data Reminder" /TR "powershell -NoProfile -ExecutionPolicy Bypass -File `"$auto\analysis-data-reminder.ps1`"" /SC MONTHLY /D 24 /ST 19:07
schtasks /Create /TN "{{BRAND_NAME}} Monthly Data Analysis" /TR "`"$auto\monthly-analysis.cmd`"" /SC MONTHLY /D 1 /ST 09:33
```

## Rules baked into the prompts

- **Strategy-level changes are never auto-applied** — headless runs write proposals for the owner to review; only owner-confirmed changes land in the strategy docs.
- **Never fabricate data** — no analytics source = skip note, not invented numbers.
- **If the machine is off** at a scheduled time, that occurrence is skipped — `/day-planner`'s due-work/staleness checks are the catch-up, and every script can be run manually anytime.

Run logs: `research-runs.log` / `analysis-runs.log` in this folder.
