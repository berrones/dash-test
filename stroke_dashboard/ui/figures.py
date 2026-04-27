import pandas as pd
import plotly.express as px

from ..services.metrics import TIMED_METRICS, weighted_average


def apply_dark_figure_theme(fig):
    fig.update_layout(
        template=None,
        paper_bgcolor="#0a1220",
        plot_bgcolor="#0a1220",
        font=dict(color="#e8edf5", family="Trebuchet MS, Arial Nova, Segoe UI, sans-serif"),
        margin=dict(l=24, r=20, t=10, b=24),
    )
    fig.update_xaxes(
        showgrid=True,
        gridcolor="rgba(163, 189, 214, 0.12)",
        zeroline=False,
        linecolor="rgba(163, 189, 214, 0.24)",
        tickfont=dict(color="#a7b6c8"),
        title_font=dict(color="#cfd8e3"),
    )
    fig.update_yaxes(
        showgrid=True,
        gridcolor="rgba(163, 189, 214, 0.12)",
        zeroline=False,
        linecolor="rgba(163, 189, 214, 0.24)",
        tickfont=dict(color="#a7b6c8"),
        title_font=dict(color="#cfd8e3"),
    )
    return fig


def build_trend_figure(
    frame: pd.DataFrame,
    metric: str,
    metric_name: str,
    unit: str,
    target: float,
):
    trend = (
        frame.groupby("quarter")
        .apply(lambda group: weighted_average(group, metric))
        .rename("weighted_metric")
        .reset_index()
    )
    fig = px.line(
        trend,
        x="quarter",
        y="weighted_metric",
        markers=True,
        labels={"quarter": "Quarter", "weighted_metric": f"{metric_name} ({unit})"},
        color_discrete_sequence=["#6ee7ff"],
    )
    fig.add_hline(
        y=target,
        line_dash="dash",
        line_color="#ff7b72",
        annotation_text=f"Target {target} {unit}",
        annotation_position="top left",
    )
    fig.update_traces(line=dict(width=5), marker=dict(size=11))
    return apply_dark_figure_theme(fig)


def build_region_figure(
    frame: pd.DataFrame,
    metric: str,
    metric_name: str,
    unit: str,
):
    regional = (
        frame.groupby("region")
        .apply(lambda group: weighted_average(group, metric))
        .rename("weighted_metric")
        .reset_index()
        .sort_values("weighted_metric", ascending=metric not in TIMED_METRICS)
    )
    fig = px.bar(
        regional,
        x="weighted_metric",
        y="region",
        orientation="h",
        labels={"weighted_metric": f"{metric_name} ({unit})", "region": ""},
        color="weighted_metric",
        color_continuous_scale=["#12304d", "#6ee7ff"],
    )
    fig.update_traces(marker_line_color="#08111d", marker_line_width=1.4)
    fig = apply_dark_figure_theme(fig)
    fig.update_layout(margin=dict(l=12, r=20, t=10, b=24), coloraxis_showscale=False)
    return fig


def build_volume_figure(frame: pd.DataFrame):
    volumes = (
        frame.groupby("region", as_index=False)[
            ["stroke_cases", "ivt_cases", "transfer_cases"]
        ]
        .sum()
        .melt(id_vars="region", var_name="volume_type", value_name="cases")
    )
    volumes["volume_type"] = volumes["volume_type"].map(
        {
            "stroke_cases": "Stroke cases",
            "ivt_cases": "IVT cases",
            "transfer_cases": "Transfer cases",
        }
    )
    fig = px.bar(
        volumes,
        x="region",
        y="cases",
        color="volume_type",
        barmode="group",
        labels={"region": "", "cases": "Cases", "volume_type": ""},
        color_discrete_sequence=["#6ee7ff", "#ffb347", "#93f5a3"],
    )
    fig.update_traces(marker_line_color="#08111d", marker_line_width=1.1)
    fig = apply_dark_figure_theme(fig)
    fig.update_layout(
        margin=dict(l=24, r=20, t=10, b=80),
        legend=dict(orientation="h", y=-0.25),
    )
    return fig
