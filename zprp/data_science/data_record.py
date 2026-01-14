class DataRecord:
    """
    Class that represents one record from dataset.
    Parameters:
    - lat (float) - latitude
    - lon (float) - longitude
    - radius (int) - within radius infrastructure objects are counted
    """
    ALL_FEATURES = [
        "lat",
        "lon",
        "stop",
        "bike station",
        "pharmacy",
        "aed",
        "attraction",
        "theatre",
        "tree",
        "bush",
        "forest",
        "police station",
        "hotel",
        "dorm",
    ]

    def __init__(self, lat: float, lon: float, radius: int):
        self.features = self.get_features(lat, lon, radius)

    def get_features(self, lat: float, lon: float, radius: int):
        """
        Gets infrastructure objects counts for given coordinates within given radius.
        Parameters:
        - lat (float) - latitude
        - lon (float) - longitude
        - radius (int) - within radius infrastructure objects are counted
        Returns: full_featurs (dict) - featurs in {obj: count} dict
        """
        import httpx

        url = "http://localhost:8000/nearby"
        params = {"lat": lat, "lon": lon, "radius": radius}
        response = httpx.get(url, params=params)
        data = response.json()
        print(data)

        features = {item["objtype"]: item["count"] for item in data}
        features["lat"] = lat
        features["lon"] = lon
        full_features = {ft: features.get(ft, 0) for ft in self.ALL_FEATURES}
        return full_features
