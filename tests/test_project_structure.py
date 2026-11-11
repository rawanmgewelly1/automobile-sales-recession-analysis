"""Offline repository contract tests; no dataset or synthetic analysis is implied."""
from pathlib import Path
import ast
import json
import nbformat
ROOT = Path(__file__).resolve().parents[1]

def test_nine_visualization_cells_and_labels():
    nb = nbformat.read(ROOT/'notebooks/automobile_sales_analysis.ipynb', as_version=4)
    nbformat.validate(nb)
    source = '\n'.join(c.source for c in nb.cells if c.cell_type == 'code')
    for key in ('sns.barplot(', 'plt.subplots(', 'ax.scatter(', 'ax.pie(', 'sns.lineplot(', 'Seasonality_Weight', 'unemployment_rate'):
        assert key in source
    assert source.count('plt.show()') >= 9

def test_screenshot_automation_waits_for_svg_titles():
    src = (ROOT/'scripts/capture_screenshots.py').read_text()
    ast.parse(src)
    assert '.gtitle' in src
    assert 'to_contain_text' in src
    assert 'full_page=True' in src

def test_reproducible_scripts_present():
    for path in ('scripts/fetch_dataset.py','scripts/check_dataset.py','scripts/analyze_answers.py',
                 'scripts/execute_notebook.py','scripts/finish_on_windows.py','FINISH_ON_WINDOWS.bat'):
        assert (ROOT/path).is_file()

def test_dataset_not_committed_in_git():
    assert 'data/*.csv' in (ROOT/'.gitignore').read_text()
