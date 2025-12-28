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

from cache.json_cache import load_json


GEOCODED_OFFERS_JSON_PATH = os.getenv("GEOCODED_OFFERS_JSON_PATH")



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


async def import_aeds():
    try:
        aeds = await fetch_aeds()
        print("Fetched AEDs from API.")
    except Exception as e:
        print(f"Error fetching AEDs from API:")
        cache = load_json()
        aeds = cache.get("aeds", [])
        print(f"Using {len(aeds)} AEDs from cache.")

    return import_obj_list(aeds)



async def import_theatres():
    try:
        theatres = await fetch_theatres()
        print("Fetched theatres from API.")
    except Exception as e:
        print(f"Error fetching theatres from API:")
        cache = load_json()
        theatres = cache.get("theatres", [])
        print(f"Using {len(theatres)} theatres from cache.")

    return import_obj_list(theatres)



async def import_attractions():
    try:
        attractions = await fetch_attractions()
        print("Fetched attractions from API.")
    except Exception as e:
        print(f"Error fetching attractions from API:")
        cache = load_json()
        attractions = cache.get("attractions", [])
        print(f"Using {len(attractions)} attractions from cache.")

    return import_obj_list(attractions)


async def import_nature():
    try:
        nature = await fetch_nature()
        print(f"Fetched nature from API.")
    except Exception as e:
        print(f"Error fetching nature: ")
        cache = load_json()
        nature = cache.get("nature", {})
        print(f"Using {len(nature)} natures from cache.")


    return import_obj_list(nature)



async def import_police_stations():
    try:
        police_stations = await fetch_police_stations()
        print("Fetched police stations from API.")
    except Exception as e:
        print(f"Error fetching police stations: ")
        cache = load_json()
        police_stations = cache.get("police_stations", [])
        print(f"Using {len(police_stations)} police stations from cache.")

    return import_obj_list(police_stations)



async def import_pharmacies():
    try:
        pharmacies = await fetch_pharmacies()
        print("Fetched pharmacies from API.")
    except Exception as e:
        print(f"Error fetching pharmacies: ")
        cache = load_json()
        pharmacies = cache.get("pharmacies", [])
        print(f"Using {len(pharmacies)} pharmacies from cache.")

    return import_obj_list(pharmacies)



async def import_stops():
    try:
        stops = await fetch_stops()
        print("Fetched stops from API.")
    except Exception as e:
        print(f"Error fetching stops: ")
        cache = load_json()
        stops = cache.get("stops", [])
        print(f"Using {len(stops)} stops from cache.")

    return import_obj_list(stops)


async def import_bike_stations():
    try:
        bike_stations = await fetch_bike_stations()
        print("Fetched bike stations from API.")
    except Exception as e:
        print(f"Error fetching bike stations: ")
        cache = load_json()
        bike_stations = cache.get("bike_stations", [])
        print(f"Using {len(bike_stations)} bike stations from cache.")

    return import_obj_list(bike_stations)


async def import_accommodations():
    try:
        accommodations = await fetch_accommodations()
        print("Fetched accommodations from API.")
    except Exception as e:
        print(f"Error fetching accommodations: ")
        cache = load_json()
        accommodations = cache.get("accommodations", [])
        print(f"Using {len(accommodations)} accommodations from cache.")

    return import_obj_list(accommodations)



async def main():
    init_db()

    # Offers
    offers_count = import_offers()
    print(f"Imported {offers_count} offers from otodom.")

    # AEDs
    aeds_count = await import_aeds()
    print(f"Imported {aeds_count} AEDs.")

    # Theatres
    theatres_count = await import_theatres()
    print(f"Imported {theatres_count} theatres.")


    # Tourist attractions
    attractions_count = await import_attractions()
    print(f"Imported {attractions_count} attractions.")

    # Nature 
    nature_count = await import_nature()
    print(f"Imported {nature_count} nature objects.")

    # Police stations
    police_count = await import_police_stations()
    print(f"Imported {police_count} police stations.")

    # Pharmacies
    pharmacies_count = await import_pharmacies()
    print(f"Imported {pharmacies_count} pharmacies.")

    # Stops
    stops_count = await import_stops()
    print(f"Imported {stops_count} public transport stops.")

    # Bike stations
    bike_count = await import_bike_stations()
    print(f"Imported {bike_count} bike stations.")

    # Accomodiations
    accommodations_count = await import_accommodations()
    print(f"Imported {accommodations_count} accommodations.")



if __name__ == "__main__":
    asyncio.run(main())
