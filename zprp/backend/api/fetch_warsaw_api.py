# tourism.py
import asyncio
import logging
import os

from fastapi import HTTPException
import httpx
from pydantic import BaseModel

logger = logging.getLogger(__name__)

API_KEY = os.getenv("WARSZAWA_API_KEY")
if not API_KEY:
    raise RuntimeError("Missing WARSZAWA_API_KEY. Add it to .env or system env.")


# Endpoints
DATASETS = {
    "attraction": {
        "base_url": "https://api.um.warszawa.pl/api/action/tourism_attraction_get/",
        "resource_id": None,
    },
    "aed": {"base_url": "https://api.um.warszawa.pl/api/action/aed_get/", "resource_id": None},
    "stop": {
        "base_url": "https://api.um.warszawa.pl/api/action/dbtimetable_get/",
        "resource_id": "ab75c33d-3a26-4342-b36a-6e5fef0a3ac3",
    },
    "bush": {
        "base_url": "https://api.um.warszawa.pl/api/action/datastore_search/",
        "resource_id": "0b1af81f-247d-4266-9823-693858ad5b5d",
    },
    "forest": {
        "base_url": "https://api.um.warszawa.pl/api/action/datastore_search/",
        "resource_id": "75bedfd5-6c83-426b-9ae5-f03651857a48",
    },
    "tree": {
        "base_url": "https://api.um.warszawa.pl/api/action/datastore_search/",
        "resource_id": "ed6217dd-c8d0-4f7b-8bed-3b7eb81a95ba",
    },
    "bike_station": {
        "base_url": "https://api.um.warszawa.pl/api/action/wfsstore_get/",
        "resource_id": "a08136ec-1037-4029-9aa5-b0d0ee0b9d88",
    },
    "hotel": {
        "base_url": "https://api.um.warszawa.pl/api/action/wfsstore_get/",
        "resource_id": "f019448f-951c-439e-bf37-c3268682752e",
    },
    "dorm": {
        "base_url": "https://api.um.warszawa.pl/api/action/wfsstore_get/",
        "resource_id": "c789b05d-31b1-4b55-970a-4d3deb923f79",
    },
    "pharmacy": {
        "base_url": "https://api.um.warszawa.pl/api/action/wfsstore_get/",
        "resource_id": "fd137190-3d65-4306-a85e-5e97e7f29a23",
    },
    "police_station": {
        "base_url": "https://api.um.warszawa.pl/api/action/wfsstore_get/",
        "resource_id": "fd137190-3d65-4306-a85e-5e97e7f29a23",
    },
    "theatre": {
        "base_url": "https://api.um.warszawa.pl/api/action/wfsstore_get/",
        "resource_id": "e26218cb-61ec-4ccb-81cc-fd19a6fee0f8",
    },
}


class WarsawApiObj(BaseModel):
    objtype: str
    latitude: float | None = None
    longitude: float | None = None


async def get_warsaw_api_obj_data_result(dataset_name):
    # params
    dataset = DATASETS[dataset_name]
    base_url = dataset["base_url"]
    resource_id = dataset["resource_id"]

    # different APIs
    if "datastore_search" in base_url:
        params = {"resource_id": resource_id}
    else:
        params = {"apikey": API_KEY, "outputFormat": "json"}
        if resource_id is not None:
            params["id"] = resource_id

    attempt = 0
    retries = 3
    backoff = 2  # in seconds
    while attempt < retries:
        attempt += 1

        try:
            async with httpx.AsyncClient(
                timeout=httpx.Timeout(60.0, connect=20.0), follow_redirects=True
            ) as client:
                response = await client.get(base_url, params=params)

            if response.status_code != 200:
                raise HTTPException(
                    status_code=500, detail=f"Warsaw API error: {response.status_code}"
                )

            try:
                data = response.json()
            except Exception:
                raise HTTPException(
                    status_code=500, detail=f"API returned non-JSON: {response.text}"
                )

            # results
            if "result" not in data:
                raise HTTPException(status_code=500, detail="API returned unexpected structure")

            result = data["result"]
            if not isinstance(result, (dict, list)):
                raise HTTPException(
                    status_code=500,
                    detail=f"API did not return structured data. API response: {result}",
                )
            return result

        except (httpx.RequestError, httpx.TimeoutException) as e:
            logger.warning(f"Attempt {attempt} failed: {e}")
            if attempt < retries:
                await asyncio.sleep(backoff * attempt)
            else:
                raise HTTPException(
                    status_code=500, detail=f"Warsaw API failed after {retries} attempts"
                )
