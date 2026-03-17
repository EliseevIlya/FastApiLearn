from datetime import datetime

from fastapi import HTTPException

from app.core.config import get_refresh_expire_days
from app.core.security.jwt import create_access_token, create_refresh_token, decode_token
from app.core.security.password import verify_password, hash_password
from app.models import User
from app.schemas.jwt.logout_request import LogoutRequest
from app.schemas.user.user_create import UserCreate
from app.schemas.user.user_login import UserLogin

REFRESH_TOKEN_EXPIRE_DAYS = get_refresh_expire_days()


class AuthService:

    def __init__(self, uow, redis):
        self.uow = uow
        self.redis = redis

    async def create_tokens(self, user_id: int) -> dict[str, str]:
        access = create_access_token(user_id)

        refresh, jti = create_refresh_token(user_id)

        await self.redis.set_value(
            f"refresh:{jti}",
            str(user_id),
            ttl=60 * 60 * 24 * REFRESH_TOKEN_EXPIRE_DAYS
        )

        return {
            "access_token": access,
            "refresh_token": refresh
        }

    async def register(self, create: UserCreate):

        email = create.email
        password = create.password

        async with self.uow:
            exists = await self.uow.users.get_by_email(email)

            if exists:
                raise HTTPException(400, "User already exists")

            user = User(
                email=email,
                password_hash=hash_password(password)
            )

            await self.uow.users.create(user)

            return await self.create_tokens(user.id)

    async def login(self, login: UserLogin):

        email = login.email
        password = login.password

        async with self.uow:

            user = await self.uow.users.get_by_email(email)

            if not user:
                raise HTTPException(401, "Invalid credentials")

            if not verify_password(password, user.password_hash):
                raise HTTPException(401, "Invalid credentials")

            return await self.create_tokens(user.id)

    async def refresh(self, refresh_token: str):
        payload = decode_token(refresh_token)

        if not payload or payload["type"] != "refresh":
            raise HTTPException(401)

        jti = payload.get("jti")
        user_id = int(payload["sub"])

        stored = await self.redis.get(f"refresh:{jti}")

        if stored != refresh_token:
            raise HTTPException(401, "Token revoked or reused")

        await self.redis.delete_key(f"refresh:{jti}")

        return await self.create_tokens(user_id)

    async def logout(self, access_token: str, refresh_token: str):

        access_payload = decode_token(access_token)

        if not access_payload or access_payload["type"] != "access":
            raise HTTPException(401, "Token revoked or reused")

        jti = access_payload.get("jti")
        exp = access_payload.get("exp")
        ttl = exp - int(datetime.utcnow().timestamp())

        if ttl > 0:
            await self.redis.set_value(
                f"blacklist:{jti}",
                "1",
                ttl=ttl
            )

        refresh_payload = decode_token(refresh_token)

        if not refresh_payload or refresh_payload["type"] != "refresh":
            raise HTTPException(401, "Token revoked or reused")

        jti = refresh_payload.get("jti")
        await self.redis.delete_key(f"refresh:{jti}")
