import json
import random
from shapely.geometry import shape, Point

with open("./warszawa-dzielnice.geojson", "r", encoding="utf-8") as f:
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
    """"Return random point from Warsaw (lat, lon) and its' district name."""
    while True:
        lon = random.uniform(min_lon, max_lon)
        lat = random.uniform(min_lat, max_lat)
        point = Point(lon, lat)

        for name, poly in districts:
            if poly.contains(point):
                return {"lat": round(lat, 6), "lon": round(lon, 6), "district": name}
