from pathlib import Path

from dash import Dash

from .callbacks.dashboard import register_dashboard_callbacks
from .config import APP_TITLE
from .data.sample import build_sample_data
from .ui.layout import build_layout


ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"


def create_app() -> Dash:
    app = Dash(__name__, title=APP_TITLE, assets_folder=str(ASSETS_DIR))
    data = build_sample_data()

    app.layout = build_layout(data)
    register_dashboard_callbacks(app, data)

    return app
