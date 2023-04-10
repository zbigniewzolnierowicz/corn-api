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
    username: str
    email: str
