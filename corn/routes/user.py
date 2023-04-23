from fastapi import APIRouter, Depends, HTTPException

from corn.dao.user import UserDAO
from corn.exc.dao import AlreadyExistsException
from corn.exc.http.auth import (IncorrectPasswordException,
                                UserDoesNotExistException)
from corn.models.pydantic.user import (UserLoginPayload, UserLoginResult,
                                       UserRegistrationPayload,
                                       UserRegistrationResult)

router = APIRouter()


@router.post("/new", response_model=UserRegistrationResult)
def signup(
        payload: UserRegistrationPayload,
        user_dao: UserDAO = Depends(UserDAO)
) -> UserRegistrationResult:
    try:
        new_user = user_dao.create_user(payload)

        return UserRegistrationResult(**new_user.__dict__)
    except AlreadyExistsException:
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
        raise UserDoesNotExistException()

    if not possible_user.check_password(payload.password):
        raise IncorrectPasswordException()

    raise HTTPException(status_code=418, detail="Not implemented yet")
