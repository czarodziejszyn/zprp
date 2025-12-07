from .db import get_conn

def get_avg_real_price(lat: float, lon: float, radius_meters: int):
    with get_conn() as conn:
        row = conn.execute("""
            SELECT AVG(price_per_m2) AS avg_price
            FROM offers
            WHERE ST_DWithin(
                geom::geography,
                ST_SetSRID(ST_MakePoint(%s, %s), 4326)::geography,
                %s
            );
        """, (lon, lat, radius_meters)).fetchone()
    price =  row['avg_price'] if row['avg_price'] is not None else 0
    return round(price, 2)

