from typing import Optional

from sqlmodel import Field, Relationship

from app.models.base_model import BaseModel
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models.task import Task
    from app.models.user import User


class Project(BaseModel, table=True):
    __tablename__ = "projects"

    id: int | None = Field(default=None, primary_key=True)

    name: str

    owner_id: int = Field(foreign_key="users.id")

    owner: Optional["User"] = Relationship(back_populates="projects")
    tasks: list["Task"] = Relationship(back_populates="project")
