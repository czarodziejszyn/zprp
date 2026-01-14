# Geocoding reference
This module is responsible for converting raw address strings from real estate listings into geographical coordinates (latitude and longitude). This transformation is essential for spatial analysis and map-based price prediction.

## Infrastructure & Pipeline Execution
The geocoding process is containerized and managed via a Makefile.
The Pipeline Workflow:
* `nominatim_start`: Spins up a Docker container with a specialized OpenStreetMap image containing Warsaw's geographical data.
* `build_geocoding`: Builds the local geocoding service image.
* `run_geocoding`: Executes the Python script that processes the listings.
* `nominatim_stop`: Shuts down the local geocoder to free up system resources.

## Core Functionality - `geocoding.py`
The module utilizes a local instance of the Nominatim geocoding engine based on OpenStreetMap data. The process is divided into three main stages:

1. Service Synchronization - `wait_for_nominatim`
Synchronization helper. It pings the server until it returns a valid response for a test query ("Warsaw"), ensuring the pipeline doesn't start before the geocoder is ready. 

2. Address Normalization - `prepare_address_str`
To improve the success rate of the geolocator, addresses are normalized by:
    * Removing administrative suffix ("mazowieckie").
    * Stripping common prefixes like "ul." or "al." 

3. Geocoding Engine - `geocode_offers`
The module iterates through the scraped JSON data, appends coordinates to each listing, and filters out any offers that could not be accurately located.



## Technical Configuration
The geocoding relies on several environment variables. The most critical are:
* `NOMINATIM_DOMAIN`: The address of the Nominatim service.  
**Note for Linux Users**: To allow communication between Docker containers, Linux users should set this to **172.17.0.1:6080**. Other users can use the default address provided in the `.env.example` file.  
* `OFFERS_JSON_PATH`: Input file containing raw scraped listings.
* `GEOCODED_OFFERS_JSON_PATH`: Output file path for listings with GPS coordinates.
