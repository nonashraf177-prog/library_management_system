from pydantic import BaseModel
from typing import Optional


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str
    role: Optional[str] = "member"


class UserResponse(UserBase):
    id: int
    role: str

    model_config = {"from_attributes": True}
