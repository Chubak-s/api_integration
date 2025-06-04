import requests
from .restaurant_directory import get_restaurant_url

def send_order_to_restaurant_api(restaurant_id, order):
    # POST запрос в ресторан для создания заказа
    base_url = get_restaurant_url(restaurant_id)
    payload = {
        "customer_name": order.customer_name,
        "customer_address": order.customer_address,
        "delivery_order_id": order.id,
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

def notify_finish_delivery(restaurant_order_id, restaurant_id):
    base_url = get_restaurant_url(restaurant_id)
    response = requests.post(f"{base_url}/orders/{restaurant_order_id}/finish")
    if response.status_code == 200:
        return response.json()
    return None

def notify_restaurant_assign_courier(restaurant_order_id, courier, restaurant_id):
    base_url = get_restaurant_url(restaurant_id)
    payload = {
        "name": courier.name,
        "phone": courier.phone
    }
    response = requests.post(f"{base_url}/orders/{restaurant_order_id}/assign-courier", json=payload)
    return response