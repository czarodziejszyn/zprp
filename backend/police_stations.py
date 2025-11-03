from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import httpx
import os

API_KEY = os.getenv("WARSZAWA_API_KEY")
if not API_KEY:
    raise RuntimeError("Missing WARSZAWA_API_KEY. Add it to .env or system env.")

POLICE_RESOURCE_ID = "85f567f1-bb56-4657-a30e-afd80544fc7f"
BASE_URL = "https://api.um.warszawa.pl/api/action/wfsstore_get"

class PoliceStation(BaseModel):
    name: str | None = None
    district: str | None = None
    latitude: float | None = None
    longitude: float | None = None

app = FastAPI(title="Warsaw Police Stations API")

async def fetch_police_stations(limit: int = 10):
    params = {
        "id": POLICE_RESOURCE_ID,
        "limit": limit,
        "apikey": API_KEY
    }

    async with httpx.AsyncClient(timeout=httpx.Timeout(60.0, connect=20.0), follow_redirects=True) as client:
        try:
            response = await client.get(BASE_URL, params=params)
        except httpx.ReadTimeout:
            raise HTTPException(status_code=504, detail="API request timed out")

    data = response.json()

    result = data.get("result")
    if not result:
        raise HTTPException(status_code=404, detail="No result field in API response")

    feature_list = result.get("featureMemberList", [])
    if not feature_list:
        raise HTTPException(status_code=404, detail="No police station data found")

    stations = []
    for item in feature_list:
        coords_list = item.get("geometry", {}).get("coordinates", [])
        lat = lon = None
        if coords_list and isinstance(coords_list, list):
            coord = coords_list[0]
            lat = float(coord.get("latitude")) if coord.get("latitude") else None
            lon = float(coord.get("longitude")) if coord.get("longitude") else None

        props = {p["key"]: p["value"] for p in item.get("properties", [])}

        stations.append(PoliceStation(
            name=props.get("OPIS"),
            district=props.get("DZIELNICA"),
            latitude=lat,
            longitude=lon
        ))

    return stations

@app.get("/police_stations", response_model=list[PoliceStation])
async def get_police_stations(limit: int = Query(10, ge=1, le=200)):
    return await fetch_police_stations(limit=limit)
