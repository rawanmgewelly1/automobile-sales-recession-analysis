# Coursera submission answers — evidence status (2026-11-11)

The IBM CSV could not be downloaded in this environment. The notebook is not executed, and real screenshots are not generated. This document is explicit about code inspection versus data verification.

| Question | Answer | Evidence |
|---|---|---|
| Q1 | `notebooks/automobile_sales_analysis.ipynb` | Notebook schema valid; real-data execution blocked |
| Q2 | `sns.barplot(x='Vehicle_Type', y='Automobile_Sales', hue='Recession', data=df)` | Correct source expression; notebook uses same with `ax=ax` |
| Q3 | Five observations below | NOT VERIFIED: IBM CSV absent |
| Q4 | `dashboard/automobile_sales_dashboard.py` | Syntax checked; Dash app cannot start until Dash installed and CSV available |
| Q5 | `html.Div` is an HTML container for grouping, layout, and styling of Dash components | Verified definition; MC option letter not provided |
| Q6 | `screenshots/RecessionReportgraphs.png` | NOT GENERATED (actual application unavailable) |
| Q7 | Individual callback statements below | Source-verified only; not browser-verified |
| Q8 | `screenshots/YearlyReportgraphs.png` | NOT GENERATED (actual application unavailable) |
| Q9 | The `dcc.Graph` containing `px.pie` of recession-period `Advertising_Expenditure` grouped by `Vehicle_Type` | Correct implementation verified by source inspection |

## Q3 — empirical checks

All five remain **NOT VERIFIED**. Once the official CSV is available, execute `python scripts/analyze_answers.py`. It prints the actual vehicle-type mean sales, writes `docs/q3_vehicle_sales_comparison.md`, and prints truth values for:

1. Every vehicle type sells more in non-recession periods.
2. SmallFamilyCar is lowest in non-recession.
3. ExecutiveCar has the highest overall mean sales.
4. SuperMiniCar exceeds ExecutiveCar in recession.
5. ExecutiveCar and sports cars are the lowest two in *both* periods.

The evaluator recognizes capitalization and the `Supperminicar` spelling variant where present. Missing categories produce `None` rather than an invented verdict.

## Q7 — actual implemented callback source

1. Missing `Output` raises an error: **FALSE** — `Output` is imported and used.
2. Year is enabled in Yearly Statistics: **TRUE** — disabled flag is false.
3. Both dropdowns reset whenever a selection changes: **FALSE as written** — changing the statistics mode resets the year to the latest available year; changing the year does not reset the statistics selection.
4. Both dropdowns remain active: **FALSE** — the year control is disabled in recession mode.
5. Year is disabled in Recession Period Statistics: **TRUE** — disabled flag is true.

Q7 applies to this repository's reconstructed callback, **not an unavailable original starter**. The correct multiple-choice letter(s) cannot be determined without the original choices.


<!-- Q3-VERIFIED-BEGIN -->
## Q3 — Verified from the local official IBM CSV

1. **TRUE** — Non-recession mean exceeds recession mean for every vehicle type
2. **FALSE** — SmallFamilyCar has the lowest non-recession mean
3. **FALSE** — ExecutiveCar has the highest overall (both periods) mean
4. **TRUE** — SuperMiniCar has higher recession mean than ExecutiveCar
5. **FALSE** — ExecutiveCar and sports are the bottom two types in both conditions

Select options: **1, 4**. Full data table: `docs/q3_vehicle_sales_comparison.md`.
<!-- Q3-VERIFIED-END -->
