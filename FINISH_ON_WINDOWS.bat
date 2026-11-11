@echo off
setlocal EnableExtensions
cd /d "%~dp0"
if errorlevel 1 (
  echo ERROR: Unable to change to the project directory.
  exit /b 2
)
if not exist "docs\execution_logs" mkdir "docs\execution_logs"
echo Project root: %CD%
echo Dataset path: %CD%\data\historical_automobile_sales.csv
echo Final report: %CD%\docs\local_execution_verification.md
set "PYTHON_EXE=%CD%\.venv\Scripts\python.exe"
if not exist "%PYTHON_EXE%" (
  where py >nul 2>&1
  if not errorlevel 1 (
    py -3 -m venv .venv
  ) else (
    where python >nul 2>&1
    if errorlevel 1 (
      echo ERROR: Python 3 not found. Install Python 3.10 or later.
      exit /b 2
    )
    python -m venv .venv
  )
  if errorlevel 1 (
    echo ERROR: Could not create the Python virtual environment.
    exit /b 2
  )
)
if not exist "%PYTHON_EXE%" (
  echo ERROR: Virtual environment Python is missing: %PYTHON_EXE%
  exit /b 2
)
"%PYTHON_EXE%" scripts\finish_on_windows.py
set "EXIT_CODE=%ERRORLEVEL%"
echo.
echo Report: %CD%\docs\local_execution_verification.md
echo Logs: %CD%\docs\execution_logs\
echo Notebook: %CD%\notebooks\automobile_sales_analysis.ipynb
echo Screenshots: %CD%\screenshots\
if not "%EXIT_CODE%"=="0" (
  echo WORKFLOW FAILED with exit code %EXIT_CODE%. Inspect the report and step logs.
) else (
  echo WORKFLOW PASSED. Inspect the output screenshots and notebook.
)
exit /b %EXIT_CODE%
