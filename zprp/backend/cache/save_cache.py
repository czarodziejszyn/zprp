import asyncio
import logging

from api.accomodations import fetch_accommodations
from api.aeds import fetch_aeds
from api.attractions import fetch_attractions
from api.bike_stations import fetch_bike_stations
from api.nature import fetch_nature
from api.pharmacies import fetch_pharmacies
from api.police_stations import fetch_police_stations
from api.stops import fetch_stops
from api.theatres import fetch_theatres
from pydantic import BaseModel

from logger import logging_config  # noqa: F401

from .json_cache import save_api_cache_json

logger = logging.getLogger(__name__)


def serialize(obj):
    if isinstance(obj, BaseModel):
        return obj.model_dump()
    if isinstance(obj, list):
        return [serialize(x) for x in obj]
    return obj


async def fetch_api_data():
    logger.info("Fetching data from APIs...")

    accommodations = await fetch_accommodations()
    theatres = await fetch_theatres()
    bike_stations = await fetch_bike_stations()
    aeds = await fetch_aeds()
    attractions = await fetch_attractions()
    nature = await fetch_nature()
    police_stations = await fetch_police_stations()
    pharmacies = await fetch_pharmacies()
    stops = await fetch_stops()

    cache = {
        "theatre": serialize(theatres),
        "aed": serialize(aeds),
        "attraction": serialize(attractions),
        "nature": serialize(nature),
        "police_station": serialize(police_stations),
        "pharmacy": serialize(pharmacies),
        "stop": serialize(stops),
        "bike_station": serialize(bike_stations),
        "accommodation": serialize(accommodations),
    }

    return cache


async def main():
    try:
        data = await fetch_api_data()
        save_api_cache_json(data)
    except Exception:
        logger.exception("API cache update failed")
        return

    logger.info("API cache updated successfully")


if __name__ == "__main__":
    asyncio.run(main())
