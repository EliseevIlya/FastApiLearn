from typing import Type, TypeVar, Generic, Optional, List

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import SQLModel, select

ModelType = TypeVar("ModelType", bound=SQLModel)


class BaseRepository(Generic[ModelType]):

    def __init__(self, model: Type[ModelType], session: AsyncSession):
        self.model = model
        self.session = session

    async def get(self, id: int) -> Optional[ModelType]:
        return await self.session.get(self.model, id)

    async def get_all(self, limit: int = 10, offset: int = 0, options: list = None) -> List[ModelType]:
        statement = select(self.model)

        if options:
            statement = statement.options(*options)

        statement = statement.limit(limit).offset(offset)

        result = await self.session.execute(statement)
        return result.scalars().all()

    async def create(self, obj: ModelType) -> ModelType:
        self.session.add(obj)
        await self.session.flush()
        return obj

    async def delete(self, obj: ModelType):
        await self.session.delete(obj)

    async def delete_by_id(self, id: int):
        obj = await self.get(id)
        if obj:
            await self.session.delete(obj)
