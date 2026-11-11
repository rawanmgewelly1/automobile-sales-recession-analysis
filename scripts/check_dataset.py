"""Audit the real IBM CSV; write no inferred or synthesized records."""
import json
import calendar
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "data" / "historical_automobile_sales.csv"
EXPECTED = {"Year", "Month", "Recession", "Automobile_Sales", "Vehicle_Type",
            "Advertising_Expenditure", "GDP", "Price", "Seasonality_Weight", "unemployment_rate"}

MONTH_ABBREVIATIONS = {name.lower(): number for number, name in enumerate(calendar.month_abbr) if number}
MONTH_NAMES = {name.lower(): number for number, name in enumerate(calendar.month_name) if number}


def parse_months(values):
    """Return a validated 1..12 integer view; never mutate original labels.

    Accept English abbreviations/full names or already-numeric months, and reject
    nulls, booleans, decimals and unrecognized labels with row positions.
    """
    result = []
    invalid = []
    for position, value in enumerate(values):
        number = None
        if not pd.isna(value):
            label = str(value).strip()
            key = label.casefold()
            if key in MONTH_ABBREVIATIONS:
                number = MONTH_ABBREVIATIONS[key]
            elif key in MONTH_NAMES:
                number = MONTH_NAMES[key]
            elif label.isascii() and label.isdecimal():
                month = int(label)
                if 1 <= month <= 12:
                    number = month
            elif isinstance(value, (int, float)) and not isinstance(value, bool):
                if float(value).is_integer() and 1 <= value <= 12:
                    number = int(value)
        if number is None:
            invalid.append((position, str(value)))
        result.append(number)
    if invalid:
        raise AssertionError(f"Invalid or missing Month values (zero-based row, value): {invalid[:10]}")
    return pd.Series(result, index=values.index, dtype='int64', name='Month_Number')


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
    numeric = ["Year", "Recession", "Automobile_Sales", "Advertising_Expenditure", "GDP", "Price", "Seasonality_Weight", "unemployment_rate"]
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
    month_numbers = parse_months(df["Month"])
    if (numbers[["Automobile_Sales", "Advertising_Expenditure"]] < 0).any().any():
        raise AssertionError("Negative sales or ad spending detected")
    if not (numbers["Year"] % 1 == 0).all():
        raise AssertionError("Year and Month must be integers")
    report = {
        "file": str(Path(path)), "rows": len(df), "columns": len(df.columns),
        "column_names": df.columns.tolist(), "dtypes": df.dtypes.astype(str).to_dict(),
        "missing_counts": df.isna().sum().to_dict(),
        "duplicate_rows": int(df.duplicated().sum()),
        "year_range": [int(numbers.Year.min()), int(numbers.Year.max())],
        "recession_counts": {str(int(k)): int(v) for k, v in numbers.Recession.value_counts().items()},
        "month_counts": {calendar.month_abbr[int(k)]: int(v) for k, v in month_numbers.value_counts().sort_index().items()},
        "numeric_ranges": {k: {"min": float(numbers[k].min()), "max": float(numbers[k].max())} for k in numeric},
    }
    return report

if __name__ == "__main__":
    print(json.dumps(validate(), indent=2))
