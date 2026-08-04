@echo off
rem Monthly marketing research - launched by Windows Task Scheduler.
rem Project root is resolved from this script's location (.claude\automation\..\..).
rem Resolves the Claude Code CLI bundled with the VS Code extension (version-proof glob).

setlocal enabledelayedexpansion
for %%I in ("%~dp0..\..") do set "PROJECT=%%~fI"
set "CLAUDE="

for /d %%D in ("%USERPROFILE%\.vscode\extensions\anthropic.claude-code-*") do (
  if exist "%%D\resources\native-binary\claude.exe" set "CLAUDE=%%D\resources\native-binary\claude.exe"
)

if not defined CLAUDE (
  echo [%date% %time%] ERROR: claude.exe not found under .vscode extensions >> "%PROJECT%\.claude\automation\research-runs.log"
  exit /b 1
)

cd /d "%PROJECT%"
echo [%date% %time%] starting monthly research via %CLAUDE% >> "%PROJECT%\.claude\automation\research-runs.log"
type "%PROJECT%\.claude\automation\monthly-research-prompt.txt" | "%CLAUDE%" -p --permission-mode acceptEdits >> "%PROJECT%\.claude\automation\research-runs.log" 2>&1
echo [%date% %time%] finished with exit code %errorlevel% >> "%PROJECT%\.claude\automation\research-runs.log"
endlocal
