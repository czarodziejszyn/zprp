import asyncio
from api.aeds import fetch_aeds
from api.theatres import fetch_theatres
from api.attractions import fetch_attractions
from api.nature import fetch_nature
from api.police_stations import fetch_police_stations
from api.pharmacies import fetch_pharmacies
from api.stops import fetch_stops
from api.bike_stations import fetch_bike_stations
from api.accomodations import fetch_accommodations
from pydantic import BaseModel

from .json_cache import save_json


def serialize(obj):
    if isinstance(obj, BaseModel):
        return obj.model_dump()
    if isinstance(obj, list):
        return [serialize(x) for x in obj]
    if isinstance(obj, dict):
        return {k: serialize(v) for k, v in obj.items()}
    return obj


async def fetch_api_data():
    print("Fetching data from APIs...")
    attractions = await fetch_attractions()
    theatres = await fetch_theatres()
    aeds = await fetch_aeds()

    # nature
    nature = {}
    for dataset in ["trees", "bushes", "forests"]:
        items = await fetch_nature(dataset)
        nature[dataset] = serialize(items)

    police_stations = await fetch_police_stations()
    pharmacies = await fetch_pharmacies()
    stops = await fetch_stops()
    bike_stations = await fetch_bike_stations("bike_stations")

    # accomodations
    hotels = await fetch_accommodations("hotels")
    dorms = await fetch_accommodations("dorms")
    accommodations = hotels + dorms

    cache = {
        "theatres": serialize(theatres),
        "aeds": serialize(aeds),
        "attractions": serialize(attractions),
        "nature": nature,
        "police_stations": serialize(police_stations),
        "pharmacies": serialize(pharmacies),
        "stops": serialize(stops),
        "bike_stations": serialize(bike_stations),
        "accommodations": serialize(accommodations),
    }

    return cache




async def main():
    data = await fetch_api_data()
    save_json(data)
    print("API cache updated successfully")


if __name__ == "__main__":
    asyncio.run(main())
