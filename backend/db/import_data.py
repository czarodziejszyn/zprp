import asyncio
from api.aeds import fetch_aeds
from .db import get_conn, init_db

async def main():
    init_db()
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

    print(f"Imported {len(aeds)} AEDs into PostgreSQL.")

if __name__ == "__main__":
    asyncio.run(main())
