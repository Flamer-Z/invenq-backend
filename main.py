from fastapi import FastAPI
from database import Base, engine
from routers import items, borrow, dashboard, logs

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(items.router)
app.include_router(borrow.router)
app.include_router(dashboard.router)
app.include_router(logs.router)

@app.get("/")
def root():
    return {"message": "InvenQ API is running 🚀"}
