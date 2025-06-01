import requests

def notify_delivery_about_status(order_id, status):
    """
    Сообщить сервису доставки о статусе заказа (например, когда кухня приняла, готовит или отменила заказ)
    """
    url = f"http://delivery-api/api/orders/{order_id}/status"
    payload = {
        "status": status
    }
    response = requests.post(url, json=payload)
    return response.json()

def get_delivery_info(order_id):
    """
    Получить информацию о доставке по заказу (например, кто курьер, где находится, время ожидания)
    """
    url = f"http://delivery-api/api/orders/{order_id}/delivery-info"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None
