"""Execute all cells from a fresh kernel; save outputs only on success."""
from pathlib import Path
import nbformat
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]
notebook = ROOT / "notebooks" / "automobile_sales_analysis.ipynb"
source = nbformat.read(notebook, as_version=4)
client = NotebookClient(source, timeout=240, kernel_name="python3", allow_errors=False,
                        resources={"metadata": {"path": str(ROOT)}})
client.execute()
codes = [cell for cell in source.cells if cell.cell_type == "code"]
assert all(cell.execution_count is not None for cell in codes)
assert not any(output.output_type == "error" for cell in codes for output in cell.outputs)
assert sum(any(o.output_type == "display_data" for o in cell.outputs) for cell in codes) >= 9
nbformat.write(source, notebook)
print("PASS: fresh-kernel notebook execution; all 9 visualizations generated")
