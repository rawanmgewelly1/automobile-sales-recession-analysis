"""Integration tests run only with official downloaded CSV and Dash installed."""
import importlib.util
from pathlib import Path
import sys
import pytest
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT/'data/historical_automobile_sales.csv'


@pytest.mark.skipif(not CSV.is_file(), reason='Original IBM CSV not present in this runtime')
def test_real_dataset_schema_and_stats():
    sys.path.insert(0,str(ROOT/'scripts'))
    from check_dataset import validate
    result = validate(CSV)
    assert result['rows'] > 0
    assert set(result['recession_counts']) == {'0','1'}


@pytest.mark.skipif(not CSV.is_file() or importlib.util.find_spec('dash') is None, reason='IBM CSV or Dash unavailable')
def test_all_eight_charts_with_original_csv():
    sys.path.insert(0,str(ROOT/'dashboard'))
    from automobile_sales_dashboard import load_data, build_recession_figures, build_yearly_figures
    data=load_data(CSV)
    recession=build_recession_figures(data)
    yearly=build_yearly_figures(data, int(data.Year.max()))
    assert len(recession)==len(yearly)==4
    for fig in recession + yearly:
        assert fig.data and fig.layout.title.text


@pytest.mark.skipif(not CSV.is_file() or importlib.util.find_spec('dash') is None, reason='IBM CSV or Dash unavailable')
def test_dash_callbacks_registered_with_real_data():
    sys.path.insert(0,str(ROOT/'dashboard'))
    from automobile_sales_dashboard import create_app, load_data
    app = create_app(load_data(CSV))
    # Dash serializes multi-output keys with a version-dependent wrapper
    # (e.g. "..select-year.disabled...select-year.value.."). Inspect the
    # actual registered dependencies rather than assuming its string format.
    def output_pairs(output):
        if isinstance(output, (list, tuple)):
            return [pair for item in output for pair in output_pairs(item)]
        return [(output.component_id, output.component_property)]

    callbacks = list(app.callback_map.values())
    expected_year_outputs = {
        ("select-year", "disabled"),
        ("select-year", "value"),
    }
    year_callbacks = [
        entry for entry in callbacks
        if set(output_pairs(entry["output"])) == expected_year_outputs
    ]
    assert len(year_callbacks) == 1, "Expected exactly one callback registering both year outputs"
    year_callback = year_callbacks[0]
    assert year_callback["inputs"] == [
        {"id": "dropdown-statistics", "property": "value"}
    ]
    assert callable(year_callback["callback"])

    # The original update function is decorated by Dash; __wrapped__ exposes
    # the user function without requiring a synthetic request context.
    from inspect import unwrap
    year_function = unwrap(year_callback["callback"])
    latest_year = int(load_data(CSV)["Year"].max())
    assert year_function("Recession Period Statistics") == (True, latest_year)
    assert year_function("Yearly Statistics") == (False, latest_year)

    report_callbacks = [
        entry for entry in callbacks
        if output_pairs(entry["output"]) == [("output-container", "children")]
    ]
    assert len(report_callbacks) == 1
    assert report_callbacks[0]["inputs"] == [
        {"id": "dropdown-statistics", "property": "value"},
        {"id": "select-year", "property": "value"},
    ]
    assert callable(report_callbacks[0]["callback"])
    assert app.server.test_client().get('/').status_code == 200
