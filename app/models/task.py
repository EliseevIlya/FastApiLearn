from __future__ import annotations
from typing import TYPE_CHECKING

from typing import Optional, List

from sqlmodel import Field, Relationship

from app.models.base_model import BaseModel
from app.models.enum.task_status import TaskStatus

if TYPE_CHECKING:
    from app.models.project import Project
    from app.models.user import User
    from app.models.comment import Comment


class Task(BaseModel, table=True):
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)

    title: str
    description: str | None = None

    status: TaskStatus = Field(default=TaskStatus.OPEN)

    project_id: int = Field(foreign_key="projects.id")
    assignee_id: int | None = Field(default=None, foreign_key="users.id")

    project: Optional[Project] = Relationship(back_populates="tasks")
    assignee: Optional[User] = Relationship(back_populates="tasks")

    comments: List[Comment] = Relationship(back_populates="task")
