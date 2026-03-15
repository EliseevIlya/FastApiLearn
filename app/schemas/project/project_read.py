from datetime import datetime
from pydantic import BaseModel


class ProjectRead(BaseModel):
    id: int
    name: str
    owner_id: int
    created_at: datetime
