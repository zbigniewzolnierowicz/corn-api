import uuid
from copy import deepcopy
from unittest.mock import MagicMock

import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from corn.dao.user import UserDAO
from corn.exc.dao import AlreadyExistsException, EntityNotFoundException
from corn.models.factories.user_factory import UserSchemaFactory
from corn.models.pydantic.user import (
    UserRegistrationPayload,
    UserSchema,
    UserUpdatePayload,
)
from corn.models.sqlalchemy.user import User


def test_does_user_exist(monkeypatch: pytest.MonkeyPatch) -> None:
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


def test_get_user(monkeypatch: pytest.MonkeyPatch) -> None:
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


def test_get_user_no_user(monkeypatch: pytest.MonkeyPatch) -> None:
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


def test_create_user(monkeypatch: pytest.MonkeyPatch) -> None:
    class MockedSession:
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
    assert user_payload.password not in new_user.password_hash
    assert new_user.check_password(user_payload.password)


def test_create_user_existing_user(monkeypatch: pytest.MonkeyPatch) -> None:
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

    with pytest.raises(AlreadyExistsException):
        dao.create_user(user_payload)

    assert session.rollback.called


def test_update_user(monkeypatch: pytest.MonkeyPatch) -> None:
    session = MagicMock()
    user_id = str(uuid.UUID(int=0))
    initial_user = UserSchemaFactory(id=user_id)

    dao = UserDAO(session)
    dao._get_user = MagicMock(  # type: ignore
        return_value=deepcopy(initial_user)
    )

    user_payload = UserUpdatePayload(
        username="boofar"
    )

    updated_user = dao.update_user(user_id, user_payload)

    assert updated_user.username == user_payload.username
    assert updated_user.username != initial_user.__dict__["username"]


def test_update_user_missing_target_user(
        monkeypatch: pytest.MonkeyPatch
) -> None:
    session = MagicMock()
    session.rollback = MagicMock()
    user_id = str(uuid.UUID(int=0))

    dao = UserDAO(session)
    dao._get_user = MagicMock(return_value=None)  # type: ignore

    user_payload = UserUpdatePayload(
        username="boofar"
    )

    with pytest.raises(EntityNotFoundException):
        dao.update_user(user_id, user_payload)
