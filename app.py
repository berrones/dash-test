import math
from datetime import date

import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, callback, dash_table, dcc, html


APP_TITLE = "Kentucky Stroke Metrics for SEQIP"
REGIONS = {
    "Appalachian": ["Eastern Kentucky Stroke Center", "Bluegrass Mountain Health"],
    "Bluegrass": ["Lexington Comprehensive Stroke", "Frankfort Regional"],
    "Louisville": ["River City Medical Center", "Jefferson Stroke Institute"],
    "Northern Kentucky": ["Covington Medical", "Ohio River Health"],
    "Purchase/Pennyrile": ["Paducah Regional", "Pennyrile Community Hospital"],
}
METRIC_LABELS = {
    "door_to_needle": "Median door-to-needle time",
    "door_to_imaging": "Median door-to-imaging time",
    "discharge_antithrombotic": "Antithrombotic at discharge",
    "dysphagia_screen": "Dysphagia screen documented",
    "nihss_documented": "NIHSS documented",
    "transfer_acceptance": "Transfer acceptance under 20 min",
}
TARGETS = {
    "door_to_needle": 45,
    "door_to_imaging": 25,
    "discharge_antithrombotic": 95,
    "dysphagia_screen": 90,
    "nihss_documented": 92,
    "transfer_acceptance": 85,
}


def build_sample_data() -> pd.DataFrame:
    quarters = pd.period_range("2024Q1", "2025Q4", freq="Q")
    rows = []

    for quarter_idx, quarter in enumerate(quarters):
        for region_idx, (region, hospitals) in enumerate(REGIONS.items()):
            for hospital_idx, hospital in enumerate(hospitals):
                volume = 42 + region_idx * 9 + hospital_idx * 7 + quarter_idx * 4
                volume += int(8 * math.sin((quarter_idx + region_idx) / 1.7))
                base_quality = 84 + quarter_idx * 1.4 - hospital_idx * 1.6
                regional_shift = (region_idx - 2) * 1.3

                rows.append(
                    {
                        "quarter": str(quarter),
                        "quarter_start": quarter.start_time.date(),
                        "region": region,
                        "hospital": hospital,
                        "hospital_type": "Comprehensive Stroke Center"
                        if hospital_idx == 0
                        else "Primary/Acute Stroke Ready",
                        "stroke_cases": max(volume, 20),
                        "ivt_cases": max(int(volume * (0.16 + 0.01 * hospital_idx)), 4),
                        "transfer_cases": max(int(volume * (0.28 + 0.02 * region_idx)), 7),
                        "door_to_needle": round(
                            53 - quarter_idx * 1.8 - hospital_idx * 2.2 + region_idx * 0.9,
                            1,
                        ),
                        "door_to_imaging": round(
                            32 - quarter_idx * 1.1 - hospital_idx * 0.7 + region_idx * 0.5,
                            1,
                        ),
                        "discharge_antithrombotic": round(
                            base_quality + regional_shift + hospital_idx * 2.3,
                            1,
                        ),
                        "dysphagia_screen": round(
                            base_quality - 2.4 + regional_shift + hospital_idx * 1.8,
                            1,
                        ),
                        "nihss_documented": round(
                            base_quality - 1.2 + regional_shift + hospital_idx * 2.1,
                            1,
                        ),
                        "transfer_acceptance": round(
                            78 + quarter_idx * 1.6 - region_idx * 0.5 + hospital_idx * 1.1,
                            1,
                        ),
                    }
                )

    df = pd.DataFrame(rows)
    percentage_cols = [
        "discharge_antithrombotic",
        "dysphagia_screen",
        "nihss_documented",
        "transfer_acceptance",
    ]
    df[percentage_cols] = df[percentage_cols].clip(upper=99.2)
    return df


df = build_sample_data()

app = Dash(__name__, title=APP_TITLE)
server = app.server


def indicator_card(label: str, value: str, detail: str, status: str = "neutral"):
    return html.Div(
        className=f"kpi-card {status}",
        children=[
            html.Div(label, className="kpi-label"),
            html.Div(value, className="kpi-value"),
            html.Div(detail, className="kpi-detail"),
        ],
    )


