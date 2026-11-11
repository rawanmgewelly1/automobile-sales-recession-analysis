# Final execution and validation report — recovery patch

**Verdict: PARTIALLY VERIFIED — EXTERNAL VERIFICATION REQUIRED**

This report describes work **actually executed** in the isolated Linux environment on 2026-11-11. It is not a Windows run and does not claim that the IBM data was executed. The user's Windows drive `E:` is not mounted here.

## Source and artifacts
- Input: `automobile-sales-recession-analysis-WINDOWS-RECOVERY(1).zip`.
- Original Git history preserved; see `git log` in the project.
- Local CSV inside input archive: **absent**. User reports a Windows CSV at `E:\automobile-sales-recession-analysis\data\historical_automobile_sales.csv`, 54,244 bytes, SHA256 `53823dde986f772834aac354357d42789bc852198bea716df5d2dd725923546c`. This hash is user-supplied evidence, not independently matched here.
- Windows logs `05_validate_ibm_csv_schema.log`, `09_automated_tests.log`, `13_final_automated_tests.log`: **absent from uploaded ZIP**. The bundled `execution_results.json` references a prior Linux run (Python 3.13.5), not the Windows 3.14.2 run.

## Root-cause assessment
1. **CSV schema validator** — plausible direct root cause: `scripts/check_dataset.py` performed comparisons on raw object columns after calling `pd.to_numeric` without assigning its result. Pandas may raise from `comp_method_OBJECT_ARRAY` when a text/numeric object is compared with integer `0`. The new validator parses each expected numeric column to a separate numeric frame before range tests, verifies NaNs and recession flags, preserves raw CSV and reports original dtypes and duplicates. Exact Windows expression remains unconfirmed because the complete Windows traceback was not uploaded.
2. **Automated tests** — exact failing Windows assertions are **unknown** without the two Windows pytest logs. Regression tests were added and the available local suite passes, but this does not prove resolution of all Windows failures.
3. **Notebook and Q3** — targeted numeric parsing added; genuine execution not performed without the user-owned CSV.
4. **Windows runner warning** — `return` inside `finally` could suppress an exception; removed without altering cleanup intent.

## Final execution table (this container only)
| Step | Status | Evidence |
|---|---|---|
| Uploaded ZIP extraction | PASS | Archive extracted locally; Git history present |
| Dataset schema with IBM CSV | BLOCKED | CSV not included in source archive |
| Q3 real-data calculations | BLOCKED | No original CSV bytes available here |
| Fresh-kernel notebook execution | BLOCKED | No original CSV bytes available here |
| Required notebook charts | NOT VERIFIED | Notebook retains unexecuted code cells |
| Python compilation | PASS | `python -m compileall -q scripts dashboard tests` exit 0 |
| Automated unit/offline tests | PASS | `python -m pytest -q -rs`: 26 passed, 5 skipped |
| Real-data integration tests | BLOCKED | 3 skipped; original IBM CSV and/or Dash missing |
| Dash HTTP test | BLOCKED | Dash unavailable and CSV absent |
| Browser verification | BLOCKED | Original dataset and running Dash app unavailable |
| Q6/Q8 genuine screenshots | BLOCKED | No actual browser capture possible |
| Windows pipeline | NOT VERIFIED | Cannot access `E:` or execute Windows commands |
| Publication | NOT PERFORMED | No authorized GitHub destination |

## Notebook inspection
- 13 existing code cells in uploaded version.
- 0 executed code cells and 0 real chart outputs in uploaded version.
- No fabricated outputs or execution counters inserted by the recovery patch.

## Testing
- Passed: **26**; failed test assertions: **0**; skipped: **5**.
- Skipped: 3 real-data integration tests and 2 genuine screenshot checks.
- Compilation exit code: **0**.
- No Windows tests claimed.

## Next Windows execution evidence
Run the corrected `FINISH_ON_WINDOWS.bat` from the existing project root while retaining the genuine CSV. The script records each stage in `docs/execution_logs`, writes `docs/local_execution_verification.md` and `docs/execution_logs/execution_results.json`, and creates `WINDOWS_EXECUTION_DIAGNOSTICS.zip` even on failure. Upload the diagnostic ZIP to inspect the original failing expressions and confirm real-data corrections. The full end-to-end acceptance decision depends on that actual run.

## Submission readiness
**PARTIALLY VERIFIED — EXTERNAL VERIFICATION REQUIRED**. A Coursera submission cannot be certified without execution of the original CSV, fresh-kernel notebook, Dash reports and two genuine screenshots.
