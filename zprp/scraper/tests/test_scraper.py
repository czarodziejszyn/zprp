import os
from unittest.mock import MagicMock, patch

import pandas as pd
from scrapping import scrap_offers, write_offers_to_json

FAKE_ENV = {
    "OTODOM_URL": "http://fake.url",
    "CHROME_BINARY_PATH": "C:/fake/chrome.exe",
    "CHROMEDRIVER_PATH": "C:/fake/chromedriver.exe",
    "MAX_OFFER_PAGES": "1",
}


def test_write_offers_to_json(tmp_path):
    file_path = tmp_path / "test_offers.json"
    fake_offers = [{"title": "Test", "price": 1000}]

    write_offers_to_json(fake_offers, str(file_path))

    assert file_path.exists()
    df = pd.read_json(str(file_path))
    assert len(df) == 1
    assert df.iloc[0]["title"] == "Test"


@patch("scrapping.webdriver.Chrome")
@patch("scrapping.Service")
@patch.dict(os.environ, FAKE_ENV)
def test_scrap_offers_logic(mock_service, mock_chrome):
    with (
        patch("scrapping.CHROME_BINARY_PATH", FAKE_ENV["CHROME_BINARY_PATH"]),
        patch("scrapping.CHROMEDRIVER_PATH", FAKE_ENV["CHROMEDRIVER_PATH"]),
    ):

        driver = MagicMock()
        mock_chrome.return_value = driver

        mock_offer = MagicMock()
        mock_offer.text = "Mieszkanie 50 m² Warszawa"

        mock_link = MagicMock()
        mock_link.get_attribute.return_value = "https://otodom.pl/oferta/ladne-mieszkanie-ID123"

        mock_price = MagicMock()
        mock_price.text = "500 000 zł"

        mock_address = MagicMock()
        mock_address.text = "ul. Marszałkowska, Warszawa"

        driver.find_elements.return_value = [mock_offer]

        def side_effect(by, value):
            if "MainPrice" in value:
                return mock_price
            if "Address" in value:
                return mock_address
            if "/oferta/" in value:
                return mock_link
            return MagicMock()

        mock_offer.find_element.side_effect = side_effect

        results = scrap_offers(max_offer_pages=1)

        assert len(results) == 1
        offer = results[0]
        assert offer["price"] == 500000
        assert offer["area_m2"] == 50.0
        assert offer["price_per_m2"] == 10000.0
        assert "ladne mieszkanie ID123" in offer["title"]
        assert offer["address"] == "ul. Marszałkowska, Warszawa"


@patch("scrapping.webdriver.Chrome")
@patch("scrapping.Service")
@patch.dict(os.environ, FAKE_ENV)
def test_scrap_offers_duplicates(mock_service, mock_chrome):
    with (
        patch("scrapping.CHROME_BINARY_PATH", FAKE_ENV["CHROME_BINARY_PATH"]),
        patch("scrapping.CHROMEDRIVER_PATH", FAKE_ENV["CHROMEDRIVER_PATH"]),
    ):

        driver = MagicMock()
        mock_chrome.return_value = driver

        mock_offer = MagicMock()
        mock_link = MagicMock()
        mock_link.get_attribute.return_value = "https://otodom.pl/oferta/mieszkanie-ID777"
        mock_offer.find_element.return_value = mock_link
        mock_offer.text = "40 m² 400000 zł"

        driver.find_elements.return_value = [mock_offer, mock_offer]

        results = scrap_offers(max_offer_pages=1)

        assert len(results) == 1
