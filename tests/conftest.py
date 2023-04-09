from starlette.testclient import TestClient
import pytest
from corn.main import create_app
from corn.config import get_settings
from corn.config import Settings


def get_settings_override():
    return Settings(database_url="sqlite:///./")


@pytest.fixture(scope="module")
def tc():
    app = create_app()
    app.dependency_overrides[get_settings] = get_settings_override

    with TestClient(app) as tc:
        yield tc
