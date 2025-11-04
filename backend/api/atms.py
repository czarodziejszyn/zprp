from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import httpx
import os

API_KEY = os.getenv("WARSZAWA_API_KEY")
if not API_KEY:
    raise RuntimeError("Missing WARSZAWA_API_KEY. Add it to .env or system env.")

# Resource ID for Euronet ATMs
RESOURCE_IDS = {
    "atms": "672729a7-5ff9-45de-8ae2-ffc87213b9a8"
}

BASE_URL = "https://api.um.warszawa.pl/api/action/wfsstore_get"

class ATM(BaseModel):
    name: str | None = None
    description: str | None = None
    latitude: float | None = None
    longitude: float | None = None

app = FastAPI(title="Warsaw ATMs API")

async def fetch_atms(limit: int = 100):
    resource_id = RESOURCE_IDS["atms"]
    params = {"id": resource_id, "limit": limit, "apikey": API_KEY}

    async with httpx.AsyncClient(timeout=httpx.Timeout(60.0, connect=20.0), follow_redirects=True) as client:
        try:
            response = await client.get(BASE_URL, params=params)
        except httpx.ReadTimeout:
            raise HTTPException(status_code=504, detail="API request timed out")

    print("Raw API response:", response.text)

    # try:
    #     data = response.json()
    # except Exception:
    #     raise HTTPException(status_code=500, detail=f"API returned non-JSON: {response.text}")

    # # Handle API error returned as string in `result`
    # if isinstance(data.get("result"), str):
    #     raise HTTPException(status_code=500, detail=f"API error: {data['result']}")

    # # Sometimes `data` is directly the object, sometimes a list of objects
    # raw_data = data.get("data") or []
    # if not raw_data:
    #     raise HTTPException(status_code=404, detail="No ATM data found")

    atms = []

    # # Normalize: if raw_data is dict with geometry+properties, wrap it in list
    # if isinstance(raw_data, dict) and "geometry" in raw_data and "properties" in raw_data:
    #     raw_data = [raw_data]

    # for item in raw_data:
    #     coords = item.get("geometry", {}).get("coordinates", {})
    #     props_list = item.get("properties", [])
    #     props = {p["key"]: p["value"] for p in props_list}

    #     atms.append(ATM(
    #         name=props.get("NAZWA"),
    #         description=props.get("OPIS"),
    #         latitude=float(coords.get("lat")) if coords.get("lat") else None,
    #         longitude=float(coords.get("lon")) if coords.get("lon") else None
    #     ))

    return atms


@app.get("/atms", response_model=list[ATM])
async def get_atms(limit: int = Query(10, ge=1, le=100)):
    """
    Get list of Euronet ATMs in Warsaw.
    """
    return await fetch_atms(limit=limit)
