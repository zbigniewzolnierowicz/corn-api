import jwt
from fastapi import APIRouter, Depends, HTTPException, Request

from corn.config import jwt_settings
from corn.dao.user import UserDAO
from corn.exc.dao import AlreadyExistsError
from corn.exc.http.auth import IncorrectPasswordError, UserDoesNotExistError
from corn.models.pydantic.user import (
    UserLoginPayload,
    UserLoginResult,
    UserRegistrationPayload,
    UserRegistrationResult,
    UserToken,
)
from corn.utils.auth import JWTBearer

router = APIRouter()


@router.post("/new", response_model=UserRegistrationResult)
def signup(
        payload: UserRegistrationPayload,
        user_dao: UserDAO = Depends(UserDAO)
) -> UserRegistrationResult:
    try:
        new_user = user_dao.create_user(payload)

        return UserRegistrationResult(**new_user.__dict__)
    except AlreadyExistsError:
        raise HTTPException(status_code=409, detail="User already exists.")


@router.post("/login", response_model=UserLoginResult)
def login(
        payload: UserLoginPayload,
        user_dao: UserDAO = Depends(UserDAO)
) -> UserLoginResult:
    possible_user = user_dao.get_user_by_username_or_email(
        payload.username_or_email
    )

    if possible_user is None:
        raise UserDoesNotExistError()

    if not possible_user.check_password(payload.password):
        raise IncorrectPasswordError()

    message = UserToken(
        iss="http://localhost",
        sub=possible_user.id,
    )

    token = jwt.encode(message.__dict__, jwt_settings.secret)

    return UserLoginResult(
        token=token
    )


@router.get("/me")
async def user_info(
        request: Request,
        user_dao: UserDAO = Depends(UserDAO),
        jwt: str = Depends(JWTBearer())
) -> UserToken:
    token = UserToken.from_jwt(jwt)
    return token
