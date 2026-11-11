# Final execution and validation report

**Date:** 2026-11-11  
**Input:** User-uploaded `automobile-sales-recession-analysis-FINAL (1).zip`  
**Decision:** **NOT READY FOR SUBMISSION**

## Source preservation and inspection

- Extracted and inspected the supplied repository, including the existing 13-code-cell notebook, Dash application, tests, `FINISH_ON_WINDOWS.bat`, dependencies, README, submissions and docs.
- Made a byte-for-byte backup of the uploaded ZIP **outside** this repository, before edits.
- Preserved existing Git commit ancestry (`7100a9a`, `f155d72`, `7d62832`). No remote is configured.
- The IBM/Coursera original starter notebooks and complete authenticated evaluation rubric **were not included in the ZIP**. Public descriptions confirm the IBM historical automobile dataset and dashboard assignment but are not a substitute for the original in-course starter and exact evaluation screen.
- The notebook includes the nine custom-brief charts plus a separate historic-rubric Task 1.2 vehicle-type comparison. Neither was removed. Exact grader matching of the extra chart is not established.

## A. Assignment compliance

| Question | Status | Evidence |
|---|---|---|
| Q1: notebook | **BLOCKED** | `notebooks/automobile_sales_analysis.ipynb` exists, 13 code cells; clean-kernel attempt fails in first code cell due to missing official CSV; no execution counts or saved rendered charts. |
| Q2: Seaborn grouped bar | **VERIFIED (source)** | Notebook preserves `sns.barplot(x='Vehicle_Type', y='Automobile_Sales', hue='Recession', data=df)` and matching imports. |
| Q3: five vehicle-type statements | **NOT VERIFIED** | `scripts/analyze_answers.py` calculates original-data means if CSV exists. No actual CSV means or answers are asserted. |
| Q4: Dash script | **BLOCKED** | `dashboard/automobile_sales_dashboard.py` source exists; cannot launch: `ModuleNotFoundError: No module named 'dash'`. |
| Q5: html.Div | **VERIFIED (concept/code)** | Dash `html.Div` groups layout components and hosts the graph output container. |
| Q6: recession screenshot | **BLOCKED** | No authentic `screenshots/RecessionReportgraphs.png`; actual app never started. |
| Q7: callback | **VERIFIED (implemented source only)** | Implemented `select-year.disabled` toggles by report and `select-year.value` resets to the latest dataset year on report switches. For the provided five statements, #2 and #5 match code; #1, #3 (both dropdowns reset), and #4 do not. Original course starter callback and live browser behavior are **not verified**. |
| Q8: yearly screenshot | **BLOCKED** | No authentic `screenshots/YearlyReportgraphs.png`; actual app never started. |
| Q9: ad distribution | **VERIFIED (source)** | `px.pie` produces recession advertising distribution by vehicle type, rendered in `dcc.Graph`. |
| Nine Part 1 charts | **NOT VERIFIED (runtime)** | Implementations are present; source CSV and genuine cell outputs absent. |
| Eight Part 2 charts | **NOT VERIFIED (runtime)** | Four recession and four yearly Plotly builders exist. Fixture-based tests are not original-data evidence. |

## B. Execution evidence

