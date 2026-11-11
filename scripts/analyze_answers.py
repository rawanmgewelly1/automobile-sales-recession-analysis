"""Compute Q3 answers directly from the official CSV; no guessed chart outcomes."""
import sys
from pathlib import Path
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_dataset import PATH, validate

def evaluate(path=PATH):
    validate(path)
    df = pd.read_csv(path)
    df["Automobile_Sales"] = pd.to_numeric(df["Automobile_Sales"], errors="raise")
    df["Recession"] = pd.to_numeric(df["Recession"], errors="raise")
    mean = df.groupby(["Vehicle_Type", "Recession"])["Automobile_Sales"].mean().unstack()
    overall = df.groupby("Vehicle_Type")["Automobile_Sales"].mean()
    names = {str(k).casefold().replace(" ", ""): k for k in mean.index}
    def lookup(*aliases):
        for candidate in aliases:
            key = candidate.casefold().replace(" ", "")
            if key in names: return names[key]
        return None
    small = lookup("SmallFamilyCar", "Smallfamiliycar", "Smallfamilycar")
    executive = lookup("ExecutiveCar")
    mini = lookup("SuperMiniCar", "Supperminicar", "Superminicar")
    sports = lookup("SportsCar", "Sports")
    if not {0,1}.issubset(mean.columns):
        raise AssertionError("Both recession conditions are needed")
    table = mean.rename(columns={0: "Non-recession mean", 1: "Recession mean"}).round(3)
    markdown = "# Q3 — Original IBM CSV empirical comparison\n\n"
    markdown += "Source: locally downloaded official IBM historical_automobile_sales.csv. All figures are means.\n\n"
    markdown += "| Vehicle type | Non-recession mean | Recession mean |\n|---|---:|---:|\n" + "".join(f"| {name} | {row['Non-recession mean']:.3f} | {row['Recession mean']:.3f} |\n" for name, row in table.iterrows()) + "\n\n"
    print("Average sales by type and recession status:\n", mean.to_string())
    print("Overall average by type:\n", overall.to_string())
    checks = [
        bool((mean[0] > mean[1]).all()),
        None if small is None else bool(mean.loc[small, 0] == mean[0].min()),
        None if executive is None else bool(overall[executive] == overall.max()),
        None if mini is None or executive is None else bool(mean.loc[mini, 1] > mean.loc[executive, 1]),
        None if executive is None or sports is None else bool(all(set(mean[regime].nsmallest(2).index) == {executive, sports} for regime in (0,1))),
    ]
    explanations = [
        "Non-recession mean exceeds recession mean for every vehicle type",
        "SmallFamilyCar has the lowest non-recession mean",
        "ExecutiveCar has the highest overall (both periods) mean",
        "SuperMiniCar has higher recession mean than ExecutiveCar",
        "ExecutiveCar and sports are the bottom two types in both conditions",
    ]
    markdown += "## Verification of all five statements\n\n"
    markdown += "| Statement | Verified result | Comparison |\n|---|---|---|\n"
    for ix, (statement, checked) in enumerate(zip(explanations, checks), 1):
        markdown += f"| {ix} | {('TRUE' if checked else 'FALSE') if checked is not None else 'UNVERIFIED: category absent'} | {statement} |\n"
    markdown += "\n**Select statements:** " + (", ".join(str(i) for i, value in enumerate(checks, 1) if value) or "none") + "\n"
    output = Path(__file__).resolve().parents[1] / 'docs' / 'q3_vehicle_sales_comparison.md'
    output.write_text(markdown, encoding='utf-8')
    answer_file = Path(__file__).resolve().parents[1] / 'SUBMISSION_ANSWERS.md'
    original = answer_file.read_text(encoding='utf-8')
    begin, end = '<!-- Q3-VERIFIED-BEGIN -->', '<!-- Q3-VERIFIED-END -->'
    summary = (begin + "\n## Q3 — Verified from the local official IBM CSV\n\n" + "\n".join(
        f"{i}. **{('TRUE' if value else 'FALSE') if value is not None else 'NOT VERIFIED'}** — {explanations[i-1]}"
        for i,value in enumerate(checks, 1)) + "\n\nSelect options: **" +
        (', '.join(str(i) for i,v in enumerate(checks,1) if v) or 'none') +
        "**. Full data table: `docs/q3_vehicle_sales_comparison.md`.\n" + end)
    if begin in original and end in original:
        start = original.index(begin)
        finish = original.index(end) + len(end)
        original = original[:start] + summary + original[finish:]
    else:
        original += '\n\n' + summary + '\n'
    answer_file.write_text(original, encoding='utf-8')
    print("\nQ3 statements (None means category missing):")
    print("A Non-recession higher for ALL types:", bool((mean[0] > mean[1]).all()))
    print("B SmallFamilyCar lowest in non-recession:", None if small is None else bool(mean.loc[small, 0] == mean[0].min()))
    print("C ExecutiveCar highest overall mean:", None if executive is None else bool(overall[executive] == overall.max()))
    print("D SuperMiniCar higher than ExecutiveCar during recession:", None if mini is None or executive is None else bool(mean.loc[mini, 1] > mean.loc[executive, 1]))
    print("E ExecutiveCar and sports are the lowest two in both conditions:", None if executive is None or sports is None else bool(all(set(mean[regime].nsmallest(2).index) == {executive, sports} for regime in (0,1))))

if __name__ == "__main__": evaluate()
