from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import httpx
import os


API_KEY = os.getenv("WARSZAWA_API_KEY")
if not API_KEY:
    raise RuntimeError("Missing WARSZAWA_API_KEY. Add it to .env or system env.")

# Endpoint and resource
BASE_URL = "https://api.um.warszawa.pl/api/action/wfsstore_get/"
THEATRES_RESOURCE_ID = "e26218cb-61ec-4ccb-81cc-fd19a6fee0f8"


class Theatre(BaseModel):
    latitude: float | None = None
    longitude: float | None = None


async def fetch_theatres():
    params = {
        "id": THEATRES_RESOURCE_ID,
        "apikey": API_KEY,
        "outputFormat": "json"
    }

    async with httpx.AsyncClient(timeout=10, follow_redirects=True) as client:
        response = await client.get(BASE_URL, params=params)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail=f"Warsaw API error: {response.status_code}")

    data = response.json()
    coordinates_list = data.get("result", {}).get("featureMemberCoordinates", [])

    theatres = []
    for coord in coordinates_list:
        theatres.append(Theatre(
            latitude=float(coord.get("latitude")),
            longitude=float(coord.get("longitude"))
        ))

    return theatres



