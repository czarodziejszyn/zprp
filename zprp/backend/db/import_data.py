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

from .db import get_conn, init_db, create_total_city_obj_table

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




async def import_aeds():
    try:
        aeds = await fetch_aeds()
        print("Fetched AEDs from API")
    except Exception as e:
        print(f"Error fetching AEDs from API:")
        cache = load_json()
        aeds = cache.get("aeds", [])
        print(f"Using {len(aeds)} AEDs from cache")


    with get_conn() as conn:
        for a in aeds:
            if isinstance(a, dict):     # from cache
                street = a.get("street")
                building = a.get("building")
                latitude = a.get("latitude")
                longitude = a.get("longitude")
            else:                       # from API - Pydantic object
                street = a.street
                building = a.building
                latitude = a.latitude
                longitude = a.longitude

            conn.execute("""
                INSERT INTO aeds (street, building, latitude, longitude, geom)
                VALUES (%s, %s, %s, %s, ST_SetSRID(ST_MakePoint(%s, %s), 4326))
                ON CONFLICT DO NOTHING;
            """, (
                street,
                building,
                latitude,
                longitude,
                longitude,  # POINT(lon, lat)
                latitude
            ))
    return len(aeds)



async def import_theatres():
    try:
        theatres = await fetch_theatres()
        print("Fetched theatres from API")
    except Exception as e:
        print(f"Error fetching theatres from API:")
        cache = load_json()
        theatres = cache.get("theatres", [])
        print(f"Using {len(theatres)} theatres from cache")


    with get_conn() as conn:
        for t in theatres:
            if isinstance(t, dict):
                name = t.get("name")
                address = t.get("address")
                district = t.get("district")
                latitude = t.get("latitude")
                longitude = t.get("longitude")
            else:
                name = t.name
                address = t.address
                district = t.district
                latitude = t.latitude
                longitude = t.longitude

            conn.execute("""
                INSERT INTO theatres (name, address, district, latitude, longitude, geom)
                VALUES (%s, %s, %s, %s, %s, ST_SetSRID(ST_MakePoint(%s, %s), 4326))
                ON CONFLICT DO NOTHING;
            """, (
                name,
                address,
                district,
                latitude,
                longitude,
                longitude,
                latitude
            ))
    return len(theatres)



async def import_attractions():
    try:
        attractions = await fetch_attractions()
        print("Fetched attractions from API")
    except Exception as e:
        print(f"Error fetching attractions from API:")
        cache = load_json()
        attractions = cache.get("attractions", [])
        print(f"Using {len(attractions)} attractions from cache")

    with get_conn() as conn:
        for a in attractions:
            if isinstance(a, dict):
                name = a.get("name")
                address = a.get("address")
                city = a.get("city")
                category = a.get("category")
                latitude = a.get("latitude")
                longitude = a.get("longitude")
            else:
                name = a.name
                address = a.address
                city = a.city
                category = a.category
                latitude = a.latitude
                longitude = a.longitude

            conn.execute("""
                INSERT INTO attractions (name, address, city, category, latitude, longitude, geom)
                VALUES (%s, %s, %s, %s, %s, %s, ST_SetSRID(ST_MakePoint(%s, %s), 4326))
                ON CONFLICT DO NOTHING;
            """, (
                name,
                address,
                city,
                category,
                latitude,
                longitude,
                longitude,
                latitude
            ))
    return len(attractions)


async def import_nature():
    total_inserted = 0
    for dataset in ["trees", "bushes", "forests"]:
        try:
            items = await fetch_nature(dataset)
            print(f"Fetched {dataset} from API")
        except Exception as e:
            print(f"Error fetching {dataset}:")
            cache = load_json()
            nature_cache = cache.get("nature", {})
            items = nature_cache.get(dataset, [])
            print(f"Using {len(items)} {dataset} from cache")

        with get_conn() as conn:
            for n in items:
                if isinstance(n, dict):
                    objtype = n.get("objtype")
                    address = n.get("address")
                    district = n.get("district")
                    latitude = n.get("latitude")
                    longitude = n.get("longitude")
                else:
                    objtype = n.objtype
                    address = n.address
                    district = n.district
                    latitude = n.latitude
                    longitude = n.longitude

                conn.execute("""
                    INSERT INTO nature (objtype, address, district, latitude, longitude, geom)
                    VALUES (%s, %s, %s, %s, %s, ST_SetSRID(ST_MakePoint(%s, %s), 4326))
                    ON CONFLICT DO NOTHING;
                """, (
                    objtype,
                    address,
                    district,
                    latitude,
                    longitude,
                    longitude,
                    latitude
                ))
        total_inserted += len(items)
    return total_inserted



async def import_police_stations():
    try:
        police_stations = await fetch_police_stations()
        print("Fetched police stations from API")
    except Exception as e:
        print(f"Error fetching police stations: ")
        cache = load_json()
        police_stations = cache.get("police_stations", [])
        print(f"Using {len(police_stations)} police stations from cache")

    with get_conn() as conn:
        for s in police_stations:
            if isinstance(s, dict):
                name = s.get("name")
                district = s.get("district")
                latitude = s.get("latitude")
                longitude = s.get("longitude")
            else:
                name = s.name
                district = s.district
                latitude = s.latitude
                longitude = s.longitude

            conn.execute("""
                INSERT INTO police_stations (name, district, latitude, longitude, geom)
                VALUES (%s, %s, %s, %s, ST_SetSRID(ST_MakePoint(%s, %s), 4326))
                ON CONFLICT DO NOTHING;
            """, (
                name,
                district,
                latitude,
                longitude,
                longitude,
                latitude
            ))
    return len(police_stations)

