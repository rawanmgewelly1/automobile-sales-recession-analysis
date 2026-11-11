# Analyzing the Impact of Economic Recession on Automobile Sales

**IBM Data Visualization with Python | Data Analyst portfolio project**

> **Verification notice:** This repository contains independently reconstructed assignment implementations. The IBM-provided starter notebook was not available. As of the latest execution attempt, the official dataset could not be downloaded inside the build environment. Notebook output, running-dashboard screenshots, numeric findings and end-to-end checks are therefore **not claimed as complete**. Consult [validation report](docs/validation_report.md).

## Project overview / business problem

Explore how recession indicators relate to automobile sales, consumer spending, advertising allocation, vehicle-type demand, pricing, seasonality, GDP and unemployment in the IBM Skills Network educational automobile dataset. A fictional automaker, XYZAutomotives, uses the insights to frame questions about planning in different economic conditions.

## Objectives

- Compare automobile sales over time and across recession and non-recession periods.
- Examine advertising expenditure and sales, by vehicle type and by economic period.
- Evaluate descriptive relationships with vehicle prices, seasonality, GDP and unemployment.
- Build an interactive Dash dashboard with recession and selected-year reporting.
- Demonstrate careful, reproducible analysis; association is not evidence of causation.

## Dataset

Official IBM Skills Network CSV: [historical_automobile_sales.csv](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv). Records are typically described as monthly observations between 1980 and 2023; actual counts and fields are validated on local load, **not assumed**. Core variables include `Year`, `Month`, `Recession`, `Automobile_Sales`, `Vehicle_Type`, `Advertising_Expenditure`, `Price`, `GDP`, `Seasonality_Weight`, and `unemployment_rate`.

**Redistribution:** Dataset redistribution permission has not been established. For that reason, this repository deliberately does **not** include the original CSV. Obtain it from IBM using the fetch script before running analyses. The dataset is used only to compute results; it is never synthesized.

## Tools / methodology

Python, pandas, NumPy, Matplotlib, Seaborn, Plotly, Dash, Jupyter Notebook, and Folium (included in course toolkit; no geographic plot fabricated without location information). Data workflow: official download → schema/quality checks → recession flag segmentation → appropriate `groupby` aggregations → nine visualizations → dashboard with responsive callbacks. Details: [methodology](docs/methodology.md).

## Nine assignment visualizations (Part 1)

| Task | Output | Approach |
| --- | --- | --- |
| 1.1 | Automobile sales over time | Mean sales by year, line |
| 1.2 (custom brief) | Advertising expenditure vs sales, non-recession | Two-axis line chart with descriptive scales |
| 1.2 (original rubric supplement) | Recession sales trends by vehicle type | Multi-line Seaborn chart; both versions retained |
| 1.3 | Vehicle type by recession status | Grouped Seaborn bar chart, original assignment API |
| 1.4 | GDP in recession vs non-recession | Two side-by-side line subplots |
| 1.5 | Seasonality and sales | Monthly bubble chart sized by mean sales |
| 1.6 | Average price vs sales, recession | Scatter plot |
| 1.7 | Spending share: recession vs non-recession | Pie chart |
| 1.8 | Recession advertising by vehicle type | Pie chart |
| 1.9 | Unemployment vs sales by vehicle type | Grouped line chart |

## Interactive dashboard (Part 2)

Two report modes: **Recession Period Statistics** (disables year selection) and **Yearly Statistics** (enables year selection). Both render four Plotly graphs from the IBM dataset. The Yearly dashboard includes a full-period trend and three selected-year comparisons. Callbacks use the standard Coursera component IDs (`dropdown-statistics`, `select-year`, `output-container`).

### Screenshot availability

- `screenshots/RecessionReportgraphs.png` — **pending** verified browser capture.
- `screenshots/YearlyReportgraphs.png` — **pending** verified browser capture.

No substitute images have been created. Use the instructions in [validation report](docs/validation_report.md) to capture the live application once dependencies and source data are accessible.

## One-command Windows completion

Run `FINISH_ON_WINDOWS.bat` from an Internet-connected Windows machine with Python 3.10+ installed. This creates a local virtual environment, installs requirements, downloads and audits the **official** IBM dataset, computes the Q3 comparison table in `docs/q3_vehicle_sales_comparison.md`, executes the notebook using a clean kernel, runs the test suite, launches the Dash server, waits for an HTTP 200 response, and captures both real full-page browser screenshots after verifying all chart titles. After successful capture it writes `docs/local_execution_verification.md`, including dataset and PNG SHA-256 checksums and confirmed notebook output counts. **It does not upload anything to GitHub.** Failures return a nonzero exit code instead of declaring success. Re-run `python -m pytest -q` after successful completion to confirm integration/screenshot tests.

The browser screenshot automation uses an explicit Plotly SVG-title check rather than fixed sleep delays. The local dataset is excluded from Git by default because redistribution permission has not been established.

## Installation and execution

Requires Python 3.10+ and internet access for the first dataset download.

```bash
git clone https://github.com/YOUR_USERNAME/automobile-sales-recession-analysis.git
cd automobile-sales-recession-analysis
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/fetch_dataset.py
jupyter notebook notebooks/automobile_sales_analysis.ipynb
```

Execute **Run All** and save notebook outputs for Coursera submission. Launch the dashboard separately:

```bash
python dashboard/automobile_sales_dashboard.py
```

Open **http://127.0.0.1:8050**. In a separate terminal, run `python scripts/capture_screenshots.py` to create both full-page screenshots directly from the running browser. This project uses port **8050** to avoid conflicting with other services.

Before analysis: `python scripts/check_dataset.py`. To evaluate Q3 on real data: `python scripts/analyze_answers.py`. Run chart-function tests: `python -m pytest -q` (test-only synthetic fixture; never used for findings).

## Structure

```text
automobile-sales-recession-analysis/
├── README.md
├── notebooks/automobile_sales_analysis.ipynb
├── dashboard/automobile_sales_dashboard.py
├── dashboard/assets/styles.css
├── screenshots/                   # real UI captures pending
├── data/                          # IBM CSV downloaded locally (not bundled)
├── scripts/fetch_dataset.py
├── scripts/check_dataset.py
├── scripts/analyze_answers.py
├── scripts/execute_notebook.py
├── scripts/capture_screenshots.py
├── tests/test_dashboard.py
├── docs/methodology.md
├── docs/validation_report.md
├── requirements.txt
├── .gitignore
├── LICENSE
└── SUBMISSION_ANSWERS.md
```

## Key findings

**Pending verified execution.** This repository does not assert specific automobile sales differences or statistical relationships before the IBM CSV has been loaded and all analyses have executed successfully.

## Limitations

The course material describes an illustrative company and an educational dataset, not audited real-world causal evidence. Aggregation choices affect the apparent size of changes. Dataset license terms have not been independently confirmed. Original course notebooks and full multiple-choice alternatives were not supplied, so exact matching to every original grading wording remains unverified.

## Credits and integrity

IBM Skills Network and Coursera are acknowledged as the original project prompt and dataset source. This is an original reconstruction of the described exercises, **not** a claim that IBM endorses the repository or that the original starter notebook was edited. Third-party sample solutions were used only to confirm task structure and known component names.
