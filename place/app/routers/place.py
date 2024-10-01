from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.schemas.place import PlaceCreate, PlaceUpdate, PlaceResponse
from app.services.place import create_place, get_places, get_place_by_id, update_place, delete_place
from app.shared.utils import verify_token

router = APIRouter( tags=["Place"], prefix="/place")

# Crear una nueva sede
@router.post("/", response_model=PlaceResponse, dependencies=[Depends(verify_token)])
def create_new_place(place: PlaceCreate, db: Session = Depends(get_db)):
    return create_place(db, place)

# Obtener todas las sedes
@router.get("/", response_model=list[PlaceResponse], dependencies=[Depends(verify_token)])
def get_all_places(db: Session = Depends(get_db)):
    return get_places(db)

# Obtener una sede por ID
@router.get("/{id}", response_model=PlaceResponse, dependencies=[Depends(verify_token)])
def get_place_by_id_endpoint(id: int, db: Session = Depends(get_db)):
    place = get_place_by_id(db, id)
    if not place:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Place not found")
    return place

# Actualizar una sede existente
@router.put("/{id}", response_model=PlaceResponse, dependencies=[Depends(verify_token)])
def update_place_endpoint(id: int, place_update: PlaceUpdate, db: Session = Depends(get_db)):
    return update_place(db, id, place_update)

# Eliminar una sede
@router.delete("/{id}", dependencies=[Depends(verify_token)])
def delete_place_endpoint(id: int, db: Session = Depends(get_db)):
    delete_place(db, id)
    return {"message": "Place deleted successfully"}
