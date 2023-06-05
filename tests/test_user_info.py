import json
from datetime import datetime, timedelta, timezone
from http import HTTPStatus

import jwt
from httpx import Response
from starlette.testclient import TestClient

from corn.config import jwt_settings
from corn.models.factories.user_factory import UserRegistrationPayloadFactory
from corn.models.pydantic.user import UserLoginPayload, UserToken


def test_user_info_successful(tc: TestClient):
    # GIVEN

    new_user_payload = UserRegistrationPayloadFactory()
    tc.post("/user/new", content=json.dumps(new_user_payload.__dict__))

    login_payload = UserLoginPayload(
        username_or_email=new_user_payload.username,
        password=new_user_payload.password
    ).__dict__

    login_result: Response = tc.post(
        "/user/login",
        content=json.dumps(login_payload)
    )

    assert login_result.status_code == HTTPStatus.OK
    assert login_result.json()["token"] is not None

    token = login_result.json()["token"]
    user_info_result = tc.get("/user/me", headers={
        'Authorization': f'Bearer {token}'
    })

    assert user_info_result.status_code == HTTPStatus.OK


def test_user_info_bad_token(tc: TestClient):
    # GIVEN

    new_user_payload = UserRegistrationPayloadFactory()
    tc.post("/user/new", content=json.dumps(new_user_payload.__dict__))

    login_payload = UserLoginPayload(
        username_or_email=new_user_payload.username,
        password=new_user_payload.password
    ).__dict__

    login_result: Response = tc.post(
        "/user/login",
        content=json.dumps(login_payload)
    )

    assert login_result.status_code == HTTPStatus.OK
    assert login_result.json()["token"] is not None

    token = login_result.json()["token"]

    user_info_result = tc.get("/user/me", headers={
        'Authorization': f'BADBEARER {token}'
    })

    assert user_info_result.status_code == HTTPStatus.FORBIDDEN
    assert user_info_result.json(
    )['detail'] == "Invalid authentication credentials"


def test_user_info_expired_token(tc: TestClient):
    # GIVEN

    new_user_payload = UserRegistrationPayloadFactory()
    tc.post("/user/new", content=json.dumps(new_user_payload.__dict__))

    login_payload = UserLoginPayload(
        username_or_email=new_user_payload.username,
        password=new_user_payload.password
    ).__dict__

    login_result: Response = tc.post(
        "/user/login",
        content=json.dumps(login_payload)
    )

    assert login_result.status_code == HTTPStatus.OK
    assert login_result.json()["token"] is not None

    token = login_result.json()["token"]
    decoded_token = UserToken.from_jwt(token)
    decoded_token.exp = datetime.now(timezone.utc) - timedelta(minutes=5)
    token = jwt.encode(decoded_token.__dict__, jwt_settings.secret)

    user_info_result = tc.get("/user/me", headers={
        'Authorization': f'Bearer {token}'
    })

    assert user_info_result.status_code == HTTPStatus.FORBIDDEN
    assert user_info_result.json(
    )['detail'] == "Invalid or expired token"
