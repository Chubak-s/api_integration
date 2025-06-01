from app.crud.delivery import add_order_to_db, get_order_from_db, update_order_status_in_db
from app.integration.restaurant_client import send_order_to_restaurant_api, get_menu_from_restaurant
from app.models.delivery import OrderStatus

def create_order_service(order_data, db):
    order = add_order_to_db(order_data, db)
    response = send_order_to_restaurant_api(order_data.restaurant_id, order)
    if not response.get("accepted", False):
        order.status = "CANCELLED"
        db.commit()
    restaurant_order_id = response.get("order", {}).get("id")
    order.restaurant_order_id = restaurant_order_id
    db.commit()
    db.refresh(order)
    print(f"Ответ сервиса ресторана: {response}") 
    return order

def get_order_service(order_id, db):
    return get_order_from_db(order_id, db)

def set_order_status_service(order_id, new_status, db):
    return update_order_status_in_db(order_id, new_status, db)

def get_restaurant_menu_service(restaurant_id):
    return get_menu_from_restaurant(restaurant_id)
