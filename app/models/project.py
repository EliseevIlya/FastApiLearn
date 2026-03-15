from __future__ import annotations
from typing import TYPE_CHECKING

from typing import Optional, List

from sqlmodel import Field, Relationship

from app.models.base_model import BaseModel

if TYPE_CHECKING:
    from app.models import User
    from app.models.task import Task


class Project(BaseModel, table=True):
    __tablename__ = "projects"

    id: Optional[int] = Field(default=None, primary_key=True)

    name: str

    owner_id: int = Field(foreign_key="users.id")

    owner: Optional[User] = Relationship(back_populates="projects")

    tasks: List[Task] = Relationship(back_populates="project")
