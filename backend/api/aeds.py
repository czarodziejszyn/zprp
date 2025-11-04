# aeds.py
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import httpx
import os

API_KEY = os.getenv("WARSZAWA_API_KEY")
if not API_KEY:
    raise RuntimeError("Missing WARSZAWA_API_KEY. Add it to .env or system env.")

BASE_URL = "https://api.um.warszawa.pl/api/action/aed_get"


class AEDs(BaseModel):
    street: str | None = None
    building: str | None = None
    latitude: float | None = None
    longitude: float | None = None



async def fetch_aeds(limit: int = 10):
    params = {"apikey": API_KEY, "limit": limit}

    async with httpx.AsyncClient(timeout=httpx.Timeout(60.0, connect=20.0), follow_redirects=True) as client:
        try:
            response = await client.get(BASE_URL, params=params)
        except httpx.ReadTimeout:
            raise HTTPException(status_code=504, detail="API request timed out")

    data = response.json()

    # Handle different possible response structures
    if isinstance(data, dict):
        # format: {"result":[...]}
        data = data.get("result", [])
    elif not isinstance(data, list):
        raise HTTPException(status_code=500, detail="Unexpected API data format")

    if not data:
        raise HTTPException(status_code=404, detail="No AED data found")

    aeds = []
    for item in data:
        coords = item.get("geometry", {}).get("coordinates", None)
        lat = lon = None

        # Coordinates = [[lon, lat]]
        if coords and isinstance(coords, list) and len(coords[0]) == 2:
            lon, lat = coords[0]
            lat = float(lat)
            lon = float(lon)

        props = item.get("properties", {})

        aeds.append(AEDs(
            street=props.get("location_street"),
            building=props.get("location_building"),
            latitude=lat,
            longitude=lon
        ))

    return aeds
