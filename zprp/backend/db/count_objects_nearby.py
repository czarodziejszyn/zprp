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




# if __name__ == '__main__':
#     # zlote tarasy
#     lat = 52.22977
#     lon = 21.00193
#     radius_meters = 200     # 200 m

#     rows = count_objects_nearby(lat, lon, radius_meters)
#     print(rows)