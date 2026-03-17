from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer

from app.core.security.jwt import decode_token
from app.db.redis import RedisClient, get_redis
from app.db.unit_of_work import get_uow

security = HTTPBearer()


async def get_current_user(
        credentials=Depends(security),
        uow=Depends(get_uow),
        redis: RedisClient = Depends(get_redis)
):
    token = credentials.credentials

    payload = decode_token(token)

    if not payload or payload.get("type") != "access":
        raise HTTPException(401, "Invalid token")

    jti = payload.get("jti")

    is_blacklisted = await redis.get_value(f"blacklist:{jti}")

    if is_blacklisted:
        raise HTTPException(401, "Token revoked")

    user_id = int(payload["sub"])

    async with uow:
        user = await uow.users.get(user_id)

    if not user:
        raise HTTPException(401, "User not found")

    return user
