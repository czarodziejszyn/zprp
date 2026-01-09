# Database and Spatial Analysis
This module manages the connection to the PostgreSQL database and uses the PostGIS extension for geospatial queries. It is responsible for schema initialization, importing data and spatial calculations.

## Database management:

### Connection management - `db.py`:
The system uses `psycopg (v3)` to interact with PostgreSQL.
* Resilience: The `get_conn` function implements a retry mechanism (up to 15 attempts). This is essential in a Dockerized environment where the database container initializes slower than the API container.

* Initialization: `init_db` enables the PostGIS extension and creates tables using the WGS 84 (SRID 4326) coordinate system:
    * city_obj: Stores urban infrastructure objects.
    * offers: Stores geocoded real estate listings.


### Data import pipeline - `import_data.py`:
A script that populates the database from two sources:
* Local Files: Imports geocoded property offers from JSON.
* Hybrid API/Cache: Fetches urban data from the Warsaw API. If the API is down, it automatically switches to the local JSON cache.

## Spatial query logic:
These functions support the FastAPI endpoints by performing heavy SQL lifting.  
* `count_objects_nearby.py` - Contains function by the same name. Aggregates urban objects by type to get their count within a user-defined radius.
* `get_avg_real_price.py` - Contains function by the same name. Calculates the average price per square meter within a user-defined radius.