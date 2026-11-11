"""Audit the real IBM CSV; write no inferred or synthesized records."""
import json
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "data" / "historical_automobile_sales.csv"
EXPECTED = {"Year", "Month", "Recession", "Automobile_Sales", "Vehicle_Type",
            "Advertising_Expenditure", "GDP", "Price", "Seasonality_Weight", "unemployment_rate"}

def validate(path=PATH):
    # Keep original source bytes and original column types intact; use a validated
    # numeric view for comparisons, aggregation and min/max calculations.
    df = pd.read_csv(path)
    missing = EXPECTED.difference(df.columns)
    if missing:
        raise AssertionError(f"Required fields absent: {sorted(missing)}")
    if df.empty:
        raise AssertionError("Dataset contains zero records")
    if df["Vehicle_Type"].isna().any():
        raise AssertionError("Vehicle types missing")
    numeric = ["Year", "Month", "Recession", "Automobile_Sales", "Advertising_Expenditure", "GDP", "Price", "Seasonality_Weight", "unemployment_rate"]
    numbers = pd.DataFrame(index=df.index)
    for name in numeric:
        numbers[name] = pd.to_numeric(df[name], errors="coerce")
        if numbers[name].isna().any():
            bad_rows = numbers.index[numbers[name].isna()].tolist()[:10]
            raise AssertionError(f"Invalid or missing numeric data in {name}; first zero-based rows: {bad_rows}")
    if not numbers["Recession"].isin([0, 1]).all():
        raise AssertionError("Unexpected recession flag")
    if not {0, 1}.issubset(set(numbers["Recession"])):
        raise AssertionError("Both recession statuses required")
    if not numbers["Month"].between(1, 12).all():
        raise AssertionError("Invalid months")
    if (numbers[["Automobile_Sales", "Advertising_Expenditure"]] < 0).any().any():
        raise AssertionError("Negative sales or ad spending detected")
    if not (numbers["Year"] % 1 == 0).all() or not (numbers["Month"] % 1 == 0).all():
        raise AssertionError("Year and Month must be integers")
    report = {
        "file": str(Path(path)), "rows": len(df), "columns": len(df.columns),
        "column_names": df.columns.tolist(), "dtypes": df.dtypes.astype(str).to_dict(),
        "missing_counts": df.isna().sum().to_dict(),
        "duplicate_rows": int(df.duplicated().sum()),
        "year_range": [int(numbers.Year.min()), int(numbers.Year.max())],
        "recession_counts": {str(int(k)): int(v) for k, v in numbers.Recession.value_counts().items()},
        "numeric_ranges": {k: {"min": float(numbers[k].min()), "max": float(numbers[k].max())} for k in numeric},
    }
    return report

if __name__ == "__main__":
    print(json.dumps(validate(), indent=2))
