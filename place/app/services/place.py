from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.models import Place
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
