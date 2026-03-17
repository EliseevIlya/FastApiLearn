from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload
from sqlmodel import select

from app.models.task import Task
from app.repositories.base_repository import BaseRepository


class TaskRepository(BaseRepository[Task]):

    def __init__(self, session: AsyncSession):
        super().__init__(Task, session)

    async def get_project_tasks(self, project_id: int, limit: int = 10, offset: int = 0, options: list = None):
        statement = select(Task).where(Task.project_id == project_id)

        if options:
            statement = statement.options(*options)

        statement = statement.limit(limit).offset(offset)

        result = await self.session.execute(statement)

        return result.scalars().all()
