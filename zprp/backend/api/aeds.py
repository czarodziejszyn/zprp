# aeds.py
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import httpx
import os

from .fetch_warsaw_api import WarsawApiObj, get_warsaw_api_obj_data_result



async def fetch_aeds():
    results = await get_warsaw_api_obj_data_result("aed")

    
    aeds = []
    for item in results:
        coords = item.get("geometry", {}).get("coordinates", None)
        lon, lat = coords[0]
        lat = float(lat)
        lon = float(lon)


        aeds.append(WarsawApiObj(
            objtype="aeds",
            latitude=lat,
            longitude=lon
        ))

    return aeds
