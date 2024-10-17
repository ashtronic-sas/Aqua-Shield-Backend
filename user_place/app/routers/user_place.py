from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.schemas.user_place import UserPlaceCreate, UserPlaceResponse
from app.services.user_place import create_user_place, get_all_user_places, get_places_by_user, get_users_by_place, delete_user_place
from app.shared.utils import verify_token

router = APIRouter( prefix="/user_place", tags=["UserPlace"] )

# Crear una nueva asignación usuario-sede
@router.post("/", response_model=UserPlaceResponse, dependencies=[Depends(verify_token)])
def assign_user_to_place(user_place: UserPlaceCreate, db: Session = Depends(get_db)):
    return create_user_place(db, user_place)

# Obtener todas las asignaciones de usuario-sede
@router.get("/", response_model=list[UserPlaceResponse], dependencies=[Depends(verify_token)])
def get_all_user_places_endpoint(db: Session = Depends(get_db)):
    return get_all_user_places(db)

# Obtener las sedes asignadas a un usuario específico
@router.get("/{user_id}", response_model=list[UserPlaceResponse], dependencies=[Depends(verify_token)])
def get_places_for_user(user_id: int, db: Session = Depends(get_db)):
    return get_places_by_user(db, user_id)

# Obtener las sedes asignadas a un usuario específico
@router.get("/place/{place_id}", response_model=list[UserPlaceResponse], dependencies=[Depends(verify_token)])
def get_users_for_place(place_id: int, db: Session = Depends(get_db)):
    return get_users_by_place(db, place_id)


# Eliminar la asignación de un usuario a una sede
@router.delete("/{user_id}/{place_id}", dependencies=[Depends(verify_token)])
def delete_user_place_endpoint(user_id: int, place_id: int, db: Session = Depends(get_db)):
    delete_user_place(db, user_id, place_id)
    return {"message": "UserPlace deleted successfully"}
