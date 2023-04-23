from fastapi import HTTPException


class IncorrectPasswordException(HTTPException):
    def __init__(self) -> None:
        self.status_code = 403
        self.detail = "Incorrect password"


class UserDoesNotExistException(HTTPException):
    def __init__(self) -> None:
        self.status_code = 404
        self.detail = "User does not exist"