| Component | Execution status | Evidence |
|---|---|---|
| IBM dataset retrieval | **BLOCKED** | Python urllib retried 3 times: `[Errno -3] Temporary failure in name resolution`. `curl -I` returned exit code 6 (`Could not resolve host`). GitHub Raw and PyPI DNS queries also failed. |
| Original dataset schema | **NOT VERIFIED** | `data/historical_automobile_sales.csv` absent. No replacement or synthetic data used. |
| Notebook full execution | **FAIL (attempted)** | `python scripts/execute_notebook.py` raised `FileNotFoundError: Official IBM dataset missing` in first data-loading cell; notebook remained unmodified/unexecuted. |
| Dash dependency installation | **BLOCKED** | `python -m pip install 'dash>=2.16,<4' --disable-pip-version-check --timeout 3 --retries 0` returned `No matching distribution found` because the package source is inaccessible. |
| Dashboard actual launch | **FAIL (attempted)** | `python dashboard/automobile_sales_dashboard.py`: `ModuleNotFoundError: No module named 'dash'`. |
| Real browser tests | **BLOCKED** | No running Dash app or original dataset; no GUI claim. |
| Q6 screenshot | **BLOCKED** | Not generated; a mock image has not been substituted. |
| Q8 screenshot | **BLOCKED** | Not generated; a mock image has not been substituted. |
| Unit/static tests | **PASS** | `python -m pytest -q -rs`: **19 passed, 5 skipped, 0 failed**, Python 3.13.5. |
| Integration tests | **SKIPPED (3)** | Depend on official CSV and Dash. |
| Screenshot checks | **SKIPPED (2)** | Depend on genuine rendered PNGs. |
| Windows batch | **NOT EXECUTED** | This is a Linux Python runtime. `FINISH_ON_WINDOWS.bat` was inspected, but Windows compatibility is not claimed. |
| GitHub publication | **NOT DONE** | No configured remote or authorized authenticated publication target. |

### Commands and actual outcomes

```text
python -m pytest -q -rs
...................sssss   [100%]
19 passed, 5 skipped in 3.06s

python scripts/fetch_dataset.py
RuntimeError: ... attempt 1/2/3: URLError: [Errno -3] Temporary failure in name resolution

curl -I <official IBM CSV>
curl: (6) Could not resolve host: cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud

python scripts/execute_notebook.py
FileNotFoundError: Official IBM dataset missing.

python dashboard/automobile_sales_dashboard.py
ModuleNotFoundError: No module named 'dash'

python -m pip install 'dash>=2.16,<4' --disable-pip-version-check --timeout 3 --retries 0
ERROR: No matching distribution found for dash<4,>=2.16
```

Detailed error output is preserved under `docs/evidence/`. The PyPI failure is an environment-access limitation, not proof Dash lacks Python compatibility.

## C. Targeted changes made in this run

1. `scripts/fetch_dataset.py`: now checks any existing local file, verifies non-HTML CSV structure and required columns, logs its SHA-256, and **does not overwrite it or perform a network download** when valid. This prevents Windows completion from failing unnecessarily when a legitimate IBM CSV was already obtained locally. A matching schema alone does not prove IBM provenance.
2. `tests/test_dataset_download_safety.py`: four regression tests verify HTML rejection, missing columns rejection, preservation of existing CSV, and no silent replacement of invalid files. Test fixtures are confined to `tmp_path` and never included in the dataset or analysis.
3. Updated README to describe this run's verifiable status and the offline-data recovery path.
4. Preserved all prior analysis, dashboard, screenshot automation and unit tests. No charts, grades, or dataset rows fabricated.

## D. Submission blockers and smallest manual action

**Submission is blocked by original-data and Dash package access.** On an Internet-connected Windows machine: unzip this repository, run `FINISH_ON_WINDOWS.bat` from the root. It installs dependencies, fetches the official CSV, validates it, computes Q3, executes/saves the notebook, launches Dash, verifies titles in a browser, takes real Q6/Q8 screenshots, and validates artifacts. This batch has **not** been executed on Windows here.

If the IBM download endpoint is unavailable but the user has the genuine CSV from the course, place it at `data/historical_automobile_sales.csv` before running the same batch. The corrected downloader validates and retains it. After execution, inspect `docs/local_execution_verification.md` and the two PNGs; share the generated report and any failure log to verify acceptance. To match the live Coursera question options exactly, compare the in-course rubric/starter on the user's account.

Dataset redistribution permissions remain unverified, and `data/*.csv` is ignored by Git to prevent accidental public redistribution. No GitHub push has been attempted.

## E. Final decision

**NOT READY FOR SUBMISSION.** The full data-dependent notebook, running Dash UI, authentic screenshots, Q3 figures, and live Q7 interaction are mandatory unverified outcomes. A clean local Git project and passing offline tests are not equivalent to end-to-end Coursera completion.
