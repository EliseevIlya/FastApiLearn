from app.core.exceptions import EmailAlreadyExistsException
from app.core.security.password import hash_password
from app.models import User
from app.schemas.user import UserUpdate, UserRead


class UserService:

    def __init__(self, uow):
        self.uow = uow

    async def get_me(self, user: User) -> UserRead:
        return UserRead.model_validate(user)

    async def update_user(self, user: User, data: UserUpdate):
        async with self.uow:
            if data.email:
                email = str(data.email)

                existing = await self.uow.users.get_by_email(email)
                if existing and existing.id != user.id:
                    raise EmailAlreadyExistsException()

                user.email = email

            if data.password:
                user.password_hash = hash_password(data.password)

            return UserRead.model_validate(user)

    async def delete_user(self, user: User):
        async with self.uow:
            await self.uow.users.delete(user.id)
