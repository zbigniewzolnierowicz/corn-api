from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from corn.db import get_session
from corn.models.pydantic.user import UserRegistrationPayload, UserSchema
from corn.models.sqlalchemy.user import User


class UserDAO:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def does_user_exist(self, id: str) -> bool:
        stmt = select(User).where(User.id == id)
        does_user_exist = self.session.scalars(stmt).first()

        return does_user_exist is not None

    def get_user(self, id: str) -> UserSchema:
        pass

    def create_user(self, payload: UserRegistrationPayload) -> UserSchema:
        pass

    def update_user(self, user_id: str, update: UserSchema) -> UserSchema:
        pass
