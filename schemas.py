from pydantic import BaseModel

class ItemCreate(BaseModel):
    name: str
    quantity: int
    condition: str
    price: int
    location: str