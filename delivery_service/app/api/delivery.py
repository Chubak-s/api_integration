from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_session
from app.models.delivery import OrderStatus
from app.schemas.delivery import OrderCreate, OrderOut
from app.integration.restaurant_client import notify_finish_delivery
from app.services.delivery_service import (
    create_order_service,
    get_order_service,
    set_order_status_service,
    get_restaurant_menu_service
)

router = APIRouter(prefix="", tags=[""])


# 1. Получение меню ресторана
@router.get("/restaurants/{restaurant_id}/menu")
def get_restaurant_menu(restaurant_id: int):
    menu = get_restaurant_menu_service(restaurant_id)
    if not menu:
        raise HTTPException(status_code=404, detail="Меню ресторана не найдено")
    return menu


# 2. Создание заказа
@router.post("/orders", response_model=OrderOut)
def create_order(
    order: OrderCreate,
    db: Session = Depends(get_session)
):
    result = create_order_service( order, db)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Заказ не был создан: ресторан отказал"
        )
    return result


# 3. Получение заказа по id
@router.get("/orders/{order_id}", response_model=OrderOut)
def get_order(order_id: int, db: Session = Depends(get_session)):
    order = get_order_service(order_id, db)
    if not order:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    return order


# 4. Заказ готов к доставке
@router.post("/orders/{order_id}/ready-for-delivery", response_model=OrderOut)
def ready_for_delivery(order_id: int, db: Session = Depends(get_session)):
    order = set_order_status_service(order_id, OrderStatus.READY_FOR_DELIVERY.value, db)
    if not order:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    return order


# 5. Заказ передан в доставку (статус "В пути")
@router.post("/orders/{order_id}/start-delivery", response_model=OrderOut)
def start_delivery(order_id: int, db: Session = Depends(get_session)):
    order = set_order_status_service(order_id, OrderStatus.IN_DELIVERY.value, db)
    if not order:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    return order

# 6. Заказ доставлен (статус "завершен")
@router.post("/orders/{order_id}/finish", response_model=OrderOut)
def finish_order(order_id: int, db: Session = Depends(get_session)):
    order = set_order_status_service(order_id, OrderStatus.DELIVERED.value, db)
    if not order:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    if not notify_finish_delivery(order.restaurant_order_id, order.restaurant_id):
        raise HTTPException(status_code=502, detail="Failed to update delivery status in delivery service")
    return order

# 7. Отмена заказа
@router.post("/orders/{order_id}/cancel", response_model=OrderOut)
def cancel_order(order_id: int, db: Session = Depends(get_session)):
    order = set_order_status_service(order_id, OrderStatus.CANCELLED.value, db)
    if not order:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    return order
