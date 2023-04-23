import logging
import pathlib
from typing import Any, Generator

import alembic
import alembic.config
import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker
from starlette.testclient import TestClient

from corn.config import pg_settings
from corn.db import engine, get_session
from corn.main import create_app


@pytest.fixture(scope="module", autouse=True)
def session_generator(
        request: pytest.FixtureRequest,
        worker_id: str
) -> Generator[Session, None, None]:
    unique_id: str = request.module.__name__.replace(
            "*", "_"
        ).replace(
            ".", "_"
        )
    test_db_name = f"{engine.url.database}_tests_{worker_id}_{unique_id}"
    db_url = pg_settings.database_url(test_db_name)

    with engine.connect().execution_options(
            isolation_level="AUTOCOMMIT"
    ) as connection:
        connection.execute(text(f"DROP DATABASE IF EXISTS {test_db_name}"))
        connection.execute(text(f"CREATE DATABASE {test_db_name}"))

    testing_db_url = engine.url.set(database=test_db_name)
    test_db_engine = create_engine(testing_db_url)
    session: sessionmaker[Session] = sessionmaker(bind=test_db_engine)

    script_location = (
        pathlib.Path(__file__).parent.parent / "corn/alembic"
    )
    config = alembic.config.Config()
    config.set_main_option("script_location", str(script_location))
    config.set_main_option(
        "sqlalchemy.url",
        db_url
    )
    alembic.command.upgrade(config=config, revision="head")

    with session() as s:
        try:
            yield s
        finally:
            s.commit()
            s.close()

    test_db_engine.dispose()


@pytest.fixture(scope="module", autouse=True)
def tc(
        session_generator: Generator[Session, None, None]
) -> Generator[TestClient, None, None]:
    app = create_app()

    app.dependency_overrides[get_session] = lambda: session_generator

    with TestClient(app) as tc:
        yield tc
