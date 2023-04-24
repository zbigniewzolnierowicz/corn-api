from fastapi import HTTPException


class BadJWTException(HTTPException):
    def __init__(self) -> None:
        self.status_code = 403
        self.detail = "The JWT the user provided is malformed."
