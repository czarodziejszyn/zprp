from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import httpx
import os



API_KEY = os.getenv("WARSZAWA_API_KEY")
if not API_KEY:
    raise RuntimeError("Missing WARSZAWA_API_KEY. Add it to .env or system env.")


# Resource IDs for accommodations
RESOURCE_IDS = {
    "hotels": "f019448f-951c-439e-bf37-c3268682752e",
    "dorms": "c789b05d-31b1-4b55-970a-4d3deb923f79",
}


BASE_URL = "https://api.um.warszawa.pl/api/action/wfsstore_get"

class Accommodation(BaseModel):
    objtype: str | None = None  # hotels or dorms
    name: str | None = None
    address: str | None = None
    latitude: float | None = None
    longitude: float | None = None


async def fetch_accommodations(dataset_name: str, limit: int = 10):
    resource_id = RESOURCE_IDS.get(dataset_name)
    if not resource_id:
        raise HTTPException(status_code=404, detail=f"Dataset {dataset_name} not found")

    params = {"id": resource_id, "limit": limit, "apikey": API_KEY}

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

    accommodations = []

    for item in data["result"]["featureMemberList"]:
        coords = item.get("geometry", {}).get("coordinates", [{}])[0]
        props_list = item.get("properties", [])
        props = {p["key"]: p["value"] for p in props_list}

        accommodations.append(Accommodation(
            objtype="hotel" if dataset_name == "hotels" else "dorm",
            name=props.get("OPIS"),
            address=props.get("ADRES"),
            latitude=float(coords.get("latitude")) if coords.get("latitude") else None,
            longitude=float(coords.get("longitude")) if coords.get("longitude") else None
        ))

    return accommodations
