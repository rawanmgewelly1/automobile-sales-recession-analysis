"""One-command Windows/portable end-to-end completion: real IBM data, notebook, browser, screenshots, tests."""
import os
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable

def run(*args):
    print('\nRUN:', *args, flush=True)
    subprocess.run([PYTHON, *args], cwd=ROOT, check=True)

def wait_for_server(server, url='http://127.0.0.1:8050', timeout=45):
    end = time.monotonic() + timeout
    while time.monotonic() < end:
        if server.poll() is not None:
            raise RuntimeError(f'Dash process exited with code {server.returncode}')
        try:
            with urllib.request.urlopen(url, timeout=2) as response:
                if response.status == 200:
                    return
        except (OSError, TimeoutError):
            pass
        time.sleep(.5)
    raise TimeoutError('Dash did not respond with HTTP 200')

def main():
    run('-m', 'pip', 'install', '-r', 'requirements.txt')
    run('scripts/fetch_dataset.py')
    run('scripts/check_dataset.py')
    run('scripts/analyze_answers.py')
    run('scripts/execute_notebook.py')
    run('-m', 'pytest', '-q')
    run('-m', 'playwright', 'install', 'chromium')
    logfile = ROOT / 'dashboard-run.log'
    with logfile.open('w', encoding='utf-8') as log:
        server = subprocess.Popen([PYTHON, 'dashboard/automobile_sales_dashboard.py'], cwd=ROOT, stdout=log, stderr=subprocess.STDOUT)
        try:
            wait_for_server(server)
            run('scripts/capture_screenshots.py')
            run('-m', 'pytest', '-q')
            run('scripts/finalize_validation.py')
        finally:
            server.terminate()
            try: server.wait(timeout=8)
            except subprocess.TimeoutExpired: server.kill()
    print('\nCompleted verified execution. Review docs/validation_report.md before publishing.')

if __name__ == '__main__': main()
