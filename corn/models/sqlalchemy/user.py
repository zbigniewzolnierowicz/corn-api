import uuid

from sqlalchemy import Column, String

from corn.db import Base
from corn.hasher import hasher


class User(Base):
    __tablename__ = "user_accounts"

    id: str = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )
    username: str = Column(String, unique=True)
    password_hash: str = Column(String)
    email: str = Column(String, unique=True)

    def check_password(self, password: str) -> bool:
        return hasher.verify(self.password_hash, password)
