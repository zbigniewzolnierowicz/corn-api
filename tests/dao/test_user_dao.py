import uuid
from unittest.mock import MagicMock

from pytest import MonkeyPatch, raises
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from corn.dao.user import UserDAO
from corn.exc.dao import AlreadyExistsException
from corn.models.factories.user_factory import UserSchemaFactory
from corn.models.pydantic.user import UserRegistrationPayload, UserSchema
from corn.models.sqlalchemy.user import User


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

    assert dao.does_user_exist(str(uuid.UUID(int=0)))


def test_get_user(monkeypatch: MonkeyPatch) -> None:
    user_id = str(uuid.UUID(int=0))

    class MockedScalars():
        @staticmethod
        def first() -> UserSchema:
            user: UserSchema = UserSchemaFactory(id=user_id)  # type: ignore
            return user

    session = Session()
    session.scalars = MagicMock(return_value=MockedScalars())  # type: ignore

    dao = UserDAO(session)

    user = dao.get_user(user_id)
    assert user is not None
    assert user.id == user_id


def test_get_user_no_user(monkeypatch: MonkeyPatch) -> None:
    user_id = str(uuid.UUID(int=0))

    class MockedScalars():
        @staticmethod
        def first() -> None:
            return None

    session = Session()
    session.scalars = MagicMock(return_value=MockedScalars())  # type: ignore

    dao = UserDAO(session)

    user = dao.get_user(user_id)

    assert user is None


def test_create_user(monkeypatch: MonkeyPatch) -> None:
    class MockedSession():
        def commit(self, payload: User) -> None:
            payload.id = str(uuid.UUID(int=0))

    session = MagicMock(return_value=MockedSession())

    dao = UserDAO(session)

    user_payload = UserRegistrationPayload(
        password="foobar",
        **UserSchemaFactory().__dict__
    )

    new_user = dao.create_user(user_payload)

    assert new_user.username == user_payload.username
    assert new_user.email == user_payload.email


def test_create_user_existing_user(monkeypatch: MonkeyPatch) -> None:
    session = MagicMock()
    session.rollback = MagicMock()
    session.commit = MagicMock(
        side_effect=IntegrityError(statement="", params={}, orig=Exception())
    )

    dao = UserDAO(session)

    user_payload = UserRegistrationPayload(
        password="foobar",
        **UserSchemaFactory().__dict__
    )

    with raises(AlreadyExistsException):
        dao.create_user(user_payload)

    assert session.rollback.called
