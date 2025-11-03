from dash import html, dcc
import dash_leaflet as dl
import utils.callbacks


def create_layout(
    warsaw: dict,
    area_outside_warsaw: list | None,
):
    rings = []
    if area_outside_warsaw and len(area_outside_warsaw) > 1:
        rings = area_outside_warsaw[1:]

    layout = html.Div([
        dcc.Store(id="mask-rings", data=rings),
        dcc.Store(id="clicked-point", data={"lat": warsaw["lat"], "lon": warsaw["lon"]}),
                dl.Map(
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
                        (dl.Polygon(
                    positions=(area_outside_warsaw or []),
                    pathOptions={"color": "#000", "fillColor": "#000", "fillOpacity": 0.92, "weight": 0},
                    interactive=False,
                ) if area_outside_warsaw else None),
                dl.LayerGroup(id="marker-layer", children=[
                    dl.Marker(id="click-marker", position=(warsaw["lat"], warsaw["lon"]), opacity=1, draggable=False),
                    dl.CircleMarker(id="click-dot", center=(warsaw["lat"], warsaw["lon"]), radius=7, color="#d33682", fill=True, fillOpacity=0.9, opacity=1)
                ]),
            ],
        ),
        html.Div([
            dcc.Input(id="addr-input", type="text", placeholder="Adres w Warszawie…", style={"width": 280, "marginRight": 8}),
            html.Button("Szukaj", id="addr-search-btn")
        ], style={"position": "fixed", "top": 8, "right": 8, "background": "#fff", "padding": "6px 8px", "border": "1px solid #ddd", "borderRadius": "4px", "fontFamily": "monospace", "display": "flex", "gap": 6, "alignItems": "center", "zIndex": 1000}),
        html.Div(
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
        ),
        html.Button(
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
        ),
    ])

    return layout


