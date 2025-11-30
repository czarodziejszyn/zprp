import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.bank-nieruchomosci.pl"
START_URL = "https://www.bank-nieruchomosci.pl/ogloszenia?type_id=&price_min=&price_max=&sym=918123&area_min=&area_max=&market_type=0&year=&type=1"

offers = []
page = 1

while True:
    print(f"Scraping strona {page}...")

    # URL z numerem strony
    url = START_URL + f"&page={page}"
    resp = requests.get(url)

    if resp.status_code != 200:
        print("Błąd HTTP, przerywam.")
        break

    soup = BeautifulSoup(resp.text, "html.parser")

    # wszystkie ogłoszenia na stronie
    items = soup.select(".feat_property.home7.style4")

    if not items:
        print("Brak ogłoszeń → koniec stron.")
        break

    for item in items:
        title_tag = item.select_one("h4.text-overflow")
        title = title_tag["title"] if title_tag else None

        location_tag = item.select_one("p.text-overflow[title]")
        location = location_tag["title"] if location_tag else None

        price_tag = item.select_one("a.fp_price b")
        price = price_tag.get_text(strip=True) if price_tag else None

        size_tag = item.select_one("li.rent_detail")
        size = size_tag.get_text(strip=True) if size_tag else None

        link_tag = item.select_one("a.details")
        link = BASE_URL + link_tag["href"] if link_tag else None

        offers.append({
            "title": title,
            "location": location,
            "price": price,
            "size": size,
            "link": link
        })

    page += 1  

offers = offers[:-1] # usuniety ostatni niepotrzbeny wiersz

for o in offers:
    print(o)

print(f"\nZebrano razem {len(offers)} ogłoszeń.")
