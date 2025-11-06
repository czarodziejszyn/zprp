from fastapi import FastAPI, Query

from api.police_stations import fetch_police_stations, PoliceStation
from api.aeds import fetch_aeds, AEDs
from api.pharmacies import fetch_pharmacies, Pharmacy
from api.nature import fetch_nature, Nature
from api.bicycle_stations import fetch_bike_stations, BikeStation
from api.accomodations import fetch_accommodations, Accommodation
from api.stops import fetch_stops, Stop
from api.theatres import fetch_theatres, Theatre
from api.attractions import fetch_attractions, Attraction



app = FastAPI(title="Warsaw Public Safety API")


@app.get("/police_stations", response_model=list[PoliceStation])
async def get_police_stations(limit: int = Query(10, ge=1, le=200)):
    return await fetch_police_stations(limit=limit)


@app.get("/aeds", response_model=list[AEDs])
async def get_aeds(limit: int = Query(10, ge=1, le=200)):
    return await fetch_aeds(limit=limit)


@app.get("/pharmacies", response_model=list[Pharmacy])
async def get_pharmacies(limit: int = Query(10, ge=1, le=100)):
    """
    Get list of pharmacies in Warsaw.
    """
    return await fetch_pharmacies(limit=limit)


@app.get("/nature/{dataset_name}", response_model=list[Nature])
async def get_nature(dataset_name: str):
    """
    Get nature data by dataset_name (bushes, forests, trees). Default limit is 100 results.
    """
    return await fetch_nature(dataset_name)


@app.get("/bike_stations", response_model=list[BikeStation])
async def get_bike_stations(limit: int = Query(10, ge=1, le=100)):
    """
    Get a list of Warsaw bicycle stations.
    """
    return await fetch_bike_stations("bike_stations", limit=limit)


@app.get("/accommodations/{dataset_name}", response_model=list[Accommodation])
async def get_accommodations(
    dataset_name: str,
    limit: int = Query(10, ge=1, le=100)
):
    """
    Get list of accommodations (hotels or university dorms).
    """
    return await fetch_accommodations(dataset_name, limit=limit)



@app.get("/stops", response_model=list[Stop])
async def get_stops(limit: int = Query(10, ge=1, le=500)):
    """
    Get a list of Warsaw public transport stops (up to `limit`).
    """
    return await fetch_stops(limit=limit)



@app.get("/theatres", response_model=list[Theatre])
async def get_theatres():
    return await fetch_theatres()


@app.get("/tourist_attractions", response_model=list[Attraction])
async def get_attractions():
    return await fetch_attractions()