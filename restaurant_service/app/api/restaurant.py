from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.restaurant import get_session
from app.schemas.restaurant import OrderCreate, OrderOut, MenuItemOut, OrderResponse
from app.integration.delivery_client import notify_delivery_ready, notify_start_delivery, notify_cancel
from app.crud.restaurant import (
    add_order_to_db,
    get_order_from_db,
    update_order_status_in_db,
    get_menu_from_db
)
from app.services.restaurant_service import assign_courier_service
from typing import List

router = APIRouter()

@router.get("/menu", response_model=List[MenuItemOut])
def get_menu(db: Session = Depends(get_session)):
    return get_menu_from_db(db)

@router.post("/orders", response_model=OrderResponse)
def create_order(order: OrderCreate, db: Session = Depends(get_session)):
    try:
        created_order = add_order_to_db(order, db)
        return {"accepted": True, "order": OrderOut.from_orm(created_order)}
    except ValueError as e:
        return {"accepted": False, "reason": str(e)}

@router.get("/orders/{id}", response_model=OrderOut)
def get_order(id: int, db: Session = Depends(get_session)):
    order = get_order_from_db(id, db)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.post("/orders/{id}/ready-for-delivery", response_model=OrderOut)
def ready_for_delivery(id: int, db: Session = Depends(get_session)):
    order = update_order_status_in_db(id, "READY_FOR_DELIVERY", db)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if not notify_delivery_ready(order.delivery_order_id):
        raise HTTPException(status_code=502, detail="Failed to update delivery status in delivery service")
    return order

@router.post("/orders/{id}/start-delivery", response_model=OrderOut)
def start_delivery(id: int, db: Session = Depends(get_session)):
    order = update_order_status_in_db(id, "IN_DELIVERY", db)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if not notify_start_delivery(order.delivery_order_id):
        raise HTTPException(status_code=502, detail="Failed to update delivery status in delivery service")
    return order
    
@router.post("/orders/{id}/finish", response_model=OrderOut)
def finish_order(id: int, db: Session = Depends(get_session)):
    order = update_order_status_in_db(id, "DELIVERED", db)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.post("/orders/{id}/cancel", response_model=OrderOut)
def cancel_order(id: int, db: Session = Depends(get_session)):
    order = update_order_status_in_db(id, "CANCELLED", db)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if not notify_cancel(order.delivery_order_id):
        raise HTTPException(status_code=502, detail="Failed to update delivery status in delivery service")
    return order

@router.post("/orders/{id}/assign-courier")
def assign_courier(id: int, courier_data: dict, db: Session = Depends(get_session)):
    courier, error = assign_courier_service(id, courier_data, db)
    if error:
        raise HTTPException(status_code=404, detail=error)
    return {"result": "Курьер сохранён", "courier_id": courier.id}
