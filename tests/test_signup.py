import json
from starlette.testclient import TestClient
from pytest import MonkeyPatch


def test_signup_valid(tc: TestClient):
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


def test_signup_already_exists(monkeypatch: MonkeyPatch(), tc: TestClient):
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
