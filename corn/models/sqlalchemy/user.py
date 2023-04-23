import uuid
from typing import List

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import Mapped, relationship

from corn.db import Base
from corn.hasher import hasher
from corn.models.sqlalchemy.mixins import HasCreatedAt


class User(Base, HasCreatedAt):
    __tablename__ = "user_accounts"

    id: str = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )
    username: str = Column(String, unique=True)
    password_hash: str = Column(String)
    email: str = Column(String, unique=True)
    refresh_tokens: Mapped[List["RefreshToken"]] = relationship(
        "RefreshToken",
        back_populates="user"
    )

    def check_password(self, password: str) -> bool:
        return hasher.verify(self.password_hash, password)


class RefreshToken(Base, HasCreatedAt):
    __tablename__ = "user_token"
    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )
    user_id: str = Column(
        ForeignKey("user_accounts.id", ondelete="CASCADE")
    )
    user: Mapped[User] = relationship(User, back_populates="refresh_tokens")
    hashed_token = Column(String)
