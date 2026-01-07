from pathlib import Path

from db.count_objects_nearby import count_objects_nearby
from db.get_avg_real_price import get_avg_real_price
from fastapi import FastAPI
from fastapi.responses import FileResponse
from model_use.run_model import calculate_prices, create_chart

app = FastAPI(title="Warsaw Public Safety API")


# Endpoints for model
@app.get("/nearby")
def nearby(lat: float, lon: float, radius: int):
    """
    Return a list of objects (object type and its count) near the given location.
    Each item corresponds to a database Row object.
    """
    result = count_objects_nearby(lat, lon, radius)
    return result


@app.get("/real_price")
def real_price(lat: float, lon: float, radius: int = 10):
    """
    Return real average prize per meter near given location.
    """
    result = get_avg_real_price(lat, lon, radius)
    return result


# Endpoints for frontend
@app.get("/prices")
def get_prices(lat: float, lon: float):
    """
    Calculate predicted and real estate prices using a pre-trained model.
    """
    predicted, real = calculate_prices(lat, lon)
    return {"predicted_price": predicted, "real_price": real}


@app.get("/chart")
def get_chart():
    """
    Create a chart and save it to the disk.
    Return chart image (PNG) as HTTP response.
    """
    file_path_str = create_chart()
    file_path = Path(file_path_str)
    return FileResponse(file_path, media_type="image/png", filename="chart.png")
