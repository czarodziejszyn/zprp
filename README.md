# About the project - Real Estate & Urban Infrastructure Analyzer

A web application designed to analyze the impact of urban infrastructure on real estate prices. This project leverages geospatial and market data to evaluate how proximity to city amenities affects housing values.
## Key Features:

* Infrastructure Impact Analysis: Evaluates how proximity to forests, bus stops, hotels, and other urban amenities influences market prices.

* Predictive Modeling: Uses Machine Learning to estimate property values based on precise geographical coordinates and surrounding infrastructure density.

* Spatial Visualization: Generates charts to illustrate real estate trends.

* Data Integration: Combines live data from the Warsaw Open Data API with market records and geocoded listings.


# Data sources

- Warsaw Open Data Portal (API) – municipal and infrastructure data
- Otodom – apartment listings and prices
- OpenStreetMap (Warsaw PBF extract) – geospatial data used for local Nominatim-based geocoding

# Application User Manual

# How to run the application:

After cloning this repository go to `zprp/` directory:
```
cd zprp
```
Before first launch, do first 3 steps from [backend section](#how-to-run-backend) and setup environment:
```
make setup
```
To run the app:
```
make run
```

## Frontend — how to run

From the `zprp/` directory:

```bash
make frontend_setup
make frontend_run
```

The frontend calls the backend using `BACKEND_BASE_URL` (defaults to `http://localhost:8000`). You can override it:

```bash
BACKEND_BASE_URL=http://127.0.0.1:8000 make frontend_run
```

### Frontend end-to-end tests

From the `zprp/` directory:

```bash
make frontend_test
```

Note: `make frontend_test` starts a local mock backend for `/prices` and `/chart` so you don't need to run the real backend to execute e2e tests.

## How to run backend:

1) Create a .env file
   Copy the file .env.example and rename it to .env. This will be your configuration file for the backend.
2) Log in to the Warszawa API:
   https://api.um.warszawa.pl/
   Read your assigned API KEY.
3) Set API KEY as an environment variable in:
   `zprp/backend/.env`
4) Ensure that Docker is running, on linux:
```
sudo systemctl start docker
```
5) Start the backend from `/zprp` directory:
   This will build and start the Docker containers and import data into the PostgreSQL database.

```
make backend
```

6) Stop and remove backend Docker containers and volumes when done:

```
make stop_backend
```

## Cache

The backend uses .json files stored in `/zprp/data` directory.There are three subdirectories, each containing one file:

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

### Unit tests (pytest)

From the `zprp/` directory:

```bash
make unit_tests
```

### Frontend e2e tests

From the `zprp/` directory:

```bash
make frontend_test
```

### Unit testing

The project uses pytest for testing. You can execute the full suite using command:

```
make unit_tests
```
