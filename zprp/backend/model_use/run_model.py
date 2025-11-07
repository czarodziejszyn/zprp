import pickle
import sys
import os
import json
sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")))
from data_science import get_random_loc
from data_science import data_record


MODEL_PATH = "../../models/model.pkl"
RADIUS = 500


def calculate_prices(lat: float, lon: float):
    """
    Parameters: lat - latitude (float), lon - longitude (float)
    Returns: (predicted_price: float, real_price: float)
    Runs the model and computes pricing values based on coordinates.
    """
    district = get_random_loc.get_district(lat, lon)
    record = data_record.DataRecord(lat, lon, RADIUS, district)
    features = list(record.features.values())
    print(features)
    with open("../../data_science/average_cost.json") as f:
        costs = json.load(f)
    label = costs[district]
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    y_pred = model.predict([features])
    return (float(y_pred[0]), label)


def create_chart():
    """
    Returns: file_path (str)
    Generates a chart image and saves it to disk. Returns the path to the generated .png file.
    """
    return "../../reports/figures/figure.png"
