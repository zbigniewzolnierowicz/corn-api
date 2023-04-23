from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, as_declarative, sessionmaker

from corn.config import pg_settings

engine = create_engine(str(pg_settings.database_url()))


def session_factory() -> Session:
    session = sessionmaker(
        engine,
        expire_on_commit=False,
    )

    return session()


def get_session() -> Generator[Session, None, None]:
    session = session_factory()
    try:
        yield session
    finally:
        session.close()


@as_declarative()
class Base(object):
    pass
