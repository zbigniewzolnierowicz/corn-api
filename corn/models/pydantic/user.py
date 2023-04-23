from pydantic import BaseModel


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
