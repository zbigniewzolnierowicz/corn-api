import json
from http import HTTPStatus

from pytest import MonkeyPatch
from starlette.testclient import TestClient

from corn.dao.user import UserDAO
from corn.exc.dao import AlreadyExistsError
from corn.models.factories.user_factory import UserRegistrationPayloadFactory


def test_signup_valid(tc: TestClient) -> None:
    # GIVEN

    user_payload = UserRegistrationPayloadFactory()

    # WHEN

    response = tc.post("/user/new", content=json.dumps(user_payload.__dict__))
    result_json = response.json()

    # THEN

    assert response.status_code == HTTPStatus.OK
    assert result_json["id"] is not None
    assert result_json["username"] == user_payload.username
    assert result_json["email"] == user_payload.email


def create_user_mock(_self: None, _payload: None) -> None:
    raise AlreadyExistsError()


def test_signup_already_exists(
        monkeypatch: MonkeyPatch,
        tc: TestClient
) -> None:
    monkeypatch.setattr(
        UserDAO,
        "create_user",
        create_user_mock
    )

    # GIVEN

    user_payload = UserRegistrationPayloadFactory()

    # WHEN

    response = tc.post("/user/new", content=json.dumps(user_payload.__dict__))

    # THEN

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json()["detail"] == "User already exists."
