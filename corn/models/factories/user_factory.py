from uuid import UUID

import factory

from corn.hasher import hasher
from corn.models.factories.main import fake
from corn.models.pydantic.user import UserRegistrationPayload
from corn.models.sqlalchemy.user import User


class BaseUserFactory(factory.Factory):  # type: ignore
    username = fake.user_name()
    email = fake.ascii_safe_email()


class UserSchemaFactory(BaseUserFactory):
    class Meta:
        model = User

    id = factory.Sequence(lambda n: UUID(int=n))
    password_hash = hasher.hash("foobar")


class UserRegistrationPayloadFactory(BaseUserFactory):
    class Meta:
        model = UserRegistrationPayload

    password = "foobar"
