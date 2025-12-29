import json
import os
API_CACHE_JSON_PATH = os.getenv("API_CACHE_JSON_PATH")

def save_api_cache_json(data):
    with open(API_CACHE_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_api_cache_json():
    if not os.path.exists(API_CACHE_JSON_PATH):
        raise FileNotFoundError(f"Backup JSON not found: {API_CACHE_JSON_PATH}")
    with open(API_CACHE_JSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)