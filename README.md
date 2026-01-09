# About the project
TODO: goals, functions etc


# Data sources
- Warsaw Open Data Portal (API) – municipal and infrastructure data  
- Otodom – apartment listings and prices 
- OpenStreetMap (Warsaw PBF extract) – geospatial data used for local Nominatim-based geocoding

# Application User Manual

# How to run the application:
TODO


## How to run backend:
1) Create a .env file
Copy the file .env.example and rename it to .env. This will be your configuration file for the backend.

2) Log in to the Warszawa API:  
https://api.um.warszawa.pl/  
Read your assigned API KEY.

3) Set API KEY as an environment variable in:  
`zprpr/backend/.env`

4) Start the backend from `/zprp` directory:
This will build and start the Docker containers and import data into the PostgreSQL database.
```
make backend
```

5) Stop and remove backend Docker containers and volumes when done:
```
make stop_backend
```


## Cache
The backend uses .json files stored in `/zprp/data` directory.  
There are three subdirectories, each containing one file:  
- `./api_backup/api_cache.json`  
Cached data from the Warsaw API
- `./raw/otodom_warszawa.json`  
Cached offers scraped from the Otodom service (without coordinates)  
- `./processed/geocoded_otodom_warszawa.json`  
Cached offers from Otodom with geocoded coordinates.  


### Updating cache files:
#### Updating the Warsaw API cache: 
This command replaces the existing `./api_backup/api_cache.json` file with a fresh one.  
Make sure the backend is running beforehand.  
```
make update_api_cache
```



#### Updating Otodom offers cache: 
1) Create .env files
Copy .env.example to .env in both `/zprp/scraper` and `/zprp/geocoding` directories. 

* In `/zprp/scraper`:  
set MAX_OFFER_PAGES to choose how many pages of offers will be scraped.
* In `/zprp/geocoding`:
    * **Linux users**: set `NOMINATIM_DOMAIN=172.17.0.1:6080` in the .env file.  
    * Other users can keep the domain from .env.example.


2) Log in to Docker (Docker account required):
```
docker login
```


3) Update offers cache:  
This command replaces the existing `./raw/otodom_warszawa.json` and `./processed/geocoded_otodom_warszawa.json` files with a fresh one.  
**Note:** Scraping setup takes around 5 minutes. Geocoding setup (Nominatim initialization) can takes around 45 minutes.
```
make update_offers_cache
```

# How to run tests:
To ensure the system is stable and all modules are functioning correctly, you should run the automated test suite.

## Prerequisites
Before running the tests, ensure you have installed all necessary dependencies:
```
pip install -r requirements.txt
```

## Running the tests
TODO

### Unit testing
The project uses pytest for testing. You can execute the full suite using command:
```
make unit_tests
```