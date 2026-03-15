from pydantic import BaseModel
from app.models.enum.task_status import TaskStatus


class TaskRead(BaseModel):
    id: int
    title: str
    description: str | None
    status: TaskStatus
