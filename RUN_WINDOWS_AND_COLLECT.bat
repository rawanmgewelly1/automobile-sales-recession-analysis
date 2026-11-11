@echo off
setlocal EnableExtensions
cd /d "%~dp0"
if errorlevel 1 exit /b 2
if not exist "docs\execution_logs" mkdir "docs\execution_logs"
if not exist "data\historical_automobile_sales.csv" (
  echo ERROR: Original CSV missing at %CD%\data\historical_automobile_sales.csv
  echo Missing CSV > "docs\execution_logs\windows_precheck_error.log"
  exit /b 3
)
call "FINISH_ON_WINDOWS.bat" > "docs\execution_logs\windows_console.log" 2>&1
set "RESULT=%ERRORLEVEL%"
type "docs\execution_logs\windows_console.log"
echo.
echo Result exit code: %RESULT%
echo Verification report: %CD%\docs\local_execution_verification.md
echo Diagnostic package: %CD%\WINDOWS_EXECUTION_DIAGNOSTICS.zip
exit /b %RESULT%
