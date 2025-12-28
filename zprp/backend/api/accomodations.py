from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import httpx
import os

from .fetch_warsaw_api import WarsawApiObj, get_warsaw_api_obj_data_result



async def fetch_accommodations(dataset_name: str):
    result = await get_warsaw_api_obj_data_result(dataset_name)

    feature_list = result.get("featureMemberList", [])
    if not feature_list:
        raise HTTPException(status_code=404, detail="API returned unexpected structure")

    accommodations = []
    for item in feature_list:
        coords = item.get("geometry", {}).get("coordinates", [{}])[0]

        accommodations.append(WarsawApiObj(
            objtype=dataset_name,
            latitude=float(coords.get("latitude")) if coords.get("latitude") else None,
            longitude=float(coords.get("longitude")) if coords.get("longitude") else None
        ))

    return accommodations
