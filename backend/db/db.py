import os
import psycopg
from psycopg.rows import dict_row

DB_HOST = os.getenv("POSTGRES_HOST", "db")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASS = os.getenv("POSTGRES_PASSWORD")

def get_conn():
    return psycopg.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        row_factory=dict_row
    )

def init_db():
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS theatres (
                id SERIAL PRIMARY KEY,
                name TEXT,
                address TEXT,
                district TEXT,
                latitude DOUBLE PRECISION,
                longitude DOUBLE PRECISION,
                geom GEOGRAPHY(POINT, 4326)
            );
        """)
