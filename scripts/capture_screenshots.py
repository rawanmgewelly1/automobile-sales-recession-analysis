"""Capture authentic full-page Dash screenshots only after Plotly renders all expected charts."""
from pathlib import Path
from playwright.sync_api import sync_playwright, expect
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'screenshots'
URL = 'http://127.0.0.1:8050'
RECESSION_TITLES = [
    'Average Automobile Sales During Recessions',
    'Average Sales by Vehicle Type During Recessions',
    'Recession Advertising Expenditure by Vehicle Type',
    'Unemployment Rate and Sales by Vehicle Type During Recessions',
]
YEARLY_TITLES = [
    'Yearly Average Automobile Sales (All Years)',
    'Monthly Total Automobile Sales',
    'Average Sales by Vehicle Type',
    'Advertising Expenditure by Vehicle Type',
]

def verify_charts(page, titles, year=None):
    """Wait for all actual SVG Plotly titles, not just Dash graph containers."""
    expect(page.locator('.chart-item')).to_have_count(4, timeout=30000)
    svg_titles = page.locator('.chart-item .js-plotly-plot .gtitle')
    expect(svg_titles).to_have_count(4, timeout=45000)
    for idx, expected in enumerate(titles):
        expect(svg_titles.nth(idx)).to_contain_text(expected, timeout=45000)
    if year is not None:
        for idx in (1, 2, 3):
            expect(svg_titles.nth(idx)).to_contain_text(str(year))
    page.wait_for_function("""() => [...document.querySelectorAll('.chart-item .js-plotly-plot')].length === 4 &&
        [...document.querySelectorAll('.chart-item .js-plotly-plot')].every(el => el.querySelector('.main-svg .gtitle') && (el.querySelectorAll('.plot').length > 0 || el.querySelectorAll('.slice').length > 0))""", timeout=45000)

def launch_available_browser(playwright):
    """Use a locally installed browser; never trigger a browser download.

    Playwright-managed Chromium is preferred. On Windows, an already installed
    Microsoft Edge/Google Chrome can be used if the managed download timed out.
    """
    attempts = []
    candidates = [("Playwright Chromium", {})]
    if __import__("sys").platform != "win32" and Path("/usr/bin/chromium").exists():
        candidates.append(("system Chromium", {"executable_path": "/usr/bin/chromium"}))
    if __import__("sys").platform == "win32":
        candidates += [("Microsoft Edge", {"channel": "msedge"}),
                       ("Google Chrome", {"channel": "chrome"})]
    for label, options in candidates:
        try:
            browser = playwright.chromium.launch(headless=True, **options)
            print(f"BROWSER PASS: launched {label}")
            return browser
        except Exception as exc:
            attempts.append(f"{label}: {type(exc).__name__}: {exc}")
    raise RuntimeError("No usable local Playwright Chromium/Edge/Chrome installation. "
                       "Checked without downloading browsers.\n" + "\n".join(attempts))


def capture():
    OUT.mkdir(exist_ok=True)
    with sync_playwright() as p:
        browser = launch_available_browser(p)
        page = browser.new_page(viewport={'width': 1440, 'height': 1024}, device_scale_factor=1)
        errors = []
        page.on('pageerror', lambda exc: errors.append(str(exc)))
        response = page.goto(URL, wait_until='domcontentloaded', timeout=30000)
        assert response and response.status == 200, 'Dashboard HTTP response was not 200'
        expect(page).to_have_title('Automobile Sales Statistics Dashboard')
        year_select = page.locator('#select-year')
        expect(year_select.locator('.Select.is-disabled, .Select--is-disabled')).to_have_count(1, timeout=15000)
        verify_charts(page, RECESSION_TITLES)
        page.screenshot(path=str(OUT / 'RecessionReportgraphs.png'), full_page=True, animations='disabled')

        page.locator('#dropdown-statistics').click()
        page.get_by_text('Yearly Statistics', exact=True).last.click()
        expect(year_select.locator('.Select.is-disabled, .Select--is-disabled')).to_have_count(0, timeout=15000)
        selected = year_select.locator('.Select-value-label').inner_text(timeout=15000).strip()
        assert selected.isdigit(), f'Unexpected year selected: {selected}'
        verify_charts(page, YEARLY_TITLES, year=int(selected))
        # Change to another actual option to prove the year callback updates charts.
        year_select.click()
        available_years = page.locator('.Select-menu-outer .VirtualizedSelectOption, .Select-menu-outer .Select-option')
        expect(available_years.first).to_be_visible(timeout=15000)
        choices = [x.strip() for x in available_years.all_inner_texts() if x.strip().isdigit() and x.strip() != selected]
        if choices:
            replacement = choices[0]
            page.locator('.Select-menu-outer .VirtualizedSelectOption, .Select-menu-outer .Select-option').get_by_text(replacement, exact=True).first.click()
            verify_charts(page, YEARLY_TITLES, year=int(replacement))
            selected = replacement
        page.screenshot(path=str(OUT / 'YearlyReportgraphs.png'), full_page=True, animations='disabled')
        assert not errors, 'Browser JavaScript errors: ' + repr(errors)
        browser.close()
    for name in ('RecessionReportgraphs.png', 'YearlyReportgraphs.png'):
        with Image.open(OUT / name) as im:
            im.verify()
        with Image.open(OUT / name) as im:
            assert im.size[0] >= 1100 and im.size[1] >= 1200, (name, im.size)
        print('PASS authentic browser capture:', name)

if __name__ == '__main__':
    capture()
