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
    name: str | None = None
    address: str | None = None
    district: str | None = None
    latitude: float | None = None
    longitude: float | None = None


async def fetch_theatres():
    params = {
        "id": THEATRES_RESOURCE_ID,
        "apikey": API_KEY,
        "outputFormat": "json"   # <-- ADD THIS
    }

    async with httpx.AsyncClient(timeout=10, follow_redirects=True) as client:
        response = await client.get(BASE_URL, params=params)

    print("RAW RESPONSE:", response.text[:200])

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail=f"Warsaw API error: {response.status_code}")

    data = response.json()
    properties_list = data.get("result", {}).get("featureMemberProperties", [])
    coordinates_list = data.get("result", {}).get("featureMemberCoordinates", [])

    theatres = []

    for i, t in enumerate(properties_list):
            # Build full address
            street = t.get("ULICA")
            number = t.get("NUMER")
            postal = t.get("KOD")
            address = f"{street} {number}, {postal}" if street and number and postal else None

            # Get coordinates
            lat = None
            lon = None
            if i < len(coordinates_list):
                lat = float(coordinates_list[i].get("latitude"))
                lon = float(coordinates_list[i].get("longitude"))

            theatres.append(Theatre(
                name=t.get("OPIS"),
                address=address,
                district=t.get("DZIELNICA"),
                latitude=lat,
                longitude=lon
            ))

    return theatres



