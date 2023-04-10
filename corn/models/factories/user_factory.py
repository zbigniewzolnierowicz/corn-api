from uuid import UUID

import factory

from corn.models.sqlalchemy.user import User


class UserSchemaFactory(factory.Factory):
    class Meta:
        model = User

    id = factory.Sequence(lambda n: UUID(int=n))
    email = factory.Sequence(lambda n: f"user-{n}@example.com")
    username = factory.Sequence(lambda n: f"user-{n}@example.com")
    password_hash = "hashedpassword"
