#user schema


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

    class Config:
        from_attributes = True