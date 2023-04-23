import json

from httpx import Response
from starlette.testclient import TestClient

from corn.models.factories.user_factory import UserRegistrationPayloadFactory
from corn.models.pydantic.user import UserLoginPayload


def test_login_successful(tc: TestClient) -> None:
    # GIVEN

    new_user_payload = UserRegistrationPayloadFactory()
    tc.post("/user/new", content=json.dumps(new_user_payload.__dict__))

    login_payload = UserLoginPayload(
        username_or_email=new_user_payload.username,
        password=new_user_payload.password
    ).__dict__

    # WHEN

    login_result: Response = tc.post(
        "/user/login",
        content=json.dumps(login_payload)
    )

    assert login_result.status_code == 200
    assert login_result.json()["token"] is not None


def test_login_incorrect_password(tc: TestClient) -> None:
    # GIVEN

    new_user_payload = UserRegistrationPayloadFactory()
    tc.post("/user/new", content=json.dumps(new_user_payload.__dict__))

    login_payload = UserLoginPayload(
        username_or_email=new_user_payload.username,
        password="!!!BADPASSWORD!!!"
    ).__dict__

    # WHEN

    login_result = tc.post("/user/login", content=json.dumps(login_payload))

    assert login_result.status_code == 403
    assert login_result.json()["detail"] == "Incorrect password"


def test_login_missing_password(tc: TestClient) -> None:
    # GIVEN

    new_user_payload = UserRegistrationPayloadFactory().__dict__
    tc.post("/user/new", content=json.dumps(new_user_payload))

    login_payload = {
        "username_or_email": new_user_payload["username"]
    }

    # WHEN

    login_result = tc.post("/user/login", content=json.dumps(login_payload))

    assert login_result.status_code == 422


def test_login_missing_email(tc: TestClient) -> None:
    # GIVEN

    new_user_payload = UserRegistrationPayloadFactory().__dict__
    tc.post("/user/new", content=json.dumps(new_user_payload))

    login_payload = {
        "password": new_user_payload["password"]
    }

    # WHEN

    login_result = tc.post("/user/login", content=json.dumps(login_payload))

    assert login_result.status_code == 422
