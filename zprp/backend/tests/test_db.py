import sys
from unittest.mock import MagicMock, mock_open, patch

import psycopg
import pytest

# Mock logger module
sys.modules["logger"] = MagicMock()
sys.modules["logger.logging_config"] = MagicMock()


from db.db import get_conn, init_db  # noqa: E402
from db.import_data import import_with_cache, normalize  # noqa: E402


def test_get_conn_retry_logic():
    with patch("psycopg.connect") as mock_connect:
        mock_connect.side_effect = [
            psycopg.OperationalError,
            psycopg.OperationalError,
            MagicMock(),
        ]

        with patch("time.sleep", return_value=None):
            conn = get_conn(max_retries=3)

        assert mock_connect.call_count == 3
        assert conn is not None


def test_get_conn_fail_after_max_retries():
    with patch("psycopg.connect", side_effect=psycopg.OperationalError):
        with patch("time.sleep", return_value=None):
            with pytest.raises(Exception) as exc:
                get_conn(max_retries=5)
            assert "after 5 attempts" in str(exc.value)


def test_init_db_executes_sql():
    with patch("db.db.get_conn") as mock_get_conn:
        mock_conn = MagicMock()
        mock_get_conn.return_value.__enter__.return_value = mock_conn

        init_db()

        mock_conn.execute.assert_called_once()
        args = mock_conn.execute.call_args[0][0]
        assert "CREATE TABLE city_obj" in args
        assert "CREATE TABLE IF NOT EXISTS offers" in args


def test_normalize_dict_and_obj():
    cache_data = {"objtype": "tree", "latitude": 52.2, "longitude": 21.0}
    assert normalize(cache_data) == ("tree", 52.2, 21.0)

    mock_obj = MagicMock()
    mock_obj.objtype = "aed"
    mock_obj.latitude = 52.3
    mock_obj.longitude = 21.1
    assert normalize(mock_obj) == ("aed", 52.3, 21.1)


@pytest.mark.asyncio
@patch("db.import_data.load_api_cache_json")
@patch("db.import_data.import_obj_list")
async def test_import_with_cache_fallback(mock_import_list, mock_load_cache):
    async def mock_fetch_fail():
        raise Exception("API Down")

    mock_load_cache.return_value = {"aed": [{"objtype": "aed", "lat": 1, "lon": 2}]}
    mock_import_list.return_value = 1

    count = await import_with_cache(mock_fetch_fail, "aed", "AEDs")

    assert count == 1
    mock_load_cache.assert_called_once()
    mock_import_list.assert_called_once()


@patch("db.import_data.get_conn")
def test_import_offers(mock_get_conn):
    fake_json = '[{"title": "Mieszkanie", "url": "http", "price": 100, "area_m2": 50, "price_per_m2": 2, "address": "X", "latitude": 50, "longitude": 20}]'

    mock_conn = MagicMock()
    mock_get_conn.return_value.__enter__.return_value = mock_conn

    with patch("builtins.open", mock_open(read_data=fake_json)):
        from db.import_data import import_offers

        with patch.dict("os.environ", {"GEOCODED_OFFERS_JSON_PATH": "fake.json"}):
            count = import_offers()

    assert count == 1
    assert mock_conn.execute.called

    sql_query = mock_conn.execute.call_args[0][0]
    assert "ST_MakePoint" in sql_query
