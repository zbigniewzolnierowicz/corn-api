import json

from pytest import MonkeyPatch
from starlette.testclient import TestClient

from corn.dao.user import UserDAO
from corn.exc.dao import AlreadyExistsException


def test_signup_valid(tc: TestClient) -> None:
    # GIVEN

    user_payload = {
        "username": "foo",
        "password": "bar",
        "email": "foobar@example.com"
    }

    # WHEN

    response = tc.post("/user/new", content=json.dumps(user_payload))

    # THEN

    assert response.status_code == 200
    assert response.json()["username"] == user_payload["username"]
    assert response.json()["email"] == user_payload["email"]


def create_user_mock(_self, _payload) -> None:
    raise AlreadyExistsException()
    return


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

    user_payload = {
        "username": "foo",
        "password": "bar",
        "email": "foobar@example.com"
    }

    # WHEN

    response = tc.post("/user/new", content=json.dumps(user_payload))

    # THEN

    assert response.status_code == 409
    assert response.json()["detail"] == "User already exists."
