from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer

from app.core.security.jwt import decode_token
from app.db.unit_of_work import get_uow

security = HTTPBearer()


async def get_current_user(
        credentials=Depends(security),
        uow=Depends(get_uow)
):
    token = credentials.credentials

    payload = decode_token(token)

    if not payload:
        raise HTTPException(401)

    user_id = int(payload["sub"])

    async with uow:
        user = await uow.users.get(user_id)

    if not user:
        raise HTTPException(401)

    return user
