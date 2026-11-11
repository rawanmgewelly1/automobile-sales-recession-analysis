# Targeted callback and browser recovery — 2026-11-11

## Scope and provenance

This revision was applied to a working copy extracted from `automobile-sales-recession-analysis-MONTH-FIX.zip`, which was the latest available project package in this session. The Windows `E:\automobile-sales-recession-analysis-BACKUP` drive, its original IBM CSV, its installed Dash package, browser cache, and its execution logs are **not accessible** from this Linux runtime. User-reported Windows results (40 passed, 1 failed, 2 skipped) have not been independently rerun here.

## Root causes and small changes

1. `tests/test_real_data_integration.py`: Dash registers the multi-output callback under a serialized key such as `..select-year.disabled...select-year.value..`. The old test compared this key to an unwrapped string, leading to a false failure. The revised test inspects callback output metadata (`Output.component_id` and `Output.component_property`), the full input dependency list, exact callback multiplicity, and the undecorated year-toggle function in both report modes. The dashboard callback itself is unchanged.
2. `scripts/capture_screenshots.py`: The existing launcher exclusively attempted managed Chromium or a hard-coded Linux executable. The updated launcher probes installed browsers without downloads, trying Playwright-managed Chromium first, system Chromium where present, then Edge and Chrome channels on Windows. Genuine screenshots are still only captured from the running dashboard after verifying all chart titles.
3. `scripts/check_browser_available.py`: New fast local Playwright browser probe (expected cache path, installed status, actual `about:blank` launch), with a nonzero exit code when no usable browser is present.
4. `scripts/finish_on_windows.py`: Replaces the unconditional 420-second Chromium installation stage with a 45-second installed-browser probe, which prevents repeated long downloads and blocks screenshot capture when no real browser is available.

## Executed locally (Linux only)

| Command | Exit | Result |
|---|---:|---|
| `python -m pytest -q -rs` | 0 | 38 passed, 5 skipped, 0 failed |
| `python -m compileall -q scripts dashboard tests` | 0 | Python sources compile |
| `python scripts/check_browser_available.py` | 0 | System `/usr/bin/chromium` launched using Playwright; managed Chromium cache not installed |

The five skipped tests: three needing actual IBM CSV and/or Dash, and two requiring genuine dashboard screenshots. These are **not** counted as passes. The changed callback integration test is included in the skipped set; it could not run against Windows Dash here.

## Windows execution to verify

After copying the targeted changes to the Windows project *without deleting or overwriting* the original CSV or `.git`, run `RUN_WINDOWS_AND_COLLECT.bat` in the project root. It generates `docs/local_execution_verification.md`, `docs/execution_logs/execution_results.json`, individual step logs, and screenshots only when the actual dashboard and browser succeed. If the installed Edge or Chrome channels are unavailable, `scripts/check_browser_available.py` reports a blocker quickly. Then either make a supported Playwright browser install after checking networking or provide the browser diagnostics to diagnose proxy restrictions.

## Not verified / not claimed

- The real-data Windows callback integration test
- Windows browser cache contents or partial Chromium downloads
- Dashboard HTTP/browser interactions in this Linux environment
- Genuine `RecessionReportgraphs.png` and `YearlyReportgraphs.png`
- Windows final test count and Coursera submission readiness

**Final verdict:** NOT VERIFIED FOR COURSERA SUBMISSION until Windows end-to-end evidence is collected.
