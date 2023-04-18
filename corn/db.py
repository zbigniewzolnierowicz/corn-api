from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import (DeclarativeBase, Session, declarative_base,
                            sessionmaker)

from corn.config import settings

engine = create_engine(str(settings.database_url))


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


Base: DeclarativeBase = declarative_base()
