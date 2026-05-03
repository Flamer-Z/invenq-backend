from fastapi import APIRouter
from database import SessionLocal
from models import Item
from schemas import ItemCreate

router = APIRouter()

@router.post("/items")
def create_item(data: ItemCreate):
    db = SessionLocal()

    item = Item(**data.dict())
    db.add(item)
    db.commit()

    return {"message": "Item created"}
