from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class BorrowResponse(BaseModel):
    id: int
    user_id: int
    book_id: int
    borrow_date: datetime
    return_date: Optional[datetime] = None
    status: str

    model_config = {"from_attributes": True}
