import asyncio
from api.theatres import fetch_theatres
from db import get_conn, init_db

async def main():
    init_db()
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
                t.longitude,  # POINT(lon, lat) order
                t.latitude
            ))

    print(f"Imported {len(theatres)} theatres into PostgreSQL.")

if __name__ == "__main__":
    asyncio.run(main())
