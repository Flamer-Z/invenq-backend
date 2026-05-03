from fastapi import FastAPI
from database import Base, engine
from routers import items

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "InvenQ API is running 🚀"}

app.include_router(items.router)