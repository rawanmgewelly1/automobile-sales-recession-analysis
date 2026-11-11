"""Month-label regression tests (isolated fixtures, never assignment data)."""
from pathlib import Path
import ast
import importlib.util
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('month_check', ROOT / 'scripts' / 'check_dataset.py')
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


def test_english_months_and_numeric_months():
    values = pd.Series(['Jan', 'feb', 'March', 'APR', 'December', '12', 8, '  Sep '])
    assert checker.parse_months(values).tolist() == [1, 2, 3, 4, 12, 12, 8, 9]
    assert values.iloc[0] == 'Jan'  # source labels unchanged


@pytest.mark.parametrize('invalid', ['Jna', '13', '0', '', None, '2.5', 'not-a-month'])
def test_invalid_month_is_rejected(invalid):
    with pytest.raises(AssertionError, match='Invalid or missing Month'):
        checker.parse_months(pd.Series(['Jan', invalid]))


def test_schema_accepts_abbreviated_month_names(tmp_path):
    df = pd.DataFrame({
        'Year': [2008, 2009], 'Month': ['Jan', 'Dec'], 'Recession': [0, 1],
        'Vehicle_Type': ['ExecutiveCar', 'SmallFamilyCar'], 'Automobile_Sales': [100, 80],
        'Advertising_Expenditure': [10, 8], 'GDP': [90, 80], 'Price': [10000, 9000],
        'Seasonality_Weight': [0.3, 0.4], 'unemployment_rate': [5.0, 6.0],
    })
    csv = tmp_path / 'original.csv'
    df.to_csv(csv, index=False)
    before = csv.read_bytes()
    report = checker.validate(csv)
    assert report['month_counts'] == {'Jan': 1, 'Dec': 1}
    assert csv.read_bytes() == before


def test_dashboard_load_data_with_names_without_dash_installed(tmp_path):
    """Extract loader for unit test without installing/impersonating Dash."""
    source = (ROOT / 'dashboard' / 'automobile_sales_dashboard.py').read_text(encoding='utf-8')
    tree = ast.parse(source)
    load = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'load_data')
    namespace = {'pd': pd, 'Path': Path, 'REQUIRED_COLUMNS': {
        'Year','Month','Recession','Automobile_Sales','Vehicle_Type',
        'Advertising_Expenditure','unemployment_rate'}, 'parse_months': checker.parse_months, 'DATA_PATH': tmp_path/'missing.csv'}
    exec(compile(ast.Module(body=[load],type_ignores=[]), '<dashboard-loader>', 'exec'), namespace)
    frame = pd.DataFrame({
        'Year':[2020,2020,2020], 'Month':['Dec','Jan','Feb'], 'Recession':[0,1,1],
        'Automobile_Sales':[2,3,4], 'Vehicle_Type':['Sports']*3,
        'Advertising_Expenditure':[1,1,1], 'unemployment_rate':[5,5,5]})
    file = tmp_path/'cars.csv'
    frame.to_csv(file,index=False)
    original = file.read_bytes()
    data = namespace['load_data'](file)
    assert data['Month'].tolist() == ['Dec','Jan','Feb']
    assert data['Month_Number'].tolist() == [12,1,2]
    assert file.read_bytes() == original


def test_notebook_parses_month_names_instead_of_numeric_month():
    import json
    nb = json.loads((ROOT/'notebooks'/'automobile_sales_analysis.ipynb').read_text(encoding='utf-8'))
    source = '\n'.join(''.join(c['source']) for c in nb['cells'] if c['cell_type']=='code')
    assert 'parse_months(df["Month"])' in source
    assert "groupby('Month_Number'" in source
    assert "pd.to_numeric(df['Month']" not in source


def test_yearly_chart_sorts_derived_months_chronologically():
    import plotly.express as px
    source = (ROOT/'dashboard'/'automobile_sales_dashboard.py').read_text(encoding='utf-8')
    tree = ast.parse(source)
    fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name=='build_yearly_figures')
    namespace = {'pd': pd, 'px': px}
    exec(compile(ast.Module(body=[fn],type_ignores=[]), '<yearly-figures>', 'exec'), namespace)
    frame = pd.DataFrame({
        'Year':[2020]*3,'Month':['Dec','Jan','Feb'],'Month_Number':[12,1,2],
        'Vehicle_Type':['Sports']*3,'Automobile_Sales':[12,1,2],
        'Advertising_Expenditure':[3,2,1]})
    figs = namespace['build_yearly_figures'](frame, 2020)
    assert len(figs)==4
    assert list(figs[1].data[0].x)==[1,2,12]
    assert list(figs[1].data[0].y)==[1,2,12]
