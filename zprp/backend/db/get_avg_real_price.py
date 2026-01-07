from .db import get_conn


def get_avg_real_price(lat: float, lon: float, radius_meters: int):
    """
    Compute the average real estate price per square meter for a given area.

    Args:
        lat (float): Latitude of the location.
        lon (float): Longitude of the location.
        radius_meters (int): Radius in meters to include in calculation.

    Returns:
        float: Average price per square meter.
               Returns 0 if no data is available.
    """
    with get_conn() as conn:
        row = conn.execute(
            """
            SELECT AVG(price_per_m2) AS avg_price
            FROM offers
            WHERE ST_DWithin(
                geom::geography,
                ST_SetSRID(ST_MakePoint(%s, %s), 4326)::geography,
                %s
            );
        """,
            (lon, lat, radius_meters),
        ).fetchone()
    price = row["avg_price"] if row["avg_price"] is not None else 0
    return round(price, 2)
