from .db import get_conn


def count_objects_nearby(lat: float, lon: float, radius_meters: int):
    """
    Count objects of different types nearby a given location.

    Args:
        lat (float): Latitude of the location.
        lon (float): Longitude of the location.
        radius (int): Radius in meters to search within.

    Returns:
        list: List of Row objects (from SQL execution), each with attributes:
            - objtype (str): Type of object
            - count (int): Number of objects of this type within the radius
    """
    with get_conn() as conn:
        rows = conn.execute(
            """
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
        """,
            (lon, lat, radius_meters),
        ).fetchall()
    return rows
