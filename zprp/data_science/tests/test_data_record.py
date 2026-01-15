from unittest.mock import patch, Mock
from data_record import DataRecord


@patch("httpx.get")
def test_get_features(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = [
        {"objtype": "stop", "count": 3},
        {"objtype": "pharmacy", "count": 1},
    ]
    mock_get.return_value = mock_response

    record = DataRecord(lat=52.1, lon=21.0, radius=300)
    features = record.features

    assert features["lat"] == 52.1
    assert features["lon"] == 21.0
    assert features["stop"] == 3
    assert features["pharmacy"] == 1
    assert features["tree"] == 0
