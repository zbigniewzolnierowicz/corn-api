from typing import Generator

import pytest
from sqlalchemy import MetaData, create_engine
from starlette.testclient import TestClient

from corn.db import Base
from corn.main import create_app


@pytest.fixture
def tc() -> Generator[TestClient, None, None]:
    engine = create_engine(url="sqlite://")
    Base.metadata.create_all(bind=engine)

    with engine.begin() as conn:
        MetaData().create_all(bind=conn)

    app = create_app()

    with TestClient(app) as tc:
        yield tc
