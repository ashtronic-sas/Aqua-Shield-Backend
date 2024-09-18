from app.models import Order
from app.schemas.order import OrderCreate
from app.utils.database import get_db
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

def create_order(order: OrderCreate, db: Session):
    new_order = Order(
        user_id=order.user_id,
        item_name=order.item_name,
        quantity=order.quantity
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order

def get_orders_by_user(user_id: int, db: Session):
    return db.query(Order).filter(Order.user_id == user_id).all()




