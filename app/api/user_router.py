from fastapi import APIRouter, Depends

from app.core.security.dependencies import get_current_user
from app.db.unit_of_work import UnitOfWork, get_uow
from app.schemas.user import UserRead, UserUpdate
from app.services import UserService

router = APIRouter(
    prefix="/user",
    tags=["User"]
)


@router.get("/me", response_model=UserRead)
async def get_me(
        user=Depends(get_current_user),
        uow: UnitOfWork = Depends(get_uow)
):
    service = UserService(uow)
    return await service.get_me(user)


@router.put("/me", response_model=UserRead)
async def update_me(
        data: UserUpdate,
        user=Depends(get_current_user),
        uow: UnitOfWork = Depends(get_uow)
):
    service = UserService(uow)
    return await service.update_user(user, data)


@router.delete("/me")
async def delete_me(
        user=Depends(get_current_user),
        uow: UnitOfWork = Depends(get_uow)
):
    service = UserService(uow)
    await service.delete_user(user)

    return {"status": "ok"}
