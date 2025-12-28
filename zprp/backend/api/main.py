from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
from pathlib import Path

from api.police_stations import fetch_police_stations
from api.aeds import fetch_aeds
from api.pharmacies import fetch_pharmacies
from api.nature import fetch_nature
from api.bike_stations import fetch_bike_stations
from api.accomodations import fetch_accommodations
from api.stops import fetch_stops
from api.theatres import fetch_theatres
from api.fetch_warsaw_api import WarsawApiObj


from api.attractions import fetch_attractions
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
@app.get("/police_stations", response_model=list[WarsawApiObj])
async def get_police_stations():
    """
    Get list of police stations in Warsaw.
    """
    return await fetch_police_stations()


@app.get("/aeds", response_model=list[WarsawApiObj])
async def get_aeds():
    """
    Get list of AEDS in Warsaw.
    """
    return await fetch_aeds()


@app.get("/pharmacies", response_model=list[WarsawApiObj])
async def get_pharmacies():
    """
    Get list of pharmacies in Warsaw.
    """
    return await fetch_pharmacies()


@app.get("/nature", response_model=list[WarsawApiObj])
async def get_nature():
    """
    Get list of nature objects (bushes, forests, trees).
    """
    return await fetch_nature()


@app.get("/bike_stations", response_model=list[WarsawApiObj])
async def get_bike_stations():
    """
    Get a list of Warsaw bicycle stations.
    """
    return await fetch_bike_stations()


@app.get("/accommodations", response_model=list[WarsawApiObj])
async def get_accommodations():
    """
    Get list of accommodations (hotels or university dorms).
    """
    return await fetch_accommodations()


@app.get("/stops", response_model=list[WarsawApiObj])
async def get_stops():
    """
    Get a list of Warsaw public transport stops.
    """
    return await fetch_stops()


@app.get("/theatres", response_model=list[WarsawApiObj])
async def get_theatres():
    """
    Get list of theatres in Warsaw.
    """
    return await fetch_theatres()


@app.get("/tourist_attractions", response_model=list[WarsawApiObj])
async def get_attractions():
    """
    Get list of tourist attractions in Warsaw.
    """
    return await fetch_attractions()
