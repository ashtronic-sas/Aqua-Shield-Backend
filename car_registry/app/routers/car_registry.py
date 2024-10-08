from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.schemas.car_registry import CarRegistryCreate, CarRegistryResponse, CarRegistryUpdate
from app.services.car_registry import create_car_registry_db,update_car_registry_db,get_car_registry_by_id_db,get_car_registry_by_car_id_db, delete_car_registry_db
from app.shared.utils import verify_token

router = APIRouter( prefix="/car_registry", tags=["car_registry"] )


@router.post("/", response_model=CarRegistryResponse, dependencies=[Depends(verify_token)])
def create_car_registry(car_registry: CarRegistryCreate, db: Session = Depends(get_db)):
    return create_car_registry_db(db, car_registry)

@router.put("/{id}", response_model=CarRegistryResponse, dependencies=[Depends(verify_token)])
def update_car_registry(id: int, car_registry: CarRegistryUpdate, db: Session = Depends(get_db)):
    return update_car_registry_db(db, id, car_registry)

@router.get("/{id}", response_model=CarRegistryResponse, dependencies=[Depends(verify_token)])
def get_car_registry_by_id(id: int, db: Session = Depends(get_db)):
    return get_car_registry_by_id_db(db, id)

@router.get("/car/{car_id}", response_model=list[CarRegistryResponse], dependencies=[Depends(verify_token)])
def get_car_registry_by_car_id(car_id: int, db: Session = Depends(get_db)):
    return get_car_registry_by_car_id_db(db, car_id)

@router.delete("/{id}", dependencies=[Depends(verify_token)])
def delete_car_registry(id: int, db: Session = Depends(get_db)):
    return delete_car_registry_db(db, id)

