# Pre-analysis data check, runs ~1 week before the monthly analysis.
# Pure script, no LLM: if no analytics export is waiting AND no platform-analytics MCP is
# connected, pop a visible reminder so the user has time to export insights.
# Project root is resolved from this script's location (.claude\automation\..\..).

$project = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
$brand = Split-Path $project -Leaf
$log = Join-Path $project ".claude\automation\analysis-runs.log"

$hasFiles = @(Get-ChildItem (Join-Path $project "data\analysis") -Include *.xls, *.xlsx, *.csv -Recurse -ErrorAction SilentlyContinue).Count -gt 0

$hasAnalyticsMcp = $false
$mcpFile = Join-Path $project ".mcp.json"
if (Test-Path $mcpFile) {
    $mcp = Get-Content $mcpFile -Raw
    if ($mcp -match "(?i)instagram|meta|graph|tiktok|analytics|insights") { $hasAnalyticsMcp = $true }
}

if ($hasFiles -or $hasAnalyticsMcp) {
    Add-Content $log "[$(Get-Date)] reminder check: data source OK (files=$hasFiles, analyticsMcp=$hasAnalyticsMcp) - no reminder needed"
    exit 0
}

Add-Content $log "[$(Get-Date)] reminder check: NO data source - showing reminder"
Add-Type -AssemblyName System.Windows.Forms
[System.Windows.Forms.MessageBox]::Show(
    "$brand monthly data analysis runs on the 1st.`n`nNo analytics export found in data\analysis\ and no analytics MCP is connected.`n`nExport your platform insights (.xls/.xlsx/.csv) and drop the file into:`n$project\data\analysis\`n`nOtherwise the analysis will be skipped this month.",
    "$brand - analytics data needed",
    [System.Windows.Forms.MessageBoxButtons]::OK,
    [System.Windows.Forms.MessageBoxIcon]::Warning
) | Out-Null
