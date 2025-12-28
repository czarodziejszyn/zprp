from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import httpx
import os

API_KEY = os.getenv("WARSZAWA_API_KEY")
if not API_KEY:
    raise RuntimeError("Missing WARSZAWA_API_KEY. Add it to .env or system env.")

# Resource ID for pharmacies
PHARMACIES_RESOURCE_ID = "fd137190-3d65-4306-a85e-5e97e7f29a23"

BASE_URL = "https://api.um.warszawa.pl/api/action/wfsstore_get"

class Pharmacy(BaseModel):
    latitude: float | None = None
    longitude: float | None = None


async def fetch_pharmacies():
    params = {
        "id": PHARMACIES_RESOURCE_ID,
        "apikey": API_KEY,
    }


    async with httpx.AsyncClient(follow_redirects=True) as client:
        response = await client.get(BASE_URL, params=params)

    data = response.json()


    result = data.get("result", {})
    feature_list = result.get("featureMemberList", [])


    if not feature_list:
        raise HTTPException(status_code=404, detail="No pharmacy data found")


    pharmacies = []
    for item in feature_list:
        coords = item.get("geometry", {}).get("coordinates", [{}])[0]

        pharmacies.append(Pharmacy(
            latitude=float(coords.get("latitude")) if coords.get("latitude") else None,
            longitude=float(coords.get("longitude")) if coords.get("longitude") else None
))

    return pharmacies


