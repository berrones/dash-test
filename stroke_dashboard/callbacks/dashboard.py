import pandas as pd
from dash import Input, Output

from ..config import METRIC_LABELS, TARGETS
from ..services.metrics import filter_data, metric_unit, target_met, weighted_average
from ..ui.components import indicator_card
from ..ui.figures import build_region_figure, build_trend_figure, build_volume_figure
from ..ui.tables import build_hospital_table_payload


def register_dashboard_callbacks(app, frame: pd.DataFrame) -> None:
    @app.callback(
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
        current = filter_data(frame, quarter_range, regions, hospital_types)
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
                f"Target threshold: {target} {unit}",
                status,
                featured=True,
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

        trend_chart = build_trend_figure(current, metric, metric_name, unit, target)
        region_chart = build_region_figure(current, metric, metric_name, unit)
        volume_chart = build_volume_figure(current)
        table_data, columns = build_hospital_table_payload(current)

        return cards, trend_chart, region_chart, volume_chart, table_data, columns
