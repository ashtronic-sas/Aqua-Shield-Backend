from app.models.models import User
from app.schemas.user import UserCreate
from app.config.security import get_password_hash, verify_password
from fastapi import HTTPException
from sqlalchemy.orm import Session

def create_user(user: UserCreate, db: Session):
    existing_user = db.query(User).filter((User.username == user.username)).first()
    if existing_user:
        if existing_user.username == user.username:
            raise HTTPException(status_code=400, detail="Username already exists")
    
    hashed_password = get_password_hash(user.password)
    new_user = User(username=user.username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user

#     Obtiene un usuario por su ID.
def get_user_by_id(id: int, db: Session):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

#     Actualiza un usuario por su ID.
def update_user_by_id(id: int, user: UserCreate, db: Session):
    db_user = db.query(User).filter(User.id == id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.username is not None:
        db_user.username = user.username
    if user.password is not None:
        db_user.password = get_password_hash(user.password)
    
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user_by_id(id: int, db: Session):
    db_user = db.query(User).filter(User.id == id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted successfully"}

#     Obtiene todos los usuarios.
def get_all_users(db: Session):
    users = db.query(User).all()
    return users


