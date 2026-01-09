import os
import sys
from unittest.mock import MagicMock, patch

import pytest

# Mock logger module
sys.modules["logger"] = MagicMock()
sys.modules["logger.logging_config"] = MagicMock()

with patch.dict(
    os.environ,
    {
        "NOMINATIM_DOMAIN": "localhost:8080",
        "OFFERS_JSON_PATH": "offers.json",
        "GEOCODED_OFFERS_JSON_PATH": "geocoded.json",
    },
):
    from geocoding import (
        geocode_offers,
        get_addr_coord,
        prepare_address_str,
        wait_for_nominatim,
    )


def test_prepare_address_str():
    addr1 = "ul. Marszałkowska 10, Warszawa, mazowieckie"
    assert prepare_address_str(addr1) == "Marszałkowska 10, Warszawa"

    addr2 = "al. Jerozolimskie 20, Warszawa, mazowieckie"
    assert prepare_address_str(addr2) == "Jerozolimskie 20, Warszawa"


@patch("geocoding.geolocator.geocode")
def test_get_addr_coord_success(mock_geocode):
    mock_location = MagicMock()
    mock_location.latitude = 52.23
    mock_location.longitude = 21.01
    mock_geocode.return_value = mock_location

    result = get_addr_coord("ul. Testowa 1, Warszawa, mazowieckie")

    assert result == (52.23, 21.01)
    mock_geocode.assert_called_with("Testowa 1, Warszawa")


@patch("geocoding.geolocator.geocode")
def test_get_addr_coord_fail(mock_geocode):
    mock_geocode.return_value = None

    result = get_addr_coord("Nieistniejacy Adres")

    assert result is None


@patch("geocoding.get_addr_coord")
def test_geocode_offers(mock_get_coord):
    mock_get_coord.return_value = (52.0, 21.0)
    offers = [{"address": "Adres 1", "title": "Mieszkanie"}]

    results = geocode_offers(offers)

    assert len(results) == 1
    assert results[0]["latitude"] == 52.0
    assert results[0]["longitude"] == 21.0


@patch("geocoding.requests.get")
@patch("geocoding.time.sleep", return_value=None)
def test_wait_for_nominatim_success(mock_sleep, mock_get):
    mock_response_fail = MagicMock()
    mock_response_fail.raise_for_status.side_effect = Exception("Not ready")

    mock_response_success = MagicMock()
    mock_response_success.json.return_value = [{"lat": "52.2"}]

    mock_get.side_effect = [mock_response_fail, mock_response_success]

    wait_for_nominatim(timeout_minutes=1, interval_seconds=1)
    assert mock_get.call_count == 2


@patch("geocoding.requests.get")
@patch("geocoding.time.sleep", return_value=None)
def test_wait_for_nominatim_timeout(mock_sleep, mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = []
    mock_get.return_value = mock_response

    with pytest.raises(TimeoutError):
        wait_for_nominatim(timeout_minutes=0.01, interval_seconds=0.01)
