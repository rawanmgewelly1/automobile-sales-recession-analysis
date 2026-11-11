"""Audit the real IBM CSV; write no inferred or synthesized records."""
import json
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "data" / "historical_automobile_sales.csv"
EXPECTED = {"Year", "Month", "Recession", "Automobile_Sales", "Vehicle_Type",
            "Advertising_Expenditure", "GDP", "Price", "Seasonality_Weight", "unemployment_rate"}

def validate(path=PATH):
    df = pd.read_csv(path)
    missing = EXPECTED.difference(df.columns)
    if missing: raise AssertionError(f"Required fields absent: {sorted(missing)}")
    if df.empty: raise AssertionError("Dataset contains zero records")
    if df["Vehicle_Type"].isna().any(): raise AssertionError("Vehicle types missing")
    if not {0,1}.issubset(set(df["Recession"])): raise AssertionError("Both recession statuses required")
    if not df["Recession"].isin([0, 1]).all(): raise AssertionError("Unexpected recession flag")
    if not df["Month"].between(1, 12).all(): raise AssertionError("Invalid months")
    numeric = ["Year", "Month", "Recession", "Automobile_Sales", "Advertising_Expenditure", "GDP", "Price", "Seasonality_Weight", "unemployment_rate"]
    for name in numeric:
        values = pd.to_numeric(df[name], errors="coerce")
        if values.isna().any(): raise AssertionError(f"Invalid numeric data in {name}")
    if (df[["Automobile_Sales", "Advertising_Expenditure"]] < 0).any().any():
        raise AssertionError("Negative sales or ad spending detected")
    report = {
        "file": str(Path(path)), "rows": len(df), "columns": len(df.columns),
        "column_names": df.columns.tolist(), "dtypes": df.dtypes.astype(str).to_dict(),
        "missing_counts": df.isna().sum().to_dict(),
        "year_range": [int(df.Year.min()), int(df.Year.max())],
        "recession_counts": {str(k): int(v) for k,v in df.Recession.value_counts().items()},
        "numeric_ranges": {k: {"min": float(df[k].min()), "max": float(df[k].max())} for k in numeric},
    }
    return report

if __name__ == "__main__":
    print(json.dumps(validate(), indent=2))
