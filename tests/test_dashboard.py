"""Test chart transformations without pretending to execute IBM data.

Sample rows are intentionally fixture-only, never published as analysis.
Full Dash integration tests require the real IBM dataset and Dash dependency.
"""
import ast
from pathlib import Path
import pandas as pd
import plotly.express as px

DASHBOARD = Path(__file__).resolve().parents[1] / 'dashboard' / 'automobile_sales_dashboard.py'
TREE = ast.parse(DASHBOARD.read_text(encoding='utf-8'))

def local_functions():
    # Build chart functions in a small isolated namespace so these tests can
    # run even when `dash` is unavailable in the execution environment.
    functions = ['build_recession_figures', 'build_yearly_figures', 'report_graphs']
    selected = [n for n in TREE.body if isinstance(n, ast.FunctionDef) and n.name in functions]
    source = ast.Module(body=selected, type_ignores=[])
    ns = {'pd': pd, 'px': px}
    exec(compile(source, str(DASHBOARD), 'exec'), ns)
    return ns

def fixture():
    return pd.DataFrame([
        {'Year': y, 'Month': m, 'Recession': r, 'Vehicle_Type': v,
         'Automobile_Sales': s, 'Advertising_Expenditure': a, 'unemployment_rate': u}
        for y,r in [(2008,1),(2015,0)]
        for m in [1,2,3]
        for v,s,a,u in [('ExecutiveCar',100,20,8.1),('SuperMiniCar',200,35,9.1)]
    ])

def test_source_parses():
    assert len(TREE.body) > 0

def test_callback_has_both_year_outputs():
    fn = next(n for n in ast.walk(TREE) if isinstance(n, ast.FunctionDef) and n.name == 'update_input_container')
    callback = ast.unparse(fn.decorator_list[0])
    assert "Output('select-year', 'disabled')" in callback
    assert "Output('select-year', 'value')" in callback

def test_recession_figures_four_real_plotly_charts():
    f = local_functions()['build_recession_figures'](fixture())
    assert len(f) == 4
    assert [v.data[0].type for v in f] == ['scatter', 'bar', 'pie', 'scatter']
    assert all(fig.layout.title.text for fig in f)

def test_yearly_figures_update_year():
    fn = local_functions()['build_yearly_figures']
    assert len(fn(fixture(),2008)) == 4
    assert len(fn(fixture(),2015)) == 4
    assert fn(fixture(),2030) == []
    assert '2008' in fn(fixture(),2008)[1].layout.title.text
    assert '2015' in fn(fixture(),2015)[1].layout.title.text

def test_statistics_switch_uses_four_graphs():
    ns = local_functions()
    assert len(ns['report_graphs']('Recession Period Statistics', None,fixture())) == 4
    assert len(ns['report_graphs']('Yearly Statistics',2015,fixture())) == 4
    assert ns['report_graphs']('Other',2015,fixture()) == []
