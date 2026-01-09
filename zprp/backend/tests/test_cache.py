import sys
from unittest.mock import MagicMock, mock_open, patch

from pydantic import BaseModel
import pytest

# Mock logger module
sys.modules["logger"] = MagicMock()
sys.modules["logger.logging_config"] = MagicMock()

from cache.json_cache import load_api_cache_json, save_api_cache_json  # noqa: E402
from cache.save_cache import fetch_api_data, serialize  # noqa: E402


# Serialization
class MockModel(BaseModel):
    id: int
    name: str


def test_serialize_pydantic():
    obj = MockModel(id=1, name="Test")
    result = serialize(obj)
    assert result == {"id": 1, "name": "Test"}


def test_serialize_list():
    lst = [MockModel(id=1, name="A"), MockModel(id=2, name="B")]
    result = serialize(lst)
    assert len(result) == 2
    assert result[0]["id"] == 1


# Open/save .json
@patch("cache.json_cache.API_CACHE_JSON_PATH", "fake_path.json")
def test_save_api_cache_json():
    m = mock_open()
    data = {"key": "value"}
    with patch("builtins.open", m):
        save_api_cache_json(data)

    m.assert_called_once_with("fake_path.json", "w", encoding="utf-8")
    handle = m()
    written_data = "".join(call.args[0] for call in handle.write.call_args_list)
    assert '"key": "value"' in written_data


@patch("cache.json_cache.os.path.exists")
@patch("cache.json_cache.API_CACHE_JSON_PATH", "fake_path.json")
def test_load_api_cache_json_not_found(mock_exists):
    mock_exists.return_value = False
    with pytest.raises(FileNotFoundError):
        load_api_cache_json()


# Mock all fetch API functions
@pytest.mark.asyncio
@patch("cache.save_cache.fetch_accommodations")
@patch("cache.save_cache.fetch_theatres")
@patch("cache.save_cache.fetch_bike_stations")
@patch("cache.save_cache.fetch_aeds")
@patch("cache.save_cache.fetch_attractions")
@patch("cache.save_cache.fetch_nature")
@patch("cache.save_cache.fetch_police_stations")
@patch("cache.save_cache.fetch_pharmacies")
@patch("cache.save_cache.fetch_stops")
async def test_fetch_api_data(
    m_stops, m_pharm, m_police, m_nature, m_attr, m_aeds, m_bike, m_theatre, m_accom
):
    m_accom.return_value = [MockModel(id=1, name="Hotel")]
    for m in [m_stops, m_pharm, m_police, m_nature, m_attr, m_aeds, m_bike, m_theatre]:
        m.return_value = []

    result = await fetch_api_data()

    assert "accommodation" in result
    assert result["accommodation"][0]["name"] == "Hotel"
    assert m_accom.called
    assert m_stops.called
