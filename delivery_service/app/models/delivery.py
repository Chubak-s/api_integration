from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship, declarative_base
import enum
import datetime

Base = declarative_base()

class OrderStatus(enum.Enum):
    ACCEPTED = "ACCEPTED"
    PREPARING = "PREPARING"
    IN_DELIVERY = "IN_DELIVERY"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"

class Courier(Base):
    __tablename__ = "couriers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=True)

    orders = relationship("Order", back_populates="courier")

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    restaurant_order_id = Column(Integer, nullable=True)
    client_id = Column(Integer, nullable=False)
    restaurant_id = Column(Integer, nullable=False)
    customer_name = Column(String, nullable=False)
    customer_address = Column(String, nullable=False)
    status = Column(String, default="ACCEPTED")
    courier_id = Column(Integer, ForeignKey("couriers.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    courier = relationship("Courier", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    menu_item_id = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)

    order = relationship("Order", back_populates="order_items")
