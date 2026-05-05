from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Borrow, Item
from schemas import BorrowCreate
from datetime import datetime

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/borrow")
def borrow_item(data: BorrowCreate, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == data.item_id).first()

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    if item.quantity <= 0:
        raise HTTPException(status_code=400, detail="Stock empty")

    item.quantity -= 1

    borrow = Borrow(
        item_id=data.item_id,
        borrower_name=data.borrower_name
    )

    db.add(borrow)
    db.commit()
    db.refresh(borrow)

    return borrow


@router.get("/borrow")
def get_borrows(db: Session = Depends(get_db)):
    return db.query(Borrow).all()


@router.put("/return/{borrow_id}")
def return_item(borrow_id: int, db: Session = Depends(get_db)):
    borrow = db.query(Borrow).filter(Borrow.id == borrow_id).first()

    if not borrow:
        raise HTTPException(status_code=404, detail="Borrow not found")
    
    if borrow.status == "returned":
        raise HTTPException(status_code=400, detail="Already returned")

    borrow.status = "returned"
    borrow.return_date = datetime.utcnow()

    item = db.query(Item).filter(Item.id == borrow.item_id).first()
    item.quantity += 1

    db.commit()

    return {"message": "Item returned"}
