"""Probe installed browser engines without downloading packages or making network calls."""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
from capture_screenshots import launch_available_browser


def main():
    with sync_playwright() as playwright:
        expected = Path(playwright.chromium.executable_path)
        print(f"Managed Chromium expected path: {expected}")
        print(f"Managed Chromium installed: {expected.is_file()}")
        try:
            browser = launch_available_browser(playwright)
            try:
                page = browser.new_page()
                page.goto("about:blank")
                print("PASS: locally installed browser can launch and render pages")
            finally:
                browser.close()
            return 0
        except Exception as exc:
            print(f"BLOCKED: {exc}", file=sys.stderr)
            print("To install managed Chromium if no installed Edge/Chrome works:\n"
                  "  .venv\\Scripts\\python.exe -m playwright install chromium", file=sys.stderr)
            return 2


if __name__ == "__main__":
    raise SystemExit(main())
