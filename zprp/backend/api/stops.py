# tourism.py
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import httpx
import os


from .fetch_warsaw_api import WarsawApiObj, get_warsaw_api_obj_data_result


async def fetch_stops():
    result = await get_warsaw_api_obj_data_result("stop")

    stops = []
    for item in result:
        values = {v["key"]: v["value"] for v in item.get("values", [])}

        stops.append(WarsawApiObj(
            objtype="stop",
            latitude=float(values.get("szer_geo")) if values.get("szer_geo") else None,
            longitude=float(values.get("dlug_geo")) if values.get("dlug_geo") else None
        ))

    return stops