async def import_pharmacies():
    try:
        pharmacies = await fetch_pharmacies()
        print("Fetched pharmacies from API")
    except Exception as e:
        print(f"Error fetching pharmacies: ")
        cache = load_json()
        pharmacies = cache.get("pharmacies", [])
        print(f"Using {len(pharmacies)} pharmacies from cache")

    with get_conn() as conn:
        for p in pharmacies:
            if isinstance(p, dict):
                name = p.get("name")
                street = p.get("street")
                number = p.get("number")
                district = p.get("district")
                latitude = p.get("latitude")
                longitude = p.get("longitude")
            else:
                name = p.name
                street = p.street
                number = p.number
                district = p.district
                latitude = p.latitude
                longitude = p.longitude

            conn.execute("""
                INSERT INTO pharmacies (name, street, number, district, latitude, longitude, geom)
                VALUES (%s, %s, %s, %s, %s, %s, ST_SetSRID(ST_MakePoint(%s, %s), 4326))
                ON CONFLICT DO NOTHING;
            """, (
                name,
                street,
                number,
                district,
                latitude,
                longitude,
                longitude,
                latitude
            ))
    return len(pharmacies)

async def import_stops():
    try:
        stops = await fetch_stops()
        print("Fetched stops from API")
    except Exception as e:
        print(f"Error fetching stops: ")
        cache = load_json()
        stops = cache.get("stops", [])
        print(f"Using {len(stops)} stops from cache")

    with get_conn() as conn:
        for s in stops:
            if isinstance(s, dict):
                stop_id = s.get("stop_id")
                stop_post = s.get("stop_post")
                stop_name = s.get("stop_name")
                latitude = s.get("latitude")
                longitude = s.get("longitude")
            else:
                stop_id = s.stop_id
                stop_post = s.stop_post
                stop_name = s.stop_name
                latitude = s.latitude
                longitude = s.longitude

            if not (latitude and longitude):
                continue

            conn.execute("""
                INSERT INTO stops (stop_id, stop_post, stop_name, latitude, longitude, geom)
                VALUES (%s, %s, %s, %s, %s, ST_SetSRID(ST_MakePoint(%s, %s), 4326))
                ON CONFLICT DO NOTHING;
            """, (
                stop_id,
                stop_post,
                stop_name,
                latitude,
                longitude,
                longitude,
                latitude
            ))
    return len(stops)


async def import_bike_stations():
    try:
        bike_stations = await fetch_bike_stations()
        print("Fetched bike stations from API")
    except Exception as e:
        print(f"Error fetching bike stations: ")
        cache = load_json()
        bike_stations = cache.get("bike_stations", [])
        print(f"Using {len(bike_stations)} bike stations from cache")

    with get_conn() as conn:
        for s in bike_stations:
            if isinstance(s, dict):
                name = s.get("name")
                description = s.get("description")
                latitude = s.get("latitude")
                longitude = s.get("longitude")
            else:
                name = s.name
                description = s.description
                latitude = s.latitude
                longitude = s.longitude

            if not (latitude and longitude):
                continue

            conn.execute("""
                INSERT INTO bike_stations (name, description, latitude, longitude, geom)
                VALUES (%s, %s, %s, %s, ST_SetSRID(ST_MakePoint(%s, %s), 4326))
                ON CONFLICT DO NOTHING;
            """, (
                name,
                description,
                latitude,
                longitude,
                longitude,
                latitude
            ))
    return len(bike_stations)


async def import_accommodations():
    try:
        hotels = await fetch_accommodations("hotels")
        dorms = await fetch_accommodations("dorms")
        accommodations = hotels + dorms
        print("Fetched accommodations from API")
    except Exception as e:
        print(f"Error fetching accommodations: ")
        cache = load_json()
        accommodations = cache.get("accommodations", [])
        print(f"Using {len(accommodations)} accommodations from cache")

    with get_conn() as conn:
        for a in accommodations:
            if isinstance(a, dict):
                objtype = a.get("objtype")
                name = a.get("name")
                address = a.get("address")
                latitude = a.get("latitude")
                longitude = a.get("longitude")
            else:
                objtype = a.objtype
                name = a.name
                address = a.address
                latitude = a.latitude
                longitude = a.longitude

            if not (latitude and longitude):
                continue

            conn.execute("""
                INSERT INTO accommodations (objtype, name, address, latitude, longitude, geom)
                VALUES (%s, %s, %s, %s, %s, ST_SetSRID(ST_MakePoint(%s, %s), 4326))
                ON CONFLICT DO NOTHING;
            """, (
                objtype,
                name,
                address,
                latitude,
                longitude,
                longitude,
                latitude
            ))
    return len(accommodations)


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

    # Nature - bushes, trees, forests
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


    create_total_city_obj_table()
    print(f"Created city_obj table.")


if __name__ == "__main__":
    asyncio.run(main())
