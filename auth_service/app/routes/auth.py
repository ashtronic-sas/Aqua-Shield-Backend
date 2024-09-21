from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.auth import UserCreate, UserLogin, Token
from app.services.auth_service import create_user, authenticate_user
from app.config.database import get_db
from app.auth.jwt_handler import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(user, db)

@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = authenticate_user(db, user.username, user.password)
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer"}







