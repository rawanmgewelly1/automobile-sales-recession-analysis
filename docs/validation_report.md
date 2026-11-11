# Latest verification — 11 November 2026, uploaded COMPLETE(1) ZIP

This section records **new attempts against the uploaded archive**, not previous assistant summaries. The project was extracted and a byte-for-byte copy of the uploaded ZIP was saved separately before modifications. The existing Git commit ancestry was retained.

| Acceptance criterion | Status | Evidence |
|---|---|---|
| Original IBM CSV | **BLOCKED** | `scripts/fetch_dataset.py`: three urllib attempts fail `[Errno -3] Temporary failure in name resolution`; `curl`: error 6, could not resolve host; public GitHub raw host also fails DNS. No data fabricated. |
| Dataset schema and numeric verification | **NOT VERIFIED** | CSV absent. Validation code exists but has not executed on IBM records. |
| Notebook code and schema | **PASS (static)** | 13 code cells successfully compiled; nbformat validated. Original nine charts plus supplemental historic-rubric chart included. |
| Notebook fresh-kernel execution | **FAIL (attempted)** | `python scripts/execute_notebook.py` ran but stopped at `FileNotFoundError` for the official CSV. No outputs claimed. |
| Nine required real-data visualizations | **NOT VERIFIED** | Requires official CSV. |
| Dash dependency installation | **BLOCKED** | `pip install dash>=2.16,<4` failed with no matching distribution; package index unreachable. Import is missing. |
| Dash actual startup | **FAIL (attempted)** | `python dashboard/automobile_sales_dashboard.py` raised `ModuleNotFoundError: No module named 'dash'`. |
| Recession and yearly reports in browser | **NOT VERIFIED** | Neither real-data dashboard mode could be launched. |
| Real `RecessionReportgraphs.png` | **NOT GENERATED** | Screenshot script cannot run against missing application. |
| Real `YearlyReportgraphs.png` | **NOT GENERATED** | Same. |
| Q3 category comparison | **NOT VERIFIED on IBM data** | No original CSV. Writer logic independently exercised with a strictly isolated test fixture and confirmed to produce both table and answer file. Its fixture values are not reported as findings. |
| Q7 callback behavior | **PASS (source/unit only)** | Dropdown disabled/value Output declarations and mode-switch source verified. No live-browser claim. Original starter not supplied. |
| Unit and static tests | **PASS (partial)** | `pytest -q -rs`: **15 passed, 5 skipped, 0 failed**. Five skips depend on official data, Dash, or browser screenshots. |
| Git history | **PASS** | Original commits `7100a9a` and `f155d72` retained. |
| GitHub publication | **NOT VERIFIED / NOT DONE** | No authenticated remote configured or authorized destination. |

## Targeted corrections in this execution

- Preserved existing user-requested advertising comparison while adding the original IBM Part 1 Task 1.2 recession vehicle-type line comparison as an additional chart. The publicly visible rubric describes the latter version. All chart results remain runtime-computed.
- Added data-computed printed interpretations below each notebook visualization; no numerical claims embedded in unexecuted outputs.
- Corrected Q3 category spelling aliases and the writer to append a clearly marked data-verification section to `SUBMISSION_ANSWERS.md` only after original CSV validation.
- Strengthened screenshot waits to inspect Plotly SVG titles, render layer presence and a changed year. Disabled-state checks now target React Select control descendants.
- Added independent offline regression tests, a retried official source downloader, and a post-success artifact evidence writer for the Windows completion runner.

**Do not submit Q1/Q4/Q6/Q8 as fully executed artifacts until the documented genuine runtime checks pass.** The final ZIP preserves the code and Git history but does not include a fabricated dataset or fake screenshots.

---

# Validation report — 11 November 2026

## Provenance and backup

Inspected the user-supplied `automobile-sales-recession-analysis(1).zip` (14 original files). A pre-modification copy of the extracted project was created outside the repository at `/mnt/data/automobile-sales-recession-analysis-backup-before-final`. The reconstructed notebook and dashboard were **not** represented as IBM-provided starter code.

