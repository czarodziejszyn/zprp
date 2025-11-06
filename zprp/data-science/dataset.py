import pandas as pd
from data_record import DataRecord


class Dataset:
    def __init__(self, circle: int, size: int):
        self.circle = circle
        self.size = size
        self.features = []
        self.label = None

    def create(self):
        records = [DataRecord(self.circle) for _ in range(self.size)]
        data = [r.features | r.label for r in records]
        return pd.DataFrame(data)

    def save_to_csv(self, path: str):
        df = self.create()
        df.to_csv(path)
        return df
