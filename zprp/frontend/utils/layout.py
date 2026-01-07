from dash import dcc, html
import dash_leaflet as dl


def build_analysis_modal():
    return html.Div(
        id="analysis-modal",
        style={
            "display": "none",
            "position": "fixed",
            "inset": 0,
            "background": "rgba(0,0,0,0.45)",
            "alignItems": "center",
            "justifyContent": "center",
            "zIndex": 2000,
        },
        children=[
            html.Div(
                id="analysis-backdrop",
                n_clicks=0,
                style={
                    "position": "absolute",
                    "inset": 0,
                    "background": "rgba(0,0,0,0)",
                },
            ),
            html.Div(
                style={
                    "background": "#fff",
                    "borderRadius": "8px",
                    "boxShadow": "0 10px 30px rgba(0,0,0,.2)",
                    "width": "min(90vw, 760px)",
                    "maxHeight": "85vh",
                    "overflow": "auto",
                    "padding": "16px",
                    "fontFamily": "monospace",
                    "position": "relative",
                    "zIndex": 1,
                },
                children=[
                    html.Div(
                        [
                            html.Div("Analiza", style={"fontWeight": 700, "fontSize": 18}),
                            html.Div(
                                [
                                    html.Button(
                                        "Pobierz wykres (PNG)",
                                        id="download-chart-modal-btn",
                                        style={
                                            "marginRight": 8,
                                            "cursor": "pointer",
                                            "border": "1px solid #ddd",
                                            "background": "#fff",
                                            "padding": "2px 8px",
                                            "borderRadius": "4px",
                                        },
                                    ),
                                    dcc.Download(id="download-chart-modal"),
                                    html.Button(
                                        "✕",
                                        id="analysis-close",
                                        style={
                                            "border": "1px solid #ddd",
                                            "background": "#fff",
                                            "cursor": "pointer",
                                            "padding": "2px 8px",
                                            "borderRadius": "4px",
                                        },
                                    ),
                                ],
                                style={"display": "flex", "alignItems": "center"},
                            ),
                        ],
                        style={
                            "display": "flex",
                            "justifyContent": "space-between",
                            "alignItems": "center",
                            "marginBottom": 12,
                        },
                    ),
                    html.Div(id="modal-prices", style={"marginBottom": 12}),
                    html.Img(
                        id="modal-chart",
                        style={"width": "100%", "border": "1px solid #eee", "borderRadius": "4px"},
                    ),
                ],
            ),
        ],
    )


def build_map(warsaw: dict, area_outside_warsaw: list | None):
    return dl.Map(
        id="leaflet-map",
        center=(warsaw["lat"], warsaw["lon"]),
        zoom=11,
        minZoom=10,
        maxZoom=17,
        dragging=False,
        doubleClickZoom=False,
        scrollWheelZoom=False,
        touchZoom=False,
        boxZoom=False,
        keyboard=False,
        style={"position": "fixed", "inset": 0, "height": "100vh", "width": "100vw"},
        children=[
            dl.TileLayer(),
            (
                dl.Polygon(
                    positions=(area_outside_warsaw or []),
                    pathOptions={
                        "color": "#000",
                        "fillColor": "#000",
                        "fillOpacity": 0.92,
                        "weight": 0,
                    },
                    interactive=False,
                )
                if area_outside_warsaw
                else None
            ),
            dl.LayerGroup(
                id="marker-layer",
                children=[
                    dl.Marker(
                        id="click-marker",
                        position=(warsaw["lat"], warsaw["lon"]),
                        opacity=1,
                        draggable=False,
                    ),
                    dl.CircleMarker(
                        id="click-dot",
                        center=(warsaw["lat"], warsaw["lon"]),
                        radius=7,
                        color="#d33682",
                        fill=True,
                        fillOpacity=0.9,
                        opacity=1,
                    ),
                ],
            ),
        ],
    )


def build_search_bar():
    return html.Div(
        [
            dcc.Input(
                id="addr-input",
                type="text",
                placeholder="Adres w Warszawie…",
                style={"width": 280, "marginRight": 8},
            ),
            html.Button("Szukaj", id="addr-search-btn"),
        ],
        style={
            "position": "fixed",
            "top": 8,
            "right": 8,
            "background": "#fff",
            "padding": "6px 8px",
            "border": "1px solid #ddd",
            "borderRadius": "4px",
            "fontFamily": "monospace",
            "display": "flex",
            "gap": 6,
            "alignItems": "center",
            "zIndex": 1000,
        },
    )


def build_coords_box(warsaw: dict):
    return html.Div(
        f"lat={warsaw['lat']:.6f}, lon={warsaw['lon']:.6f}",
        id="coords",
        style={
            "position": "fixed",
            "bottom": 8,
            "left": 8,
            "background": "#fff",
            "color": "#000",
            "padding": "6px 8px",
            "border": "1px solid #ddd",
            "borderRadius": "4px",
            "fontFamily": "monospace",
            "zIndex": 1000,
        },
    )


def build_analyze_button():
    return html.Button(
        "analizuj",
        id="analyze-btn",
        style={
            "position": "fixed",
            "bottom": 8,
            "right": 8,
            "background": "#fff",
            "padding": "6px 10px",
            "border": "1px solid #ddd",
            "borderRadius": "4px",
            "cursor": "pointer",
            "zIndex": 1000,
        },
    )


def create_layout(
    warsaw: dict,
    area_outside_warsaw: list | None,
):
    rings = []
    if area_outside_warsaw and len(area_outside_warsaw) > 1:
        rings = area_outside_warsaw[1:]

    layout = html.Div(
        [
            dcc.Store(id="mask-rings", data=rings),
            dcc.Store(id="clicked-point", data={"lat": warsaw["lat"], "lon": warsaw["lon"]}),
            dcc.Store(id="prices-raw"),
            dcc.Store(id="chart-b64"),
            build_analysis_modal(),
            build_map(warsaw, area_outside_warsaw),
            build_search_bar(),
            build_coords_box(warsaw),
            build_analyze_button(),
        ]
    )

    return layout
