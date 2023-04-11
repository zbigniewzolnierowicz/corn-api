from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from corn.config import settings

Base = declarative_base()


def session_factory() -> Session:
    engine = create_engine(str(settings.database_url))
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
