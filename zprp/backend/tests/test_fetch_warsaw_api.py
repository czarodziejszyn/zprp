from unittest.mock import patch

from api.accomodations import fetch_accommodations
from api.aeds import fetch_aeds
from api.attractions import fetch_attractions
from api.bike_stations import fetch_bike_stations
from api.fetch_warsaw_api import get_warsaw_api_obj_data_result
from api.nature import fetch_nature
from api.pharmacies import fetch_pharmacies
from api.police_stations import fetch_police_stations
from api.stops import fetch_stops
from api.theatres import fetch_theatres
from fastapi import HTTPException
import httpx
import pytest
import respx

with patch.dict("os.environ", {"WARSZAWA_API_KEY": "test_key"}):
    pass


@pytest.mark.asyncio
@respx.mock
async def test_get_warsaw_api_data_success():
    dataset_name = "attraction"
    url = "https://api.um.warszawa.pl/api/action/tourism_attraction_get/"
    respx.get(url).mock(return_value=httpx.Response(200, json={"result": [{"id": 1}]}))

    result = await get_warsaw_api_obj_data_result(dataset_name)

    assert result == [{"id": 1}]


@pytest.mark.asyncio
@respx.mock
async def test_get_warsaw_api_data_retry_logic():
    url = "https://api.um.warszawa.pl/api/action/tourism_attraction_get/"

    respx.get(url).side_effect = [
        httpx.TimeoutException("Timeout!"),
        httpx.Response(200, json={"result": [{"id": "success"}]}),
    ]

    with patch("asyncio.sleep", return_value=None):
        result = await get_warsaw_api_obj_data_result("attraction")

    assert result == [{"id": "success"}]


@pytest.mark.asyncio
@respx.mock
async def test_error_status_code_500():
    url = "https://api.um.warszawa.pl/api/action/tourism_attraction_get/"
    respx.get(url).mock(return_value=httpx.Response(404))

    with pytest.raises(HTTPException) as excinfo:
        await get_warsaw_api_obj_data_result("attraction")

    assert excinfo.value.status_code == 500
    assert "Warsaw API error: 404" in excinfo.value.detail


@pytest.mark.asyncio
@respx.mock
async def test_error_non_json_response():
    url = "https://api.um.warszawa.pl/api/action/tourism_attraction_get/"
    respx.get(url).mock(return_value=httpx.Response(200, text="Not a JSON"))

    with pytest.raises(HTTPException) as excinfo:
        await get_warsaw_api_obj_data_result("attraction")

    assert "API returned non-JSON" in excinfo.value.detail


@pytest.mark.asyncio
@respx.mock
async def test_error_missing_result_key():
    url = "https://api.um.warszawa.pl/api/action/tourism_attraction_get/"
    respx.get(url).mock(return_value=httpx.Response(200, json={"wrong_key": "data"}))

    with pytest.raises(HTTPException) as excinfo:
        await get_warsaw_api_obj_data_result("attraction")

    assert "API returned unexpected structure" in excinfo.value.detail


@pytest.mark.asyncio
@respx.mock
async def test_error_invalid_result_type():
    url = "https://api.um.warszawa.pl/api/action/tourism_attraction_get/"
    respx.get(url).mock(return_value=httpx.Response(200, json={"result": "Błędny klucz API"}))

    with pytest.raises(HTTPException) as excinfo:
        await get_warsaw_api_obj_data_result("attraction")

    assert "API did not return structured data" in excinfo.value.detail


@pytest.mark.asyncio
@respx.mock
async def test_error_max_retries_exceeded():
    url = "https://api.um.warszawa.pl/api/action/tourism_attraction_get/"
    respx.get(url).side_effect = httpx.TimeoutException("Timeout")

    with patch("asyncio.sleep", return_value=None):
        with pytest.raises(HTTPException) as excinfo:
            await get_warsaw_api_obj_data_result("attraction")

    assert excinfo.value.status_code == 500
    assert "Warsaw API failed after 3 attempts" in excinfo.value.detail


# FETCHING SPECIFIC CITY OBJECT
@pytest.mark.asyncio
async def test_fetch_accommodations_parsing():
    fake_api_result = {
        "featureMemberList": [
            {"geometry": {"coordinates": [{"latitude": "52.2", "longitude": "21.0"}]}}
        ]
    }

    with patch("api.accomodations.get_warsaw_api_obj_data_result") as mock_get:
        mock_get.return_value = fake_api_result

        results = await fetch_accommodations()

        assert len(results) == 2
        assert results[0].latitude == 52.2
        assert results[0].objtype == "hotel"


