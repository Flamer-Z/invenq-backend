from pydantic import BaseModel, Field
from datetime import datetime

class ItemCreate(BaseModel):
    name: str
    quantity: int = Field(..., ge=0)
    condition: str
    price: int = Field(..., ge=0)
    location: str


class ItemResponse(BaseModel):
    id: int
    name: str
    quantity: int
    condition: str
    price: int
    location: str

    class Config:
        from_attributes = True

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

class UserCreate(BaseModel):
    username: str
    password: str
    role: str = "staff"

class UserLogin(BaseModel):
    username: str
    password: str

