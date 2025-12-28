from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx

from .fetch_warsaw_api import WarsawApiObj, get_warsaw_api_obj_data_result

async def fetch_nature_obj(dataset_name: str):
    results = await get_warsaw_api_obj_data_result(dataset_name)

    records = results.get("records", [])
    natures = []

    for r in records:
        lat = float(r.get("y_wgs84")) if r.get("y_wgs84") else None
        lon = float(r.get("x_wgs84")) if r.get("x_wgs84") else None

        natures.append(WarsawApiObj(
            objtype=dataset_name,
            latitude=lat,
            longitude=lon
        ))

    return natures

async def fetch_nature():
    nature = []
    for dataset in ["tree", "bush", "forest"]:
        items = await fetch_nature_obj(dataset)
        nature += items
    return nature

