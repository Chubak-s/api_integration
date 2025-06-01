# Справочник ресторанов: restaurant_id -> base_url
RESTAURANT_DIRECTORY = {
    1: "http://restaurant-api:8000",  # docker-compose сервис
    2: "http://another-restaurant-api:8000",
    # Другие рестораны по мере необходимости
}

def get_restaurant_url(restaurant_id: int) -> str:
    return RESTAURANT_DIRECTORY.get(restaurant_id)