from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum
import datetime

# 1. Enum статусов заказа (OrderStatus)
class OrderStatus(str, Enum):
    ACCEPTED = "ACCEPTED"
    READY_FOR_DELIVERY = "READY_FOR_DELIVERY"
    IN_DELIVERY = "IN_DELIVERY"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"

# 2. OrderItem (позиция в заказе)
class OrderItemCreate(BaseModel):
    menu_item_id: int
    quantity: int

class OrderItemOut(BaseModel):
    id: int
    menu_item_id: int
    quantity: int
    class Config:
        orm_mode = True

# 3. Заказ (Order)
class OrderCreate(BaseModel):
    client_id: int
    restaurant_id: int
    customer_name: str
    customer_address: str
    items: List[OrderItemCreate]

class OrderOut(BaseModel):
    id: int
    restaurant_order_id: Optional[int] = None
    client_id: int
    restaurant_id: int
    customer_name: str
    customer_address: str
    status: str
    items: List[OrderItemOut] = Field(..., alias="order_items")
    courier_id: Optional[int] = None
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

# 4. Для ручек обновления статуса заказа
class OrderStatusUpdate(BaseModel):
    status: str

# 5. (Опционально) Курьер
class CourierBase(BaseModel):
    name: str
    phone: Optional[str]

class CourierCreate(CourierBase):
    pass

class CourierOut(CourierBase):
    id: int
    class Config:
        orm_mode = True
