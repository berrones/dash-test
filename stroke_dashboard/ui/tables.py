import pandas as pd
from dash import dash_table


TABLE_HEADER_STYLE = {
    "backgroundColor": "#111826",
    "color": "#f7fafc",
    "fontWeight": "700",
    "border": "0",
}

TABLE_CELL_STYLE = {
    "backgroundColor": "#08111d",
    "color": "#d6deeb",
    "fontFamily": "Trebuchet MS, Arial Nova, Segoe UI, sans-serif",
    "fontSize": "14px",
    "padding": "12px 10px",
    "border": "0",
    "borderBottom": "1px solid #16263b",
    "whiteSpace": "normal",
    "height": "auto",
    "textAlign": "left",
}

TABLE_DATA_CONDITIONAL = [
    {
        "if": {"row_index": "odd"},
        "backgroundColor": "#0c1524",
    }
]


def hospital_table():
    return dash_table.DataTable(
        id="hospital-table",
        page_size=10,
        sort_action="native",
        style_as_list_view=True,
        style_header=TABLE_HEADER_STYLE,
        style_cell=TABLE_CELL_STYLE,
        style_data_conditional=TABLE_DATA_CONDITIONAL,
        style_table={"overflowX": "auto"},
    )


def build_hospital_table_payload(frame: pd.DataFrame):
    table = frame.copy()
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
    return table.to_dict("records"), columns
