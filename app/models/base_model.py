from datetime import datetime
from sqlmodel import SQLModel, Field


class BaseModel(SQLModel):
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime | None = None