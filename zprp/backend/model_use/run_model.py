import os
import pickle
import sys
from db.get_avg_real_price import get_avg_real_price

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")
)
sys.path.append(BASE_DIR)

from data_science import data_record


MODEL_PATH = "models/model.pkl"
RADIUS = 700


def calculate_prices(lat: float, lon: float):
    """
    Parameters: lat - latitude (float), lon - longitude (float)
    Returns: (predicted_price: float, real_price: float)
    Runs the model and computes pricing values based on coordinates.
    """
    record = data_record.DataRecord(lat, lon, RADIUS)
    features = list(record.features.values())
    label = get_avg_real_price(lat, lon, 500)
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    y_pred = model.predict([features])
    return (float(y_pred[0]), label)


def create_chart():
    """
    Returns: file_path (str)
    Generates a chart image and saves it to disk. Returns the path to the generated .png file.
    """
    return "reports/figures/chart.png"
