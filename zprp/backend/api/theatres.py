from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import httpx
import os


from .fetch_warsaw_api import WarsawApiObj, get_warsaw_api_obj_data_result

async def fetch_theatres():
    result = await get_warsaw_api_obj_data_result("theatre")
    coordinates_list = result.get("featureMemberCoordinates", [])
    if not coordinates_list:
        raise HTTPException(status_code=404, detail="API returned unexpected structure")


    theatres = []
    for coord in coordinates_list:
        theatres.append(WarsawApiObj(
            objtype="theatre",
            latitude=float(coord.get("latitude")),
            longitude=float(coord.get("longitude"))
        ))

    return theatres



