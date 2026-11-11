"""Compute Q3 answers directly from the official CSV; no guessed chart outcomes."""
import sys
from pathlib import Path
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_dataset import PATH, validate

def evaluate(path=PATH):
    validate(path)
    df = pd.read_csv(path)
    mean = df.groupby(["Vehicle_Type", "Recession"])["Automobile_Sales"].mean().unstack()
    overall = df.groupby("Vehicle_Type")["Automobile_Sales"].mean()
    names = {str(k).casefold().replace(" ", ""): k for k in mean.index}
    def lookup(*aliases):
        for candidate in aliases:
            key = candidate.casefold().replace(" ", "")
            if key in names: return names[key]
        return None
    small = lookup("SmallFamilyCar")
    executive = lookup("ExecutiveCar")
    mini = lookup("SuperMiniCar", "Supperminicar")
    sports = lookup("SportsCar", "Sports")
    if not {0,1}.issubset(mean.columns):
        raise AssertionError("Both recession conditions are needed")
    table = mean.rename(columns={0: "Non-recession mean", 1: "Recession mean"}).round(3)
    markdown = "# Q3 — Original IBM CSV empirical comparison\n\n"
    markdown += "Source: locally downloaded official IBM historical_automobile_sales.csv. All figures are means.\n\n"
    markdown += "| Vehicle type | Non-recession mean | Recession mean |\n|---|---:|---:|\n" + "".join(f"| {name} | {row['Non-recession mean']:.3f} | {row['Recession mean']:.3f} |\n" for name, row in table.iterrows()) + "\n\n"
    (Path(__file__).resolve().parents[1] / "docs" / "q3_vehicle_sales_comparison.md").write_text(markdown, encoding="utf-8")
    print("Average sales by type and recession status:\n", mean.to_string())
    print("Overall average by type:\n", overall.to_string())
    print("\nQ3 statements (None means category missing):")
    print("A Non-recession higher for ALL types:", bool((mean[0] > mean[1]).all()))
    print("B SmallFamilyCar lowest in non-recession:", None if small is None else bool(mean.loc[small, 0] == mean[0].min()))
    print("C ExecutiveCar highest overall mean:", None if executive is None else bool(overall[executive] == overall.max()))
    print("D SuperMiniCar higher than ExecutiveCar during recession:", None if mini is None or executive is None else bool(mean.loc[mini, 1] > mean.loc[executive, 1]))
    print("E ExecutiveCar and sports are the lowest two in both conditions:", None if executive is None or sports is None else bool(all(set(mean[regime].nsmallest(2).index) == {executive, sports} for regime in (0,1))))

if __name__ == "__main__": evaluate()
