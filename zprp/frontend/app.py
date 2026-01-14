import json
import os

from dash import Dash
from utils.layout import create_layout

WARSAW_CENTER = {"lat": 52.2297, "lon": 21.0122}
WORLD_RECT = [
    [-89.9, -179.9],
    [89.9, -179.9],
    [89.9, 179.9],
    [-89.9, 179.9],
    [-89.9, -179.9],
]
WARSAW_BORDER_PATH = os.path.join(
    os.path.normpath(os.path.join(os.path.dirname(__file__), "utils")),
    "warsaw.json",
)


def generate_layout():
    with open(WARSAW_BORDER_PATH, "r", encoding="utf-8") as _rf:
        warsaw_border = json.load(_rf).get("rings_latlng", [])

    area_outside_warsaw = [WORLD_RECT] + warsaw_border
    return create_layout(WARSAW_CENTER, area_outside_warsaw)


if __name__ == "__main__":
    app = Dash(__name__, suppress_callback_exceptions=True, title="ZPRP Frontend")
    app.layout = generate_layout()
    app.run(debug=False)
