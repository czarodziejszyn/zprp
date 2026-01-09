import os
import pytest


@pytest.fixture(scope="session")
def base_url() -> str:
    return os.getenv("FRONTEND_BASE_URL", "http://127.0.0.1:8050")


