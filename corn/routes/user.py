from fastapi import APIRouter, Depends
from corn.models.pydantic.user import (
    UserRegistrationResult,
    UserRegistrationPayload
)
from corn.dao.user import UserDAO
from typing import Annotated


router = APIRouter()


@router.post("/new", response_model=UserRegistrationResult)
def signup(
        payload: UserRegistrationPayload,
) -> UserRegistrationResult:
    return UserRegistrationResult(**payload.dict())