## Actual execution and checks

| Criterion | Status | Evidence / exact reason |
|---|---|---|
| Original dataset retrieved | **FAIL** | `python scripts/fetch_dataset.py` → `urllib.error.URLError: [Errno -3] Temporary failure in name resolution`; direct file downloader also failed; web viewer returned unsupported CSV content-type. No data substituted. |
| Dataset integrity, columns, types, ranges | **NOT VERIFIED** | Source CSV absent. `scripts/check_dataset.py` is prepared to inspect it. |
| Part 1 notebook contains 9 task code cells | **PASS (static)** | Task 1.1 through 1.9 code cells inspected, source names retained. |
| Notebook structure valid | **PASS** | `nbformat.validate()` executed without error. |
| Notebook fresh-kernel run with original data | **FAIL** | `python scripts/execute_notebook.py` attempted; first data-loading cell raised `FileNotFoundError: Official IBM dataset missing`. Execution outputs not saved; original notebook remains unexecuted. |
| All nine actual charts generated | **NOT VERIFIED** | Original CSV unavailable. |
| Part 2 Python syntax | **PASS** | `compileall` and AST parsing. |
| Plotly transformations return 4 recession and 4 yearly graphs | **PASS (fixture only)** | `pytest` tests with isolated, explicitly test-only sample rows. Not proof of source-data output. |
| Yearly chart titles change with selected year | **PASS (fixture only)** | Automated test compared 2008 and 2015 fixture-year figure titles. |
| Callback exposes year disabled and year value outputs | **PASS (static)** | AST-based automated test of callback declarations. |
| Actual Dash launch | **FAIL** | `python dashboard/automobile_sales_dashboard.py` → `ModuleNotFoundError: No module named 'dash'`. `pip install dash` was attempted; package index unreachable/no distribution available. |
| Actual browser and dropdown interactivity | **NOT VERIFIED** | Cannot launch app without Dash and source CSV. |
| Recession full-page screenshot | **NOT GENERATED** | Browser capture cannot be performed against nonexistent running app. |
| Yearly full-page screenshot | **NOT GENERATED** | Same blocker. |
| Chart screenshots PNG validation | **NOT VERIFIED** | No authentic screenshots exist. |
| Q2, Q5, Q9 | **PASS (code/concept)** | Syntax and component semantics inspected; actual visual output not verified. |
| Q3 vehicle-type assertions | **NOT VERIFIED** | All five require actual IBM dataset; evaluation script included. |
| Q7 callback statements | **PASS (static)** | Implementation verified; not confirmed in real browser. |
| README, docs, submission sheet | **PASS (present)** | Inspected and revised to avoid unsupported data findings. |
| requirements.txt existence / dependency names | **PASS (static)** | Dependency declarations match project scripts. |
| Clean dependency installation | **FAIL** | `dash` not installable from inaccessible package index. All compatible-version resolutions unverified. |
| Data publication rights | **NOT VERIFIED** | Therefore CSV is ignored by Git and not included in public package. |
| Local Git commit | **PASS** | Git revision documented in repository history. |
| GitHub remote publication | **NOT VERIFIED / NOT DONE** | No confirmed authenticated GitHub connection or authorized target account in current environment. |

## Commands run (real outcomes)

- `python scripts/fetch_dataset.py` — FAIL: DNS resolution error.
- Official IBM URL via web viewer — FAIL: CSV content type unsupported by reader.
- Direct downloader (official source and public mirror attempt) — FAIL: transfer not available; mirror not used.
- `python -m pip install dash --disable-pip-version-check --timeout 8 --retries 0` — FAIL: no package index access.
- `python scripts/execute_notebook.py` — FAIL: missing original CSV, halted in first data cell.
- `python dashboard/automobile_sales_dashboard.py` — FAIL: `dash` module unavailable.
- `python -m pytest -q` — **PASS, 5 tests**, all on source or explicit fixture-only inputs.
- `python -m compileall -q dashboard scripts tests` — PASS.
- `nbformat.validate()` — PASS.

