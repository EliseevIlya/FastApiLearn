from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.project import Project
from app.repositories.base_repository import BaseRepository


class ProjectRepository(BaseRepository[Project]):

    def __init__(self, session: AsyncSession):
        super().__init__(Project, session)

    async def get_user_projects(self, user_id: int,limit: int = 10, offset: int = 0, options: list = None):

        statement = select(Project).where(Project.owner_id == user_id)

        if options:
            statement = statement.options(*options)

        statement = statement.limit(limit).offset(offset)

        result = await self.session.execute(statement)

        return result.scalars().all()
