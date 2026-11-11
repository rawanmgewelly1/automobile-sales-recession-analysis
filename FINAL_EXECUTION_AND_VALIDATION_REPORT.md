# Windows completion recovery — execution and validation

**Decision: NOT READY FOR COURSERA SUBMISSION** (until a genuine Windows/data run passes).

## Why the prior Windows run could appear successful without outputs

Inspected the uploaded original `FINISH_ON_WINDOWS.bat`, `scripts/finish_on_windows.py`, and `scripts/finalize_validation.py`. The prior Python orchestration used `subprocess.run(..., check=True)` and placed `scripts/finalize_validation.py` **at the end** of the pipeline, after pip installation, CSV acquisition, notebook execution, tests, browser launch, and screenshot capture. A nonzero exit from **any earlier step** prevented the report generator from running. The batch file only showed a console message and exited: it did **not** save a stage-by-stage report or diagnostics. The historical cause on the user's Windows computer cannot be identified without that computer's logs, which the previous runner did not reliably preserve. This is a **confirmed control-flow defect**, not evidence of what failed on that particular Windows run.

## Targeted recovery changes

1. `FINISH_ON_WINDOWS.bat`: reliably uses the virtual environment's **absolute Python executable**; prints the CSV, notebook, screenshot, and report paths; propagates the runner exit code.
2. `scripts/finish_on_windows.py`: tracks each stage's status and subprocess exit code in `docs/execution_logs/`, writes `docs/local_execution_verification.md` and JSON evidence after every stage **and in a finalizer**, even on failure, and returns nonzero if required steps fail.
3. Dataset and notebook tasks can proceed independently when Dash dependencies are unavailable. A valid existing local CSV is retained; network download is attempted only if missing.
4. `scripts/package_diagnostics.py`: automatically produces `WINDOWS_EXECUTION_DIAGNOSTICS.zip` containing the notebook, answer sheet, generated screenshots if present, Q3 comparison if produced, and all step logs and report, **excluding** the original dataset.
5. New `tests/test_windows_pipeline_evidence.py` includes regression tests for failed subprocess exit codes, blocked steps, report creation, and exclusion of CSV from the diagnostics.
6. `.gitignore` excludes machine-specific logs, execution reports, diagnostics archives and the CSV from public Git commits.

## Tests actually executed in the isolated Linux runtime

```text
python -m pytest -q -rs
23 passed, 5 skipped, 0 failed

python -m compileall -q scripts dashboard tests
Exit code 0
```

A **real failed-pipeline recovery test** was also performed using `PIP_NO_INDEX=1 python scripts/finish_on_windows.py`. The script exited **1**, logged DNS failures for the official IBM CSV and an unavailable Dash distribution, and **created** `docs/local_execution_verification.md`, `docs/execution_logs/execution_results.json`, per-step logs, and `WINDOWS_EXECUTION_DIAGNOSTICS.zip`. This verifies fail-closed *Linux* behavior only, not compatibility with Windows.

## Acceptance evidence

| Requirement | Status | Evidence |
|---|---|---|
| Existing project and Git history | PASS | Source ZIP copied before edits; previous commit ancestry retained |
| Local dataset `data/historical_automobile_sales.csv` | BLOCKED | User reports it exists on their Windows PC, but it is not present in the uploaded ZIP or accessible to this runtime |
| Notebook output with nine real charts | NOT VERIFIED | Notebook lacks execution counts and real data outputs |
| Q3 answers based on IBM dataset | NOT VERIFIED | Dataset unavailable here; script ready for Windows run |
| Q7 source behavior | PASS (source only) | Current code enables year selection in Yearly, disables it in Recession, resets year value on report switch; original starter/real browser not verified |
| Dash installed and dashboard started | BLOCKED | `dash` unavailable here; no access to the user's Windows session |
| Genuine Q6/Q8 browser screenshots | NOT VERIFIED | No real screenshots generated or fabricated |
| Offline automated tests | PASS | 23 passed; 5 skipped in this isolated runtime |
| Windows execution script | NOT VERIFIED ON WINDOWS | Inspected and corrected; no Windows executor connected |
| Failure-path logging and report generation | PASS ON LINUX | Exit code 1 with generated report, JSON evidence and diagnostic ZIP |
| GitHub publication | NOT PERFORMED | No authorized remote or push |

## Remaining action on the user's Windows computer

The CSV is already at `data/historical_automobile_sales.csv` beside the runner. Replace the existing source files with the updated ZIP while **preserving that `data/` folder** (do not delete/recreate it). Double-click `FINISH_ON_WINDOWS.bat` or run it from Command Prompt in the project root. The runner will not overwrite a valid local CSV. It writes the report **even when a stage fails** and produces:

- `docs/local_execution_verification.md`
- `docs/execution_logs/execution_results.json` and step `.log` files
- `WINDOWS_EXECUTION_DIAGNOSTICS.zip`

If the run fails, upload **one file**, `WINDOWS_EXECUTION_DIAGNOSTICS.zip`, for diagnosis. It intentionally excludes the original IBM CSV. If it succeeds, the same archive includes the executed notebook and genuine screenshots for independent checking, while the two PNGs remain in `screenshots/`.

**Do not submit until the real Windows report confirms notebook execution, both screenshots, dashboard browser verification and required integration tests.**
