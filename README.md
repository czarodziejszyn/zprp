# Application User Manual

# How to run the application:
TODO


## How to run backend:
1. Log in to the Warszawa API:  
https://api.um.warszawa.pl/  
Read your assigned API KEY.

2. Set API KEY as an environment variable in:  
`zprpr/backend/.env`

3. Make sure Docker is running.

4. Start the backend from `/zprp` directory:
This will build and start the Docker containers and import data into the PostgreSQL database.
```
make backend
```

5. Stop and remove backend Docker containers and volumes:
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
This command replaces the existing `zprp/data/api_backup/api_cache.json` file with a fresh one:
```
docker compose exec api bash
python -m cache.save_cache
```



#### Updating Otodom offers cache: 
Updating the Otodom cache consists of two mandatory stages:
1. Updating .json file in `zprp/data/raw`  
2. Using that file to generate .json file in `zprp/data/processed`  

Both steps must be executed in order. The application reads data only from the processed directory.


##### Scrapping - updating .json file in `zprp/data/raw`
1) Create a .env file in `zrpr/scraper`. 
You can configure: 
* number of pages to scrap, 
* output .json file name.

2) Build the Docker image.
```
docker compose build --no-cache
```

3) Run main.py to scrape offers. This will create .json file in `./data/raw`. (Offers are not geocoded yet).
```
docker compose up
```

4) Stop the containter:
```
docker compose down
```


##### Geocoding - updating .json file in `zprp/data/processed`
###### Setting up the Nominativ server:
1) Log in to Docker (Docker account required):
```
docker login
```

2) Run the Nominatim server:
```
docker run -d -p 6080:8080 -e NOMINATIM_PBF_URL="https://download.bbbike.org/osm/bbbike/Warsaw/Warsaw.osm.pbf" -e POSTGRES_PASSWORD="haslo" --name nominatim-warsaw peterevans/nominatim:latest
```
3) Monitor the logs. Setup takes around 20-30min:
```
docker logs -f nominatim-warsaw
```

After completion, the Nominatim server will be available at:  
http://localhost:6080/ 


**Linux users**:  
In the .env file, set:  
`NOMINATIM_DOMAIN=172.17.0.1:6080`



4) To stop or restart the server:
```
docker stop nominatim-warsaw
docker start nominatim-warsaw
```


###### Geocoding 
This process generates a .json file with geocoded offers in `./data/processed`. 
```
docker compose build --no-cache
docker compose up
```


