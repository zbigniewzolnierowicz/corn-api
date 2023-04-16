import uuid

from sqlalchemy.orm import Mapped, mapped_column

from corn.db import Base
from corn.hasher import hasher


class User(Base):
    __tablename__ = "user_accounts"

    id: Mapped[str] = mapped_column(
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )
    username: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(unique=True)

    def check_password(self, password: str) -> bool:
        return hasher.verify(self.password_hash, password)
