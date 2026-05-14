from pydantic import BaseModel
from typing import Optional


class BookBase(BaseModel):
    title: str
    author: str
    category: Optional[str] = None
    published_year: Optional[int] = None


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    category: Optional[str] = None
    published_year: Optional[int] = None
    available: Optional[bool] = None


class BookResponse(BookBase):
    id: int
    available: bool

    model_config = {"from_attributes": True}
