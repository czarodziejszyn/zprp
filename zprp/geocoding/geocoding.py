import json
import logging
import os
import time

from geopy.geocoders import Nominatim
import pandas as pd
import requests

from logger import logging_config  # noqa: F401

NOMINATIM_DOMAIN = os.getenv("NOMINATIM_DOMAIN")
OFFERS_JSON_PATH = os.getenv("OFFERS_JSON_PATH")
GEOCODED_OFFERS_JSON_PATH = os.getenv("GEOCODED_OFFERS_JSON_PATH")

geolocator = Nominatim(user_agent="my_app", scheme="http", domain=NOMINATIM_DOMAIN)
logger = logging.getLogger(__name__)


def wait_for_nominatim(timeout_minutes: int = 60, interval_seconds: int = 60):
    """
    Wait until Nominatim is fully initialized and returns real results.
    """
    if not NOMINATIM_DOMAIN:
        raise RuntimeError("NOMINATIM_DOMAIN is not set")

    test_url = f"http://{NOMINATIM_DOMAIN}/search"
    params = {
        "q": "Warsaw",
        "format": "json",
        "limit": 1,
    }

    logger.info(
        "Waiting for Nominatim to be fully initialized " f"(timeout: {timeout_minutes} minutes)..."
    )

    deadline = time.time() + timeout_minutes * 60
    attempt = 0

    while time.time() < deadline:
        attempt += 1
        try:
            response = requests.get(test_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if isinstance(data, list) and len(data) > 0 and "lat" in data[0]:
                logger.info("Nominatim is READY " f"(attempt {attempt})")
                return

            logger.info(f"Nominatim not ready yet (attempt {attempt})")

        except Exception as e:
            logger.warning(f"Nominatim not ready yet (attempt {attempt}): {e}")

        time.sleep(interval_seconds)

    raise TimeoutError(f"Nominatim did not become ready within {timeout_minutes} minutes")


def prepare_address_str(address):
    # remove last word - 'mazowieckie'
    addr_parts = address.split(",")[:-1]
    new_addr = ",".join(addr_parts).strip()

    # remove 'ul., al.' from the start
    if new_addr[:3] in ("ul.", "al."):
        new_addr = new_addr[4:]

    return new_addr


def get_addr_coord(address):
    prepared_address = prepare_address_str(address)
    location = geolocator.geocode(prepared_address)
    if not location:
        return None
    return (location.latitude, location.longitude)


def geocode_offers(offers):
    geocoded_offers = []

    for offer in offers:
        coord = get_addr_coord(offer["address"])
        if not coord:
            continue
        lat, lon = coord
        offer.update({"latitude": lat, "longitude": lon})
        geocoded_offers.append(offer)

    return geocoded_offers


def geocode_json_file(in_file_path, out_file_path):
    with open(in_file_path, "r", encoding="utf-8") as handler:
        offers = json.load(handler)

    geocoded_offers = geocode_offers(offers)
    df = pd.DataFrame(geocoded_offers)
    df.to_json(out_file_path, orient="records", force_ascii=False, indent=2)
    logger.info(f"[OK] Written {len(geocoded_offers)} records to {out_file_path}")


def main():
    wait_for_nominatim()
    geocode_json_file(OFFERS_JSON_PATH, GEOCODED_OFFERS_JSON_PATH)


if __name__ == "__main__":
    main()
