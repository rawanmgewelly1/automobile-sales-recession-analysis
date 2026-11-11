"""Package execution evidence for review, without including the IBM CSV or secrets."""
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile
ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'WINDOWS_EXECUTION_DIAGNOSTICS.zip'
RELATIVE_CANDIDATES = [
    'docs/local_execution_verification.md',
    'docs/q3_vehicle_sales_comparison.md',
    'SUBMISSION_ANSWERS.md',
    'notebooks/automobile_sales_analysis.ipynb',
    'screenshots/RecessionReportgraphs.png',
    'screenshots/YearlyReportgraphs.png',
]

def main():
    reports = list((ROOT / 'docs' / 'execution_logs').glob('*')) if (ROOT / 'docs' / 'execution_logs').exists() else []
    with ZipFile(DEST, 'w', ZIP_DEFLATED) as output:
        for path in [*(ROOT / name for name in RELATIVE_CANDIDATES), *reports]:
            if path.is_file():
                output.write(path, arcname=path.relative_to(ROOT).as_posix())
    print(f'Diagnostics ZIP: {DEST}; IBM CSV deliberately excluded')
if __name__ == '__main__': main()
