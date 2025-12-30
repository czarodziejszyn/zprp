
import os
from scrapping import scrap_offers, write_offers_to_json


MAX_OFFER_PAGES = int(os.getenv("MAX_OFFER_PAGES"))
OFFERS_JSON_PATH = os.getenv("OFFERS_JSON_PATH")


def main():
    # Scrap offers and write them to .json file
    all_offers = scrap_offers(MAX_OFFER_PAGES)
    write_offers_to_json(all_offers, OFFERS_JSON_PATH)


if __name__ == "__main__":
    main()
