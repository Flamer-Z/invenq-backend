from fastapi import APIRouter, HTTPException
from database import SessionLocal
from models import Item
from schemas import ItemCreate

router = APIRouter()

# CREATE
@router.post("/items")
def create_item(data: ItemCreate):
    db = SessionLocal()
    # Ini akan otomatis memasukkan image_url karena kita pakai **data.dict()
    item = Item(**data.dict()) 
    db.add(item)
    db.commit()
    db.refresh(item)
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
    item.image_url = data.image_url # Tambahan baru agar bisa diupdate

    db.commit()
    db.refresh(item)
    return item

# READ ALL & DELETE tetap sama seperti sebelumnya
@router.get("/items")
def get_items():
    db = SessionLocal()
    items = db.query(Item).all()
    return items

@router.delete("/items/{item_id}")
def delete_item(item_id: int):
    db = SessionLocal()
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    return {"message": "Item deleted"}
