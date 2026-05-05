from fastapi import FastAPI
from database import Base, engine
from routers import items, borrow, dashboard

app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(items.router)
app.include_router(borrow.router)
app.include_router(dashboard.router)

@app.get("/")
def root():
    return {"message": "InvenQ API is running 🚀"}