## Completion procedure (when source and package access become available)

```bash
python -m pip install -r requirements.txt
python scripts/fetch_dataset.py
python scripts/check_dataset.py
python scripts/analyze_answers.py
python scripts/execute_notebook.py
python -m pytest -q
python dashboard/automobile_sales_dashboard.py
# In another terminal, after validating the running Dash UI:
python scripts/capture_screenshots.py
```

Do not mark end-to-end criteria PASS until the source notebook runs without exceptions, both report modes are tested in a genuine browser, screenshots are validated, and missing original course question alternatives are checked. Source URL is a known IBM Skills Network dataset endpoint, but permission to redistribute the CSV in a public repo has not been established.


## Follow-up execution against the user-provided final ZIP (11 Nov 2026)

A complete copy of the uploaded `automobile-sales-recession-analysis-final(1).zip` was saved at `source-backup.zip` alongside the extracted repository before editing. The existing `.git` objects and commit history were preserved.

- **Official data: FAIL** — Requests and urllib to IBM host both raised DNS name-resolution errors (`[Errno -3] Temporary failure in name resolution`); attempted a GitHub-hosted copy of the same dataset via `raw.githubusercontent.com`, which also failed DNS; direct artifact downloader failed. No CSV was created or fabricated.
- **Notebook execution: FAIL** — fresh-kernel `scripts/execute_notebook.py` was actually run; it stopped at `FileNotFoundError: Official IBM dataset missing` before any visualizations could be verified.
- **Dash installation: FAIL** — `python -m pip install dash --disable-pip-version-check --timeout 4 --retries 0` returned `No matching distribution found for dash` with unavailable package index. Python version: 3.13.5.
- **Dash startup: FAIL** — actual launch command produced `ModuleNotFoundError: No module named 'dash'`.
- **Recession/yearly E2E, screenshots and Q3: FAIL / NOT VERIFIED** — blocked on source dataset and Dash. No PNGs manufactured.
- **Unit and static tests: PASS** — `python -m pytest -q` returned **9 passed, 5 skipped**. Skipped tests require original dataset/Dash/screenshot files. These passes are *not* a claim of end-to-end completion.
- **Python compilation: PASS** — `python -m compileall -q scripts dashboard tests`.
- **Screenshot automation: IMPROVED, NOT EXECUTED** — checks all four Plotly SVG chart titles for both modes, checks rendered plot layers, verifies selected year, validates PNG dimensions, and fails on browser JS errors. Real browser verification requires running app.
- **Git preservation: PASS** — original Git history preserved, new code committed locally. No remote GitHub publication performed.
- **Windows completion automation: CREATED, NOT EXECUTED HERE** — `FINISH_ON_WINDOWS.bat` starts `scripts/finish_on_windows.py` and performs installation/data checks/notebook execution/tests/browser capture on Windows when networking and dependencies work.
- **Dataset redistribution:** permission unresolved; `data/*.csv` remains excluded from Git. If the local CSV is available after Windows completion, it is for analysis, not automatically for public distribution.

### Final acceptance matrix

| Component | Status | Evidence |
|---|---|---|
| Official dataset | FAIL | DNS blocked official and alternate sources |
| Notebook execution | FAIL | Fresh-kernel run raised FileNotFoundError |
| Nine visualizations | NOT VERIFIED | Notebook did not reach visualization cells |
| Dash installation | FAIL | pip resolver could not access package |
| Dashboard startup | FAIL | ModuleNotFoundError for dash |
| Recession report | NOT VERIFIED | No live Dash runtime |
| Yearly report | NOT VERIFIED | No live Dash runtime |
| Screenshot 1 | FAIL | Real PNG not generated |
| Screenshot 2 | FAIL | Real PNG not generated |
| Q3 verification | NOT VERIFIED | Source CSV absent |
| Q7 verification | PASS (source only) | Callback declarations and branches inspected; original course starter unavailable |
| Automated tests | PASS (partial) | 9 passed, 5 skipped (offline static/unit tests only) |
| GitHub publication | FAIL | No authenticated/authorized remote push |
