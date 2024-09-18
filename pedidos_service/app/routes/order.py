from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.order import OrderCreate, OrderOut
from app.services.order_service import create_order, get_orders_by_user
from app.utils.database import get_db
from app.auth.jwt_handler import decode_access_token
from fastapi.security import OAuth2PasswordBearer

router = APIRouter(prefix="/orders", tags=["orders"])

# Define the OAuth2PasswordBearer instance
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return payload

@router.post("/", response_model=OrderOut)
def create_new_order(order: OrderCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    current_user = get_current_user(token)
    if current_user["sub"] != order.user_id:
        raise HTTPException(status_code=403, detail="Not authorized to create order for this user")
    return create_order(order, db)

@router.get("/", response_model=list[OrderOut])
def read_orders(user_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    current_user = get_current_user(token)
    if current_user["sub"] != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to view orders for this user")
    return get_orders_by_user(user_id, db)





