# tourism.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
import os


API_KEY = os.getenv("WARSZAWA_API_KEY")
if not API_KEY:
    raise RuntimeError("Missing WARSZAWA_API_KEY. Add it to .env or system env.")

# Endpoint
BASE_URL = "https://api.um.warszawa.pl/api/action/tourism_attraction_get/"


class Attraction(BaseModel):
    latitude: float | None = None
    longitude: float | None = None




async def fetch_attractions():
    params = {"apikey": API_KEY}

    async with httpx.AsyncClient(timeout=10, follow_redirects=True) as client:
        response = await client.get(BASE_URL, params=params)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail=f"Warsaw API error: {response.status_code}")

    data = response.json()
    result_list = data.get("result", [])

    attractions = []
    for t in result_list:
        latlng = t.get("latlng", {})
        attractions.append(Attraction(
            latitude=float(latlng.get("lat")) if latlng.get("lat") else None,
            longitude=float(latlng.get("lng")) if latlng.get("lng") else None
        ))

    return attractions

