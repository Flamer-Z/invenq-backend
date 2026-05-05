from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Item, Borrow

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/dashboard")
def get_dashboard(db: Session = Depends(get_db)):
    total_items = db.query(Item).count()
    borrowed = db.query(Borrow).filter(Borrow.status == "borrowed").count()
    available = db.query(Item).filter(Item.quantity > 0).count()

    return {
        "total_items": total_items,
        "borrowed_items": borrowed,
        "available_items": available
    }
