from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Borrow, Item, ActivityLog
from schemas import BorrowCreate, BorrowResponse
from datetime import datetime

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/borrow", response_model=BorrowResponse)
def borrow_item(data: BorrowCreate, db: Session = Depends(get_db)):
    # Gunakan with_for_update() untuk mengunci baris agar quantity tetap sinkron
    item = db.query(Item).filter(Item.id == data.item_id).with_for_update().first()

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    if item.quantity <= 0:
        raise HTTPException(status_code=400, detail="Stock empty")

    try:
        # Update stok secara atomik
        item.quantity -= 1

        borrow = Borrow(
            item_id=data.item_id,
            borrower_name=data.borrower_name,
            status="borrowed"
        )
        db.add(borrow)

        log = ActivityLog(action="BORROW", item_id=data.item_id)
        db.add(log)

        db.commit()
        db.refresh(borrow)
        return borrow

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/borrow", response_model=list[BorrowResponse])
def get_borrows(db: Session = Depends(get_db)):
    # Tetap pastikan hanya mengambil yang 'borrowed'
    return db.query(Borrow).filter(Borrow.status == "borrowed").all()


@router.put("/return/{borrow_id}")
def return_item(borrow_id: int, db: Session = Depends(get_db)):
    # Lock data borrow agar tidak diproses ganda
    borrow = db.query(Borrow).filter(Borrow.id == borrow_id).with_for_update().first()

    if not borrow:
        raise HTTPException(status_code=404, detail="Borrow not found")

    if borrow.status == "returned":
        # Jika sudah returned, kembalikan 200 OK agar Android menganggap sukses 
        # dan merefresh UI, daripada melempar error 400.
        return "Already returned"

    item = db.query(Item).filter(Item.id == borrow.item_id).with_for_update().first()

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    try:
        borrow.status = "returned"
        borrow.return_date = datetime.utcnow()
        
        # Update stok barang kembali
        item.quantity += 1

        log = ActivityLog(action="RETURN", item_id=borrow.item_id)
        db.add(log)

        db.commit()

        # FIX: Kembalikan String murni, bukan DICT {message: ...}
        # Ini supaya sinkron dengan Call<String> di Retrofit Android
        return "Item returned successfully"

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
