import uuid
from unittest.mock import MagicMock

from pytest import MonkeyPatch
from sqlalchemy.orm import Session

from corn.dao.user import UserDAO
from corn.models.factories.user_factory import UserSchemaFactory
from corn.models.pydantic.user import UserSchema


def test_does_user_exist(monkeypatch: MonkeyPatch) -> None:
    class MockedScalars():
        @staticmethod
        def first() -> None:
            return None

    session = Session()
    session.scalars = MagicMock(return_value=MockedScalars())  # type: ignore

    dao = UserDAO(session)

    assert not dao.does_user_exist(str(uuid.UUID(int=0)))


def test_does_user_exist_user_already_exists() -> None:
    class MockedScalars():
        @staticmethod
        def first() -> UserSchema:
            user: UserSchema = UserSchemaFactory()  # type: ignore
            return user

    session = Session()
    session.scalars = MagicMock(return_value=MockedScalars())  # type: ignore

    dao = UserDAO(session)

    assert dao.does_user_exist(str(uuid.UUID(int=1)))
