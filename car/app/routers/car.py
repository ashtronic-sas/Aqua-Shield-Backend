from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.schemas.car import CarCreate,CarResponse,CarUpdate
from app.services.car import create_car_db,get_all_car_db,get__car_by_id_db,update_car_by_id_db,delete_car_by_id_db
from app.shared.utils import verify_token

router = APIRouter( prefix="/car", tags=["car"] )

# Rutas de la entidad Car
@router.post("/", response_model=CarCreate, dependencies=[Depends(verify_token)])
def create_car(car: CarCreate, db: Session = Depends(get_db)):
    return create_car_db(db, car)

# Rutas de la entidad Car
@router.get("/", response_model=CarResponse, dependencies=[Depends(verify_token)])
def get_all_car(db: Session = Depends(get_db)):
    return get_all_car_db(db)

@router.get("/{id}", response_model=CarResponse, dependencies=[Depends(verify_token)])
def get_car_by_id(id: int, db: Session = Depends(get_db)):

    return get__car_by_id_db(db)

@router.put("/{id}", response_model=CarResponse, dependencies=[Depends(verify_token)])
def update_car_by_id(id: int, car: CarUpdate, db: Session = Depends(get_db)):
    return update_car_by_id_db(db,car)

@router.delete("/{id}", dependencies=[Depends(verify_token)])
def delete_car_by_id(id: int, db: Session = Depends(get_db)):
    return delete_car_by_id_db(db, id)
