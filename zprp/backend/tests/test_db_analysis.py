from unittest.mock import MagicMock, patch

from db.count_objects_nearby import count_objects_nearby
from db.get_avg_real_price import get_avg_real_price


def test_get_avg_real_price_success():
    lat, lon = 52.2, 21.0
    rad = 500
    price = 12500.56
    with patch("db.get_avg_real_price.get_conn") as mock_get_conn:
        mock_conn = MagicMock()
        mock_conn.execute.return_value.fetchone.return_value = {"avg_price": price}
        mock_get_conn.return_value.__enter__.return_value = mock_conn

        result = get_avg_real_price(lat, lon, rad)

        assert result == price
        args = mock_conn.execute.call_args[0][1]
        assert args == (lon, lat, rad)


def test_get_avg_real_price_no_data():
    with patch("db.get_avg_real_price.get_conn") as mock_get_conn:
        mock_conn = MagicMock()
        mock_conn.execute.return_value.fetchone.return_value = {"avg_price": None}
        mock_get_conn.return_value.__enter__.return_value = mock_conn

        result = get_avg_real_price(52.2, 21.0, 100)

        assert result == 0


def test_count_objects_nearby_success():
    fake_rows = [{"objtype": "stop", "count": 10}, {"objtype": "pharmacy", "count": 2}]
    with patch("db.count_objects_nearby.get_conn") as mock_get_conn:
        mock_conn = MagicMock()
        mock_conn.execute.return_value.fetchall.return_value = fake_rows
        mock_get_conn.return_value.__enter__.return_value = mock_conn

        results = count_objects_nearby(52.2, 21.0, 1000)

        assert len(results) == 2
        assert results[0]["objtype"] == "stop"
        assert results[1]["count"] == 2

        sql_query = mock_conn.execute.call_args[0][0]
        assert "ST_DWithin" in sql_query
        assert "GROUP BY objtype" in sql_query


def test_count_objects_nearby_empty():
    with patch("db.count_objects_nearby.get_conn") as mock_get_conn:
        mock_conn = MagicMock()
        mock_conn.execute.return_value.fetchall.return_value = []
        mock_get_conn.return_value.__enter__.return_value = mock_conn

        results = count_objects_nearby(52.2, 21.0, 100)

        assert results == []
