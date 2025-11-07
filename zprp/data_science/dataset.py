import pandas as pd
import json
from data_record import DataRecord
from get_random_loc import random_warsaw_loc


class Dataset:
    def __init__(self, radius: int, size: int):
        self.radius = radius
        self.size = size

    def create(self):
        with open("./average_cost.json") as f:
            costs = json.load(f)
        records = []
        for _ in range(self.size):
            rand_loc = random_warsaw_loc()
            lat, lon, district = rand_loc["lat"], rand_loc["lon"], rand_loc["district"]
            record = DataRecord(lat, lon, self.radius, district)
            label = costs[district]
            print(record.features)
            records.append(record.features | {"cost": label})
        return pd.DataFrame(records)

    def save_to_csv(self, path: str):
        df = self.create()
        df.to_csv(path)
        return df
