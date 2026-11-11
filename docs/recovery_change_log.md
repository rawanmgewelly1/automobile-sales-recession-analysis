# Recovery change log — 2026-11-11

Source archive: `automobile-sales-recession-analysis-WINDOWS-RECOVERY(1).zip`.

## Inspection
- Existing Git history retained. Base commit: `b0ec09c`.
- The uploaded archive does **not** contain the requested Windows `05_validate_ibm_csv_schema.log`, `09_automated_tests.log`, or `13_final_automated_tests.log`. The bundled logs and results are from a Linux run without the IBM CSV. Accordingly, the exact Windows traceback and pytest failures cannot be independently reconstructed from this archive.
- No IBM CSV is embedded. The Windows CSV exists according to the user's report (54,244 bytes; SHA256 beginning `53823dde...`), but its contents are not accessible in this runtime.

## Narrow fixes
1. `scripts/check_dataset.py`: all numeric-dependent comparisons and ranges now operate on a separately parsed numeric DataFrame. The original CSV is never modified. Previously, `pd.to_numeric(..., errors='coerce')` was called but its result discarded, before `df[['Automobile_Sales', 'Advertising_Expenditure']] < 0` and `Month.between(1,12)` potentially compared mixed object/string values with integers. That is a credible source of the Pandas `comp_method_OBJECT_ARRAY` failure, but the absent Windows log prevents proving the exact failing expression.
2. `notebooks/automobile_sales_analysis.ipynb`: added strict numeric conversion in its original data-loading code cell, preserving all original cells and outputs (none existed). No execution counts or fake outputs were inserted.
3. `scripts/analyze_answers.py`: explicitly parse the two grouping columns as numeric after validating the original CSV.
4. `scripts/finish_on_windows.py`: removed `return` from a `finally` block; it now defers returning code 2 until cleanup completes, avoiding exception suppression. Existing error reports, subprocess exit checks and cleanup retained.
5. `tests/test_csv_numeric_validation.py`: three regression tests cover numeric text values, invalid numeric text, and negative spending.

## Actual environment evidence
- `python -m pytest -q -rs`: **26 passed, 5 skipped, 0 failed**. The skips are authentic-data and browser integration checks.
- `python -m compileall -q scripts dashboard tests`: exit code 0.
- Original IBM CSV runtime, fresh notebook, Dash browser, screenshots, and real-data Q3 remain unverified here.

The supplied Windows computer must run the corrected pipeline to produce environment-specific evidence. Its original CSV must stay in `data/historical_automobile_sales.csv` and should not be overwritten.

## 2026-11-11 — Month names in original CSV

Fixed the month-label parsing mismatch in the validator, notebook loader, and Dash loader. Preserved original Month labels and added numeric Month_Number only for chart ordering. Added regression tests and documented Linux-only verification in `docs/MONTH_FIX_LOCAL_VERIFICATION.md`. The actual Windows CSV and runtime were not available in this execution environment.
