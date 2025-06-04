from app.crud.restaurant import add_order_to_db, get_order_from_db, update_order_status_in_db
from app.crud.restaurant import get_order_by_id, create_courier_for_order

def get_order_service(order_id, db):
    return get_order_from_db(order_id, db)

def set_order_status_service(order_id, new_status, db):
    return update_order_status_in_db(order_id, new_status, db)

def assign_courier_service(order_id: int, courier_data: dict, db):
    order = get_order_by_id(db, order_id)
    if not order:
        return None, "Order not found"
    courier = create_courier_for_order(db, order_id, courier_data["name"], courier_data["phone"])
    return courier, None