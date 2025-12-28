import os


class DataRecord:
    ALL_FEATURES = ["lat", "lon", "stop", "bike station",
                    "pharmacy", "aed", "attraction", "theatre", "tree", "bush", "forest", "police station", "hotel", "dorm"]

    def __init__(self, lat: float, lon: float, radius: int, district: str):
        self.features = self.get_features(lat, lon, radius)
        self.label = self.get_label(district)

    def get_features(self, lat: float, lon: float, radius: int):
        import httpx
        url = "http://localhost:8000/nearby"
        params = {
            "lat": lat,
            "lon": lon,
            "radius": radius
        }
        response = httpx.get(url, params=params)
        data = response.json()
        print(data)

        features = {item["objtype"]: item["count"] for item in data}
        features["lat"] = lat
        features["lon"] = lon
        full_features = {ft: features.get(ft, 0) for ft in self.ALL_FEATURES}
        return full_features

    def get_label(self, district):
        import json
        base_dir = os.path.dirname(__file__)
        average_path = os.path.join(base_dir, "average_cost.json")
        with open(average_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data[district]
