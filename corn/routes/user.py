from fastapi import APIRouter, Depends, HTTPException

from corn.dao.user import UserDAO
from corn.exc.dao import AlreadyExistsException
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
    raise HTTPException(status_code=418, detail="Route not implemented yet.")
