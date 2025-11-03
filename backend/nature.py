from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx

# Resource IDs for nature datasets
RESOURCE_IDS = {
    "bushes": "0b1af81f-247d-4266-9823-693858ad5b5d",
    "forests": "75bedfd5-6c83-426b-9ae5-f03651857a48",
    "trees": "ed6217dd-c8d0-4f7b-8bed-3b7eb81a95ba",
}

BASE_URL = "https://api.um.warszawa.pl/api/action/datastore_search"

# Pydantic model
class Nature(BaseModel):
    objtype: str | None = None  # bushes, forests, trees
    address: str | None = None
    district: str | None = None
    latitude: float | None = None
    longitude: float | None = None

app = FastAPI(title="Warsaw Nature API")


# Shared fetch function
async def fetch_nature(dataset_name: str, limit: int = 100):
    resource_id = RESOURCE_IDS.get(dataset_name)
    if not resource_id:
        raise HTTPException(status_code=404, detail=f"Dataset {dataset_name} not found")

    params = {"resource_id": resource_id, "limit": limit}  # no API key

    async with httpx.AsyncClient(timeout=20, follow_redirects=True) as client:
        response = await client.get(BASE_URL, params=params)


    data = response.json()
    records = data.get("result", {}).get("records", [])
    natures = []

    for r in records:
        lat = float(r.get("y_wgs84")) if r.get("y_wgs84") else None
        lon = float(r.get("x_wgs84")) if r.get("x_wgs84") else None
        addr = r.get("adres") or r.get("lokalizacja")

        type_label = (
            "tree" if dataset_name == "trees" else
            "bush" if dataset_name == "bushes" else
            "forest" if dataset_name == "forests" else
            "unknown"
        )

        natures.append(Nature(
            objtype=type_label,
            address=addr,
            district=r.get("dzielnica"),
            latitude=lat,
            longitude=lon
        ))

    return natures

@app.get("/nature/{dataset_name}", response_model=list[Nature])
async def get_nature(dataset_name: str):
    """
    Get nature data by dataset_name (bushes, forests, trees). Default limit is 100 results.
    """
    return await fetch_nature(dataset_name)
