from pydantic import BaseModel


class CommentCreate(BaseModel):
    text: str
    task_id: int
