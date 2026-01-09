# Cache Management
This module handles the local persistence of external API data. It ensures that the system remains functional even when Warsaw Open Data services are offline by providing a JSON-based fallback.

## Overview

The caching system performs two main tasks:
1.  Serialization: Converting Pydantic models from API into a JSON format.
2.  Persistence: Saving and loading data from the `zprp/data/api_backup/`.


## Data Sources
The cache aggregates data from the following Warsaw API endpoints:
* Accommodations, Theatres, and Attractions.
* Public transport (Stops, Bike stations).
* Public safety (Police, AEDs, Pharmacies).
* Nature (Trees, Bushes, Forests).