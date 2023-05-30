from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, declarative_mixin, declared_attr, mapped_column


@declarative_mixin
class HasCreatedAt:
    @declared_attr
    def created_at(cls) -> Mapped[DateTime]:
        return mapped_column(DateTime, server_default=func.now())
