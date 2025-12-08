
import json
import os
import pandas as pd
from geopy.geocoders import Nominatim


NOMINATIM_DOMAIN = os.getenv("NOMINATIM_DOMAIN")
OFFERS_JSON_PATH = os.getenv("OFFERS_JSON_PATH")
GEOCODED_OFFERS_JSON_PATH = os.getenv("GEOCODED_OFFERS_JSON_PATH")

geolocator = Nominatim(user_agent="my_app", scheme="http", domain=NOMINATIM_DOMAIN)


def prepare_address_str(address):
    # remove last word - 'mazowieckie'
    addr_parts = address.split(',')[:-1]
    new_addr = ','.join(addr_parts).strip()

    # remove 'ul., al.' from the start
    if new_addr[:3] in ('ul.', 'al.'):
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
    print(f"[OK] Written {len(geocoded_offers)} records to {out_file_path}")

    





def main():
    geocode_json_file(OFFERS_JSON_PATH, GEOCODED_OFFERS_JSON_PATH)




if __name__ == "__main__":
    main()