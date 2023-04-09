from corn.models.pydantic.user import (
    UserRegistrationPayload,
    UserSchema
)


class UserDAO:
    def __init__(self):
        pass

    def does_user_exist(self, id: str) -> bool:
        return False

    def get_user(self, id: str) -> UserSchema:
        pass

    def create_user(self, payload: UserRegistrationPayload):
        pass

    def update_user(self, user_id: str, update: UserSchema) -> UserSchema:
        pass
