from datetime import date

import pandas as pd
from dash import dcc, html

from ..config import (
    APP_TITLE,
    FOOTER_NOTE,
    HEADER_BADGE_LABEL,
    HEADER_DESCRIPTION,
    HEADER_EYEBROW,
)
from .components import control_panel
from .tables import hospital_table


def build_layout(frame: pd.DataFrame):
    return html.Div(
        className="page",
        children=[
            html.Header(
                className="header",
                children=[
                    html.Div(
                        [
                            html.P(HEADER_EYEBROW, className="eyebrow"),
                            html.H1(APP_TITLE),
                            html.P(HEADER_DESCRIPTION),
                        ],
                        className="header-copy",
                    ),
                    html.Div(
                        [
                            html.Span(HEADER_BADGE_LABEL, className="data-badge"),
                            html.Span(f"Generated {date.today().isoformat()}"),
                        ],
                        className="header-meta",
                    ),
                ],
            ),
            html.Main(
                [
                    control_panel(frame),
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
                                    dcc.Graph(
                                        id="trend-chart",
                                        config={"displayModeBar": False},
                                    ),
                                ],
                            ),
                            html.Div(
                                className="chart-panel",
                                children=[
                                    html.Div(
                                        [
                                            html.H2("Regional comparison"),
                                            html.P(
                                                "Current filtered period, case-weighted averages."
                                            ),
                                        ],
                                        className="panel-heading",
                                    ),
                                    dcc.Graph(
                                        id="region-chart",
                                        config={"displayModeBar": False},
                                    ),
                                ],
                            ),
                            html.Div(
                                className="chart-panel",
                                children=[
                                    html.Div(
                                        [
                                            html.H2("Care volume mix"),
                                            html.P(
                                                "Stroke, IV thrombolysis, and transfer volumes."
                                            ),
                                        ],
                                        className="panel-heading",
                                    ),
                                    dcc.Graph(
                                        id="volume-chart",
                                        config={"displayModeBar": False},
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
                            hospital_table(),
                        ],
                    ),
                ]
            ),
            html.Footer(FOOTER_NOTE, className="footer"),
        ],
    )
