from sqlmodel import Field, Relationship

from app.models.base_model import BaseModel
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models.comment import Comment
    from app.models.project import Project
    from app.models.task import Task


class User(BaseModel, table=True):
    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True)

    email: str = Field(index=True, unique=True)
    password_hash: str

    projects: list["Project"] = Relationship(back_populates="owner")
    tasks: list["Task"] = Relationship(back_populates="assignee")
    comments: list["Comment"] = Relationship(back_populates="author")
