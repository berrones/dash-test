import math

import pandas as pd

from ..config import REGIONS


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
                        "hospital_type": (
                            "Comprehensive Stroke Center"
                            if hospital_idx == 0
                            else "Primary/Acute Stroke Ready"
                        ),
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

    frame = pd.DataFrame(rows)
    percentage_cols = [
        "discharge_antithrombotic",
        "dysphagia_screen",
        "nihss_documented",
        "transfer_acceptance",
    ]
    frame[percentage_cols] = frame[percentage_cols].clip(upper=99.2)
    return frame
