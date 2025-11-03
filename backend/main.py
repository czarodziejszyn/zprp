from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import httpx
import os

# Load API key
API_KEY = os.getenv("WARSZAWA_API_KEY")
if not API_KEY:
    raise RuntimeError("Missing WARSZAWA_API_KEY. Add it to .env or system env.")

# Endpoint & resource
BASE_URL = "https://api.um.warszawa.pl/api/action/wfsstore_get/"
THEATRES_RESOURCE_ID = "e26218cb-61ec-4ccb-81cc-fd19a6fee0f8"

# Pydantic model for theatre data
class Theatre(BaseModel):
    name: str | None = None
    address: str | None = None
    district: str | None = None
    latitude: float | None = None
    longitude: float | None = None

app = FastAPI(title="Warsaw Theatres API")

async def fetch_theatres(limit: int = 100):
    params = {
        "id": THEATRES_RESOURCE_ID,
        "limit": limit,
        "apikey": API_KEY
    }

    async with httpx.AsyncClient(timeout=10, follow_redirects=True) as client:
        response = await client.get(BASE_URL, params=params)

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

            # Get corresponding coordinates
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


@app.get("/theatres", response_model=list[Theatre])
async def get_theatres(limit: int = Query(100, ge=1, le=1000)):
    """
    Get list of Warsaw theatres with full information.
    """
    return await fetch_theatres(limit=limit)
