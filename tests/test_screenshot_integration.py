"""Screenshot validation runs only after real browser screenshots exist."""
from pathlib import Path
import pytest
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
SHOTS=['RecessionReportgraphs.png','YearlyReportgraphs.png']
@pytest.mark.parametrize('name',SHOTS)
def test_real_browser_png_exists_and_valid(name):
    path=ROOT/'screenshots'/name
    if not path.is_file(): pytest.skip('Authentic live browser screenshot has not been captured')
    with Image.open(path) as img:
        img.verify()
    with Image.open(path) as img:
        assert img.format=='PNG'
        assert img.width>=1100 and img.height>=1200
