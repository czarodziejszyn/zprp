# Data

This directory contains JSON files used as a local data cache for the project.
All files are generated automatically by backend processes and should not be
edited manually.


## Directory Structure

### `api_backup/`
Failover storage for external API data. It provides a local cache used automatically when primary remote services are unavailable.

- `api_cache.json`  
  Cached data fetched from the Warsaw Open Data API



### `raw/`
Contains unprocessed data collected from external sources.

- `otodom_warszawa.json`  
  Offers scraped from the Otodom service without geocoded coordinates.


### `processed/`
Contains processed datasets derived from raw data.

- `geocoded_otodom_warszawa.json`  
  Scraped offers integrated with latitude and longitude using the geocoding module.


