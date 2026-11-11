"""Capture REAL browser screenshots from a running local Dash app.

Requires playwright and Chromium installed; never synthesizes the screenshots.
Run server separately first: python dashboard/automobile_sales_dashboard.py
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'screenshots'
URL = 'http://127.0.0.1:8050'

def capture():
    OUT.mkdir(exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1440, "height": 1000}, device_scale_factor=1)
        errors = []
        page.on('pageerror', lambda exc: errors.append(str(exc)))
        page.goto(URL, wait_until='networkidle', timeout=30000)
        assert page.title() == 'Automobile Sales Statistics Dashboard'
        assert 'is-disabled' in (page.locator('#select-year').get_attribute('class') or '') or page.locator('#select-year').get_attribute('aria-disabled') == 'true'
        assert page.locator('.chart-item').count() == 4
        page.screenshot(path=str(OUT / 'RecessionReportgraphs.png'), full_page=True, animations='disabled')

        page.locator('#dropdown-statistics').click()
        page.get_by_text('Yearly Statistics', exact=True).last.click()
        page.locator('.chart-item').first.wait_for()
        assert page.locator('.chart-item').count() == 4
        assert 'is-disabled' not in (page.locator('#select-year').get_attribute('class') or '')
        page.screenshot(path=str(OUT / 'YearlyReportgraphs.png'), full_page=True, animations='disabled')
        assert not errors, 'Browser JS errors: ' + repr(errors)
        browser.close()
    from PIL import Image
    for name in ['RecessionReportgraphs.png','YearlyReportgraphs.png']:
        with Image.open(OUT / name) as im:
            im.verify()
        print('PASS verified browser capture:', name)

if __name__ == '__main__': capture()
