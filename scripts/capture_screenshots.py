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
        [...document.querySelectorAll('.chart-item .js-plotly-plot')].every(el => el.querySelector('.main-svg .gtitle') && el.querySelectorAll('.plot').length > 0)""", timeout=45000)

def capture():
    OUT.mkdir(exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, executable_path='/usr/bin/chromium' if Path('/usr/bin/chromium').exists() else None)
        page = browser.new_page(viewport={'width': 1440, 'height': 1024}, device_scale_factor=1)
        errors = []
        page.on('pageerror', lambda exc: errors.append(str(exc)))
        response = page.goto(URL, wait_until='domcontentloaded', timeout=30000)
        assert response and response.status == 200, 'Dashboard HTTP response was not 200'
        expect(page).to_have_title('Automobile Sales Statistics Dashboard')
        year_select = page.locator('#select-year')
        assert 'is-disabled' in (year_select.get_attribute('class') or '') or year_select.get_attribute('aria-disabled') == 'true'
        verify_charts(page, RECESSION_TITLES)
        page.screenshot(path=str(OUT / 'RecessionReportgraphs.png'), full_page=True, animations='disabled')

        page.locator('#dropdown-statistics').click()
        page.get_by_text('Yearly Statistics', exact=True).last.click()
        assert 'is-disabled' not in (year_select.get_attribute('class') or '') and year_select.get_attribute('aria-disabled') != 'true'
        selected = year_select.locator('.Select-value-label').inner_text(timeout=15000).strip()
        assert selected.isdigit(), f'Unexpected year selected: {selected}'
        verify_charts(page, YEARLY_TITLES, year=int(selected))
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
