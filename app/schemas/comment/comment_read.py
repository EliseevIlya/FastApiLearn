from pydantic import BaseModel


class CommentRead(BaseModel):
    id: int
    text: str
    author_id: int
