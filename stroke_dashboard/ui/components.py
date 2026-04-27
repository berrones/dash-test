import pandas as pd
from dash import dcc, html

from ..config import METRIC_LABELS


def indicator_card(
    label: str,
    value: str,
    detail: str,
    status: str = "neutral",
    featured: bool = False,
):
    return html.Div(
        className=f"kpi-card {'featured' if featured else ''} {status}".strip(),
        children=[
            html.Div(label, className="kpi-label"),
            html.Div(value, className="kpi-value"),
            html.Div(detail, className="kpi-detail"),
        ],
    )


def control_panel(frame: pd.DataFrame):
    quarters = sorted(frame["quarter"].unique())
    regions = sorted(frame["region"].unique())
    hospital_types = sorted(frame["hospital_type"].unique())

    return html.Div(
        className="control-panel",
        children=[
            html.Div(
                [
                    html.Label("Quarter range", htmlFor="quarter-range"),
                    dcc.RangeSlider(
                        id="quarter-range",
                        min=0,
                        max=len(quarters) - 1,
                        value=[0, len(quarters) - 1],
                        marks={idx: label for idx, label in enumerate(quarters)},
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
                        options=[{"label": region, "value": region} for region in regions],
                        value=regions,
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
                            for hospital_type in hospital_types
                        ],
                        value=hospital_types,
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
