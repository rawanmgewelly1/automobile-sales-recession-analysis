"""Offline unit checks for preserving a pre-existing authentic-data file.

Fixtures are test-only CSV bytes, never committed to data/ or reported as IBM findings.
"""
import importlib.util
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('fetch_dataset', ROOT/'scripts'/'fetch_dataset.py')
fetch_dataset = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(fetch_dataset)


def example_csv():
    columns = sorted(fetch_dataset.REQUIRED)
    values = {c: '1' for c in columns}
    values['Year'] = '2008'
    values['Vehicle_Type'] = 'ExampleOnly'
    return (','.join(columns) + '\n' + ','.join(values[c] for c in columns) + '\n').encode()


def test_html_response_rejected():
    with pytest.raises(ValueError, match='HTML'):
        fetch_dataset.validate_csv_bytes(b'<html>404</html>')


def test_missing_columns_rejected():
    with pytest.raises(ValueError, match='columns'):
        fetch_dataset.validate_csv_bytes(b'Year,Automobile_Sales\n2008,100\n')


def test_existing_valid_file_not_overwritten(tmp_path, monkeypatch):
    csv_path = tmp_path/'historical_automobile_sales.csv'
    original = example_csv()
    csv_path.write_bytes(original)
    monkeypatch.setattr(fetch_dataset, 'DEST', csv_path)
    def block_network(*args, **kwargs):
        raise AssertionError('Network must not be used when local CSV exists')
    monkeypatch.setattr(fetch_dataset, 'urlopen', block_network)
    fetch_dataset.fetch()
    assert csv_path.read_bytes() == original


def test_existing_invalid_file_not_silently_replaced(tmp_path, monkeypatch):
    csv_path = tmp_path/'historical_automobile_sales.csv'
    csv_path.write_text('<html>Oops</html>')
    monkeypatch.setattr(fetch_dataset, 'DEST', csv_path)
    with pytest.raises(ValueError, match='HTML'):
        fetch_dataset.fetch()
    assert csv_path.read_text() == '<html>Oops</html>'
