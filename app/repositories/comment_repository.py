from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlmodel import select

from app.models.comment import Comment
from app.repositories.base_repository import BaseRepository


class CommentRepository(BaseRepository[Comment]):

    def __init__(self, session: AsyncSession):
        super().__init__(Comment, session)

    async def get_task_comments(self, task_id: int, limit: int = 10, offset: int = 0, options: list = None):

        statement = select(Comment).where(Comment.task_id == task_id)

        if options:
            statement = statement.options(*options)

        statement = statement.limit(limit).offset(offset)

        result = await self.session.execute(statement)

        return result.scalars().all()
