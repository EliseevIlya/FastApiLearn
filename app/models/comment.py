from __future__ import annotations
from typing import TYPE_CHECKING
from typing import Optional

from sqlmodel import Field, Relationship

from app.models.base_model import BaseModel

if TYPE_CHECKING:
    from app.models.task import Task
    from app.models.user import User


class Comment(BaseModel, table=True):
    __tablename__ = "comments"

    id: Optional[int] = Field(default=None, primary_key=True)

    text: str

    task_id: int = Field(foreign_key="tasks.id")
    author_id: int = Field(foreign_key="users.id")

    task: Optional[Task] = Relationship(back_populates="comments")
    author: Optional[User] = Relationship(back_populates="comments")
