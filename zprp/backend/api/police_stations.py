from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import httpx
import os


from .fetch_warsaw_api import WarsawApiObj, get_warsaw_api_obj_data_result


async def fetch_police_stations():
    result = await get_warsaw_api_obj_data_result("police_station")
    feature_list = result.get("featureMemberList", [])
    if not feature_list:
        raise HTTPException(status_code=404, detail="API returned unexpected structure")

    stations = []
    for item in feature_list:
        coords = item.get("geometry", {}).get("coordinates", [{}])[0]

        stations.append(WarsawApiObj(
            objtype="police_station",
            latitude=float(coords.get("latitude")) if coords.get("latitude") else None,
            longitude=float(coords.get("longitude")) if coords.get("longitude") else None
))
    return stations
