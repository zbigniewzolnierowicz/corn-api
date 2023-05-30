from datetime import datetime, timedelta, timezone

import jwt
from pydantic import BaseModel

from corn.config import jwt_settings
from corn.exc.token import BadJWTException


class UserSchema(BaseModel):
    id: str
    username: str
    password_hash: str
    email: str


class UserRegistrationPayload(BaseModel):
    username: str
    password: str
    email: str


class UserRegistrationResult(BaseModel):
    id: str
    username: str
    email: str


class UserUpdatePayload(BaseModel):
    username: str


class UserLoginPayload(BaseModel):
    username_or_email: str
    password: str


class UserLoginResult(BaseModel):
    token: str


class UserToken(BaseModel):
    iss: str
    sub: str
    iat: datetime = datetime.now(timezone.utc)

    @property
    def exp(self) -> datetime:
        return (self.iat + timedelta(seconds=jwt_settings.expiration))

    @classmethod
    def from_jwt(cls, token: str) -> "UserToken":
        try:
            parsed_jwt = jwt.decode(
                token,
                jwt_settings.secret,
                algorithms=[jwt_settings.algorithm]
            )
        except Exception:
            raise BadJWTException()

        if parsed_jwt is None:
            raise BadJWTException()

        return cls(**parsed_jwt)
