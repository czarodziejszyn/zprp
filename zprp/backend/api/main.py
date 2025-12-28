from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
from pathlib import Path

from api.police_stations import fetch_police_stations, PoliceStation
from api.aeds import fetch_aeds, AEDs
from api.pharmacies import fetch_pharmacies, Pharmacy
from api.nature import fetch_nature, Nature
from api.bike_stations import fetch_bike_stations, BikeStation
from api.accomodations import fetch_accommodations, Accommodation
from api.stops import fetch_stops, Stop
from api.theatres import fetch_theatres, Theatre
from api.attractions import fetch_attractions, Attraction
from db.count_objects_nearby import count_objects_nearby
from db.get_avg_real_price import get_avg_real_price
from model_use.run_model import calculate_prices, create_chart


app = FastAPI(title="Warsaw Public Safety API")

# Endpoints for model

@app.get("/nearby")
def nearby(lat: float, lon: float, radius: int):
    result = count_objects_nearby(lat, lon, radius)
    return result

@app.get("/real_price")
def real_price(lat: float, lon: float, radius: int = 10):
    result = get_avg_real_price(lat, lon, radius)
    return result


# Endpoints for frontend
@app.get("/prices")
def get_prices(lat: float, lon: float):
    predicted, real = calculate_prices(lat, lon)
    return {
        "predicted_price": predicted,
        "real_price": real
    }


@app.get("/chart")
def get_chart():
    """
    Returns: chart image (PNG) as HTTP response
    """
    file_path_str = create_chart()
    file_path = Path(file_path_str)
    return FileResponse(file_path, media_type="image/png", filename="chart.png")


# Endpoints for database
@app.get("/police_stations", response_model=list[PoliceStation])
async def get_police_stations():
    return await fetch_police_stations()


@app.get("/aeds", response_model=list[AEDs])
async def get_aeds():
    return await fetch_aeds()


@app.get("/pharmacies", response_model=list[Pharmacy])
async def get_pharmacies():
    """
    Get list of pharmacies in Warsaw.
    """
    return await fetch_pharmacies()


@app.get("/nature/{dataset_name}", response_model=list[Nature])
async def get_nature(dataset_name: str):
    """
    Get nature data by dataset_name (bushes, forests, trees).
    """
    return await fetch_nature(dataset_name)


@app.get("/bike_stations", response_model=list[BikeStation])
async def get_bike_stations():
    """
    Get a list of Warsaw bicycle stations.
    """
    return await fetch_bike_stations("bike_stations")


@app.get("/accommodations/{dataset_name}", response_model=list[Accommodation])
async def get_accommodations(dataset_name: str):
    """
    Get list of accommodations (hotels or university dorms).
    """
    return await fetch_accommodations(dataset_name)


@app.get("/stops", response_model=list[Stop])
async def get_stops():
    """
    Get a list of Warsaw public transport stops.
    """
    return await fetch_stops()


@app.get("/theatres", response_model=list[Theatre])
async def get_theatres():
    return await fetch_theatres()


@app.get("/tourist_attractions", response_model=list[Attraction])
async def get_attractions():
    return await fetch_attractions()
