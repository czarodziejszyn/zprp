from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import httpx
import os

API_KEY = os.getenv("WARSZAWA_API_KEY")
if not API_KEY:
    raise RuntimeError("Missing WARSZAWA_API_KEY. Add it to .env or system env.")


RESOURCE_ID = "a08136ec-1037-4029-9aa5-b0d0ee0b9d88"

BASE_URL = "https://api.um.warszawa.pl/api/action/wfsstore_get"

class BikeStation(BaseModel):
    latitude: float | None = None
    longitude: float | None = None


async def fetch_bike_stations():
    resource_id = RESOURCE_ID

    params = {"id": resource_id, "apikey": API_KEY}

    async with httpx.AsyncClient(timeout=httpx.Timeout(60.0, connect=20.0), follow_redirects=True) as client:
        try:
            response = await client.get(BASE_URL, params=params)
        except httpx.ReadTimeout:
            raise HTTPException(status_code=504, detail="API request timed out")


    try:
        data = response.json()
    except Exception:
        raise HTTPException(status_code=500, detail=f"API returned non-JSON: {response.text}")

    if "result" not in data or "featureMemberList" not in data["result"]:
        raise HTTPException(status_code=500, detail="API returned unexpected structure")

    stations = []

    for item in data["result"]["featureMemberList"]:
        coords = item.get("geometry", {}).get("coordinates", [{}])[0]

        stations.append(BikeStation(
            latitude=float(coords.get("latitude")) if coords.get("latitude") else None,
            longitude=float(coords.get("longitude")) if coords.get("longitude") else None
        ))

    return stations
