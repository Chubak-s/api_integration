from fastapi import FastAPI
from app.api import restaurant
from app.db.restaurant import init_db

app = FastAPI(title="Restaurant Service")

@app.on_event("startup")
def startup():
    init_db()

app.include_router(
    restaurant.router, 
    prefix="", 
    tags=[""]
)

