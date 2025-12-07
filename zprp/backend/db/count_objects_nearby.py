from .db import get_conn

def count_objects_nearby(lat: float, lon: float, radius_meters: int):
    with get_conn() as conn:
        rows = conn.execute("""
            SELECT
                objtype,
                COUNT(*) AS count
            FROM city_obj
            WHERE ST_DWithin(
                geom,
                ST_SetSRID(ST_MakePoint(%s, %s), 4326)::geography,
                %s
            )
            GROUP BY objtype
            ORDER BY count DESC;
        """, (
            lon,
            lat,
            radius_meters
        )).fetchall() 
    return rows
