from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.schemas.car import CarCreate,CarResponse,CarUpdate
from app.services.car import create_car_db,get_all_car_db,get__car_by_id_db, get_car_by_license_plate_db, update_car_by_id_db,delete_car_by_id_db
from app.shared.utils import verify_token

router = APIRouter( prefix="/car", tags=["car"] )


@router.post("/", response_model=CarResponse, dependencies=[Depends(verify_token)])
def create_car(car: CarCreate, db: Session = Depends(get_db)):
    return create_car_db(db, car)


@router.get("/", response_model=list[CarResponse] , dependencies=[Depends(verify_token)])
def get_all_car(db: Session = Depends(get_db)):
    return get_all_car_db(db)

@router.get("/{id}", response_model=CarResponse, dependencies=[Depends(verify_token)])
def get_car_by_id(id: int, db: Session = Depends(get_db)):

    return get__car_by_id_db(db, id)

# Obtener un car por license_plate
@router.get("/license_plate/{license_plate}", response_model=CarResponse,dependencies=[Depends(verify_token)])
def get_employee_by_license_plate_endpoint(license_plate: str, db: Session = Depends(get_db)):
    return get_car_by_license_plate_db(db, license_plate)

@router.put("/{id}", response_model=CarResponse, dependencies=[Depends(verify_token)])
def update_car_by_id(id: int, car: CarUpdate, db: Session = Depends(get_db)):
    return update_car_by_id_db(db, id, car)

@router.delete("/{id}", dependencies=[Depends(verify_token)])
def delete_car_by_id(id: int, db: Session = Depends(get_db)):
    return delete_car_by_id_db(db, id)
