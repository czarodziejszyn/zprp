from dash import callback, Output, Input, State, no_update
import dash
import httpx


def _point_in_ring(lat: float, lon: float, ring_latlng):
    if not ring_latlng or len(ring_latlng) < 3:
        return False
    x = float(lon)
    y = float(lat)
    inside = False
    j = len(ring_latlng) - 1
    for i in range(len(ring_latlng)):
        yi = float(ring_latlng[i][0]); xi = float(ring_latlng[i][1])
        yj = float(ring_latlng[j][0]); xj = float(ring_latlng[j][1])
        intersects = ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / ((yj - yi) if (yj - yi) != 0 else 1e-12) + xi)
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
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0] if ctx and ctx.triggered else None

    latlng_pair = None
    if trigger_id == "addr-search-btn" and n_addr_clicks and addr_value:
        latlng_pair = _geocode_address_to_city_latlon(addr_value, mask_rings)
    elif trigger_id == "leaflet-map":
        latlng_pair = _from_dblclick(dblclick_data)
    if not latlng_pair:
        return no_update, no_update, no_update, no_update, no_update, no_update
    lat, lon = latlng_pair
    if not _point_in_city(lat, lon, mask_rings):
        return no_update, no_update, no_update, no_update, no_update, no_update
    return [lat, lon], 1, [lat, lon], 1, f"lat={lat:.6f}, lon={lon:.6f}", {"lat": lat, "lon": lon}


