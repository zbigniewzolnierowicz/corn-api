from typing import Annotated

from fastapi import APIRouter, Depends

from corn.dao.user import UserDAO
from corn.models.pydantic.user import (UserRegistrationPayload,
                                       UserRegistrationResult)

router = APIRouter()


@router.post("/new", response_model=UserRegistrationResult)
def signup(
        payload: UserRegistrationPayload,
) -> UserRegistrationResult:
    return UserRegistrationResult(**payload.dict())
