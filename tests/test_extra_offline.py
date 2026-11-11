"""Additional offline checks; fixtures never count as actual IBM data verification."""
from pathlib import Path
import ast
import json
import pytest
import pandas as pd
import nbformat
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]

def test_notebook_all_code_parses_and_has_ten_charts():
    nb = nbformat.read(ROOT/'notebooks/automobile_sales_analysis.ipynb',as_version=4)
    nbformat.validate(nb)
    sources=[cell.source for cell in nb.cells if cell.cell_type=='code']
    for src in sources: compile(src, '<notebook cell>', 'exec')
    assert sum('plt.show()' in src for src in sources) >= 10
    assert any('recession_by_type' in src for src in sources)
    assert any("sns.barplot(x='Vehicle_Type', y='Automobile_Sales', hue='Recession', data=df" in src for src in sources)

def test_q3_aliases_and_auto_answer_saving_code_present():
    source=(ROOT/'scripts/analyze_answers.py').read_text()
    compile(source, 'scripts/analyze_answers.py','exec')
    for phrase in ('Smallfamiliycar', 'Supperminicar', 'SUBMISSION_ANSWERS.md', 'q3_vehicle_sales_comparison.md', 'Q3-VERIFIED-BEGIN'):
        assert phrase in source

def test_screenshot_waits_for_both_real_rendered_modes():
    src=(ROOT/'scripts/capture_screenshots.py').read_text()
    assert 'to_have_count(4' in src
    assert 'verify_charts(page, RECESSION_TITLES)' in src
    assert 'verify_charts(page, YEARLY_TITLES' in src
    assert '.Select.is-disabled' in src
    assert 'all_inner_texts()' in src
    assert 'full_page=True' in src

def test_csv_validation_rejects_invalid_data(tmp_path):
    import sys
    sys.path.insert(0,str(ROOT/'scripts'))
    from check_dataset import validate, EXPECTED
    fake={key:1 for key in EXPECTED}
    fake.update(Year=2020,Month=15,Recession=1,Vehicle_Type='Sports',unemployment_rate=6)
    file=tmp_path/'invalid.csv';pd.DataFrame([fake]).to_csv(file,index=False)
    with pytest.raises(AssertionError,match='Both recession statuses|required|Invalid months'):
        validate(file)

def test_git_history_has_two_original_commits():
    import subprocess
    res=subprocess.run(['git','rev-list','--count','HEAD'],cwd=ROOT,text=True,capture_output=True,check=True)
    assert int(res.stdout.strip())>=2

def test_q3_generator_writes_results_from_fixture_only(tmp_path):
    """Exercise the writer on isolated fabricated fixture rows, never used as project findings."""
    import importlib.util
    import sys
    origin = ROOT/'scripts/analyze_answers.py'
    sandbox = tmp_path/'project'
    (sandbox/'scripts').mkdir(parents=True)
    (sandbox/'docs').mkdir()
    (sandbox/'SUBMISSION_ANSWERS.md').write_text('# Fixture-only evaluation\n',encoding='utf-8')
    spec = importlib.util.spec_from_file_location('q3_fixture_only',origin)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    # evaluate() uses __file__ to determine the destination; point that location at the temp project.
    module.__file__=str(sandbox/'scripts/analyze_answers.py')
    rows=[]
    for recession in (0,1):
        for vehicle, non, rec in [('Smallfamiliycar',200,90),('Supperminicar',350,130),('ExecutiveCar',210,50),('Sports',220,40),('Mediumfamilycar',450,190)]:
            rows.append(dict(Year=2005,Month=2,Recession=recession,Vehicle_Type=vehicle,Automobile_Sales=(rec if recession else non),Advertising_Expenditure=12,GDP=100,Price=20000,Seasonality_Weight=1,unemployment_rate=4))
    path=tmp_path/'fixture.csv'
    pd.DataFrame(rows).to_csv(path,index=False)
    module.evaluate(path)
    sheet=(sandbox/'SUBMISSION_ANSWERS.md').read_text()
    assert 'Q3-VERIFIED-BEGIN' in sheet
    assert '1. **TRUE**' in sheet
    assert '2. **TRUE**' in sheet
    assert '4. **TRUE**' in sheet
    assert (sandbox/'docs/q3_vehicle_sales_comparison.md').is_file()
