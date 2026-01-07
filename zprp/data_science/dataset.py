import pandas as pd
import json
from data_record import DataRecord


class Dataset:
    def __init__(self, radius: int, json_path: str):
        self.radius = radius
        self.json_path = json_path

    def create(self):
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
        df = self.create()
        df.to_csv(save_path)
        return df
