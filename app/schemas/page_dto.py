from typing import Generic, TypeVar, List
from pydantic import BaseModel

T = TypeVar("T")


class PageDTO(BaseModel, Generic[T]):
    items: List[T]
    limit: int
    offset: int
