from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.models import Place, UserPlace, User
from app.schemas.place import PlaceCreate, PlaceUpdate

# Crear una nueva sede
def create_place(db: Session, place: PlaceCreate):
    db_place = Place(name=place.name, address=place.address, nit=place.nit)
    db.add(db_place)
    db.commit()
    db.refresh(db_place)
    return db_place


# Obtener todas las sedes
def get_places(db: Session):
    return db.query(Place).all()

# Obtener una sede por ID
def get_place_by_id(db: Session, place_id: int):
    return db.query(Place).filter(Place.id == place_id).first()

# Obtener una sede por Nit
def get_place_by_Nit(db: Session, nit: str):
    place = db.query(Place).filter(Place.nit == nit).first()

    if not place:
        raise HTTPException(status_code=404, detail="Place not found")

    # Obtener todos los user_id asociados al place_id a través de la tabla UserPlace
    user_places = db.query(UserPlace).filter(UserPlace.place_id == place.id).all()

    # Lista de IDs de los usuarios asociados
    user_ids = [user_place.user_id for user_place in user_places]

    # Buscar los usuarios en la tabla User utilizando los user_id obtenidos
    users = db.query(User).filter(User.id.in_(user_ids)).all()

    # Estructura de la respuesta final, similar al ejemplo que me diste
    place_with_users = {
        "id": place.id,
        "name": place.name,
        "address": place.address,
        "nit": place.nit,
        "created_at": place.created_at,
        "updated_at": place.updated_at,
        # Lista de usuarios asociados a este lugar
        "users": [
            {
                "id": user.id,
                "username": user.username,
                "created_at": user.created_at,
                "updated_at": user.updated_at
            }
            for user in users  # Recorremos los usuarios
        ]
    }

    return place_with_users

# Obtener una sede por address
def get_place_by_address(db: Session, address: str):
    place = db.query(Place).filter(Place.address == address).first()

    if not place:
        raise HTTPException(status_code=404, detail="Place not found")

    # Obtener todos los user_id asociados al place_id a través de la tabla UserPlace
    user_places = db.query(UserPlace).filter(UserPlace.place_id == place.id).all()

    # Lista de IDs de los usuarios asociados
    user_ids = [user_place.user_id for user_place in user_places]

    # Buscar los usuarios en la tabla User utilizando los user_id obtenidos
    users = db.query(User).filter(User.id.in_(user_ids)).all()

    # Estructura de la respuesta final, similar al ejemplo que me diste
    place_with_users = {
        "id": place.id,
        "name": place.name,
        "address": place.address,
        "nit": place.nit,
        "created_at": place.created_at,
        "updated_at": place.updated_at,
        # Lista de usuarios asociados a este lugar
        "users": [
            {
                "id": user.id,
                "username": user.username,
                "created_at": user.created_at,
                "updated_at": user.updated_at
            }
            for user in users  # Recorremos los usuarios
        ]
    }

    return place_with_users
# Actualizar una sede
def update_place(db: Session, place_id: int, place_update: PlaceUpdate):
    db_place = get_place_by_id(db, place_id)
    if not db_place:
        raise HTTPException(status_code=404, detail="Place not found")

    if place_update.name:
        db_place.name = place_update.name
    if place_update.address:
        db_place.address = place_update.address
    if place_update.nit:
        db_place.nit = place_update.nit

    db.commit()
    db.refresh(db_place)
    return db_place

# Eliminar una sede
def delete_place(db: Session, place_id: int):
    db_place = get_place_by_id(db, place_id)
    if not db_place:
        raise HTTPException(status_code=404, detail="Place not found")
    
    db.delete(db_place)
    db.commit()
