import requests
from .restaurant_directory import get_restaurant_url

def send_order_to_restaurant_api(restaurant_id, order):
    # POST запрос в ресторан для создания заказа
    base_url = get_restaurant_url(restaurant_id)
    payload = {
        "customer_name": order.customer_name,
        "customer_address": order.customer_address,
        "items": [
            {"menu_item_id": i.menu_item_id, "quantity": i.quantity}
            for i in order.order_items
        ]
    }
    response = requests.post(f"{base_url}/orders/", json=payload)
    return response.json()

def get_menu_from_restaurant(restaurant_id):
    base_url = get_restaurant_url(restaurant_id)
    response = requests.get(f"{base_url}/menu")
    if response.status_code == 200:
        return response.json()
    return None
