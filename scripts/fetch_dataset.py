"""Download the official IBM Skills Network teaching dataset (no synthetic fallback)."""
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import URLError
import csv
import time
import hashlib

URL = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv"
DEST = Path(__file__).resolve().parents[1] / "data" / "historical_automobile_sales.csv"
REQUIRED = {"Year", "Month", "Recession", "Automobile_Sales", "Vehicle_Type", "Advertising_Expenditure", "GDP", "Price", "Seasonality_Weight", "unemployment_rate"}

def validate_csv_bytes(payload):
    if not payload or payload[:128].lstrip().lower().startswith((b'<!doctype html', b'<html')):
        raise ValueError('Source is empty or returned HTML, not a CSV')
    text = payload.decode('utf-8-sig')
    rows = list(csv.DictReader(text.splitlines()))
    if not rows or not REQUIRED.issubset(rows[0].keys()):
        raise ValueError('Unexpected dataset columns or empty data; refusing to save')
    if not all(str(x['Year']).isdigit() for x in rows):
        raise ValueError('Invalid Year column')
    return len(rows)

def fetch():
    DEST.parent.mkdir(parents=True, exist_ok=True)
    if DEST.is_file():
        existing = DEST.read_bytes()
        count = validate_csv_bytes(existing)
        print(f'Validated existing local CSV ({count} rows, sha256={hashlib.sha256(existing).hexdigest()}); not overwriting. Confirm original IBM provenance independently.')
        return
    errors = []
    payload = None
    for attempt in range(3):
        try:
            request = Request(URL, headers={"User-Agent": "Mozilla/5.0 (IBM course reproducibility)"})
            with urlopen(request, timeout=30) as response:
                if response.status != 200:
                    raise RuntimeError(f"Official IBM endpoint HTTP {response.status}")
                payload = response.read()
            break
        except (URLError, TimeoutError, OSError, RuntimeError) as exc:
            errors.append(f"attempt {attempt+1}: {type(exc).__name__}: {exc}")
            if attempt < 2:
                time.sleep(attempt + 1)
    if payload is None:
        raise RuntimeError("Could not retrieve official IBM CSV: " + " | ".join(errors))
    count = validate_csv_bytes(payload)
    DEST.write_bytes(payload)
    print(f"Saved {count} original IBM dataset rows to {DEST} (sha256={hashlib.sha256(payload).hexdigest()})")

if __name__ == "__main__":
    fetch()
