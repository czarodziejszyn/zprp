import json
import random
import os
from shapely.geometry import shape, Point

base_dir = os.path.dirname(__file__)
geojson_path = os.path.join(base_dir, "warszawa-dzielnice.geojson")
with open(geojson_path, "r", encoding="utf-8") as f:
    geo = json.load(f)

districts = []
for feature in geo["features"]:
    name = feature["properties"]["name"]
    if name == "Warszawa":
        continue
    polygon = shape(feature["geometry"])
    districts.append((name, polygon))

min_lon, max_lon = 20.51, 21.16
min_lat, max_lat = 52.05, 52.22


def random_warsaw_loc():
    """"Returns random point from Warsaw (lat, lon) and its' district name."""
    while True:
        lon = random.uniform(min_lon, max_lon)
        lat = random.uniform(min_lat, max_lat)
        point = Point(lon, lat)

        for name, poly in districts:
            if poly.contains(point):
                return {"lat": round(lat, 6), "lon": round(lon, 6), "district": name}


def get_district(lat: float, lon: float):
    point = Point(lon, lat)
    for name, poly in districts:
        print(name)
        if poly.contains(point):
            return name
