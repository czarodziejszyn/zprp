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


from .db import get_conn, init_db, create_total_city_obj_table


async def import_aeds():
    aeds = await fetch_aeds()

    with get_conn() as conn:
        for a in aeds:
            conn.execute("""
                INSERT INTO aeds (street, building, latitude, longitude, geom)
                VALUES (%s, %s, %s, %s, ST_SetSRID(ST_MakePoint(%s, %s), 4326))
                ON CONFLICT DO NOTHING;
            """, (
                a.street,
                a.building,
                a.latitude,
                a.longitude,
                a.longitude,  # POINT(lon, lat)
                a.latitude
            ))
    return len(aeds)


async def import_theatres():
    theatres = await fetch_theatres()

    with get_conn() as conn:
        for t in theatres:
            conn.execute("""
                INSERT INTO theatres (name, address, district, latitude, longitude, geom)
                VALUES (%s, %s, %s, %s, %s, ST_SetSRID(ST_MakePoint(%s, %s), 4326))
                ON CONFLICT DO NOTHING;
            """, (
                t.name,
                t.address,
                t.district,
                t.latitude,
                t.longitude,
                t.longitude,  # POINT(lon, lat)
                t.latitude
            ))
    return len(theatres)


async def import_attractions():
    attractions = await fetch_attractions()

    with get_conn() as conn:
        for a in attractions:
            conn.execute("""
                INSERT INTO attractions (name, address, city, category, latitude, longitude, geom)
                VALUES (%s, %s, %s, %s, %s, %s, ST_SetSRID(ST_MakePoint(%s, %s), 4326))
                ON CONFLICT DO NOTHING;
            """, (
                a.name,
                a.address,
                a.city,
                a.category,
                a.latitude,
                a.longitude,
                a.longitude,  # lon
                a.latitude    # lat
            ))
    return len(attractions)


async def import_nature():
    total_inserted = 0

    for dataset in ["trees", "bushes", "forests"]:
        items = await fetch_nature(dataset)

        with get_conn() as conn:
            for n in items:
                conn.execute("""
                    INSERT INTO nature (objtype, address, district, latitude, longitude, geom)
                    VALUES (%s, %s, %s, %s, %s, ST_SetSRID(ST_MakePoint(%s, %s), 4326))
                    ON CONFLICT DO NOTHING;
                """, (
                    n.objtype,
                    n.address,
                    n.district,
                    n.latitude,
                    n.longitude,
                    n.longitude,  # lon
                    n.latitude    # lat
                ))

        total_inserted += len(items)

    return total_inserted



async def import_police_stations():
    stations = await fetch_police_stations(limit=200)

    with get_conn() as conn:
        for s in stations:
            conn.execute("""
                INSERT INTO police_stations (name, district, latitude, longitude, geom)
                VALUES (%s, %s, %s, %s, ST_SetSRID(ST_MakePoint(%s, %s), 4326))
                ON CONFLICT DO NOTHING;
            """, (
                s.name,
                s.district,
                s.latitude,
                s.longitude,
                s.longitude,  # lon
                s.latitude    # lat
            ))
    return len(stations)


async def import_pharmacies():
    pharmacies = await fetch_pharmacies(limit=300)

    with get_conn() as conn:
        for p in pharmacies:
            conn.execute("""
                INSERT INTO pharmacies (name, street, number, district, latitude, longitude, geom)
                VALUES (%s, %s, %s, %s, %s, %s, ST_SetSRID(ST_MakePoint(%s, %s), 4326))
                ON CONFLICT DO NOTHING;
            """, (
                p.name,
                p.street,
                p.number,
                p.district,
                p.latitude,
                p.longitude,
                p.longitude,  # lon
                p.latitude    # lat
            ))
    return len(pharmacies)


async def import_stops():
    stops = await fetch_stops()

    with get_conn() as conn:
        for s in stops:
            if not (s.latitude and s.longitude):
                continue

            conn.execute("""
                INSERT INTO stops (stop_id, stop_post, stop_name, latitude, longitude, geom)
                VALUES (%s, %s, %s, %s, %s, ST_SetSRID(ST_MakePoint(%s, %s), 4326))
                ON CONFLICT DO NOTHING;
            """, (
                s.stop_id,
                s.stop_post,
                s.stop_name,
                s.latitude,
                s.longitude,
                s.longitude,
                s.latitude
            ))
    return len(stops)



async def import_bike_stations():
    stations = await fetch_bike_stations("bike_stations")

    with get_conn() as conn:
        for s in stations:
            if not (s.latitude and s.longitude):
                continue

            conn.execute("""
                INSERT INTO bike_stations (name, description, latitude, longitude, geom)
                VALUES (%s, %s, %s, %s, ST_SetSRID(ST_MakePoint(%s, %s), 4326))
                ON CONFLICT DO NOTHING;
            """, (
                s.name,
                s.description,
                s.latitude,
                s.longitude,
                s.longitude,
                s.latitude
            ))
    return len(stations)


async def import_accommodations():
    hotels = await fetch_accommodations("hotels")
    dorms = await fetch_accommodations("dorms")
    accommodations = hotels + dorms

    with get_conn() as conn:
        for a in accommodations:
            if not (a.latitude and a.longitude):
                continue

            conn.execute("""
                INSERT INTO accommodations (objtype, name, address, latitude, longitude, geom)
                VALUES (%s, %s, %s, %s, %s, ST_SetSRID(ST_MakePoint(%s, %s), 4326))
                ON CONFLICT DO NOTHING;
            """, (
                a.objtype,
                a.name,
                a.address,
                a.latitude,
                a.longitude,
                a.longitude,
                a.latitude
            ))

    return len(accommodations)



async def main():
    init_db()

    # AEDs
    aeds_count = await import_aeds()
    print(f"Imported {aeds_count} AEDs into PostgreSQL.")

    # Theatres
    theatres_count = await import_theatres()
    print(f"Imported {theatres_count} Theatres into PostgreSQL.")


    # Tourist attractions
    attractions_count = await import_attractions()
    print(f"Imported {attractions_count} tourism attractions.")

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
