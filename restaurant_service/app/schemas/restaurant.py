from pydantic import BaseModel, Field
from typing import List, Optional
import datetime

class CourierOut(BaseModel):
    id: int
    name: str
    phone: Optional[str]

    class Config:
        orm_mode = True

class MenuItemBase(BaseModel):
    name: str
    description: Optional[str]
    price: float

class MenuItemCreate(MenuItemBase):
    pass

class MenuItemOut(MenuItemBase):
    id: int
    class Config:
        orm_mode = True

class OrderItemBase(BaseModel):
    menu_item_id: int
    quantity: int

class OrderItemCreate(OrderItemBase):
    pass

class OrderItemOut(OrderItemBase):
    id: int
    menu_item: MenuItemOut
    class Config:
        orm_mode = True

class OrderBase(BaseModel):
    customer_name: str
    customer_address: str

class OrderCreate(OrderBase):
    items: List[OrderItemCreate]
    delivery_order_id: Optional[int] = None

class OrderOut(OrderBase):
    id: int
    delivery_order_id: Optional[int] = None
    status: str
    items: List[OrderItemOut] = Field(..., alias="order_items")
    created_at: datetime.datetime
    updated_at: datetime.datetime
    courier: Optional[CourierOut] = None

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

class OrderResponse(BaseModel):
    accepted: bool
    order: OrderOut