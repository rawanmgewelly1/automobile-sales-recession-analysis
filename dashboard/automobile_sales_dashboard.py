"""IBM DV0101EN automobile sales dashboard; source data never fabricated."""
from pathlib import Path
import sys
import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, dcc, html

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from check_dataset import parse_months

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "historical_automobile_sales.csv"
REQUIRED_COLUMNS = {"Year", "Month", "Recession", "Automobile_Sales", "Vehicle_Type", "Advertising_Expenditure", "unemployment_rate"}

def load_data(path=DATA_PATH):
    if not Path(path).is_file():
        raise FileNotFoundError(f"Official dataset is missing: {path}. Run: python scripts/fetch_dataset.py")
    frame = pd.read_csv(path)
    missing = REQUIRED_COLUMNS - set(frame.columns)
    if missing:
        raise ValueError(f"Required columns missing: {sorted(missing)}")
    frame["Year"] = pd.to_numeric(frame["Year"], errors="raise").astype(int)
    frame["Month_Number"] = parse_months(frame["Month"])
    for column in ["Recession", "Automobile_Sales", "Advertising_Expenditure", "unemployment_rate"]:
        frame[column] = pd.to_numeric(frame[column], errors="raise")
    if frame.empty or not frame["Recession"].isin([0, 1]).all():
        raise ValueError("Dataset empty or invalid recession/month values")
    return frame

def build_recession_figures(frame):
    rec = frame.loc[frame["Recession"] == 1]
    if rec.empty:
        raise ValueError("No recession records")
    yearly_rec = rec.groupby("Year", as_index=False)["Automobile_Sales"].mean()
    avg_vehicles_sold = rec.groupby("Vehicle_Type", as_index=False)["Automobile_Sales"].mean()
    exp_rec = rec.groupby("Vehicle_Type", as_index=False)["Advertising_Expenditure"].sum()
    unemployment_effect = rec.groupby(["Vehicle_Type", "unemployment_rate"], as_index=False)["Automobile_Sales"].mean()
    return [
        px.line(yearly_rec, x="Year", y="Automobile_Sales", markers=True, title="Average Automobile Sales During Recessions", labels={"Automobile_Sales": "Average automobile sales"}),
        px.bar(avg_vehicles_sold, x="Vehicle_Type", y="Automobile_Sales", title="Average Sales by Vehicle Type During Recessions", labels={"Automobile_Sales": "Average automobile sales", "Vehicle_Type": "Vehicle type"}),
        px.pie(exp_rec, names="Vehicle_Type", values="Advertising_Expenditure", title="Recession Advertising Expenditure by Vehicle Type"),
        px.line(unemployment_effect, x="unemployment_rate", y="Automobile_Sales", color="Vehicle_Type", markers=True, title="Unemployment Rate and Sales by Vehicle Type During Recessions", labels={"unemployment_rate": "Unemployment rate", "Automobile_Sales": "Average automobile sales", "Vehicle_Type": "Vehicle type"}),
    ]

def build_yearly_figures(frame, year):
    if year is None or int(year) not in set(frame["Year"]):
        return []
    subset = frame.loc[frame["Year"] == int(year)]
    trend = frame.groupby("Year", as_index=False)["Automobile_Sales"].mean()
    if "Month_Number" not in subset.columns:
        # Compatibility with existing numeric-month DataFrame fixtures.
        subset = subset.assign(Month_Number=pd.to_numeric(subset["Month"], errors="raise").astype(int))
    monthly = subset.groupby("Month_Number", as_index=False)["Automobile_Sales"].sum().sort_values("Month_Number")
    vehicles = subset.groupby("Vehicle_Type", as_index=False)["Automobile_Sales"].mean()
    advertising = subset.groupby("Vehicle_Type", as_index=False)["Advertising_Expenditure"].sum()
    return [
        px.line(trend, x="Year", y="Automobile_Sales", markers=True, title="Yearly Average Automobile Sales (All Years)"),
        px.line(monthly, x="Month_Number", y="Automobile_Sales", markers=True, title=f"Monthly Total Automobile Sales — {year}", labels={"Month_Number": "Month"}).update_xaxes(tickmode="array", tickvals=list(range(1, 13)), ticktext=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]),
        px.bar(vehicles, x="Vehicle_Type", y="Automobile_Sales", title=f"Average Sales by Vehicle Type — {year}"),
        px.pie(advertising, names="Vehicle_Type", values="Advertising_Expenditure", title=f"Advertising Expenditure by Vehicle Type — {year}"),
    ]

def report_graphs(statistics, year, frame):
    if statistics == "Recession Period Statistics":
        return build_recession_figures(frame)
    if statistics == "Yearly Statistics":
        return build_yearly_figures(frame, year)
    return []

def create_app(frame=None):
    frame = load_data() if frame is None else frame
    years = sorted(frame["Year"].unique().tolist())
    app = Dash(__name__)
    app.title = "Automobile Sales Statistics Dashboard"
    app.layout = html.Div([
        html.Header([
            html.P("IBM DATA VISUALIZATION WITH PYTHON · CAPSTONE", className="eyebrow"),
            html.H1("Automobile Sales Statistics Dashboard"),
            html.P("Explore recession-period and annual automobile sales performance.", className="subtitle"),
        ], className="masthead"),
        html.Div([
            html.Div([html.Label("Select Statistics", htmlFor="dropdown-statistics"), dcc.Dropdown(
                id="dropdown-statistics", options=[{"label": x, "value": x} for x in ["Recession Period Statistics", "Yearly Statistics"]],
                value="Recession Period Statistics", clearable=False)], className="control"),
            html.Div([html.Label("Select Year", htmlFor="select-year"), dcc.Dropdown(
                id="select-year", options=[{"label": str(y), "value": y} for y in years],
                value=years[-1], clearable=False, disabled=True)], className="control"),
        ], className="controls"),
        html.Div(id="output-container", className="chart-grid"),
        html.Footer(
    "Source: IBM Skills Network · Historical Automobile Sales "
    "| Developed by Rawan Mahmoud Gewelly"
)
    ], className="page")

    @app.callback(
        Output("select-year", "disabled"),
        Output("select-year", "value"),
        Input("dropdown-statistics", "value"),
    )
    def update_input_container(selected_statistics):
        # Every report switch reinitializes the year to an actual dataset year.
        return selected_statistics != "Yearly Statistics", years[-1]


    @app.callback(
        Output("output-container", "children"),
        Input("dropdown-statistics", "value"),
        Input("select-year", "value")
    )
    def update_output_container(selected_statistics, selected_year):
        figures = report_graphs(selected_statistics, selected_year, frame)

        if not figures:
            return html.P("Select a report and an available year to display charts.")

        for figure in figures:
            figure.update_layout(
                margin=dict(
                    l=50,
                    r=30,
                    t=50,
                    b=100
                )
            )

            figure.add_annotation(
                text="Created by Rawan Mahmoud Gewelly",
                xref="paper",
                yref="paper",
                x=0.5,
                y=-0.18,
                xanchor="center",
                yanchor="top",
                showarrow=False,
                font=dict(
                    size=10,
                    color="rgba(80, 80, 80, 0.65)"
                )
            )

        return [
            html.Div(
                dcc.Graph(
                    figure=figure,
                    config={"displaylogo": False},
                    style={"height": "410px"}
                ),
                className="chart-item"
            )
            for figure in figures
        ]

    return app


if __name__ == "__main__":
    create_app().run(host="127.0.0.1", port=8050, debug=False)