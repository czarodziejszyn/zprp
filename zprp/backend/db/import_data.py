import asyncio
import json
import os
from api.aeds import fetch_aeds
from api.theatres import fetch_theatres
from api.attractions import fetch_attractions
from api.nature import fetch_nature
from api.police_stations import fetch_police_stations
from api.pharmacies import fetch_pharmacies
from api.stops import fetch_stops
from api.bike_stations import fetch_bike_stations
from api.accomodations import fetch_accommodations

from .db import get_conn, init_db

from cache.json_cache import load_api_cache_json
from logger import logging_config 
import logging


GEOCODED_OFFERS_JSON_PATH = os.getenv("GEOCODED_OFFERS_JSON_PATH")
logger = logging.getLogger(__name__)


def import_offers():
    with open(GEOCODED_OFFERS_JSON_PATH, "r", encoding="utf-8") as handler:
        offers = json.load(handler)

    with get_conn() as conn:
        for o in offers:
            conn.execute("""
                INSERT INTO offers (title, url, price, area_m2, price_per_m2, address, latitude, longitude, geom)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, ST_SetSRID(ST_MakePoint(%s, %s), 4326))
                ON CONFLICT DO NOTHING;
            """, (
                o["title"],
                o["url"],
                o["price"],
                o["area_m2"],
                o["price_per_m2"],
                o["address"],
                o["latitude"],
                o["longitude"],
                o["longitude"],  # POINT(lon, lat)
                o["latitude"]
            ))

    return len(offers)


def normalize(obj):
    if isinstance(obj, dict):     # from cache
        return (
            obj.get("objtype"),
            obj.get("latitude"),
            obj.get("longitude")
        )

    else:           # from api
        return (
            obj.objtype,
            obj.latitude,
            obj.longitude
        )



def insert_city_obj(conn, objtype: str, latitude: float | None, longitude: float | None):
    if latitude is None or longitude is None:
        return

    conn.execute("""
        INSERT INTO city_obj (objtype, latitude, longitude, geom)
        VALUES (
            %s,
            %s,
            %s,
            ST_SetSRID(ST_MakePoint(%s, %s), 4326)::geography
        );
    """, (
        objtype,
        latitude,
        longitude,
        longitude,  # POINT(lon, lat)
        latitude,  
    ))

def import_obj_list(obj_list):
    with get_conn() as conn:
        for obj in obj_list:
            objtype, lat, lon = normalize(obj)
            insert_city_obj(conn, objtype, lat, lon)
        return len(obj_list)



async def import_with_cache(fetch_func, cache_key: str, obj_name :str):
    try:
        objs = await fetch_func()
        logger.info(f"Fetched {obj_name} from API.")
    except Exception as e:
        logger.warning(f"Error fetching {obj_name} from API")
        try:
            cache = load_api_cache_json()
        except Exception:
            logger.error(f"Error loading {obj_name} from cache. Skipping import.")
            return 0
        objs = cache.get(cache_key, [])
        logger.info(f"Using {obj_name} from cache.")

    return import_obj_list(objs)





async def main():
    init_db()

    # Offers
    offers_count = import_offers()
    logger.info(f"Imported {offers_count} offers from JSON.")

    # AEDs
    aeds_count = await import_with_cache(fetch_aeds, "aed", "AEDs")
    logger.info(f"Imported {aeds_count} AEDs.")

    # Theatres
    theatres_count = await import_with_cache(fetch_theatres, "theatre", "theatres")
    logger.info(f"Imported {theatres_count} theatres.")

    # Tourist attractions
    attractions_count = await  import_with_cache(fetch_attractions, "attraction", "attractions")
    logger.info(f"Imported {attractions_count} attractions.")

    # Nature 
    nature_count = await import_with_cache(fetch_nature, "nature", "nature")
    logger.info(f"Imported {nature_count} nature objects.")

    # Police stations
    police_count = await import_with_cache(fetch_police_stations, "police_station", "police stations")
    logger.info(f"Imported {police_count} police stations.")

    # Pharmacies
    pharmacies_count = await import_with_cache(fetch_pharmacies, "pharmacy", "pharmacies")
    logger.info(f"Imported {pharmacies_count} pharmacies.")

    # Stops
    stops_count = await import_with_cache(fetch_pharmacies, "stop", "stops")
    logger.info(f"Imported {stops_count} public transport stops.")

    # Bike stations
    bike_count = await import_with_cache(fetch_bike_stations, "bike_station", "bike stations")
    logger.info(f"Imported {bike_count} bike stations.")

    # Accomodiations
    accommodations_count = await import_with_cache(fetch_accommodations, "accommodation", "accommodations")
    logger.info(f"Imported {accommodations_count} accommodations.")



if __name__ == "__main__":
    asyncio.run(main())
