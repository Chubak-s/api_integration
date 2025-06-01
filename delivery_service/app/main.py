from fastapi import FastAPI
from app.api import delivery
from app.db.database import init_db

app = FastAPI(title="Delivery Service")

@app.on_event("startup")
def startup():
    init_db()

app.include_router(
    delivery.router, 
    prefix="", 
    tags=[""]
)
