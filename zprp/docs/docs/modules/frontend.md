# Frontend (Dash)

This module is a Dash + dash-leaflet web UI for selecting a point in Warsaw and showing analysis results (prices + chart) in a modal.

## Quickstart

From the `zprp/` directory:

```bash
make frontend_setup
make frontend_run
```

Open: `http://127.0.0.1:8050`

## Configuration

The frontend calls the backend using `BACKEND_BASE_URL`:

- default: `http://localhost:8000`
- override example:

```bash
BACKEND_BASE_URL=http://127.0.0.1:8000 make frontend_run
```

## Main user flow

1) User selects a point (map click/double click) or searches an address.
2) The UI updates the marker and the "lat/lon" box.
3) User clicks "analyze".
4) Frontend calls backend endpoints:
   - `GET /prices?lat=...&lon=...`
   - `GET /chart`
5) Modal opens in the center of the screen:
   - shows predicted and real price (formatted as PLN)
   - shows chart image
   - allows PNG download
6) Modal can be closed via X button or click outside.

## Code layout

Key files:

- `zprp/frontend/app.py`
  - Dash app entrypoint
  - loads Warsaw border rings (`utils/warsaw.json`) and builds the "outside Warsaw" mask

- `zprp/frontend/utils/layout.py`
  - UI composition (map, modal, search, coords, analyze button)
  - important component ids used by callbacks and tests:
    - `leaflet-map`, `click-marker`, `click-dot`
    - `addr-input`, `addr-search-btn`
    - `coords`, `analyze-btn`
    - `analysis-modal`, `analysis-close`, `analysis-backdrop`
    - `modal-prices`, `modal-chart`
    - `download-chart-modal-btn`, `download-chart-modal`

- `zprp/frontend/utils/callbacks.py`
  - map click handling and Warsaw boundary check (PIP)
  - address geocoding (Nominatim)
  - analysis modal logic (calls `/prices` and `/chart`)
  - PNG download callback

## Warsaw boundary check (PIP)

Warsaw border is represented as a list of rings (lat/lon pairs).

- `_point_in_ring(lat, lon, ring_latlng)` implements ray-casting point-in-polygon
- `_point_in_city(lat, lon, rings)` checks if point is inside any ring

If the click is outside Warsaw, the marker and coordinates are not updated.

## Address search

Address search uses Nominatim:

- `https://nominatim.openstreetmap.org/search`

The first result that falls inside Warsaw rings is accepted.

## Analysis modal

When user clicks "analyze":

- `/prices` is called with `params={"lat": ..., "lon": ...}`
  - on HTTP 200: JSON is rendered as two price tiles (predicted + real)
  - otherwise: modal shows an error string (HTTP status or connection error)
- `/chart` is called
  - on HTTP 200: PNG bytes are base64-encoded and inserted into `img#modal-chart`

Download button:

- reads base64 from `dcc.Store(id="chart-b64")`
- downloads `chart.png` via `dcc.Download`

## E2E tests (Playwright)

Run:

```bash
make frontend_test
```

Notes:

- `make frontend_test` starts a local mock backend for `/prices` and `/chart` so tests do not require a real backend.
- e2e tests are in `zprp/frontend/tests/e2e/`:
  - `test_smoke.py` - basic UI loads
  - `test_search_and_marker.py` - address search updates coords
  - `test_clicks.py` - blocking outside Warsaw
  - `test_analyze_modal.py` - modal open/close
  - `test_download_png.py` - download PNG works
  - `test_errors.py` - error message when `/prices` returns 500


