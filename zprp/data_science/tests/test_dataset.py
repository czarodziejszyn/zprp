import json
import pandas as pd
from unittest.mock import patch
from dataset import Dataset


def test_create_dataset(tmp_path):
    data = [
        {"latitude": 52.1, "longitude": 21.0, "price_per_m2": 12000},
        {"latitude": 52.2, "longitude": 21.1, "price_per_m2": 15000},
    ]

    json_file = tmp_path / "data.json"
    json_file.write_text(json.dumps(data))

    fake_features = {
        "lat": 52.1,
        "lon": 21.0,
        "stop": 1,
        "bike station": 0,
        "pharmacy": 0,
        "aed": 0,
        "attraction": 0,
        "theatre": 0,
        "tree": 0,
        "bush": 0,
        "forest": 0,
        "police station": 0,
        "hotel": 0,
        "dorm": 0,
    }

    with patch("dataset.DataRecord") as mock_record:
        mock_record.return_value.features = fake_features

        ds = Dataset(radius=300, json_path=str(json_file))
        df = ds.create()

        assert isinstance(df, pd.DataFrame)
        assert "cost" in df.columns
        assert len(df) == 2
