import asyncio
from api.aeds import fetch_aeds
from api.theatres import fetch_theatres
from api.attractions import fetch_attractions

from .db import get_conn, init_db


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


async def main():
    init_db()

    # # AEDs
    # aeds_count = await import_aeds()
    # print(f"Imported {aeds_count} AEDs into PostgreSQL.")

    # # Theatres
    # theatres_count = await import_theatres()
    # print(f"Imported {theatres_count} Theatres into PostgreSQL.")


    # Tourist attractions
    attractions_count = await import_attractions()
    print(f"Imported {attractions_count} tourism attractions.")



if __name__ == "__main__":
    asyncio.run(main())
