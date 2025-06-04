from app.models.delivery import Order, OrderItem, Courier
from sqlalchemy.orm import Session

def add_order_to_db(order_data, db: Session):
    order = Order(
        client_id=order_data.client_id,
        restaurant_id=order_data.restaurant_id,
        customer_name=order_data.customer_name,
        customer_address=order_data.customer_address,
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    for item in order_data.items:
        db_item = OrderItem(
            order_id=order.id,
            menu_item_id=item.menu_item_id,
            quantity=item.quantity,
        )
        db.add(db_item)
    db.commit()
    db.refresh(order)
    return order


def get_order_from_db(order_id: int, db: Session):
    return db.query(Order).filter(Order.id == order_id).first()

def update_order_status_in_db(order_id: int, new_status, db: Session):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        return None
    order.status = new_status
    db.commit()
    db.refresh(order)
    return order

def get_first_free_courier(db):
    return db.query(Courier).filter(Courier.is_busy == False).first()

def set_courier_busy(db, courier_id: int):
    courier = db.query(Courier).filter(Courier.id == courier_id).first()
    if courier is None:
        return None
    courier.is_busy = True
    db.commit()
    db.refresh(courier)
    return courier

def get_courier_by_id(db, courier_id: int):
    return db.query(Courier).filter(Courier.id == courier_id).first()

def assign_courier_to_order(db, order_id: int, courier_id: int):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        return None
    order.courier_id = courier_id
    db.commit()
    db.refresh(order)
    return order