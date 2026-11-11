"""Download the official IBM Skills Network teaching dataset (no synthetic fallback)."""
from pathlib import Path
from urllib.request import urlopen
import csv

URL = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv"
DEST = Path(__file__).resolve().parents[1] / "data" / "historical_automobile_sales.csv"
REQUIRED = {"Year", "Month", "Recession", "Automobile_Sales", "Vehicle_Type", "Advertising_Expenditure", "GDP", "Price", "Seasonality_Weight", "unemployment_rate"}

def fetch():
    DEST.parent.mkdir(parents=True, exist_ok=True)
    with urlopen(URL, timeout=45) as response:
        payload = response.read()
    text = payload.decode("utf-8-sig")
    rows = list(csv.DictReader(text.splitlines()))
    if not rows or not REQUIRED.issubset(rows[0].keys()):
        raise ValueError("Unexpected dataset columns or empty data; refusing to save")
    if not all(str(x["Year"]).isdigit() for x in rows):
        raise ValueError("Invalid Year column")
    DEST.write_bytes(payload)
    print(f"Saved {len(rows)} original IBM dataset rows to {DEST}")

if __name__ == "__main__":
    fetch()
