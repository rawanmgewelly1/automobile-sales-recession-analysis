"""Regression for an IBM-shaped CSV with numeric fields stored as text.

Test fixtures are never used for assignment findings.
"""
import importlib.util
from pathlib import Path
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('check_dataset', ROOT/'scripts'/'check_dataset.py')
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


def sample():
    return pd.DataFrame({
        'Year': [2008, 2009], 'Month': ['1', '12'], 'Recession': ['0', '1'],
        'Automobile_Sales': ['100', '200'], 'Vehicle_Type': ['SmallFamilyCar', 'ExecutiveCar'],
        'Advertising_Expenditure': ['10.2', '9.3'], 'GDP': ['30', '29'],
        'Price': ['2000', '2500'], 'Seasonality_Weight': ['0.2', '0.4'],
        'unemployment_rate': ['4', '9']})


def test_numeric_text_columns_are_compared_numerically(tmp_path):
    frame = sample()
    csv = tmp_path/'source.csv'
    frame.to_csv(csv, index=False)
    report = checker.validate(csv)
    assert report['rows'] == 2
    assert report['numeric_ranges']['Automobile_Sales']['min'] == 100.0
    assert report['recession_counts'] == {'0': 1, '1': 1}


def test_object_array_unsafe_comparison_regression(tmp_path):
    frame = sample()
    frame.loc[0, 'Automobile_Sales'] = 'not a number'
    csv = tmp_path/'source.csv'
    frame.to_csv(csv, index=False)
    with pytest.raises(AssertionError, match='Invalid or missing numeric data in Automobile_Sales'):
        checker.validate(csv)


def test_negative_numeric_text_is_rejected(tmp_path):
    frame = sample()
    frame.loc[1, 'Advertising_Expenditure'] = '-5'
    csv = tmp_path/'source.csv'
    frame.to_csv(csv, index=False)
    with pytest.raises(AssertionError, match='Negative sales'):
        checker.validate(csv)
