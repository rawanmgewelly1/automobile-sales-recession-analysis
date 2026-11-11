"""Fail-closed, auditable Windows completion pipeline; never fabricates results.

Every step's exit code and output is persisted. Final evidence is written in finally,
even when dependencies, the real dataset, the notebook, or browser capture fail.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
import platform
import re
import subprocess
import sys
import time
import traceback
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PYTHON = Path(sys.executable).resolve()
LOGS = ROOT / "docs" / "execution_logs"
REPORT = ROOT / "docs" / "local_execution_verification.md"
RESULTS_JSON = LOGS / "execution_results.json"
SCREENSHOTS = ("RecessionReportgraphs.png", "YearlyReportgraphs.png")


def write_text_atomic(path: Path, data: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".writing")
    temporary.write_text(data, encoding="utf-8")
    temporary.replace(path)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def inspect_artifacts():
    """Truthfully describe files in the current run; never create missing outputs."""
    result = {}
    csv = ROOT / "data" / "historical_automobile_sales.csv"
    result["dataset"] = {"exists": csv.is_file()}
    if csv.is_file():
        result["dataset"].update({"size_bytes": csv.stat().st_size, "sha256": sha256(csv)})
    notebook = ROOT / "notebooks" / "automobile_sales_analysis.ipynb"
    result["notebook"] = {"exists": notebook.is_file()}
    if notebook.is_file():
        try:
            parsed = json.loads(notebook.read_text(encoding="utf-8"))
            cells = [c for c in parsed.get("cells", []) if c.get("cell_type") == "code"]
            images = sum(any(o.get("output_type") in ("display_data", "execute_result") and
                             any(x.startswith("image/") for x in o.get("data", {})) for o in c.get("outputs", [])) for c in cells)
            result["notebook"].update({"code_cells": len(cells), "executed_cells": sum(c.get("execution_count") is not None for c in cells),
                                       "code_cells_with_image_outputs": images,
                                       "errors": sum(o.get("output_type") == "error" for c in cells for o in c.get("outputs", []))})
        except (OSError, ValueError, TypeError) as exc:
            result["notebook"]["inspection_error"] = str(exc)
    for name in SCREENSHOTS:
        path = ROOT / "screenshots" / name
        info = {"exists": path.is_file()}
        if path.is_file():
            info.update({"size_bytes": path.stat().st_size, "sha256": sha256(path)})
            try:
                import struct
                with path.open("rb") as f:
                    head = f.read(24)
                if head[:8] != b"\x89PNG\r\n\x1a\n":
                    raise ValueError("Not a PNG")
                w, h = struct.unpack(">II", head[16:24])
                info.update({"width": w, "height": h, "png_header_valid": w > 0 and h > 0})
            except (ValueError, OSError) as exc:
                info["validation_error"] = str(exc)
        result[name] = info
    return result


class Pipeline:
    def __init__(self):
        self.records = []
        self.start = dt.datetime.now(dt.timezone.utc)
        self.fatal = False
        self.server = None
        self.server_log = None
        LOGS.mkdir(parents=True, exist_ok=True)

    def record(self, name, status, detail="", *, exit_code=None, logfile=None):
        item = {"name": name, "status": status, "detail": str(detail), "exit_code": exit_code,
                "log": str(logfile.relative_to(ROOT)) if logfile else None,
                "at_utc": dt.datetime.now(dt.timezone.utc).isoformat()}
        self.records.append(item)
        print(f"[{status}] {name}: {detail}", flush=True)
        self.persist()
        return status == "PASS"

    def persist(self):
        evidence = {"started_utc": self.start.isoformat(), "updated_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
                    "python": str(PYTHON), "python_version": sys.version, "platform": platform.platform(),
                    "root": str(ROOT), "steps": self.records, "artifacts": inspect_artifacts()}
        write_text_atomic(RESULTS_JSON, json.dumps(evidence, indent=2, ensure_ascii=False))
        lines = ["# Local execution verification — recorded results", "",
                 f"Run started UTC: `{self.start.isoformat()}`", f"Project directory: `{ROOT}`",
                 f"Python executable: `{PYTHON}`", f"Python version: `{sys.version.split()[0]}`",
                 f"Platform: `{platform.platform()}`", "",
                 "This is generated from actual command exit codes. A present file is not proof of successful browser execution.", "",
                 "| Step | Status | Exit code | Evidence |", "|---|---|---:|---|"]
        for r in self.records:
            detail = r["detail"].replace("|", "\\|").replace("\n", " ")[:240]
            evidence_path = f'`{r["log"]}`' if r["log"] else "—"
            lines.append(f'| {r["name"]} | **{r["status"]}** | {r["exit_code"] if r["exit_code"] is not None else "—"} | {detail}; {evidence_path} |')
        lines.extend(["", "## Artifact inspection (not a pass assertion)", "", "```json", json.dumps(evidence["artifacts"], indent=2), "```", "",
                      "## Machine-readable evidence", "", "`docs/execution_logs/execution_results.json`", ""])
        verdict = "PASS" if self.records and all(r["status"] == "PASS" for r in self.records) else "NOT READY FOR COURSERA SUBMISSION"
        lines.insert(2, f"**Pipeline verdict: {verdict}**")
        write_text_atomic(REPORT, "\n".join(lines))

    def command(self, name, args, *, necessary=True, prerequisite=True, timeout=900, require_no_skips=False):
        if not prerequisite:
            self.record(name, "BLOCKED", "Prerequisite step did not pass; command not executed")
            if necessary: self.fatal = True
            return False
        label = re.sub(r"[^a-zA-Z0-9_-]+", "_", name.lower())
        logfile = LOGS / f"{len(self.records)+1:02d}_{label}.log"
        command = [str(PYTHON)] + list(args)
        print("RUN:", subprocess.list2cmdline(command), flush=True)
        try:
            with logfile.open("w", encoding="utf-8", errors="replace") as log:
                log.write("Command: " + subprocess.list2cmdline(command) + "\nWorking directory: " + str(ROOT) + "\n\n")
                log.flush()
                outcome = subprocess.run(command, cwd=ROOT, stdout=log, stderr=subprocess.STDOUT,
                                         timeout=timeout, check=False)
            output = logfile.read_text(encoding="utf-8", errors="replace")
            if outcome.returncode == 0:
                if require_no_skips and re.search(r"\b[1-9]\d* skipped\b", output):
                    self.fatal = True
                    return self.record(name, "FAIL", "Required integration tests were skipped; inspect pytest report", exit_code=0, logfile=logfile)
                return self.record(name, "PASS", "Command completed", exit_code=0, logfile=logfile)
            tail = " ".join(output.splitlines()[-5:])[-450:]
            if necessary: self.fatal = True
            return self.record(name, "FAIL", tail, exit_code=outcome.returncode, logfile=logfile)
        except Exception as exc:
            if necessary: self.fatal = True
            return self.record(name, "FAIL", f"{type(exc).__name__}: {exc}", logfile=logfile)

    def check_server(self, timeout=60):
        end = time.monotonic() + timeout
        url = "http://127.0.0.1:8050/"
        while time.monotonic() < end:
            if self.server.poll() is not None:
                raise RuntimeError(f"Dashboard process exited with code {self.server.returncode}. See {self.server_log}")
            try:
                with urllib.request.urlopen(url, timeout=2) as response:
                    if response.status == 200:
                        return
            except (OSError, TimeoutError):
                pass
            time.sleep(0.7)
        raise TimeoutError(f"Dashboard didn't serve HTTP 200 within {timeout}s; check {self.server_log}")

    def stop_server(self):
        if self.server is not None and self.server.poll() is None:
            self.server.terminate()
            try:
                self.server.wait(timeout=8)
            except subprocess.TimeoutExpired:
                self.server.kill()
                self.server.wait(timeout=8)
        if self.server_log is not None:
            self.server_log.close()

    def execute(self):
        # A locally present, valid CSV is preferred and will not be downloaded again.
        source_ok = self.command("Official CSV availability", ["scripts/fetch_dataset.py"], timeout=120)
        deps_ok = self.command("Install project requirements", ["-m", "pip", "install", "-r", "requirements.txt"], timeout=1200)
        notebook_imports_ok = self.command("Verify notebook imports", ["-c", "import pandas,numpy,matplotlib,seaborn,nbclient,nbformat,ipykernel; print('Notebook packages import successfully')"])
        dash_imports_ok = self.command("Verify dashboard imports", ["-c", "import dash,plotly,pandas,playwright,PIL; print('Dash:',dash.__version__); print('Pandas:',pandas.__version__); print('Plotly:',plotly.__version__)"])
        # Data/notebook work is independent of Dash/browser installation.
        schema_ok = self.command("Validate IBM CSV schema", ["scripts/check_dataset.py"], prerequisite=source_ok and notebook_imports_ok)
        q3_ok = self.command("Verify Q3 from IBM CSV", ["scripts/analyze_answers.py"], prerequisite=schema_ok)
        notebook_ok = self.command("Execute notebook fresh kernel", ["scripts/execute_notebook.py"], prerequisite=schema_ok and notebook_imports_ok, timeout=900)
        self.command("Compile Python source", ["-m", "compileall", "-q", "scripts", "dashboard", "tests"])
        self.command("Automated tests", ["-m", "pytest", "-q", "-rs"], timeout=420)
        browser_ok = False
        if schema_ok and dash_imports_ok:
            self.server_log = (LOGS / "dashboard_server.log").open("w", encoding="utf-8", errors="replace")
            try:
                self.server = subprocess.Popen([str(PYTHON), "dashboard/automobile_sales_dashboard.py"],
                                               cwd=ROOT, stdout=self.server_log, stderr=subprocess.STDOUT)
                self.check_server()
                self.record("Dashboard HTTP startup", "PASS", "http://127.0.0.1:8050/ served HTTP 200", exit_code=0,
                            logfile=LOGS / "dashboard_server.log")
                chromium_ok = self.command("Install Playwright Chromium", ["-m", "playwright", "install", "chromium"], timeout=420)
                # Also attempt browser capture if Chromium installer fails: a system browser may already exist.
                browser_ok = self.command("Browser verification and genuine screenshots", ["scripts/capture_screenshots.py"], timeout=240)
            except Exception as exc:
                self.fatal = True
                self.record("Dashboard HTTP startup", "FAIL", f"{type(exc).__name__}: {exc}", logfile=LOGS / "dashboard_server.log")
                self.record("Browser verification and genuine screenshots", "BLOCKED", "Dashboard startup failed")
            finally:
                self.stop_server()
        else:
            self.fatal = True
            self.record("Dashboard HTTP startup", "BLOCKED", "Dataset and dashboard imports must pass first")
            self.record("Browser verification and genuine screenshots", "BLOCKED", "No validated running dashboard")
        self.command("Verify real notebook and screenshot artifacts", ["scripts/finalize_validation.py"],
                     prerequisite=schema_ok and notebook_ok and q3_ok and browser_ok)
        self.command("Final automated tests", ["-m", "pytest", "-q", "-rs"], timeout=420, require_no_skips=True)


def main():
    pipe = Pipeline()
    try:
        pipe.execute()
    except BaseException as exc:
        pipe.fatal = True
        pipe.record("Pipeline internal exception", "FAIL", "".join(traceback.format_exception_only(type(exc), exc)).strip())
    finally:
        try:
            pipe.stop_server()
            pipe.persist()
            try:
                from package_diagnostics import main as package_evidence
                package_evidence()
            except Exception as package_error:
                print("WARNING: diagnostics ZIP packaging failed:", repr(package_error), file=sys.stderr)
            print("\nVERIFICATION REPORT:", REPORT)
            print("EXECUTION LOGS:", LOGS)
            print("RECESSION SCREENSHOT:", ROOT / "screenshots" / SCREENSHOTS[0])
            print("YEARLY SCREENSHOT:", ROOT / "screenshots" / SCREENSHOTS[1])
            print("NOTEBOOK:", ROOT / "notebooks" / "automobile_sales_analysis.ipynb")
        except Exception as exc:
            print("CRITICAL: could not write verification report:", repr(exc), file=sys.stderr)
            return 2
    success = bool(pipe.records) and not pipe.fatal and all(r["status"] == "PASS" for r in pipe.records)
    print("FINAL STATUS:", "PASS" if success else "FAIL — see report and step logs", flush=True)
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
