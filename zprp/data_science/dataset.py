import json

from data_record import DataRecord
import pandas as pd


class Dataset:
    """
    CLass used to create dataset.

    Parameters: 
    - radius (int) - within radius infrastructure objects are counted
    - json_path (str) - path to JSON file with offers coordinates and real prices
    """

    def __init__(self, radius: int, json_path: str):
        self.radius = radius
        self.json_path = json_path

    def create(self):
        """
        Creates dataset.
        Returns: dataset (DataFrame)
        """
        with open(self.json_path) as f:
            data = json.load(f)

        records = []
        for offer in data:
            lat = offer["latitude"]
            lon = offer["longitude"]
            label = offer["price_per_m2"]
            record = DataRecord(lat, lon, self.radius)
            records.append(record.features | {"cost": label})
        return pd.DataFrame(records)

    def save_to_csv(self, save_path: str):
        """
        Saves dataset to file.
        Parameters: save_path (string) - path to save file
        """
        df = self.create()
        df.to_csv(save_path)
        return df
