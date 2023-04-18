import json

from starlette.testclient import TestClient

from corn.models.factories.user_factory import UserRegistrationPayloadFactory
from corn.models.pydantic.user import UserLoginPayload


def test_login_successful(tc: TestClient) -> None:
    # GIVEN

    new_user_payload = UserRegistrationPayloadFactory().__dict__
    tc.post("/user/new", content=json.dumps(new_user_payload))

    login_payload = UserLoginPayload(**new_user_payload).__dict__

    # WHEN

    login_result = tc.post("/user/login", content=json.dumps(login_payload))

    assert login_result.status_code == 200

    # TODO: add checking for a JWT cookie


def test_login_incorrect_password(tc: TestClient) -> None:
    # GIVEN

    new_user_payload = UserRegistrationPayloadFactory().__dict__
    tc.post("/user/new", content=json.dumps(new_user_payload))

    login_payload = UserLoginPayload(**new_user_payload).__dict__
    login_payload.update(password="BADPASSWORD")

    # WHEN

    login_result = tc.post("/user/login", content=json.dumps(login_payload))

    assert login_result.status_code == 403


def test_login_missing_password(tc: TestClient) -> None:
    # GIVEN

    new_user_payload = UserRegistrationPayloadFactory().__dict__
    tc.post("/user/new", content=json.dumps(new_user_payload))

    login_payload = UserLoginPayload(**new_user_payload).__dict__
    login_payload.update(password=None)

    # WHEN

    login_result = tc.post("/user/login", content=json.dumps(login_payload))

    assert login_result.status_code == 400
