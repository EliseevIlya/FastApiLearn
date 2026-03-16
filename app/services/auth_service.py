from fastapi import HTTPException

from app.core.config import get_refresh_expire_days
from app.core.security.jwt import create_access_token, create_refresh_token, decode_token
from app.core.security.password import verify_password, hash_password
from app.models import User
from app.schemas.user.user_create import UserCreate
from app.schemas.user.user_login import UserLogin

REFRESH_TOKEN_EXPIRE_DAYS = get_refresh_expire_days()


class AuthService:

    def __init__(self, uow, redis):
        self.uow = uow
        self.redis = redis

    async def register(self, create: UserCreate):

        email = create.email
        password = create.password

        async with self.uow:
            exists = await self.uow.users.get_by_email(email)

            if exists:
                raise ValueError("User already exists")

            user = User(
                email=email,
                password_hash=hash_password(password)
            )

            await self.uow.users.create(user)

            access = create_access_token(user.id)
            refresh = create_refresh_token(user.id)

            await self.redis.set_value(
                f"refresh:{user.id}",
                refresh,
                ttl=60 * 60 * 24 * REFRESH_TOKEN_EXPIRE_DAYS
            )

            return {
                "access_token": access,
                "refresh_token": refresh
            }

    async def login(self, login: UserLogin):

        email = login.email
        password = login.password

        async with self.uow:

            user = await self.uow.users.get_by_email(email)

            if not user:
                raise HTTPException(401, "Invalid credentials")

            if not verify_password(password, user.password_hash):
                raise HTTPException(401, "Invalid credentials")

            access = create_access_token(user.id)
            refresh = create_refresh_token(user.id)

            await self.redis.set(
                f"refresh:{user.id}",
                refresh,
                ex=60 * 60 * 24 * REFRESH_TOKEN_EXPIRE_DAYS
            )

            return {
                "access_token": access,
                "refresh_token": refresh
            }

    async def refresh(self, refresh_token: str):
        payload = decode_token(refresh_token)

        if not payload:
            raise HTTPException(401)

        if payload["type"] != "refresh":
            raise HTTPException(401)

        user_id = int(payload["sub"])

        stored = await self.redis.get(f"refresh:{user_id}")

        if stored != refresh_token:
            raise HTTPException(401)

        new_access = create_access_token(user_id)

        return {"access_token": new_access}

    async def logout(self, refresh_token: str):

        payload = decode_token(refresh_token)

        if not payload:
            raise HTTPException(401)

        if payload["type"] != "refresh":
            raise HTTPException(401)

        user_id = int(payload["sub"])

        await self.redis.delete_key(f"refresh:{user_id}")
