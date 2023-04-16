from uuid import UUID

import factory

from corn.hasher import hasher
from corn.models.pydantic.user import UserRegistrationPayload
from corn.models.sqlalchemy.user import User


class UserSchemaFactory(factory.Factory):  # type: ignore
    class Meta:
        model = User

    id = factory.Sequence(lambda n: UUID(int=n))
    email = factory.Sequence(lambda n: f"user-{n}@example.com")
    username = factory.Sequence(lambda n: f"user-{n}@example.com")
    password_hash = hasher.hash("foobar")


class UserRegistrationPayloadFactory(factory.Factory):  # type: ignore
    class Meta:
        model = UserRegistrationPayload
    email = factory.Sequence(lambda n: f"user-{n}@example.com")
    username = factory.Sequence(lambda n: f"user-{n}@example.com")
    password = "foobar"