@pytest.mark.asyncio
async def test_fetch_aeds_parsing():
    fake_data = [{"geometry": {"coordinates": [[21.0, 52.2]]}}]
    with patch("api.aeds.get_warsaw_api_obj_data_result", return_value=fake_data):
        results = await fetch_aeds()
        assert len(results) == 1
        assert results[0].latitude == 52.2
        assert results[0].longitude == 21.0
        assert results[0].objtype == "aeds"


@pytest.mark.asyncio
async def test_fetch_attractions_parsing():
    fake_data = [{"latlng": {"lat": "52.2", "lng": "21.0"}}]
    with patch("api.attractions.get_warsaw_api_obj_data_result", return_value=fake_data):
        results = await fetch_attractions()
        assert results[0].latitude == 52.2
        assert results[0].longitude == 21.0


@pytest.mark.asyncio
async def test_fetch_bike_stations_parsing():
    fake_data = {
        "featureMemberList": [
            {"geometry": {"coordinates": [{"latitude": "52.2", "longitude": "21.0"}]}}
        ]
    }
    with patch("api.bike_stations.get_warsaw_api_obj_data_result", return_value=fake_data):
        results = await fetch_bike_stations()
        assert results[0].objtype == "bike_station"


@pytest.mark.asyncio
async def test_fetch_bike_stations_404():
    with patch("api.bike_stations.get_warsaw_api_obj_data_result", return_value={}):
        with pytest.raises(HTTPException) as exc:
            await fetch_bike_stations()
        assert exc.value.status_code == 404


@pytest.mark.asyncio
async def test_fetch_nature_parsing():
    fake_record = {"records": [{"y_wgs84": "52.2", "x_wgs84": "21.0"}]}

    with patch("api.nature.get_warsaw_api_obj_data_result", return_value=fake_record):
        results = await fetch_nature()
        assert len(results) == 3
        assert results[0].latitude == 52.2

        types = [r.objtype for r in results]
        assert "tree" in types
        assert "bush" in types
        assert "forest" in types


@pytest.mark.asyncio
async def test_fetch_pharmacies_parsing():
    fake_data = {
        "featureMemberList": [
            {"geometry": {"coordinates": [{"latitude": "52.25", "longitude": "21.05"}]}}
        ]
    }
    with patch("api.pharmacies.get_warsaw_api_obj_data_result", return_value=fake_data):
        results = await fetch_pharmacies()
        assert results[0].objtype == "pharmacy"
        assert results[0].latitude == 52.25


@pytest.mark.asyncio
async def test_fetch_police_stations_parsing():
    fake_data = {
        "featureMemberList": [
            {"geometry": {"coordinates": [{"latitude": "52.21", "longitude": "21.01"}]}}
        ]
    }
    with patch("api.police_stations.get_warsaw_api_obj_data_result", return_value=fake_data):
        results = await fetch_police_stations()
        assert results[0].objtype == "police_station"
        assert results[0].longitude == 21.01


@pytest.mark.asyncio
async def test_fetch_stops_parsing():
    fake_data = [
        {
            "values": [
                {"key": "szer_geo", "value": "52.23"},
                {"key": "dlug_geo", "value": "21.01"},
                {"key": "nazwa_zespolu", "value": "Centrum"},
            ]
        }
    ]
    with patch("api.stops.get_warsaw_api_obj_data_result", return_value=fake_data):
        results = await fetch_stops()
        assert len(results) == 1
        assert results[0].latitude == 52.23
        assert results[0].longitude == 21.01
        assert results[0].objtype == "stop"


@pytest.mark.asyncio
async def test_fetch_theatres_parsing():
    fake_data = {"featureMemberCoordinates": [{"latitude": "52.24", "longitude": "21.02"}]}
    with patch("api.theatres.get_warsaw_api_obj_data_result", return_value=fake_data):
        results = await fetch_theatres()
        assert len(results) == 1
        assert results[0].objtype == "theatre"
        assert results[0].latitude == 52.24


@pytest.mark.asyncio
async def test_fetch_theatres_404():
    with patch("api.theatres.get_warsaw_api_obj_data_result", return_value={}):
        with pytest.raises(HTTPException) as exc:
            await fetch_theatres()
        assert exc.value.status_code == 404
