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
            CREATE EXTENSION IF NOT EXISTS postgis;

            CREATE TABLE IF NOT EXISTS aeds (
                id SERIAL PRIMARY KEY,
                street TEXT,
                building TEXT,
                latitude DOUBLE PRECISION,
                longitude DOUBLE PRECISION,
                geom GEOGRAPHY(POINT, 4326)
            );

            CREATE TABLE IF NOT EXISTS theatres (
                id SERIAL PRIMARY KEY,
                name TEXT,
                address TEXT,
                district TEXT,
                latitude DOUBLE PRECISION,
                longitude DOUBLE PRECISION,
                geom GEOGRAPHY(POINT, 4326)
            );
                     
            CREATE TABLE IF NOT EXISTS attractions (
                id SERIAL PRIMARY KEY,
                name TEXT,
                address TEXT,
                city TEXT,
                category TEXT,
                latitude DOUBLE PRECISION,
                longitude DOUBLE PRECISION,
                geom GEOGRAPHY(POINT, 4326)
            );
                
            CREATE TABLE IF NOT EXISTS nature (
                id SERIAL PRIMARY KEY,
                objtype TEXT,               -- tree / bush / forest
                address TEXT,
                district TEXT,
                latitude DOUBLE PRECISION,
                longitude DOUBLE PRECISION,
                geom GEOGRAPHY(POINT, 4326)
            );        

                     
            CREATE TABLE IF NOT EXISTS police_stations (
                id SERIAL PRIMARY KEY,
                name TEXT,
                district TEXT,
                latitude DOUBLE PRECISION,
                longitude DOUBLE PRECISION,
                geom GEOGRAPHY(POINT, 4326)
            );

            CREATE TABLE IF NOT EXISTS pharmacies (
                id SERIAL PRIMARY KEY,
                name TEXT,
                street TEXT,
                number TEXT,
                district TEXT,
                latitude DOUBLE PRECISION,
                longitude DOUBLE PRECISION,
                geom GEOGRAPHY(POINT, 4326)
            );

                     
            CREATE TABLE IF NOT EXISTS stops (
                id SERIAL PRIMARY KEY,
                stop_id TEXT,
                stop_post TEXT,
                stop_name TEXT,
                latitude DOUBLE PRECISION,
                longitude DOUBLE PRECISION,
                geom GEOGRAPHY(POINT, 4326)
            );

                     
            CREATE TABLE IF NOT EXISTS bike_stations (
                id SERIAL PRIMARY KEY,
                name TEXT,
                description TEXT,
                latitude DOUBLE PRECISION,
                longitude DOUBLE PRECISION,
                geom GEOGRAPHY(POINT, 4326)
            );

                     
            CREATE TABLE IF NOT EXISTS accommodations (
                id SERIAL PRIMARY KEY,
                objtype TEXT,  -- hotel or dorm
                name TEXT,
                address TEXT,
                latitude DOUBLE PRECISION,
                longitude DOUBLE PRECISION,
                geom GEOGRAPHY(POINT, 4326)
            );
                     

        """)
