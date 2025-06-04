from app.models.restaurant import Order, OrderItem, MenuItem, Courier
from sqlalchemy.orm import Session
from typing import List

def add_order_to_db(order_data, db: Session):
    # Создаём заказ
    order = Order(
        customer_name=order_data.customer_name,
        customer_address=order_data.customer_address,
        delivery_order_id=order_data.delivery_order_id,
        status="created",
    )
    db.add(order)
    db.commit()
    db.refresh(order)

    # Для каждого OrderItem из запроса создаём запись в order_items
    for item in order_data.items:
        # Проверяем, что позиция меню реально существует
        menu_item = db.query(MenuItem).filter(MenuItem.id == item.menu_item_id).first()
        if not menu_item:
            db.rollback()
            raise ValueError(f"MenuItem с id {item.menu_item_id} не найден")
        db_order_item = OrderItem(
            order_id=order.id,
            menu_item_id=item.menu_item_id,
            quantity=item.quantity,
        )
        db.add(db_order_item)
    db.commit()
    db.refresh(order)
    return order

def get_order_from_db(order_id: int, db: Session):
    return db.query(Order).filter(Order.id == order_id).first()

def update_order_status_in_db(order_id: int, new_status: str, db: Session):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        return None
    order.status = new_status
    db.commit()
    db.refresh(order)
    return order

def get_menu_from_db(db: Session) -> List[MenuItem]:
    return db.query(MenuItem).all()

def get_order_by_id(db, order_id: int):
    return db.query(Order).filter(Order.id == order_id).first()

def create_courier_for_order(db, order_id: int, name: str, phone: str):
    courier = Courier(name=name, phone=phone, order_id=order_id)
    db.add(courier)
    db.commit()
    db.refresh(courier)
    return courier