from __future__ import annotations
from typing import TYPE_CHECKING

from typing import Optional, List

from sqlmodel import Field, Relationship

from app.models.base_model import BaseModel

if TYPE_CHECKING:
    from app.models.project import Project
    from app.models.task import Task
    from app.models.comment import Comment


class User(BaseModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)

    email: str = Field(index=True, unique=True)
    password_hash: str

    projects: List[Project] = Relationship(back_populates="owner")
    tasks: List[Task] = Relationship(back_populates="assignee")
    comments: List[Comment] = Relationship(back_populates="author")
