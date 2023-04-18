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
