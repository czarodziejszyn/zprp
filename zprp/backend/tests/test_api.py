import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from unittest.mock import MagicMock

from api.main import app

client = TestClient(app)

@patch("api.main.count_objects_nearby")
def test_nearby_endpoint(mock_db_call):
    lat, lon = 52.2, 21.0
    rad = 100
    expected_data = [{"type": "tree", "count": 2}]
    
    mock_db_call.return_value = expected_data

    url = f"/nearby?lat={lat}&lon={lon}&radius={rad}"
    response = client.get(url)
    
    assert response.status_code == 200
    assert response.json() == expected_data
    
    mock_db_call.assert_called_once_with(lat, lon, rad)


@patch("api.main.calculate_prices")
def test_prices(mock_model):
    lat, lon = 52.2, 21.0
    expected_predicted = 10000.0
    expected_real = 9500.0
    
    mock_model.return_value = (expected_predicted, expected_real)
    
    url = f"/prices?lat={lat}&lon={lon}"
    response = client.get(url)
    
    assert response.status_code == 200
    data = response.json()
    assert data["predicted_price"] == expected_predicted
    assert data["real_price"] == expected_real
    mock_model.assert_called_once_with(lat, lon)


@patch("api.main.FileResponse")
@patch("api.main.Path")
@patch("api.main.create_chart")
def test_chart(mock_create, mock_path_class, mock_file_response_class):
    fake_file_name = "generated_chart.png"
    mock_create.return_value = fake_file_name
    
    mock_path_instance = MagicMock()
    mock_path_instance.exists.return_value = True

    mock_path_class.return_value = mock_path_instance
    
    mock_response_instance = MagicMock()
    mock_response_instance.status_code = 200
    mock_file_response_class.return_value = mock_response_instance

    response = client.get("/chart")

    assert response.status_code == 200
    
    mock_path_class.assert_called_once_with(fake_file_name)
    
    mock_file_response_class.assert_called_once()
    args, kwargs = mock_file_response_class.call_args
    
    assert args[0] == mock_path_instance 
    assert kwargs["media_type"] == "image/png"
    assert kwargs["filename"] == "chart.png"