from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_session
from app.repositories import UserRepository, ProjectRepository, TaskRepository, CommentRepository


class UnitOfWork:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def __aenter__(self):
        self.users = UserRepository(self.session)
        self.projects = ProjectRepository(self.session)
        self.tasks = TaskRepository(self.session)
        self.comments = CommentRepository(self.session)

        return self

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()

    async def __aexit__(self, exc_type, exc, tb):

        if exc:
            await self.session.rollback()
        else:
            await self.session.commit()


async def get_uow(session: AsyncSession = Depends(get_session)):
    return UnitOfWork(session)
