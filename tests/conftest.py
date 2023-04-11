from typing import Generator

import pytest
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import Session, sessionmaker
from starlette.testclient import TestClient

from corn.db import Base, get_session
from corn.main import create_app


def session_override() -> Generator[Session, None, None]:
    engine = create_engine(url="sqlite://")
    Base.metadata.create_all(bind=engine)

    with engine.begin() as conn:
        MetaData().create_all(bind=conn)

    session: sessionmaker[Session] = sessionmaker(bind=engine)

    with session() as s:
        try:
            yield s
        finally:
            s.commit()
            s.close()


@pytest.fixture(scope="module")
def tc() -> Generator[TestClient, None, None]:
    app = create_app()

    app.dependency_overrides[get_session] = session_override

    with TestClient(app) as tc:
        yield tc
