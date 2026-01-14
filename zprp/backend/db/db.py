import logging
import os
import time

import psycopg
from psycopg.rows import dict_row

logger = logging.getLogger(__name__)

DB_HOST = os.getenv("POSTGRES_HOST", "db")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASS = os.getenv("POSTGRES_PASSWORD")


def get_conn(max_retries=15, delay=1):
    for attempt in range(max_retries):
        try:
            conn = psycopg.connect(
                host=DB_HOST,
                port=DB_PORT,
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASS,
                row_factory=dict_row,
            )
            logger.debug(f"Connected to PostgreSQL on attempt {attempt + 1}")
            return conn
        except psycopg.OperationalError:
            logger.warning(f"PostgreSQL not ready (attempt {attempt + 1}/{max_retries})")
            time.sleep(delay)
    raise Exception(
        f"Could not connect to PostgreSQL at {DB_HOST}:{DB_PORT} after {max_retries} attempts"
    )


def init_db():
    with get_conn() as conn:
        conn.execute(
            """
            CREATE EXTENSION IF NOT EXISTS postgis;

            CREATE TABLE city_obj (
                id SERIAL PRIMARY KEY,
                objtype TEXT,
                latitude DOUBLE PRECISION,
                longitude DOUBLE PRECISION,
                geom GEOGRAPHY(POINT, 4326)
            );

            CREATE INDEX city_obj_geom_gix
            ON city_obj USING GIST (geom);


            CREATE TABLE IF NOT EXISTS offers (
                id SERIAL PRIMARY KEY,
                title TEXT,
                url TEXT,
                price INTEGER,
                area_m2 NUMERIC,
                price_per_m2 NUMERIC,
                address TEXT,
                latitude DOUBLE PRECISION,
                longitude DOUBLE PRECISION,
                geom GEOGRAPHY(POINT, 4326)
            );

        """
        )
