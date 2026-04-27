import pandas as pd

from ..config import TARGETS


TIMED_METRICS = {"door_to_needle", "door_to_imaging"}


def filter_data(
    frame: pd.DataFrame,
    quarter_range: list[int],
    regions: list[str] | None,
    hospital_types: list[str] | None,
) -> pd.DataFrame:
    quarters = sorted(frame["quarter"].unique())
    start_idx, end_idx = quarter_range
    selected_quarters = quarters[start_idx : end_idx + 1]

    selected_regions = regions or sorted(frame["region"].unique())
    selected_types = hospital_types or sorted(frame["hospital_type"].unique())

    return frame[
        frame["quarter"].isin(selected_quarters)
        & frame["region"].isin(selected_regions)
        & frame["hospital_type"].isin(selected_types)
    ].copy()


def weighted_average(group: pd.DataFrame, metric: str) -> float:
    weights = group["stroke_cases"]
    return (group[metric] * weights).sum() / weights.sum()


def metric_unit(metric: str) -> str:
    return "min" if metric in TIMED_METRICS else "%"


def target_met(metric: str, value: float) -> bool:
    if metric in TIMED_METRICS:
        return value <= TARGETS[metric]
    return value >= TARGETS[metric]
