import base64
import json as _json

import dash
from dash import Input, Output, State, callback, dcc, html, no_update
import httpx


def _point_in_ring(lat: float, lon: float, ring_latlng):
    if not ring_latlng or len(ring_latlng) < 3:
        return False
    x = float(lon)
    y = float(lat)
    inside = False
    j = len(ring_latlng) - 1
    for i in range(len(ring_latlng)):
        yi = float(ring_latlng[i][0])
        xi = float(ring_latlng[i][1])
        yj = float(ring_latlng[j][0])
        xj = float(ring_latlng[j][1])
        intersects = ((yi > y) != (yj > y)) and (
            x < (xj - xi) * (y - yi) / ((yj - yi) if (yj - yi) != 0 else 1e-12) + xi
        )
        if intersects:
            inside = not inside
        j = i
    return inside


def _point_in_city(lat: float, lon: float, rings) -> bool:
    rings = rings or []
    for ring in rings:
        if _point_in_ring(lat, lon, ring):
            return True
    return False


NOMINATIM_HEADERS = {
    "User-Agent": "ZPRP-Frontend/0.1 (search)",
    "Accept-Language": "pl,en;q=0.8",
}


def _geocode_address_to_city_latlon(query: str, rings):
    if not query or not isinstance(query, str):
        return None
    q_list = [f"{query}, Warszawa", query]
    for q in q_list:
        try:
            r = httpx.get(
                "https://nominatim.openstreetmap.org/search",
                params={
                    "q": q,
                    "format": "jsonv2",
                    "limit": 5,
                    "countrycodes": "pl",
                },
                headers=NOMINATIM_HEADERS,
                timeout=15.0,
            )
            if r.status_code != 200:
                continue
            items = r.json() or []
            for it in items:
                try:
                    lat = float(it.get("lat"))
                    lon = float(it.get("lon"))
                except Exception:
                    continue
                if _point_in_city(lat, lon, rings):
                    return [lat, lon]
        except httpx.HTTPError:
            continue
    return None


@callback(
    Output("click-marker", "position"),
    Output("click-marker", "opacity"),
    Output("click-dot", "center"),
    Output("click-dot", "opacity"),
    Output("coords", "children"),
    Output("clicked-point", "data"),
    Input("leaflet-map", "click_lat_lng"),
    Input("leaflet-map", "dblclickData"),
    Input("addr-search-btn", "n_clicks"),
    State("addr-input", "value"),
    State("mask-rings", "data"),
    prevent_initial_call=True,
)
def handle_click(click_latlng, dblclick_data, n_addr_clicks, addr_value, mask_rings):
    def _pair(val):
        if val is None:
            return None
        if isinstance(val, dict):
            lat = val.get("lat") or val.get("latitude")
            lon = val.get("lng") or val.get("lon") or val.get("longitude")
            if lat is not None and lon is not None:
                return [float(lat), float(lon)]
            return None
        if isinstance(val, (list, tuple)) and len(val) == 2:
            return [float(val[0]), float(val[1])]
        return None

    def _from_dblclick(data):
        if data is None:
            return None
        if isinstance(data, dict):
            cand = data.get("latlng") or data.get("latLng") or data.get("lat_lng") or data
            return _pair(cand)
        return None

    ctx = dash.callback_context
    trigger_prop = ctx.triggered[0]["prop_id"] if ctx and ctx.triggered else ""
    trigger_id = trigger_prop.split(".")[0] if trigger_prop else None
    trigger_attr = trigger_prop.split(".")[1] if trigger_prop and "." in trigger_prop else None

    latlng_pair = None
    if trigger_id == "addr-search-btn" and n_addr_clicks and addr_value:
        latlng_pair = _geocode_address_to_city_latlon(addr_value, mask_rings)
    elif trigger_id == "leaflet-map" and trigger_attr == "click_lat_lng":
        latlng_pair = _pair(click_latlng)
    elif trigger_id == "leaflet-map" and trigger_attr == "dblclickData":
        latlng_pair = _from_dblclick(dblclick_data)
    if not latlng_pair:
        return no_update, no_update, no_update, no_update, no_update, no_update
    lat, lon = latlng_pair
    if not _point_in_city(lat, lon, mask_rings):
        return no_update, no_update, no_update, no_update, no_update, no_update
    return [lat, lon], 1, [lat, lon], 1, f"lat={lat:.6f}, lon={lon:.6f}", {"lat": lat, "lon": lon}


