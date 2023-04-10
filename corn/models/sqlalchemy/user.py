from corn.db import Base
from sqlalchemy.orm import Mapped, mapped_column
import uuid


def generate_id() -> str:
    return str(uuid.uuid4())


class User(Base):
    __tablename__ = "user_accounts"

    id: Mapped[str] = mapped_column(primary_key=True, default=generate_id)
    username: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(unique=True)
