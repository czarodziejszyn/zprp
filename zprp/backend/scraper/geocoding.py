import requests
import time


def get_street_coord(street_address):
    base_url = "https://nominatim.openstreetmap.org/search"
    query = street_address

    if query[:3] in ('ul.', 'al.'):
        query = query[4:]

    params = {
        'q': query,
        'format': 'json',
        'limit': 1,
        'addressdetails': 1
    }
    
    headers = {
        'User-Agent': 'real_estate_scrapper/1.0 (julaczyzewska28@gmail.com)'
    }


    try:
        response = requests.get(base_url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        if not data:
            return None
        

        result = data[0]
        lat = float(result['lat'])
        lon = float(result['lon'])
        return (lat, lon)
    

    except Exception as e:
        print(f"Geocoding exception: {e}")
        return None
    
    
if __name__ == "__main__":
    offer = {"address":"gen. Tadeusza Pełczyńskiego, Górce, Bemowo, Warszawa, mazowieckie"}
    coord = get_street_coord(offer["address"])
    print(coord)
