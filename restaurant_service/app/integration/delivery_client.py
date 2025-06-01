import requests

def notify_delivery_ready(order_id: int) -> bool:
    delivery_url = f"http://api:8000/orders/{order_id}/ready-for-delivery"
    try:
        resp = requests.post(delivery_url)
        resp.raise_for_status()
        return True
    except requests.RequestException as e:
        # Можно логировать ошибку e
        return False

def notify_start_delivery(order_id: int) -> bool:
    delivery_url = f"http://api:8000/orders/{order_id}/start-delivery"
    try:
        resp = requests.post(delivery_url)
        resp.raise_for_status()
        return True
    except requests.RequestException as e:
        # Можно логировать ошибку e
        return False

def notify_cancel(order_id: int) -> bool:
    delivery_url = f"http://api:8000/orders/{order_id}/cancel"
    try:
        resp = requests.post(delivery_url)
        resp.raise_for_status()
        return True
    except requests.RequestException as e:
        # Можно логировать ошибку e
        return False