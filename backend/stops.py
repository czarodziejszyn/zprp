# tourism.py
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import httpx
import os


API_KEY = os.getenv("WARSZAWA_API_KEY")
if not API_KEY:
    raise RuntimeError("Missing WARSZAWA_API_KEY. Add it to .env or system env.")

# Endpoint
BASE_URL = "https://api.um.warszawa.pl/api/action/dbtimetable_get/"
STOPS_RESOURCE_ID = "ab75c33d-3a26-4342-b36a-6e5fef0a3ac3"

class Stop(BaseModel):
    set_id: str | None = None
    stop_post: str | None = None
    set_name: str | None = None
    latitude: float | None = None
    longitude: float | None = None

app = FastAPI(title="Warsaw Public Transport API")
async def fetch_stops(limit: int = 10):
    params = {"id": STOPS_RESOURCE_ID}
    headers = {"Cache-Control": "no-cache"}

    async with httpx.AsyncClient(timeout=20, follow_redirects=True) as client:
        response = await client.get(BASE_URL, params=params, headers=headers)

    print("Raw API response:", response.text)

    try:
        data = response.json()
    except Exception:
        raise HTTPException(status_code=500, detail=f"API returned non-JSON: {response.text}")

    if response.status_code != 200 or "result" not in data:
        raise HTTPException(status_code=500, detail=f"API error: {data.get('result', response.text)}")

    stops = []
    for item in data["result"]:
        values = {v["key"]: v["value"] for v in item.get("values", [])}

        stops.append(Stop(
            set_id=values.get("zespol"),
            slupek=values.get("slupek"),
            nazwa_zespolu=values.get("nazwa_zespolu"),
            latitude=float(values.get("szer_geo")) if values.get("szer_geo") else None,
            longitude=float(values.get("dlug_geo")) if values.get("dlug_geo") else None
        ))

    return stops

@app.get("/stops", response_model=list[Stop])
async def get_stops(limit: int = Query(10, ge=1, le=500)):
    """
    Get a list of Warsaw public transport stops (up to `limit`).
    """
    return await fetch_stops(limit=limit)