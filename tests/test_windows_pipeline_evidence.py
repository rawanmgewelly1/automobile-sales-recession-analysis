"""Offline regression tests for fail-closed Windows reporting."""
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('windows_pipeline', ROOT/'scripts'/'finish_on_windows.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def setup_paths(monkeypatch, tmp_path):
    monkeypatch.setattr(module,'ROOT',tmp_path)
    monkeypatch.setattr(module,'LOGS',tmp_path/'docs'/'execution_logs')
    monkeypatch.setattr(module,'REPORT',tmp_path/'docs'/'local_execution_verification.md')
    monkeypatch.setattr(module,'RESULTS_JSON',tmp_path/'docs'/'execution_logs'/'execution_results.json')

def test_failure_writes_report_and_json(monkeypatch, tmp_path):
    setup_paths(monkeypatch, tmp_path)
    pipeline = module.Pipeline()
    assert pipeline.record('Example failing stage','FAIL','Intentional test failure',exit_code=7) is False
    text=module.REPORT.read_text(encoding='utf-8')
    assert 'NOT READY FOR COURSERA SUBMISSION' in text
    assert 'Intentional test failure' in text
    payload=json.loads(module.RESULTS_JSON.read_text(encoding='utf-8'))
    assert payload['steps'][0]['exit_code']==7

def test_command_exit_code_propagates_to_report(monkeypatch, tmp_path):
    setup_paths(monkeypatch, tmp_path)
    pipeline=module.Pipeline()
    ok=pipeline.command('Failing actual Python subprocess',['-c','import sys; sys.exit(13)'])
    assert not ok and pipeline.fatal
    assert pipeline.records[-1]['exit_code']==13
    assert pipeline.records[-1]['status']=='FAIL'
    assert (module.LOGS/'01_failing_actual_python_subprocess.log').is_file()

def test_blocked_step_is_not_counted_as_success(monkeypatch, tmp_path):
    setup_paths(monkeypatch, tmp_path)
    pipeline=module.Pipeline()
    assert not pipeline.command('Unavailable input',['-c','print(42)'],prerequisite=False)
    assert pipeline.records[-1]['status']=='BLOCKED'
    assert pipeline.fatal

def test_diagnostics_excludes_dataset(monkeypatch, tmp_path):
    (tmp_path/'data').mkdir(); (tmp_path/'data'/'historical_automobile_sales.csv').write_text('not for redistribution')
    (tmp_path/'docs').mkdir(); (tmp_path/'docs'/'local_execution_verification.md').write_text('FAIL')
    from zipfile import ZipFile
    spec2=importlib.util.spec_from_file_location('diagnostics',ROOT/'scripts'/'package_diagnostics.py')
    pkg=importlib.util.module_from_spec(spec2); spec2.loader.exec_module(pkg)
    monkeypatch.setattr(pkg,'ROOT',tmp_path); monkeypatch.setattr(pkg,'DEST',tmp_path/'WINDOWS_EXECUTION_DIAGNOSTICS.zip')
    pkg.main()
    with ZipFile(pkg.DEST) as z:
        assert 'data/historical_automobile_sales.csv' not in z.namelist()
        assert 'docs/local_execution_verification.md' in z.namelist()
