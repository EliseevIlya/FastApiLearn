from fastapi import APIRouter, Depends

from app.db.redis import RedisClient, get_redis
from app.db.unit_of_work import UnitOfWork, get_uow
from app.schemas.jwt.refresh_request import RefreshRequest
from app.schemas.jwt.token_response import TokenResponse
from app.schemas.user.user_create import UserCreate
from app.schemas.user.user_login import UserLogin
from app.services.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post("/register", response_model=TokenResponse)
async def register(
        data: UserCreate,
        uow: UnitOfWork = Depends(get_uow),
        redis: RedisClient = Depends(get_redis)
):
    service = AuthService(uow, redis)

    return await service.register(create=data)


@router.post("/login", response_model=TokenResponse)
async def login(
        data: UserLogin,
        uow: UnitOfWork = Depends(get_uow),
        redis: RedisClient = Depends(get_redis)
):
    service = AuthService(uow, redis)

    return await service.login(login=data)


@router.post("/refresh", response_model=TokenResponse)
async def refresh(
        data: RefreshRequest,
        uow: UnitOfWork = Depends(get_uow),
        redis: RedisClient = Depends(get_redis)
):
    service = AuthService(uow, redis)

    return await service.refresh(data.refresh_token)


@router.post("/logout")
async def logout(
        data: RefreshRequest,
        uow: UnitOfWork = Depends(get_uow),
        redis: RedisClient = Depends(get_redis)
):
    service = AuthService(uow, redis)

    await service.logout(data.refresh_token)

    return {"status": "ok"}