@callback(
    Output("modal-prices", "children"),
    Output("modal-chart", "src"),
    Output("prices-raw", "data"),
    Output("chart-b64", "data"),
    Output("analysis-modal", "style"),
    Input("analyze-btn", "n_clicks"),
    Input("analysis-close", "n_clicks"),
    Input("analysis-backdrop", "n_clicks"),
    State("clicked-point", "data"),
    prevent_initial_call=True,
)
def analyze_point(analyze_clicks, close_clicks, backdrop_clicks, clicked_point):
    ctx = dash.callback_context
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0] if ctx and ctx.triggered else None
    closed = {"display": "none", "position": "fixed", "inset": 0}

    if trigger_id in ("analysis-close", "analysis-backdrop"):
        return no_update, no_update, no_update, no_update, closed

    if not analyze_clicks:
        return no_update, no_update, no_update, no_update, no_update

    try:
        if not isinstance(clicked_point, dict):
            return "Brak punktu.", no_update, None, None, closed
        lat = float(clicked_point.get("lat"))
        lon = float(clicked_point.get("lon"))
    except Exception:
        return "Nieprawidłowe współrzędne.", no_update, None, None, closed

    prices_raw = None
    chart_b64 = None
    chart_src = None
    modal_prices_children = "Brak danych."

    # /prices
    try:
        r = httpx.get(
            "http://localhost:8000/prices", params={"lat": lat, "lon": lon}, timeout=20.0
        )
        if r.status_code == 200:
            data = r.json()
            prices_raw = _json.dumps(data, ensure_ascii=False, indent=2)
            pred = data.get("predicted_price")
            real = data.get("real_price")

            def _fmt_pln(v):
                try:
                    val = float(v)
                    s = f"{val:,.0f}".replace(",", " ")
                    return f"{s} zł"
                except Exception:
                    return str(v)

            pred_txt = _fmt_pln(pred)
            real_txt = _fmt_pln(real)
            modal_prices_children = html.Div(
                [
                    html.Div("Ceny", style={"fontWeight": 700, "marginBottom": 6, "fontSize": 14}),
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Div("Prognoza", style={"fontSize": 12, "color": "#555"}),
                                    html.Div(pred_txt, style={"fontWeight": 700, "fontSize": 20}),
                                ],
                                style={
                                    "flex": 1,
                                    "background": "#f7f7f9",
                                    "border": "1px solid #eee",
                                    "borderRadius": "6px",
                                    "padding": "8px 10px",
                                },
                            ),
                            html.Div(
                                [
                                    html.Div(
                                        "Rzeczywista", style={"fontSize": 12, "color": "#555"}
                                    ),
                                    html.Div(real_txt, style={"fontWeight": 700, "fontSize": 20}),
                                ],
                                style={
                                    "flex": 1,
                                    "background": "#f7f7f9",
                                    "border": "1px solid #eee",
                                    "borderRadius": "6px",
                                    "padding": "8px 10px",
                                },
                            ),
                        ],
                        style={"display": "flex", "gap": 12},
                    ),
                ]
            )
        else:
            modal_prices_children = f"Błąd /prices: HTTP {r.status_code}"
            prices_raw = modal_prices_children
    except httpx.HTTPError as e:
        modal_prices_children = f"Błąd połączenia z /prices: {e}"
        prices_raw = modal_prices_children

    # /chart
    try:
        r2 = httpx.get("http://localhost:8000/chart", timeout=20.0)
        if r2.status_code == 200 and r2.content:
            b64 = base64.b64encode(r2.content).decode("ascii")
            chart_src = f"data:image/png;base64,{b64}"
            chart_b64 = b64
    except httpx.HTTPError:
        pass

    open_style = {
        "display": "flex",
        "position": "fixed",
        "inset": 0,
        "background": "rgba(0,0,0,0.45)",
        "alignItems": "center",
        "justifyContent": "center",
        "zIndex": 2000,
    }

    return modal_prices_children, chart_src, prices_raw, chart_b64, open_style


@callback(
    Output("download-chart-modal", "data"),
    Input("download-chart-modal-btn", "n_clicks"),
    State("chart-b64", "data"),
    prevent_initial_call=True,
)
def download_chart_modal(n, b64_data):
    if not n or not b64_data:
        return no_update
    try:
        content = base64.b64decode(b64_data)
    except Exception:
        return no_update
    return dcc.send_bytes(lambda buf: buf.write(content), "chart.png")
