from typing import Optional

import jwt
from fastapi import HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from corn.config import jwt_settings


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):  # type: ignore
        credentials: Optional[HTTPAuthorizationCredentials] = await super(
            JWTBearer, self
        ).__call__(request)
        if credentials is not None:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403, detail="Invalid authentication scheme."
                )
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(
                    status_code=403, detail="Invalid token or expired token."
                )
            return credentials.credentials
        else:
            raise HTTPException(
                status_code=403, detail="Invalid authorization code."
            )

    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False

        try:
            payload = jwt.decode(
                jwtoken,
                jwt_settings.secret,
                algorithms=[jwt_settings.algorithm]
            )
        except Exception:
            payload = None
        if payload:
            isTokenValid = True
        return isTokenValid