def control_panel():
    return html.Div(
        className="control-panel",
        children=[
            html.Div(
                [
                    html.Label("Quarter range", htmlFor="quarter-range"),
                    dcc.RangeSlider(
                        id="quarter-range",
                        min=0,
                        max=len(sorted(df["quarter"].unique())) - 1,
                        value=[0, len(sorted(df["quarter"].unique())) - 1],
                        marks={
                            idx: label
                            for idx, label in enumerate(sorted(df["quarter"].unique()))
                        },
                        step=1,
                        allowCross=False,
                    ),
                ],
                className="filter filter-wide",
            ),
            html.Div(
                [
                    html.Label("Region", htmlFor="region-filter"),
                    dcc.Dropdown(
                        id="region-filter",
                        options=[
                            {"label": region, "value": region}
                            for region in sorted(df["region"].unique())
                        ],
                        value=sorted(df["region"].unique()),
                        multi=True,
                        clearable=False,
                    ),
                ],
                className="filter",
            ),
            html.Div(
                [
                    html.Label("Hospital type", htmlFor="type-filter"),
                    dcc.Dropdown(
                        id="type-filter",
                        options=[
                            {"label": hospital_type, "value": hospital_type}
                            for hospital_type in sorted(df["hospital_type"].unique())
                        ],
                        value=sorted(df["hospital_type"].unique()),
                        multi=True,
                        clearable=False,
                    ),
                ],
                className="filter",
            ),
            html.Div(
                [
                    html.Label("Metric", htmlFor="metric-filter"),
                    dcc.Dropdown(
                        id="metric-filter",
                        options=[
                            {"label": label, "value": metric}
                            for metric, label in METRIC_LABELS.items()
                        ],
                        value="door_to_needle",
                        clearable=False,
                    ),
                ],
                className="filter",
            ),
        ],
    )


app.layout = html.Div(
    className="page",
    children=[
        html.Header(
            className="header",
            children=[
                html.Div(
                    [
                        html.P("SEQIP statewide system of care group", className="eyebrow"),
                        html.H1(APP_TITLE),
                        html.P(
                            "Sample dashboard for reviewing statewide stroke care access, "
                            "timeliness, and documentation trends across Kentucky regions."
                        ),
                    ],
                    className="header-copy",
                ),
                html.Div(
                    [
                        html.Span("Dummy data", className="data-badge"),
                        html.Span(f"Generated {date.today().isoformat()}"),
                    ],
                    className="header-meta",
                ),
            ],
        ),
        html.Main(
            [
                control_panel(),
                html.Section(id="summary-cards", className="kpi-grid"),
                html.Section(
                    className="chart-grid",
                    children=[
                        html.Div(
                            className="chart-panel wide",
                            children=[
                                html.Div(
                                    [
                                        html.H2("Statewide trend"),
                                        html.P(
                                            "Weighted by stroke case volume; target line reflects a sample SEQIP goal."
                                        ),
                                    ],
                                    className="panel-heading",
                                ),
                                dcc.Graph(id="trend-chart", config={"displayModeBar": False}),
                            ],
                        ),
                        html.Div(
                            className="chart-panel",
                            children=[
                                html.Div(
                                    [
                                        html.H2("Regional comparison"),
                                        html.P("Current filtered period, case-weighted averages."),
                                    ],
                                    className="panel-heading",
                                ),
                                dcc.Graph(
                                    id="region-chart", config={"displayModeBar": False}
                                ),
                            ],
                        ),
                        html.Div(
                            className="chart-panel",
                            children=[
                                html.Div(
                                    [
                                        html.H2("Care volume mix"),
                                        html.P("Stroke, IV thrombolysis, and transfer volumes."),
                                    ],
                                    className="panel-heading",
                                ),
                                dcc.Graph(
                                    id="volume-chart", config={"displayModeBar": False}
                                ),
                            ],
                        ),
                    ],
                ),
                html.Section(
                    className="table-panel",
                    children=[
                        html.Div(
                            [
                                html.H2("Hospital detail"),
                                html.P(
                                    "Synthetic AHA GWTG-style metrics for demonstration and planning only."
                                ),
                            ],
                            className="panel-heading",
                        ),
                        dash_table.DataTable(
                            id="hospital-table",
                            page_size=10,
                            sort_action="native",
                            style_as_list_view=True,
                            style_header={
                                "backgroundColor": "#eef3f7",
                                "fontWeight": "700",
                                "border": "0",
                            },
                            style_cell={
                                "fontFamily": "Inter, Segoe UI, Arial, sans-serif",
                                "fontSize": "14px",
                                "padding": "12px 10px",
                                "border": "0",
                                "borderBottom": "1px solid #e4ebf0",
                                "whiteSpace": "normal",
                                "height": "auto",
                                "textAlign": "left",
                            },
                            style_table={"overflowX": "auto"},
                        ),
                    ],
                ),
            ],
        ),
        html.Footer(
            "Data are fabricated for product demonstration. Do not use for clinical, regulatory, or performance reporting.",
            className="footer",
        ),
    ],
)


def filtered_data(quarter_range, regions, hospital_types):
    quarters = sorted(df["quarter"].unique())
    start_idx, end_idx = quarter_range
    selected_quarters = quarters[start_idx : end_idx + 1]

    if not regions:
        regions = sorted(df["region"].unique())
    if not hospital_types:
        hospital_types = sorted(df["hospital_type"].unique())

    return df[
        df["quarter"].isin(selected_quarters)
        & df["region"].isin(regions)
        & df["hospital_type"].isin(hospital_types)
    ].copy()


def weighted_average(group, metric):
    weights = group["stroke_cases"]
    return (group[metric] * weights).sum() / weights.sum()


def metric_unit(metric):
    return "min" if metric in {"door_to_needle", "door_to_imaging"} else "%"


def target_met(metric, value):
    if metric in {"door_to_needle", "door_to_imaging"}:
        return value <= TARGETS[metric]
    return value >= TARGETS[metric]


