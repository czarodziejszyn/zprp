# tourism.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
import os


from .fetch_warsaw_api import WarsawApiObj, get_warsaw_api_obj_data_result




async def fetch_attractions():
    results = await get_warsaw_api_obj_data_result("attraction")

    attractions = []
    for t in results:
        latlng = t.get("latlng", {})
        attractions.append(WarsawApiObj(
            objtype="attractions",
            latitude=float(latlng.get("lat")) if latlng.get("lat") else None,
            longitude=float(latlng.get("lng")) if latlng.get("lng") else None
        ))

    return attractions

