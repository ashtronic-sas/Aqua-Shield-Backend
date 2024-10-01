from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.models import UserPlace
from app.schemas.user_place import UserPlaceCreate

# Crear una nueva relación usuario-sede
def create_user_place(db: Session, user_place: UserPlaceCreate):
    db_user_place = UserPlace(**user_place.dict())
    db.add(db_user_place)
    db.commit()
    db.refresh(db_user_place)
    return db_user_place

# Obtener todas las relaciones usuario-sede
def get_all_user_places(db: Session):
    return db.query(UserPlace).all()

# Obtener las sedes asignadas a un usuario
def get_places_by_user(db: Session, user_id: int):
    return db.query(UserPlace).filter(UserPlace.user_id == user_id).all()

# Obtener los usuarios asignados a una sede
def get_users_by_place(db: Session, place_id: int):
    return db.query(UserPlace).filter(UserPlace.place_id == place_id).all()

# Eliminar la relación usuario-sede
def delete_user_place(db: Session, user_id: int, place_id: int):
    db_user_place = db.query(UserPlace).filter(UserPlace.user_id == user_id, UserPlace.place_id == place_id).first()
    if not db_user_place:
        raise HTTPException(status_code=404, detail="UserPlace not found")
    
    db.delete(db_user_place)
    db.commit()
