from fastapi import APIRouter, HTTPException
from database import SessionLocal
from models import Item
from schemas import ItemCreate

router = APIRouter()

# CREATE
@router.post("/items")
def create_item(data: ItemCreate):
    db = SessionLocal()
    item = Item(**data.dict())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


# READ ALL
@router.get("/items")
def get_items():
    db = SessionLocal()
    items = db.query(Item).all()
    return items


# READ BY ID
@router.get("/items/{item_id}")
def get_item(item_id: int):
    db = SessionLocal()
    item = db.query(Item).filter(Item.id == item_id).first()

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    return item


# UPDATE
@router.put("/items/{item_id}")
def update_item(item_id: int, data: ItemCreate):
    db = SessionLocal()
    item = db.query(Item).filter(Item.id == item_id).first()

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    item.name = data.name
    item.quantity = data.quantity
    item.condition = data.condition
    item.price = data.price
    item.location = data.location

    db.commit()
    db.refresh(item)

    return item


# DELETE (soft delete nanti kita upgrade)
@router.delete("/items/{item_id}")
def delete_item(item_id: int):
    db = SessionLocal()
    item = db.query(Item).filter(Item.id == item_id).first()

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    db.delete(item)
    db.commit()

    return {"message": "Item deleted"}
