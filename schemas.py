from pydantic import BaseModel
from datetime import datetime

class BorrowCreate(BaseModel):
    item_id: int
    borrower_name: str

class BorrowResponse(BaseModel):
    id: int
    item_id: int
    borrower_name: str
    borrow_date: datetime
    return_date: datetime | None
    status: str

    class Config:
        from_attributes = True
