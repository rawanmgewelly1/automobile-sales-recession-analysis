# Methodology

## Data provenance and integrity

The only permitted analysis input is IBM Skills Network's original `historical_automobile_sales.csv`. Its download URL is defined in `scripts/fetch_dataset.py`. `scripts/check_dataset.py` validates the schema, nonempty records, recession/month domains, numeric conversion, missing-value counts and numerical ranges; it does not repair or invent data. Dataset redistribution rights were not established, so `data/*.csv` is excluded from Git.

## Notebook

The nine course-aligned tasks are independent visualizations of the recorded data: yearly means, non-recession advertising and sales, vehicle-type group means by economic condition, GDP subplots, monthly seasonality bubble sizes, recession price/sales scatter, total advertising share across economic conditions, advertising by vehicle category during recessions, and recession unemployment/sales by vehicle type. Aggregate means describe a typical recorded observation; spending shares use sums. Month-number aggregation removes year variation, so the bubble plot is descriptive only. Twin-axis presentation in task 1.2 prevents treating separate units as identical. All displayed findings should come from the notebook itself after execution.

## Dashboard

Recession statistics use only observations with `Recession == 1`, returning yearly mean sales, mean sales by vehicle type, advertising totals by vehicle type, and unemployment rate against mean sales by vehicle type. Yearly report uses a global sales trend plus three charts for the selected year. The disabled state and default year are updated together by a callback; charts come from another callback using selected report/year.

## Validity and interpretation

The original data is an educational dataset and the example automaker a teaching scenario. The analyses are descriptive, not a causal inference design. Aggregation can conceal within-group variation, missing economic covariates, or year-based confounding. Categories and time coverage must be inspected from the actual data, not assumed. The final workbook-style findings and evaluation-answer truth values are withheld until the IBM CSV is available and the notebook runs end-to-end.

## Verification boundary

The current environment blocked source download and Dash installation. Five isolated tests passed using an artificial test fixture with two test years, two vehicle types and three months. Fixture rows are never included in any real-data deliverable or used to infer course results. Real screenshots require the running Dash application and browser automation; neither image has been created.
