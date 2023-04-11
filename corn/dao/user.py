from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from corn.db import get_session
from corn.exc.dao import AlreadyExistsException, EntityNotFoundException
from corn.models.pydantic.user import (UserRegistrationPayload, UserSchema,
                                       UserUpdatePayload)
from corn.models.sqlalchemy.user import User


class UserDAO:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def _get_user(self, id: str) -> User | None:
        stmt = select(User).where(User.id == id)
        user = self.session.scalars(stmt).first()

        return user

    def _get_user_by_username(self, username: str) -> User | None:
        stmt = select(User).where(User.username == username)
        user = self.session.scalars(stmt).first()

        return user

    def does_user_exist(self, id: str) -> bool:
        user = self._get_user(id)

        return user is not None

    def does_user_with_username_exist(self, username: str) -> bool:
        user = self._get_user_by_username(username)

        return user is not None

    def get_user(self, id: str) -> UserSchema | None:
        user = self._get_user(id)

        if user is not None:
            return UserSchema(**user.__dict__)

        return None

    def create_user(self, payload: UserRegistrationPayload) -> UserSchema:
        new_user = User(
            username=payload.username,
            email=payload.email,
            password_hash=f"hashed{payload.password}"
        )

        self.session.add(new_user)

        try:
            self.session.commit()
        except IntegrityError:
            self.session.rollback()
            raise AlreadyExistsException()

        self.session.refresh(new_user)

        return new_user

    def update_user(
            self,
            user_id: str,
            update: UserUpdatePayload
    ) -> UserSchema:
        user = self._get_user(user_id)

        if user is None:
            self.session.rollback()
            raise EntityNotFoundException()

        user.username = update.username

        try:
            self.session.commit()
        except:  # noqa: E722
            self.session.rollback()

        return UserSchema(**user.__dict__)