@callback(
    Output("summary-cards", "children"),
    Output("trend-chart", "figure"),
    Output("region-chart", "figure"),
    Output("volume-chart", "figure"),
    Output("hospital-table", "data"),
    Output("hospital-table", "columns"),
    Input("quarter-range", "value"),
    Input("region-filter", "value"),
    Input("type-filter", "value"),
    Input("metric-filter", "value"),
)
def update_dashboard(quarter_range, regions, hospital_types, metric):
    current = filtered_data(quarter_range, regions, hospital_types)
    metric_name = METRIC_LABELS[metric]
    unit = metric_unit(metric)
    metric_value = weighted_average(current, metric)
    target = TARGETS[metric]
    total_cases = int(current["stroke_cases"].sum())
    total_ivt = int(current["ivt_cases"].sum())
    total_transfers = int(current["transfer_cases"].sum())
    status = "good" if target_met(metric, metric_value) else "watch"

    cards = [
        indicator_card(
            metric_name,
            f"{metric_value:.1f} {unit}",
            f"Sample target: {target} {unit}",
            status,
        ),
        indicator_card(
            "Stroke encounters",
            f"{total_cases:,}",
            f"{total_ivt:,} sample IV thrombolysis cases",
        ),
        indicator_card(
            "Transfers",
            f"{total_transfers:,}",
            "Regional coordination volume",
        ),
        indicator_card(
            "Hospitals represented",
            f"{current['hospital'].nunique()}",
            f"{current['region'].nunique()} Kentucky regions",
        ),
    ]

    trend = (
        current.groupby("quarter", as_index=False)
        .apply(lambda group: pd.Series({"weighted_metric": weighted_average(group, metric)}))
        .reset_index(drop=True)
    )
    trend_fig = px.line(
        trend,
        x="quarter",
        y="weighted_metric",
        markers=True,
        labels={"quarter": "Quarter", "weighted_metric": f"{metric_name} ({unit})"},
        color_discrete_sequence=["#1f6f8b"],
    )
    trend_fig.add_hline(
        y=target,
        line_dash="dash",
        line_color="#b84a39",
        annotation_text=f"Target {target} {unit}",
        annotation_position="top left",
    )
    trend_fig.update_layout(template="plotly_white", margin=dict(l=24, r=20, t=10, b=24))

    regional = (
        current.groupby("region", as_index=False)
        .apply(lambda group: pd.Series({"weighted_metric": weighted_average(group, metric)}))
        .reset_index(drop=True)
        .sort_values("weighted_metric", ascending=metric not in {"door_to_needle", "door_to_imaging"})
    )
    region_fig = px.bar(
        regional,
        x="weighted_metric",
        y="region",
        orientation="h",
        labels={"weighted_metric": f"{metric_name} ({unit})", "region": ""},
        color="weighted_metric",
        color_continuous_scale=["#d4e8ef", "#1f6f8b"],
    )
    region_fig.update_layout(
        template="plotly_white",
        margin=dict(l=12, r=20, t=10, b=24),
        coloraxis_showscale=False,
    )

    volumes = (
        current.groupby("region", as_index=False)[
            ["stroke_cases", "ivt_cases", "transfer_cases"]
        ]
        .sum()
        .melt(
            id_vars="region",
            var_name="volume_type",
            value_name="cases",
        )
    )
    volumes["volume_type"] = volumes["volume_type"].map(
        {
            "stroke_cases": "Stroke cases",
            "ivt_cases": "IVT cases",
            "transfer_cases": "Transfer cases",
        }
    )
    volume_fig = px.bar(
        volumes,
        x="region",
        y="cases",
        color="volume_type",
        barmode="group",
        labels={"region": "", "cases": "Cases", "volume_type": ""},
        color_discrete_sequence=["#24515c", "#d18f3f", "#6b8e6e"],
    )
    volume_fig.update_layout(
        template="plotly_white",
        margin=dict(l=24, r=20, t=10, b=80),
        legend=dict(orientation="h", y=-0.25),
    )

    table = current.copy()
    table["Period"] = table["quarter"]
    table["Stroke cases"] = table["stroke_cases"]
    table["DTN min"] = table["door_to_needle"].round(1)
    table["Imaging min"] = table["door_to_imaging"].round(1)
    table["Discharge antithrombotic %"] = table["discharge_antithrombotic"].round(1)
    table["NIHSS documented %"] = table["nihss_documented"].round(1)
    table = table[
        [
            "Period",
            "region",
            "hospital",
            "hospital_type",
            "Stroke cases",
            "DTN min",
            "Imaging min",
            "Discharge antithrombotic %",
            "NIHSS documented %",
        ]
    ].rename(
        columns={
            "region": "Region",
            "hospital": "Hospital",
            "hospital_type": "Hospital type",
        }
    )
    columns = [{"name": column, "id": column} for column in table.columns]

    return cards, trend_fig, region_fig, volume_fig, table.to_dict("records"), columns


if __name__ == "__main__":
    app.run(debug=True)
