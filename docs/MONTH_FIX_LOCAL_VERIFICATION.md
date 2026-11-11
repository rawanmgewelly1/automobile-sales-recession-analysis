# Month-label repair — actual execution evidence (isolated Linux runtime)

**Verdict:** PARTIALLY VERIFIED — WINDOWS EXECUTION REQUIRED.

This report records commands executed against the uploaded ZIP working copy. It **does not** represent a test run on `E:\automobile-sales-recession-analysis`, which is not accessible from this sandbox. The original dataset is not in the uploaded ZIP; no dataset bytes were replaced or fabricated.

## Root cause and targeted changes

- `scripts/check_dataset.py`: `Month` was included in the numeric validation list; `pd.to_numeric('Jan', errors='coerce')` yielded missing values and raised an assertion. `Month` is now checked separately with `parse_months` which recognizes 12 English abbreviations, full names, and valid numeric month values; rejects invalid/missing values; and returns an integer `Month_Number` view without mutating the original CSV. Other required columns, flags, and numeric checks remain.
- `dashboard/automobile_sales_dashboard.py`: `load_data()` previously used `pd.to_numeric(frame['Month'], errors='raise').astype(int)`, which fails on `Jan`. It now retains `Month` and adds `Month_Number`. The yearly month chart groups and sorts numerically and displays abbreviated month tick labels. A numeric-month compatibility path for existing test fixtures is retained in the yearly graph function.
- `notebooks/automobile_sales_analysis.ipynb`: The initial data-loading cell now validates `Month` through the shared parser rather than coercing it to a number. The seasonality chart uses derived `Month_Number` for chronological ordering. No code cell execution counters or outputs were fabricated.
- `tests/test_named_months.py`: Tests named-month parsing, invalid values, CSV immutability, dashboard loader, notebook parsing, and month chart order. Existing tests remain in place.

## Commands run

All commands were run under the sandbox's Linux Python (not the Windows `.venv`).

| Command | Exit code | Status | Evidence |
|---|---:|---|---|
| `python -m pytest -q -rs` | 0 | PASS: 38 passed, 5 skipped | `docs/month_repair_evidence/pytest_linux.txt` |
| `python -m compileall -q scripts dashboard tests` | 0 | PASS | `docs/month_repair_evidence/compile_linux.txt` |
| `python scripts/check_dataset.py` | 1 | BLOCKED: real CSV absent | `docs/month_repair_evidence/check_dataset_linux.txt` |
| `python scripts/execute_notebook.py` | 1 | BLOCKED: real CSV absent; notebook execution did not finish | `docs/month_repair_evidence/notebook_execution_linux.txt` |
| `python dashboard/automobile_sales_dashboard.py` | 1 | BLOCKED: Dash is not installed in this runtime | `docs/month_repair_evidence/dashboard_start_linux.txt` |

Skipped tests: 3 original-data/Dash integration checks and 2 genuine browser screenshot checks. The focused month-related tests use isolated fixtures, not the IBM CSV.

## Windows acceptance work remaining

Your Windows machine reportedly has the official IBM CSV and installed Dash. After merging the **source changes** into a backup of the project, run `RUN_WINDOWS_AND_COLLECT.bat` at the project root. The existing Windows runner creates `docs/local_execution_verification.md`, `docs/execution_logs/execution_results.json` and `WINDOWS_EXECUTION_DIAGNOSTICS.zip` from actual exit codes. It will attempt the real notebook, dashboard, browser screenshots and previously failing real-data tests. These outputs must be inspected before marking the project submission-ready.

**Important:** The Windows report and JSON are intentionally not created from this isolated Linux test run; they must reflect the real Windows environment rather than simulated evidence.
