@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>&1
if %errorlevel%==0 (py -3 -m venv .venv) else (python -m venv .venv)
if errorlevel 1 (echo Failed to create virtual environment & exit /b 1)
call .venv\Scripts\activate.bat
python scripts\finish_on_windows.py
if errorlevel 1 (echo FAILED - see console output and dashboard-run.log & exit /b 1)
echo VERIFIED STEPS FINISHED - review results
endlocal
